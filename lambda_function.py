import json
import os

from aws_services import get_table, save_result
from monitor import check_url


def lambda_handler(event, context):
    target_url = os.environ.get("TARGET_URL")
    table_name = os.environ.get("RESULTS_TABLE")
    monitor_id = os.environ.get("MONITOR_ID", "portfolio")

    if not target_url:
        raise RuntimeError("TARGET_URL environment variable is required")

    if not table_name:
        raise RuntimeError("RESULTS_TABLE environment variable is required")

    result = check_url(target_url)

    table = get_table(table_name)
    save_result(table, monitor_id, result)

    print(json.dumps(result))
    return result