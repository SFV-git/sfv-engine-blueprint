from pathlib import Path


def main() -> None:
    sandbox = Path(__file__).resolve().parent

    for letter in "ABCDE":
        source = sandbox / f"test_3_{letter}.txt"
        processed = sandbox / f"test_3_{letter}_processed.txt"

        source.touch(exist_ok=True)
        source.rename(processed)


if __name__ == "__main__":
    main()
