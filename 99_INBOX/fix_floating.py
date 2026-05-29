"""
SFV ENGINE — FIX FLOATING NODES
For each floating vault file (no incoming links), reads its CONNECTED FILES
outgoing links and injects a back-reference into each target file.
This makes the graph bidirectional without re-running Ollama.
"""

import re
from pathlib import Path

VAULT = Path(r"C:\SFV_BLUEPRINT")
SKIP  = {'.git', '.obsidian', '.smart-env', 'Excalidraw'}

# Files to fix — real vault content with no incoming links
FLOATING = [
    "06_TOOLS/INTEGRATIONS.md",
    "08_TESTS/FAILURE_TESTS.md",
    "09_PROMPTS/OLLAMA_PROMPTS.md",
    "09_PROMPTS/RESEARCH_PROMPTS.md",
    "10_REFERENCES/CASE_STUDIES.md",
    "10_REFERENCES/EXTERNAL_LINKS.md",
    "11_VERSIONS/UPGRADE_CHECKPOINTS.md",
    "12_DATABANKS/RESEARCH_BANKS.md",
]

# Also fix SEMANTIC_LINKS_RUN.md to reference worker logs
WORKER_LOGS = [
    "SEMANTIC_LINKS_WORKER_A",
    "SEMANTIC_LINKS_WORKER_B",
    "SEMANTIC_LINKS_WORKER_C",
    "SEMANTIC_LINKS_WORKER_E",
    "SEMANTIC_LINKS_WORKER_F",
]

SECTION_RE = re.compile(
    r'(## CONNECTED FILES|## Connected Files)(.*?)(?=\n## |\Z)',
    re.DOTALL
)


def get_outgoing_links(text: str) -> list[tuple[str, str]]:
    """Return list of (stem, display_name) from ## CONNECTED FILES section."""
    m = SECTION_RE.search(text)
    if not m:
        return []
    section = m.group(2)
    results = []
    for link in re.finditer(r'\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]', section):
        stem    = link.group(1).strip()
        display = link.group(2).strip() if link.group(2) else stem
        results.append((stem, display))
    return results


def find_file_by_stem(stem: str) -> Path | None:
    """Find a vault .md file by its stem (case-insensitive)."""
    for f in VAULT.rglob("*.md"):
        if any(s in f.parts for s in SKIP):
            continue
        if f.stem.lower() == stem.lower():
            return f
    return None


def add_backref(target_path: Path, backref_stem: str, backref_display: str) -> bool:
    """Add [[backref_stem|backref_display]] to target's CONNECTED FILES if not present."""
    try:
        text = target_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"    READ ERROR {target_path.name}: {e}")
        return False

    # Check if already referenced
    if backref_stem.lower() in text.lower():
        return False

    new_link = f"- [[{backref_stem}|{backref_display}]]"

    m = SECTION_RE.search(text)
    if m:
        # Insert into existing section
        section_end = m.end()
        insert_pos = section_end
        # Find last non-empty line in section to append after it
        updated = text[:section_end].rstrip() + f"\n{new_link}\n" + text[section_end:]
    else:
        # Append new section
        updated = text.rstrip() + f"\n\n## CONNECTED FILES\n{new_link}\n"

    try:
        target_path.write_text(updated, encoding="utf-8")
        return True
    except Exception as e:
        print(f"    WRITE ERROR {target_path.name}: {e}")
        return False


def fix_floating():
    total_added = 0

    print("\nSFV ENGINE - FIX FLOATING NODES")
    print(f"Files to fix: {len(FLOATING)}\n")

    for rel_str in FLOATING:
        filepath = VAULT / rel_str.replace("/", "\\")
        if not filepath.exists():
            print(f"MISSING: {rel_str}")
            continue

        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"READ ERROR {filepath.name}: {e}")
            continue

        links = get_outgoing_links(text)
        if not links:
            print(f"  {filepath.name}: no outgoing links found — skipping")
            continue

        print(f"  {filepath.name}: {len(links)} outgoing links, injecting back-refs...")
        added_to = []
        for stem, display in links:
            target = find_file_by_stem(stem)
            if not target:
                continue
            if target == filepath:
                continue
            back_display = filepath.stem.replace("_", " ").title()
            did_add = add_backref(target, filepath.stem, back_display)
            if did_add:
                print(f"    + [[{filepath.stem}]] -> {target.relative_to(VAULT)}")
                added_to.append(target.name)
                total_added += 1
            if len(added_to) >= 3:  # cap at 3 back-refs per floating file
                break

        if not added_to:
            print(f"    (all targets already reference this file)")

    # Fix SEMANTIC_LINKS_RUN.md to link worker logs
    print(f"\n  Fixing SEMANTIC_LINKS_RUN.md -> worker logs...")
    run_log = VAULT / "00_DEV_LOG" / "SEMANTIC_LINKS_RUN.md"
    if run_log.exists():
        text = run_log.read_text(encoding="utf-8", errors="ignore")
        worker_links = "\n".join(
            f"- [[{w}|{w.replace('_', ' ').title()}]]" for w in WORKER_LOGS
        )
        if "SEMANTIC_LINKS_WORKER_A" not in text:
            m = SECTION_RE.search(text)
            if m:
                updated = text[:m.end()].rstrip() + f"\n{worker_links}\n" + text[m.end():]
            else:
                updated = text.rstrip() + f"\n\n## CONNECTED FILES\n{worker_links}\n"
            run_log.write_text(updated, encoding="utf-8")
            print(f"    Added {len(WORKER_LOGS)} worker log links to SEMANTIC_LINKS_RUN.md")
            total_added += len(WORKER_LOGS)

    print(f"\n{'='*50}")
    print(f"  Back-references added: {total_added}")
    print(f"{'='*50}")


if __name__ == "__main__":
    fix_floating()

# CONNECTED FILES
# - [[SEMANTIC_LINKS_RUN|SEMANTIC LINKS RUN]]
# - [[COMPRESSED_CONTEXT|Compressed Context]]
# - [[MASTER_CONTEXT|Master Context]]
# - [[SESSION_STATE|Session State]]
# - [[USAGE_OPTIMIZATION|Usage Optimization]]
