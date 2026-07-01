from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "filler_06_filenames.txt"
OUTPUT_FILE = BASE_DIR / "filler_06_filenames_sorted.txt"


def main() -> None:
    filenames = INPUT_FILE.read_text(encoding="utf-8").splitlines()
    OUTPUT_FILE.write_text("\n".join(sorted(filenames)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
