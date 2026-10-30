from decimal import Decimal
from unittest.mock import Mock

from aws_services import build_result_item, save_result


def successful_result():
    return {
        "checked_at": "2026-10-30T16:30:00+00:00",
        "url": "https://example.com",
        "final_url": "https://example.com/",
        "success": True,
        "status_code": 200,
        "latency_ms": 125.75,
        "error_type": None,
        "error_message": None,
    }


def test_build_result_item_creates_dynamodb_safe_record():
    item = build_result_item("portfolio", successful_result())

    assert item == {
        "monitor_id": "portfolio",
        "checked_at": "2026-10-30T16:30:00+00:00",
        "url": "https://example.com",
        "final_url": "https://example.com/",
        "success": True,
        "status_code": 200,
        "latency_ms": Decimal("125.75"),
    }


def test_build_result_item_preserves_failure_details():
    result = {
        "checked_at": "2026-10-30T16:31:00+00:00",
        "url": "https://example.com",
        "final_url": None,
        "success": False,
        "status_code": None,
        "latency_ms": 5000.0,
        "error_type": "timeout",
        "error_message": "Request timed out",
    }

    item = build_result_item("portfolio", result)

    assert item["success"] is False
    assert item["latency_ms"] == Decimal("5000.0")
    assert item["error_type"] == "timeout"
    assert item["error_message"] == "Request timed out"
    assert "status_code" not in item
    assert "final_url" not in item


def test_save_result_writes_item_to_table():
    table = Mock()

    item = save_result(table, "portfolio", successful_result())

    table.put_item.assert_called_once_with(Item=item)