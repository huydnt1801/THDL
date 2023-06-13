import requests


def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
