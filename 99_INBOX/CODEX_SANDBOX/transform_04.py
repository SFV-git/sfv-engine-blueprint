from pathlib import Path


directory = Path(__file__).resolve().parent
source = directory / "story_04.txt"
destination = directory / "story_04_upper.txt"

destination.write_text(source.read_text(encoding="utf-8").upper(), encoding="utf-8")
