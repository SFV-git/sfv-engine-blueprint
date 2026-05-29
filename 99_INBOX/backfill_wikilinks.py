"""
SFV ENGINE — BACKFILL WIKILINKS
Scans all existing .md files in the vault and adds CONNECTED FILES sections
where missing, using the same FOLDER_LINKS dict as vault_watcher.py.
"""

from pathlib import Path

VAULT = Path(r"C:\SFV_BLUEPRINT")
SKIP  = {'.git', '.obsidian', '.smart-env', '99_INBOX', 'Excalidraw', '.claude'}

FOLDER_LINKS: dict[str, list[str]] = {
    "02_BRANCHES": [
        "[[04_WORKFLOWS/INGEST|Ingest Workflow]]",
        "[[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]",
        "[[05_AI_LAYER/COST_ROUTING|Cost Routing]]",
        "[[05_AI_LAYER/RATE_LIMITS|Rate Limits]]",
    ],
    "04_WORKFLOWS": [
        "[[03_INFRASTRUCTURE/ENVIRONMENT_CONFIG|Environment Config]]",
        "[[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]",
        "[[05_AI_LAYER/COST_ROUTING|Cost Routing]]",
    ],
    "05_AI_LAYER": [
        "[[05_AI_LAYER/COST_ROUTING|Cost Routing]]",
        "[[05_AI_LAYER/RATE_LIMITS|Rate Limits]]",
        "[[COMPRESSED_CONTEXT|Compressed Context]]",
    ],
    "06_TOOLS": [
        "[[06_TOOLS/TOOL_STATUS|Tool Status]]",
        "[[05_AI_LAYER/COST_ROUTING|Cost Routing]]",
    ],
    "07_SCALING": [
        "[[COMPRESSED_CONTEXT|Compressed Context]]",
        "[[02_BRANCHES/SFV_UGC|SFV_UGC]]",
    ],
    "08_TESTS": [
        "[[04_WORKFLOWS/INGEST|Ingest Workflow]]",
        "[[04_WORKFLOWS/DELIVERY|Delivery Workflow]]",
        "[[08_TESTS/PAPER_TRIAL_RUNS|Paper Trial Runs]]",
    ],
    "09_PROMPTS": [
        "[[05_AI_LAYER/COST_ROUTING|Cost Routing]]",
        "[[05_AI_LAYER/RATE_LIMITS|Rate Limits]]",
    ],
    "10_REFERENCES": [
        "[[COMPRESSED_CONTEXT|Compressed Context]]",
        "[[12_DATABANKS/RESEARCH_BANKS|Research Banks]]",
    ],
    "11_VERSIONS": [
        "[[SESSION_STATE|Session State]]",
        "[[DASHBOARD|Dashboard]]",
    ],
    "12_DATABANKS": [
        "[[12_DATABANKS/DATABANK_ARCHITECTURE|Databank Architecture]]",
        "[[COMPRESSED_CONTEXT|Compressed Context]]",
    ],
    "00_DEV_LOG": [
        "[[SESSION_STATE|Session State]]",
        "[[DASHBOARD|Dashboard]]",
    ],
    "03_INFRASTRUCTURE": [
        "[[03_INFRASTRUCTURE/ENVIRONMENT_CONFIG|Environment Config]]",
        "[[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]",
    ],
    "FOR_HUMAN_REVIEW": [
        "[[DASHBOARD|Dashboard]]",
        "[[SESSION_STATE|Session State]]",
    ],
}


def has_connected_section(text: str) -> bool:
    return "## CONNECTED FILES" in text or "## Connected Files" in text


def get_folder_key(filepath: Path) -> str | None:
    rel = filepath.relative_to(VAULT)
    if len(rel.parts) >= 2:
        return rel.parts[0]
    return None


def backfill():
    added_count    = 0
    already_count  = 0
    no_links_count = 0

    for filepath in VAULT.rglob("*.md"):
        if any(s in filepath.parts for s in SKIP):
            continue

        folder_key = get_folder_key(filepath)
        links = FOLDER_LINKS.get(folder_key, []) if folder_key else []

        if not links:
            print(f"  NO LINKS FOR FOLDER  [{folder_key or 'root'}]  {filepath.name}")
            no_links_count += 1
            continue

        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"  READ ERROR  {filepath.name}: {e}")
            no_links_count += 1
            continue

        if has_connected_section(text):
            print(f"  ALREADY HAS  {filepath.relative_to(VAULT)}")
            already_count += 1
            continue

        # Filter self-references
        stem = filepath.stem.lower()
        filtered = [l for l in links if stem not in l.lower()]
        if not filtered:
            print(f"  NO LINKS FOR FOLDER  (self-ref only)  {filepath.name}")
            no_links_count += 1
            continue

        section = "\n\n## CONNECTED FILES\n" + "\n".join(f"- {l}" for l in filtered)
        try:
            filepath.write_text(text.rstrip() + section + "\n", encoding="utf-8")
            print(f"  ADDED  {filepath.relative_to(VAULT)}")
            added_count += 1
        except PermissionError:
            print(f"  LOCKED  {filepath.name} — skipped")
            no_links_count += 1
        except Exception as e:
            print(f"  WRITE ERROR  {filepath.name}: {e}")
            no_links_count += 1

    print(f"\n{'='*50}")
    print(f"  ADDED       : {added_count}")
    print(f"  ALREADY HAS : {already_count}")
    print(f"  SKIPPED     : {no_links_count}")
    print(f"{'='*50}")


if __name__ == "__main__":
    print(f"\nSFV ENGINE — BACKFILL WIKILINKS")
    print(f"Vault: {VAULT}\n")
    backfill()

# CONNECTED FILES
# - [[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]
# - [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
# - [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
# - [[COMPRESSED_CONTEXT|Compressed Context]]
# - [[SESSION_STATE|Session State]]
# - [[DASHBOARD|Dashboard]]
