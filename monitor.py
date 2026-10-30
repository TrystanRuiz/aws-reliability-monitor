import argparse
import json
import time
from datetime import datetime, timezone

import requests


def elapsed_milliseconds(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000, 2)


def check_url(url: str, timeout: float = 5.0) -> dict:
    checked_at = datetime.now(timezone.utc).isoformat()
    started_at = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "aws-reliability-monitor/0.1"},
        )

        return {
            "checked_at": checked_at,
            "url": url,
            "final_url": response.url,
            "success": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "latency_ms": elapsed_milliseconds(started_at),
            "error_type": None,
            "error_message": None,
        }

    except requests.exceptions.Timeout as error:
        error_type = "timeout"
        error_message = str(error)

    except requests.exceptions.SSLError as error:
        error_type = "tls_error"
        error_message = str(error)

    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.InvalidURL,
    ) as error:
        error_type = "invalid_url"
        error_message = str(error)

    except requests.exceptions.ConnectionError as error:
        error_type = "connection_error"
        error_message = str(error)

    except requests.exceptions.RequestException as error:
        error_type = "request_error"
        error_message = str(error)

    return {
        "checked_at": checked_at,
        "url": url,
        "final_url": None,
        "success": False,
        "status_code": None,
        "latency_ms": elapsed_milliseconds(started_at),
        "error_type": error_type,
        "error_message": error_message,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check website availability and response time."
    )
    parser.add_argument("url", help="Website URL to check")
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout in seconds",
    )
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    result = check_url(args.url, args.timeout)
    print(json.dumps(result, indent=2))

    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())