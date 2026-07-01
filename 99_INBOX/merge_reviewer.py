from __future__ import annotations

import os
import re
from pathlib import Path


ROOT = Path(r"C:\SFV_BLUEPRINT")
OUTPUT = ROOT / "99_INBOX" / "REVIEW_QUEUE.md"
TARGET = "OVERNIGHT DRAFT — UNREVIEWED"
EXCLUDED_DIRS = {".git", ".obsidian", ".smart-env"}

ATX_HEADING = re.compile(
    rf"^[ ]{{0,3}}#{{1,6}}[ \t]+{re.escape(TARGET)}"
    rf"(?:[ \t]+[^#].*?)?(?:[ \t]+#+)?[ \t]*$"
)
SETEXT_UNDERLINE = re.compile(r"^[ ]{0,3}(?:=+|-+)[ \t]*$")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [
            name for name in subdirectories if name not in EXCLUDED_DIRS
        ]
        directory_path = Path(directory)
        files.extend(
            directory_path / filename
            for filename in filenames
            if filename.lower().endswith(".md")
        )
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix().lower())


def matching_lines(path: Path) -> list[int]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    matches: list[int] = []

    for index, line in enumerate(lines):
        if ATX_HEADING.fullmatch(line):
            matches.append(index + 1)
        elif (
            line.strip() == TARGET
            and index + 1 < len(lines)
            and SETEXT_UNDERLINE.fullmatch(lines[index + 1])
        ):
            matches.append(index + 1)

    return matches


def main() -> None:
    occurrences: list[tuple[Path, int]] = []
    for path in markdown_files():
        occurrences.extend((path, line_number) for line_number in matching_lines(path))

    output_lines = [
        "# Overnight Merge Review Queue",
        "",
        f"Found {len(occurrences)} unreviewed overnight merge heading(s).",
        "",
    ]

    if occurrences:
        for path, line_number in occurrences:
            relative_path = path.relative_to(ROOT).as_posix()
            output_lines.append(f"- `{relative_path}`: line {line_number}")
    else:
        output_lines.append("_No unreviewed overnight merge headings found._")

    OUTPUT.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(occurrences)} occurrence(s) to {OUTPUT}")


if __name__ == "__main__":
    main()
