from pathlib import Path


directory = Path(__file__).resolve().parent
output = directory / "summary.txt"

files = sorted(
    (path for path in directory.iterdir() if path.is_file() and path != output),
    key=lambda path: path.name.casefold(),
)

output.write_text(
    "".join(f"{path.name} {path.stat().st_size}\n" for path in files),
    encoding="utf-8",
)
