from decimal import Decimal


def get_table(table_name: str):
    import boto3

    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)


def build_result_item(monitor_id: str, result: dict) -> dict:
    item = {
        "monitor_id": monitor_id,
        "checked_at": result["checked_at"],
        "url": result["url"],
        "success": result["success"],
    }

    if result.get("final_url") is not None:
        item["final_url"] = result["final_url"]

    if result.get("status_code") is not None:
        item["status_code"] = result["status_code"]

    if result.get("latency_ms") is not None:
        item["latency_ms"] = Decimal(str(result["latency_ms"]))

    if result.get("error_type") is not None:
        item["error_type"] = result["error_type"]

    if result.get("error_message") is not None:
        item["error_message"] = result["error_message"]

    return item


def save_result(table, monitor_id: str, result: dict) -> dict:
    item = build_result_item(monitor_id, result)
    table.put_item(Item=item)
    return item