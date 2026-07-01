import csv
from collections import Counter
from pathlib import Path


INPUT_PATH = Path(__file__).with_name("mock_log.csv")


def main() -> None:
    with INPUT_PATH.open(newline="", encoding="utf-8") as csv_file:
        counts = Counter(row["status"] for row in csv.DictReader(csv_file))

    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")


if __name__ == "__main__":
    main()
