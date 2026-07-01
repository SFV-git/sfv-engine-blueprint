from pathlib import Path


def main() -> None:
    sandbox = Path(__file__).resolve().parent

    for letter in "ABCDE":
        original = sandbox / f"test_8_{letter}.txt"
        processed = sandbox / f"test_8_{letter}_processed.txt"
        original.touch(exist_ok=True)
        original.replace(processed)


if __name__ == "__main__":
    main()
