import json
import os

from monitor import check_url


def lambda_handler(event, context):
    target_url = os.environ.get("TARGET_URL")

    if not target_url:
        raise RuntimeError("TARGET_URL environment variable is required")

    result = check_url(target_url)
    print(json.dumps(result))

    return result