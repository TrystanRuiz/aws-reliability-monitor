from unittest.mock import Mock

import pytest

import lambda_function


def test_lambda_handler_checks_configured_url(monkeypatch):
    target_url = "https://example.com"
    expected_result = {
        "success": True,
        "status_code": 200,
        "latency_ms": 125.5,
    }

    mock_check = Mock(return_value=expected_result)
    monkeypatch.setenv("TARGET_URL", target_url)
    monkeypatch.setattr(lambda_function, "check_url", mock_check)

    result = lambda_function.lambda_handler({}, None)

    mock_check.assert_called_once_with(target_url)
    assert result == expected_result


def test_lambda_handler_requires_target_url(monkeypatch):
    monkeypatch.delenv("TARGET_URL", raising=False)

    with pytest.raises(
        RuntimeError,
        match="TARGET_URL environment variable is required",
    ):
        lambda_function.lambda_handler({}, None)