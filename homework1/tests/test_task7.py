from unittest.mock import patch, Mock

from src.task7 import fetch_status_code


@patch("src.task7.requests.get")
def test_fetch_status_code(mock_get):
    mock_get.return_value = Mock(status_code=200)
    assert fetch_status_code("https://example.com") == 200
    mock_get.assert_called_once_with("https://example.com", timeout=5)
