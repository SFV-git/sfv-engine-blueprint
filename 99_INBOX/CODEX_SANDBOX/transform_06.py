from pathlib import Path


base_dir = Path(__file__).resolve().parent
source_path = base_dir / "story_06.txt"
output_path = base_dir / "story_06_upper.txt"

output_path.write_text(source_path.read_text(encoding="utf-8").upper(), encoding="utf-8")
