from pathlib import Path


base_dir = Path(__file__).resolve().parent
source = base_dir / "story_10.txt"
destination = base_dir / "story_10_upper.txt"

destination.write_text(source.read_text(encoding="utf-8").upper(), encoding="utf-8")
