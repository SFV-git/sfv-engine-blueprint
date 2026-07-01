from pathlib import Path


def main() -> None:
    sandbox = Path(__file__).resolve().parent

    for suffix in "ABCDE":
        original = sandbox / f"test_1_{suffix}.txt"
        processed = original.with_name(f"{original.stem}_processed{original.suffix}")
        original.touch(exist_ok=True)
        original.rename(processed)


if __name__ == "__main__":
    main()
