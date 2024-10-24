import requests


def get_json_data(endpoint: str):
    """Sends a GET request to retrieve the JSON data."""
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return None


def send_post_data(endpoint: str, data=None, file=None):
    """Sends a POST request to upload JSON data or a file."""
    try:
        if file:
            with open(file, 'rb') as f:
                response = requests.post(endpoint, files={'file': f})
        else:
            response = requests.post(endpoint, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return None, None
