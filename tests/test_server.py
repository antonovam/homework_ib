import pytest
import os
import json
from flask import Flask
from flask_server.routes import register_routes

# Define the path for the JSON file
DATA_FILE_NAME = 'example.json'


# Setup a Flask test client
@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../flask_server/uploads')

    register_routes(app)

    with app.test_client() as client:
        yield client


# Fixture to prepare data by creating a JSON file in the uploads folder
@pytest.fixture
def prepare_data(client):
    """Fixture to create a JSON file with test data."""
    data_path = os.path.join(client.application.config['UPLOAD_FOLDER'], DATA_FILE_NAME)

    # Sample data to be saved in the JSON file
    sample_data = {"items": [{"id": 1, "name": "Test Item", "value": 100}]}

    # Ensure the uploads directory exists
    os.makedirs(client.application.config['UPLOAD_FOLDER'], exist_ok=True)

    # Write sample data to the JSON file
    with open(data_path, 'w') as file:
        json.dump(sample_data, file)

    yield  # Allows test to proceed, cleanup occurs after

    # Cleanup: Delete the JSON file after the test
    if os.path.exists(data_path):
        os.remove(data_path)


# Fixture to ensure the JSON file is removed if it exists before the test
@pytest.fixture
def remove_data(client):
    """Fixture to delete the JSON file if it exists."""
    data_path = os.path.join(client.application.config['UPLOAD_FOLDER'], DATA_FILE_NAME)

    # Remove the file if it exists
    if os.path.exists(data_path):
        os.remove(data_path)

    yield  # Allows test to proceed


# Test the GET /api/v2/get/data endpoint when data exists
def test_get_data_exists(client, prepare_data):
    """Test that GET /api/v2/get/data returns data when available."""
    response = client.get('/api/v2/get/data')
    assert response.status_code == 200
    assert response.data is not None


# Test the GET /api/v2/get/data endpoint when no data is available
def test_get_data_not_found(client, remove_data):
    """Test that GET /api/v2/get/data returns 404 when no data is available."""
    response = client.get('/api/v2/get/data')
    assert response.status_code == 404
    assert response.json['error'] == "No data available"


# Test the POST /api/v2/add/data endpoint with a JSON payload
def test_post_json_data(client):
    """Test the POST /api/v2/add/data endpoint with JSON payload."""
    json_data = {"key": "value"}
    response = client.post('/api/v2/add/data', json=json_data)

    assert response.status_code == 200
    assert response.json['message'] == "JSON data saved successfully"

    # Check that the JSON file was created in the uploads folder
    data_path = os.path.join(client.application.config['UPLOAD_FOLDER'], DATA_FILE_NAME)
    assert os.path.exists(data_path)


# Test the POST /api/v2/add/data endpoint with file upload
def test_post_file_upload(client, tmp_path):
    """Test the POST /api/v2/add/data endpoint with file upload."""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "file_data"}')

    with open(test_file, 'rb') as f:
        data = {'file': (f, 'test.json')}
        response = client.post('/api/v2/add/data', content_type='multipart/form-data', data=data)

        assert response.status_code == 200
        assert response.json['message'] == "File uploaded successfully"
