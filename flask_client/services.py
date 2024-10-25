import requests


def get_json_data(endpoint: str):
    """Sends a GET request to retrieve the JSON data."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is JSON
        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            print("Error: Expected JSON response, got:", response.text)
            return None

    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"Error during GET request: {e}")
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
        print("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")
    return None, None
