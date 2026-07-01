import os
from pathlib import Path


root = Path(__file__).resolve().parent / "sandbox_tree"

for directory, _, filenames in os.walk(root):
    for filename in sorted(filenames):
        print(Path(directory) / filename)
