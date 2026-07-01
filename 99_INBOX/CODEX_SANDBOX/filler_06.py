from pathlib import Path
import random


OUTPUT_FILE = Path(__file__).resolve().parent / "filler_06_filenames.txt"


def main() -> None:
    rng = random.SystemRandom()
    categories = ["EVENTS", "PORTRAITS", "BACKSTAGE", "VENUES", "PROMO"]
    extensions = ["jpg", "jpeg", "png", "tif"]
    sequence_numbers = rng.sample(range(1, 1000), 20)

    filenames = [
        f"SFV_{rng.choice(categories)}_20260701_{number:03d}.{rng.choice(extensions)}"
        for number in sequence_numbers
    ]
    OUTPUT_FILE.write_text("\n".join(filenames) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
