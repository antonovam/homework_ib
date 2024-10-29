import logging
import requests
# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_json_data(endpoint: str):
    """Sends a GET request to retrieve the JSON data."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is JSON
        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            logger.error("Error: Expected JSON response, got:", response.text)
            return None

    except requests.exceptions.Timeout:
        logger.error("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        logger.error("Error: Failed to connect to the server.")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during GET request: {e}")
    return None


def send_post_data(endpoint: str, data=None, file=None):
    """Sends a POST request with JSON data or file."""
    try:
        if file:
            with open(file, 'rb') as f:
                response = requests.post(endpoint, files={'file': f})
        else:
            response = requests.post(endpoint, json=data)

        response.raise_for_status()  # Check for HTTP errors
        return response.status_code, response.json()
    except requests.exceptions.Timeout:
        logger.error("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        logger.error("Error: Failed to connect to the server.")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during GET request: {e}")
    return None, None
