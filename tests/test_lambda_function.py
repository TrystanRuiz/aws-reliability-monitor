from unittest.mock import Mock

import pytest

import lambda_function


def test_lambda_handler_checks_and_saves_result(monkeypatch):
    target_url = "https://example.com"
    table_name = "monitor-results"
    monitor_id = "portfolio"

    expected_result = {
        "checked_at": "2026-10-30T16:30:00+00:00",
        "url": target_url,
        "success": True,
        "status_code": 200,
        "latency_ms": 125.5,
    }

    table = Mock()
    mock_check = Mock(return_value=expected_result)
    mock_get_table = Mock(return_value=table)
    mock_save = Mock()

    monkeypatch.setenv("TARGET_URL", target_url)
    monkeypatch.setenv("RESULTS_TABLE", table_name)
    monkeypatch.setenv("MONITOR_ID", monitor_id)
    monkeypatch.setattr(lambda_function, "check_url", mock_check)
    monkeypatch.setattr(lambda_function, "get_table", mock_get_table)
    monkeypatch.setattr(lambda_function, "save_result", mock_save)

    result = lambda_function.lambda_handler({}, None)

    mock_check.assert_called_once_with(target_url)
    mock_get_table.assert_called_once_with(table_name)
    mock_save.assert_called_once_with(table, monitor_id, expected_result)
    assert result == expected_result


def test_lambda_handler_requires_target_url(monkeypatch):
    monkeypatch.delenv("TARGET_URL", raising=False)
    monkeypatch.setenv("RESULTS_TABLE", "monitor-results")

    with pytest.raises(
        RuntimeError,
        match="TARGET_URL environment variable is required",
    ):
        lambda_function.lambda_handler({}, None)


def test_lambda_handler_requires_results_table(monkeypatch):
    monkeypatch.setenv("TARGET_URL", "https://example.com")
    monkeypatch.delenv("RESULTS_TABLE", raising=False)

    with pytest.raises(
        RuntimeError,
        match="RESULTS_TABLE environment variable is required",
    ):
        lambda_function.lambda_handler({}, None)