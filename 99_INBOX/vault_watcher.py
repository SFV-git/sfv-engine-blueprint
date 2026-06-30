"""
SFV ENGINE — VAULT WATCHER v2
Monitors vault for new .md files.
Auto-adds CONNECTED FILES section.
Queues Ollama for semantic link suggestions.

USAGE (Windows Terminal — keep running in its own tab):
    python C:\SFV_BLUEPRINT\99_INBOX\vault_watcher.py

WHAT HAPPENS ON NEW FILE:
    1. Standard wikilinks added based on folder (instant, no AI)
    2. Ollama task queued to suggest additional semantic links
    3. Results appear in OLLAMA_RESULTS.md → review in Obsidian

NO EXTRA INSTALLS — stdlib only.
"""

import time
from pathlib import Path
from datetime import datetime

VAULT    = Path(r"C:\SFV_BLUEPRINT")
QUEUE    = VAULT / "99_INBOX" / "TASK_QUEUE.md"
INTERVAL = 15
SKIP     = {'.git', '.obsidian', '.smart-env', '99_INBOX', 'Excalidraw', '.claude'}

# Standard links per top-level folder
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


def scan_vault() -> set[str]:
    """Return set of lowercase string paths — avoids Path hash inconsistency on Windows."""
    found = set()
    try:
        for f in VAULT.rglob("*.md"):
            if any(s in f.parts for s in SKIP):
                continue
            found.add(str(f).lower())
    except Exception as e:
        print(f"  [SCAN ERROR] {e}")
    return found


def get_folder_key(filepath_str: str) -> str | None:
    rel = Path(filepath_str).relative_to(VAULT)
    if len(rel.parts) >= 2:
        return rel.parts[0]
    return None


def has_connected_section(text: str) -> bool:
    return "## CONNECTED FILES" in text or "## Connected Files" in text


def add_links(filepath: Path, links: list[str]) -> bool:
    """Append CONNECTED FILES to file if not already present. Returns True if added."""
    try:
        # Wait briefly — file may still be written by another process
        time.sleep(0.5)
        text = filepath.read_text(encoding="utf-8", errors="ignore")
        if has_connected_section(text):
            return False
        # Filter out self-references
        stem = filepath.stem.lower()
        filtered = [l for l in links if stem not in l.lower()]
        if not filtered:
            return False
        section = "\n\n## CONNECTED FILES\n" + "\n".join(f"- {l}" for l in filtered)
        filepath.write_text(text.rstrip() + section + "\n", encoding="utf-8")
        return True
    except PermissionError:
        print(f"  [LOCKED] {filepath.name} is open — will retry next cycle")
        return False
    except Exception as e:
        print(f"  [WRITE ERROR] {filepath.name}: {e}")
        return False


def queue_ollama(filepath: Path, rel_path: str):
    """Queue Ollama to suggest additional wikilinks for the new file."""
    try:
        if not QUEUE.exists():
            return
        existing = QUEUE.read_text(encoding="utf-8")
        if filepath.stem in existing:
            return  # already queued
        task = (
            f"READ: {rel_path.replace(chr(92), '/')}\n"
            f"This is a new file added to the SFV vault. "
            f"Based on its content and purpose, suggest up to 5 wikilinks "
            f"to other vault files that belong in its CONNECTED FILES section. "
            f"Format each suggestion as: [[filename]] — one-line reason. Nothing else."
        )
        with open(QUEUE, "a", encoding="utf-8") as f:
            f.write(f"\n---\n{task}\n")
        print(f"  → Ollama queued for: {filepath.name}")
    except Exception as e:
        print(f"  [QUEUE ERROR] {e}")


def run():
    print("\n SFV ENGINE — VAULT WATCHER v2")
    print(f" Vault    : {VAULT}")
    print(f" Interval : {INTERVAL}s")
    print(f" Queue    : {QUEUE.name}")
    print(" Ctrl+C to stop.\n")

    if not VAULT.exists():
        print(f" ERROR: Vault not found at {VAULT}")
        return

    known = scan_vault()
    print(f" Indexed {len(known)} existing .md files. Watching for new ones...\n")

    while True:
        try:
            time.sleep(INTERVAL)
            current = scan_vault()
            new_paths = current - known

            for path_str in new_paths:
                filepath = Path(path_str)
                if not filepath.exists():
                    continue

                try:
                    rel = filepath.relative_to(VAULT)
                except ValueError:
                    continue

                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] NEW: {rel}")

                folder_key = get_folder_key(path_str)
                links = FOLDER_LINKS.get(folder_key, [])

                if links:
                    added = add_links(filepath, links)
                    if added:
                        print(f"  ✓ Added {len(links)} standard links")
                    else:
                        print(f"  = CONNECTED FILES already present")
                else:
                    print(f"  = No standard links for folder: {folder_key or 'root'}")

                queue_ollama(filepath, str(rel))

            known = current

        except KeyboardInterrupt:
            print("\n\n Watcher stopped.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    run()

# CONNECTED FILES
# - [[TASK_QUEUE|Task Queue]]
# - [[OLLAMA_RESULTS|Ollama Results]]
# - [[SFV Engine|SFV Engine]]
