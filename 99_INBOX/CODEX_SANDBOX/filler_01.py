from pathlib import Path


output_path = Path(__file__).with_name("numbers.txt")
output_path.write_text(
    "".join(f"{number}\n" for number in range(1, 101)),
    encoding="utf-8",
)
