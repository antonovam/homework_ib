import pytest
from click.testing import CliRunner
import requests_mock
from unittest.mock import patch
from app import cli, fetch_and_store_data, post_data, save_to_database
from parser import DataParser
from models import Base, ItemModel, IndicatorModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SERVER_URL = "http://localhost:5001"

# Fixture to setup and teardown an in-memory SQLite database for testing
@pytest.fixture(scope='module')
def db_session():
    """Set up an in-memory SQLite database for testing."""
    engine = create_engine('sqlite:///:memory:')  # In-memory database
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # Provide the session to the test

    session.close()
    Base.metadata.drop_all(engine)


# Fixture to setup a moke HTTP request
@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as m:
        yield m


# Test the 'get' command with mocked server response including indicators
@patch('services.get_json_data')
def test_fetch_and_store_data_with_indicators(mock_get_json_data, db_session):
    """Test the client fetching and storing data with mocked server response including indicators."""

    # Mock server response data with indicators
    mock_response = {
        "count": 1,
        "items": [
            {
                "id": "item1",
                "author": "Author1",
                "companyId": ["company1"],
                "indicators": [
                    {
                        "id": "ind1",
                        "dateFirstSeen": "2020-09-30T11:03:52+00:00",
                        "dateLastSeen": "2020-09-30T11:03:52+00:00",
                        "deleted": False,
                        "description": "Test indicator description",
                        "domain": "example1.com"
                    }
                ],
                "indicatorsIds": ["ind1"],
                "isPublished": True,
                "isTailored": False,
                "labels": ["label1"],
                "langs": ["en"],
                "malwareList": ["Malware1"],
                "seqUpdate": 1617292803402
            }
        ],
        "seqUpdate": 1617292803402
    }
    mock_get_json_data.return_value = mock_response

    # Simulate fetching and storing the data
    parser = DataParser(mock_response)
    save_to_database(parser, db_session)  # Use the save_to_database function in client.py

    # Verify that data was stored in the database
    item = db_session.query(ItemModel).filter_by(id="item1").first()
    assert item is not None
    assert item.author == "Author1"
    assert item.company_ids == ["company1"]
    assert item.malware_list == ["Malware1"]

    # Verify that the associated indicators are stored correctly
    indicators = db_session.query(IndicatorModel).filter_by(item_id="item1").all()
    assert len(indicators) == 1
    indicator = indicators[0]
    assert indicator.id == "ind1"
    assert indicator.date_first_seen == "2020-09-30T11:03:52+00:00"
    assert indicator.date_last_seen == "2020-09-30T11:03:52+00:00"
    assert indicator.deleted is False
    assert indicator.description == "Test indicator description"
    assert indicator.domain == "example1.com"


# Test the 'post' command with mocked server response
def test_post_data(requests_mock_fixture):
    server_url = f"{SERVER_URL}/api/v2/add/data"
    # Define the mock response for the POST request
    requests_mock_fixture.post(server_url, json={"message": "POST successful"}, status_code=200)

    # Invoke the CLI command
    runner = CliRunner()
    result = runner.invoke(cli, ['post'])

    # Assert that the CLI executed without errors
    assert result.exit_code == 0

    # Verify the mock received the request
    assert requests_mock_fixture.called
    assert requests_mock_fixture.call_count == 1
    assert requests_mock_fixture.last_request.json() == {"key": "value"}  # Adjust to match the data you expect to send


# Test POST file functionality with mocked server response
def test_post_file(requests_mock_fixture, tmp_path):
    """Test the client POSTing a file using requests-mock with multipart handling."""

    # Create a temporary JSON file for testing
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "file_data"}')

    server_url = f"{SERVER_URL}/api/v2/add/data"
    # Define the mock response for the POST request
    requests_mock_fixture.post(server_url, json={"message": "File upload successful"},
                               status_code=200)
    # Run the CLI command with file option
    runner = CliRunner()
    result = runner.invoke(cli, ['post', '--file', str(test_file)])

    # Check that the CLI command exited successfully
    assert result.exit_code == 0

    # Assert that the POST request was made
    assert requests_mock_fixture.called
    assert requests_mock_fixture.call_count == 1

    # Verify that the Content-Type is multipart/form-data
    content_type = requests_mock_fixture.last_request.headers["Content-Type"]
    assert "multipart/form-data" in content_type

    # Extract the file content from the multipart request body
    multipart_body = requests_mock_fixture.last_request.body
    assert b'{"key": "file_data"}' in multipart_body  # Check the file content within the multipart body

# Test save_to_database function with edge cases including incomplete indicator data
def test_save_to_database_with_incomplete_indicators(db_session):
    """Test save_to_database with incomplete indicator data."""

    # Mock data with incomplete indicators
    mock_data = {
        "count": 1,
        "items": [
            {
                "id": "item2",
                "author": None,
                "companyId": [],
                "indicators": [
                    {
                        "id": "ind2",
                        "dateFirstSeen": "2021-01-01T00:00:00+00:00",
                        "dateLastSeen": None,  # Missing dateLastSeen
                        "deleted": False,
                        "description": None,
                        "domain": None  # Missing domain
                    }
                ],
                "indicatorsIds": ["ind2"],
                "isPublished": False,
                "isTailored": True,
                "labels": [],
                "langs": ["fr"],
                "malwareList": [],
                "seqUpdate": 1617292810000
            }
        ],
        "seqUpdate": 1617292810000
    }

    parser = DataParser(mock_data)
    save_to_database(parser, db_session)

    # Verify that the item was stored
    item = db_session.query(ItemModel).filter_by(id="item2").first()
    assert item is not None

    # Verify that the associated incomplete indicator is stored correctly
    indicators = db_session.query(IndicatorModel).filter_by(item_id="item2").all()
    assert len(indicators) == 1
    indicator = indicators[0]
    assert indicator.id == "ind2"
    assert indicator.date_first_seen == "2021-01-01T00:00:00+00:00"
    assert indicator.date_last_seen is None  # Should handle missing data
    assert indicator.domain is None  # Should handle missing data


# Test save_to_database function with an incomplete item case
def test_save_to_database_with_incomplete_item(db_session):
    """Test save_to_database with incomplete item data."""

    # Mock data with an incomplete item (missing optional and some required fields)
    mock_data = {
        "count": 1,
        "items": [
            {
                "id": "item3",
                # "author" field is missing
                "companyId": None,  # Set to None instead of an empty list
                # Indicators are completely missing
                "indicatorsIds": [],
                "isPublished": None,  # Explicitly set to None instead of True/False
                "isTailored": False,
                "labels": None,  # Explicitly set to None instead of an empty list
                "langs": ["en"],
                "malwareList": None,  # Explicitly set to None instead of a list
                "seqUpdate": 1617292819999
            }
        ],
        "seqUpdate": 1617292819999
    }

    parser = DataParser(mock_data)
    save_to_database(parser, db_session)

    # Verify that the item was stored in the database, even if incomplete
    item = db_session.query(ItemModel).filter_by(id="item3").first()
    assert item is not None
    assert item.author is None  # Author is missing, should be None
    assert item.company_ids == []  # Should default to an empty list if None
    assert item.is_published is False  # Should handle None
    assert item.is_tailored is False
    assert item.labels == []  # Should default to an empty list if None
    assert item.langs == ["en"]
    assert item.malware_list == []  # Should default to an empty list if None

    # Verify no indicators are present since they were missing
    indicators = db_session.query(IndicatorModel).filter_by(item_id="item3").all()
    assert len(indicators) == 0  # No indicators should be present


# Test that invalid JSON data is handled gracefully
@patch('services.get_json_data')
def test_invalid_json_handling(mock_get_json_data):
    """Test handling of invalid JSON data during GET request."""
    mock_get_json_data.return_value = None  # Simulate invalid JSON response

    runner = CliRunner()
    result = runner.invoke(fetch_and_store_data)
    assert result.exit_code == 0