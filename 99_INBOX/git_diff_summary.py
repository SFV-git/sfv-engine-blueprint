"""Generate a read-only summary of the repository's current changes."""

from __future__ import annotations

import subprocess
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(r"C:\SFV_BLUEPRINT")
OUTPUT_PATH = REPO_ROOT / "99_INBOX" / "TONIGHT_CHANGES_SUMMARY.md"


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def describe_status(code: str) -> str:
    if code == "??":
        return "New"
    labels = {
        "M": "Modified",
        "A": "Added",
        "D": "Deleted",
        "R": "Renamed",
        "C": "Copied",
        "U": "Unmerged",
        "T": "Type changed",
    }
    states = [labels[c] for c in code if c in labels]
    return " / ".join(dict.fromkeys(states)) or "Changed"


def parse_status(status_output: str) -> dict[str, list[tuple[str, str]]]:
    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for line in status_output.splitlines():
        if not line:
            continue
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        normalized = path.replace("\\", "/")
        parts = normalized.split("/", 1)
        folder = parts[0] if len(parts) > 1 else "(repository root)"
        grouped[folder].append((normalized, describe_status(code)))
    return dict(sorted(grouped.items()))


def main() -> None:
    status_output = run_git("status", "--short", "--untracked-files=all")
    diff_stat = run_git("diff", "--stat").strip()
    grouped = parse_status(status_output)
    total = sum(len(files) for files in grouped.values())

    lines = [
        "# Tonight's Changes Summary",
        "",
        f"**Total: {total} changed file{'s' if total != 1 else ''} "
        f"across {len(grouped)} top-level folder"
        f"{'s' if len(grouped) != 1 else ''}.**",
        "",
    ]

    if grouped:
        for folder, files in grouped.items():
            lines.extend([f"## {folder}", ""])
            for path, description in files:
                lines.append(f"- {description}: `{path}`")
            lines.append("")
    else:
        lines.extend(["No modified or new files were found.", ""])

    lines.extend(["## Tracked-file diff statistics", ""])
    if diff_stat:
        lines.extend(["```text", diff_stat, "```", ""])
    else:
        lines.extend(["No unstaged tracked-file differences were reported.", ""])

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
