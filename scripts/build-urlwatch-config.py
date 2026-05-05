import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

TARGETS_PATH = ROOT / "docs" / "config" / "targets.json"
SELECTION_PATH = ROOT / "docs" / "config" / "selection.json"
GENERATED_DIR = ROOT / "generated"

URLS_OUTPUT = GENERATED_DIR / "urls.yaml"
CONFIG_OUTPUT = GENERATED_DIR / "urlwatch.yaml"


def main() -> None:
    targets_config = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))

    selected_ids = set(selection.get("selectedTargets", []))
    targets_by_id = {
        item["id"]: item
        for item in targets_config.get("targets", [])
    }

    jobs = []

    for target_id in selected_ids:
        target = targets_by_id.get(target_id)
        if not target:
            raise SystemExit(f"Unknown target id: {target_id}")

        jobs.append({
            "name": target["name"],
            "url": target["url"],
            "headers": {
                "User-Agent": "urlwatch-github-actions"
            }
        })

    if not jobs:
        raise SystemExit("No targets selected.")

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
