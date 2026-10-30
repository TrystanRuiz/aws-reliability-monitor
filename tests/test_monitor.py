from unittest.mock import Mock, patch

import requests

from monitor import check_url


@patch("monitor.requests.get")
def test_check_url_returns_success_for_http_200(mock_get):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.url = "https://example.com/"
    mock_get.return_value = fake_response

    result = check_url("https://example.com")

    assert result["success"] is True
    assert result["status_code"] == 200
    assert result["final_url"] == "https://example.com/"
    assert result["error_type"] is None


@patch("monitor.requests.get")
def test_check_url_returns_failure_for_http_503(mock_get):
    fake_response = Mock()
    fake_response.status_code = 503
    fake_response.url = "https://example.com/"
    mock_get.return_value = fake_response

    result = check_url("https://example.com")

    assert result["success"] is False
    assert result["status_code"] == 503
    assert result["error_type"] is None


@patch("monitor.requests.get")
def test_check_url_categorizes_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout(
        "The request timed out"
    )

    result = check_url("https://example.com", timeout=1.0)

    assert result["success"] is False
    assert result["status_code"] is None
    assert result["error_type"] == "timeout"
    assert "timed out" in result["error_message"]


@patch("monitor.requests.get")
def test_check_url_categorizes_tls_error(mock_get):
    mock_get.side_effect = requests.exceptions.SSLError(
        "Certificate verification failed"
    )

    result = check_url("https://example.com")

    assert result["success"] is False
    assert result["status_code"] is None
    assert result["error_type"] == "tls_error"
    assert "Certificate" in result["error_message"]


@patch("monitor.requests.get")
def test_check_url_categorizes_invalid_url(mock_get):
    mock_get.side_effect = requests.exceptions.MissingSchema(
        "Invalid URL"
    )

    result = check_url("example.com")

    assert result["success"] is False
    assert result["status_code"] is None
    assert result["error_type"] == "invalid_url"


@patch("monitor.requests.get")
def test_check_url_categorizes_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Unable to connect"
    )

    result = check_url("https://example.com")

    assert result["success"] is False
    assert result["status_code"] is None
    assert result["error_type"] == "connection_error"
    assert "Unable to connect" in result["error_message"]