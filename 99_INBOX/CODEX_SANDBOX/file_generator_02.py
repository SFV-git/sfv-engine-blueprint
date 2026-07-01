from pathlib import Path


def main() -> None:
    directory = Path(__file__).resolve().parent

    for letter in "ABCDE":
        original = directory / f"test_2_{letter}.txt"
        processed = directory / f"test_2_{letter}_processed.txt"
        original.touch(exist_ok=True)
        original.replace(processed)


if __name__ == "__main__":
    main()
