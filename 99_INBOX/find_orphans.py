"""
SFV ENGINE — ORPHAN FINDER
Finds all .md files with no incoming wikilinks.
Run from Windows Terminal:
    python C:\SFV_BLUEPRINT\99_INBOX\find_orphans.py

Output: C:\SFV_BLUEPRINT\00_DEV_LOG\ORPHANS.md
"""

import re
from pathlib import Path
from datetime import datetime

VAULT = Path(r"C:\SFV_BLUEPRINT")
SKIP = {'.git', '.obsidian', '.smart-env', '99_INBOX'}
OUTPUT = VAULT / "00_DEV_LOG" / "ORPHANS.md"

def find_all_files():
    files = {}
    for f in VAULT.rglob("*.md"):
        if any(s in f.parts for s in SKIP):
            continue
        rel = f.relative_to(VAULT)
        files[f] = rel
    return files

def find_all_links():
    linked = set()
    pattern = re.compile(r'\[\[([^\]|#\n]+)')
    for f in VAULT.rglob("*.md"):
        if any(s in f.parts for s in SKIP):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            for m in pattern.finditer(text):
                raw = m.group(1).strip()
                linked.add(raw.lower())
                linked.add(Path(raw).stem.lower())
                linked.add(raw.lower().replace("/", "\\"))
        except:
            pass
    return linked

def main():
    files = find_all_files()
    linked = find_all_links()

    orphans = []
    for filepath, rel in files.items():
        stem = filepath.stem.lower()
        rel_str = str(rel).lower().replace("\\", "/").replace(".md", "")
        rel_back = str(rel).lower().replace("/", "\\").replace(".md", "")
        if stem not in linked and rel_str not in linked and rel_back not in linked:
            orphans.append(str(rel))

    orphans.sort()

    lines = [
        "---",
        "STATUS: FOR HUMAN REVIEW",
        f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# VAULT ORPHANS",
        f"> {len(orphans)} files with no incoming wikilinks.",
        "> Review each — add links or flag as intentionally standalone.",
        "",
    ]

    # Group by folder
    grouped = {}
    for o in orphans:
        folder = str(Path(o).parent)
        grouped.setdefault(folder, []).append(o)

    for folder, items in sorted(grouped.items()):
        lines.append(f"## {folder}")
        for item in items:
            lines.append(f"- [[{Path(item).stem}]]")
        lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nDone. {len(orphans)} orphans found.")
    print(f"Output: {OUTPUT}")
    print("\nOrphans by folder:")
    for folder, items in sorted(grouped.items()):
        print(f"  {folder}/  ({len(items)} files)")

if __name__ == "__main__":
    main()

# CONNECTED FILES
# - [[to-review|To Review]]
# - [[source-of-truth-rules|Source of Truth Rules]]
# - [[ultraplan-review|UltraPlan Review]]
# - [[architecture-audit|Architecture Audit]]
# - [[proposals|Proposals]]
