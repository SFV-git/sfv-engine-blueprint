from pathlib import Path


root = Path(__file__).resolve().parent / "sandbox_tree"

for relative_dir, filename in (
    (Path("."), "level_root.empty"),
    (Path("a"), "level_a.empty"),
    (Path("a/b"), "level_b.empty"),
    (Path("a/b/c"), "level_c.empty"),
):
    directory = root / relative_dir
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).touch()
