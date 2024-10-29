import pytest
import os
from flask_server.routes import create_app


# Setup a Flask test client
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../flask_server/uploads')

    with app.test_client() as client:
        yield client


def test_unsupported_version(client):
    # Make a request to a non-existent API version
    response = client.get("/api/v99/get/data")

    # Verify that a 404 Not Found is returned
    assert response.status_code == 404
    assert "Not Found" in response.get_data(as_text=True)


@pytest.mark.parametrize("version", ["v2"])  # Set to v2 only now, as there are no other versions
def test_blueprint_registration(client, version):
    # Test that /api/v2/get/data is registered and accessible
    response = client.get(f"/api/{version}/get/data")
    assert response.status_code == 200
    

