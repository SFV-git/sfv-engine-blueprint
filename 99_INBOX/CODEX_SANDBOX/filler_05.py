import csv
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_PATH = Path(__file__).with_name("mock_log.csv")
STATUSES = ["pending", "running", "completed", "failed"]


def main() -> None:
    start = datetime(2026, 7, 1, 9, 0, 0)
    rows = [
        {
            "timestamp": (start + timedelta(minutes=index * 5)).isoformat(),
            "directive_id": f"DIR-{index + 1:03d}",
            "status": STATUSES[index % len(STATUSES)],
        }
        for index in range(10)
    ]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["timestamp", "directive_id", "status"],
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
