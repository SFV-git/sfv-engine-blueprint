from pathlib import Path


directory = Path(__file__).parent
numbers = (
    int(line)
    for line in (directory / "numbers.txt").read_text(encoding="utf-8").splitlines()
)
(directory / "numbers_sum.txt").write_text(
    f"{sum(numbers)}\n",
    encoding="utf-8",
)
