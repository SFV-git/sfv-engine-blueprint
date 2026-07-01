from pathlib import Path


def main() -> None:
    sandbox = Path(__file__).resolve().parent

    for letter in "ABCDE":
        original = sandbox / f"test_5_{letter}.txt"
        processed = sandbox / f"test_5_{letter}_processed.txt"
        original.touch()
        original.rename(processed)


if __name__ == "__main__":
    main()
