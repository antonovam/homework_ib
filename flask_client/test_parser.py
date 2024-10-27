import pytest
from parser import DataParser, Item, Indicator


# Test DataParser with valid JSON data
def test_parser_valid_data():
    """Test the DataParser with valid JSON data."""

    # Sample JSON structure for testing
    json_data = {
        "count": 2,
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
                        "description": None,
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

    # Initialize the parser
    parser = DataParser(json_data)

    # Test if the parser correctly creates Item and Indicator objects
    assert parser.count == 2
    assert len(parser.items) == 1
    assert parser.seq_update == 1617292803402

    # Check the first item
    item = parser.items[0]
    assert item.id == "item1"
    assert item.author == "Author1"
    assert item.company_ids == ["company1"]
    assert item.is_published is True
    assert item.is_tailored is False
    assert item.labels == ["label1"]
    assert item.langs == ["en"]
    assert item.malware_list == ["Malware1"]
    assert item.seq_update == 1617292803402

    # Check indicators
    assert len(item.indicators) == 1
    indicator = item.indicators[0]
    assert indicator.id == "ind1"
    assert indicator.date_first_seen == "2020-09-30T11:03:52+00:00"
    assert indicator.date_last_seen == "2020-09-30T11:03:52+00:00"
    assert indicator.deleted is False
    assert indicator.domain == "example1.com"


# Test DataParser with incomplete data
def test_parser_incomplete_data():
    """Test the DataParser with incomplete JSON data."""

    # JSON with missing optional fields
    json_data = {
        "count": 1,
        "items": [
            {
                "id": "item2",
                "author": None,  # Missing author
                "companyId": [],
                "indicators": [],
                "indicatorsIds": [],
                "isPublished": False,
                "isTailored": True,
                "labels": [],
                "langs": ["fr"],
                "malwareList": [],
                "seqUpdate": 1617292809999
            }
        ],
        "seqUpdate": 1617292809999
    }

    # Initialize the parser
    parser = DataParser(json_data)

    # Test if the parser handles missing fields correctly
    assert parser.count == 1
    assert len(parser.items) == 1
    assert parser.seq_update == 1617292809999

    # Check the item with missing data
    item = parser.items[0]
    assert item.id == "item2"
    assert item.author is None
    assert item.company_ids == []
    assert item.indicators == []
    assert item.indicator_ids == []
    assert item.is_published is False
    assert item.is_tailored is True
    assert item.labels == []
    assert item.langs == ["fr"]
    assert item.malware_list == []
    assert item.seq_update == 1617292809999


# Test DataParser with no items (empty list)
def test_parser_no_items():
    """Test the DataParser with an empty 'items' list."""

    json_data = {
        "count": 0,
        "items": [],
        "seqUpdate": 1617292810000
    }

    # Initialize the parser
    parser = DataParser(json_data)

    # Ensure that the parser correctly handles an empty list of items
    assert parser.count == 0
    assert len(parser.items) == 0
    assert parser.seq_update == 1617292810000


# Test DataParser with missing 'items' key
def test_parser_missing_items_key():
    """Test the DataParser with a missing 'items' key in JSON."""

    json_data = {
        "count": 0,
        "seqUpdate": 1617292810001
    }

    # Initialize the parser with a missing 'items' key
    parser = DataParser(json_data)

    # Ensure that 'items' defaults to an empty list
    assert parser.count == 0
    assert len(parser.items) == 0
    assert parser.seq_update == 1617292810001


# Test DataParser with invalid JSON structure
def test_parser_invalid_structure():
    """Test the DataParser with an invalid JSON structure."""

    # JSON data that doesn't match the expected structure
    json_data = {
        "invalidKey": "This is not the expected structure"
    }

    # Initialize the parser with invalid JSON data
    parser = DataParser(json_data)

    # Ensure that 'count' and 'items' are default values when structure is invalid
    assert parser.count == 0
    assert len(parser.items) == 0
    assert parser.seq_update is None
