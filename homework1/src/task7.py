"""Task 7: package management -- demonstrates the `requests` package."""

import requests


def fetch_status_code(url):
    """Return the HTTP status code for a GET request to url."""
    response = requests.get(url, timeout=5)
    return response.status_code


if __name__ == "__main__":
    print(fetch_status_code("https://www.google.com"))
