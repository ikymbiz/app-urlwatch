import json
from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]

SELECTION_PATH = ROOT / "docs" / "config" / "selection.json"
GENERATED_DIR = ROOT / "generated"

URLS_OUTPUT = GENERATED_DIR / "urls.yaml"
CONFIG_OUTPUT = GENERATED_DIR / "urlwatch.yaml"


def is_valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> None:
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))

    targets = selection.get("targets", [])
    if not isinstance(targets, list):
        raise SystemExit("selection.json: targets must be a list.")

    jobs = []

    for index, target in enumerate(targets, start=1):
        name = str(target.get("name", "")).strip()
        url = str(target.get("url", "")).strip()

        if not name:
            raise SystemExit(f"selection.json: targets[{index}].name is required.")

        if not is_valid_http_url(url):
            raise SystemExit(f"selection.json: targets[{index}].url must be http or https URL.")

        jobs.append({
            "name": name,
            "url": url,
            "headers": {
                "User-Agent": "urlwatch-github-actions"
            }
        })

    if not jobs:
        raise SystemExit("No URLs configured in docs/config/selection.json.")

    GENERATED_DIR.mkdir(exist_ok=True)

    URLS_OUTPUT.write_text(
        yaml.safe_dump_all(jobs, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    urlwatch_config = {
        "display": {
            "new": False,
            "error": True,
            "unchanged": False,
            "empty-diff": False,
        },
        "job_defaults": {
            "url": {
                "timeout": 30,
                "ignore_connection_errors": True,
            }
        },
        "report": {
            "text": {
                "details": True,
                "footer": True,
                "line_length": 120,
            },
            "stdout": {
                "enabled": True,
                "color": False,
            },
            "shell": {
                "enabled": True,
                "command": "python scripts/rss_reporter.py",
            },
        },
    }

    CONFIG_OUTPUT.write_text(
        yaml.safe_dump(urlwatch_config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    print(f"Wrote {URLS_OUTPUT}")
    print(f"Wrote {CONFIG_OUTPUT}")


if __name__ == "__main__":
    main()
