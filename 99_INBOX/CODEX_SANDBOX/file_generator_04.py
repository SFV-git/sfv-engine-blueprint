from pathlib import Path


def main() -> None:
    directory = Path(__file__).resolve().parent

    for suffix in "ABCDE":
        original = directory / f"test_4_{suffix}.txt"
        processed = directory / f"test_4_{suffix}_processed.txt"
        original.touch(exist_ok=True)
        original.replace(processed)


if __name__ == "__main__":
    main()
