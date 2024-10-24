import pytest
import os
from flask import Flask
from routes import register_routes


# Setup a Flask test client
@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = './uploads'

    register_routes(app)

    with app.test_client() as client:
        yield client


def test_get_data(client):
    """Test the GET /api/v2/get/data endpoint."""
    response = client.get('/api/v2/get/data')

    # Check if the response is 200 OK or 404 if file is missing
    if response.status_code == 200:
        assert response.data is not None
    elif response.status_code == 404:
        assert response.json['error'] == "No data available"


def test_post_json_data(client):
    """Test the POST /api/v2/add/data endpoint with JSON payload."""
    json_data = {"key": "value"}
    response = client.post('/api/v2/add/data', json=json_data)

    assert response.status_code == 200
    assert response.json['message'] == "JSON data saved successfully"

    # Check that the file was created in the uploads folder
    assert os.path.exists('./uploads/example.json')


def test_post_file_upload(client, tmp_path):
    """Test the POST /api/v2/add/data endpoint with file upload."""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "file_data"}')

    with open(test_file, 'rb') as f:
        data = {'file': (f, 'test.json')}
        response = client.post('/api/v2/add/data', content_type='multipart/form-data', data=data)

        assert response.status_code == 200
        assert response.json['message'] == "File uploaded successfully"
