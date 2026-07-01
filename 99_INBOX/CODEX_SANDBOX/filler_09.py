import json
from pathlib import Path


def main() -> None:
    queue = [
        {"id": 1, "task": "collect input", "status": "PENDING"},
        {"id": 2, "task": "process data", "status": "PENDING"},
        {"id": 3, "task": "save result", "status": "PENDING"},
    ]

    for item in queue:
        if item["status"] == "PENDING":
            item["status"] = "COMPLETE"

    output_path = Path(__file__).with_name("queue_state.json")
    output_path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
