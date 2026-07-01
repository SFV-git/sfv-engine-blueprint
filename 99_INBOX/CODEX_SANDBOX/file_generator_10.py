from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent

    for suffix in "ABCDE":
        original = base_dir / f"test_10_{suffix}.txt"
        processed = original.with_name(f"{original.stem}_processed{original.suffix}")
        original.touch(exist_ok=True)
        original.rename(processed)


if __name__ == "__main__":
    main()
