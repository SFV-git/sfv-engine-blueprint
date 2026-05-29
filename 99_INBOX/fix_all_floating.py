"""
SFV ENGINE — FIX ALL FLOATING NODES
Adds proper incoming wikilinks for every remaining floating .md file.
Uses exact wikilink matching (not substring) to check existing refs.
"""

import re
from pathlib import Path

VAULT = Path(r"C:\SFV_BLUEPRINT")
SKIP  = {'.git', '.obsidian', '.smart-env', 'Excalidraw'}

SECTION_RE = re.compile(
    r'(## CONNECTED FILES|## Connected Files)(.*?)(?=\n## |\Z)',
    re.DOTALL
)


def wikilinks_in(text: str) -> set[str]:
    """Return lowercase set of all [[stem]] references in text."""
    return {s.lower().strip() for s in re.findall(r'\[\[([^\]|/\n]+?)(?:\|[^\]]+)?\]\]', text)}


def append_link_to_section(filepath: Path, stem: str, display: str) -> bool:
    """Add [[stem|display]] to filepath's CONNECTED FILES. Returns True if added."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"    READ ERROR {filepath.name}: {e}")
        return False

    if stem.lower() in wikilinks_in(text):
        return False

    new_link = f"- [[{stem}|{display}]]"
    m = SECTION_RE.search(text)
    if m:
        updated = text[:m.end()].rstrip() + f"\n{new_link}\n" + text[m.end():]
    else:
        updated = text.rstrip() + f"\n\n## CONNECTED FILES\n{new_link}\n"

    try:
        filepath.write_text(updated, encoding="utf-8")
        return True
    except Exception as e:
        print(f"    WRITE ERROR {filepath.name}: {e}")
        return False


def link_into(target_rel: str, stem: str, display: str):
    target = VAULT / target_rel.replace("/", "\\")
    if not target.exists():
        print(f"  TARGET MISSING: {target_rel}")
        return False
    added = append_link_to_section(target, stem, display)
    if added:
        print(f"  + [[{stem}]] -> {target_rel}")
    return added


def fix():
    total = 0

    # ── 1. New Python log files → link from SEMANTIC_LINKS_RUN.md ────────────
    print("\n[1] Python log files")
    for log in ["SEMANTIC_LINKS_PYTHON_G", "SEMANTIC_LINKS_PYTHON_H", "SEMANTIC_LINKS_PYTHON_retry"]:
        display = log.replace("_", " ").title()
        if link_into("00_DEV_LOG/SEMANTIC_LINKS_RUN.md", log, display):
            total += 1

    # ── 2. .claude/rules → link from CLAUDE.md ───────────────────────────────
    print("\n[2] .claude/rules files -> CLAUDE.md")
    rules = [
        ("blueprint-only",  "Blueprint Only Rule"),
        ("canon-control",   "Canon Control Rule"),
        ("file-editing",    "File Editing Rule"),
        ("human-approval",  "Human Approval Rule"),
        ("no-assumptions",  "No Assumptions Rule"),
    ]
    for stem, display in rules:
        if link_into("CLAUDE.md", stem, display):
            total += 1

    # ── 3. Session log → DEV_LOG.md ──────────────────────────────────────────
    print("\n[3] Session log -> DEV_LOG.md")
    if link_into("00_DEV_LOG/DEV_LOG.md", "2026-05-27_SESSION_END", "2026-05-27 Session End"):
        total += 1

    # ── 4. Forced back-refs for vault content files still floating ────────────
    print("\n[4] Vault content floating files — forced back-refs")
    forced = [
        # (floating_stem, display, target_to_link_from)
        ("FAILURE_TESTS",   "Failure Tests",   "08_TESTS/PAPER_TRIAL_RUNS.md"),
        ("OLLAMA_PROMPTS",  "Ollama Prompts",  "09_PROMPTS/CLAUDE_PROMPTS.md"),
        ("RESEARCH_PROMPTS","Research Prompts","09_PROMPTS/CLAUDE_PROMPTS.md"),
    ]
    for stem, display, target in forced:
        if link_into(target, stem, display):
            total += 1

    # ── 5. OUTPUTS files → PAPER_TRIAL_RUNS.md ───────────────────────────────
    print("\n[5] OUTPUTS files -> PAPER_TRIAL_RUNS.md")
    outputs_dir = VAULT / "99_INBOX" / "OUTPUTS"
    paper_trials = VAULT / "08_TESTS" / "PAPER_TRIAL_RUNS.md"
    if outputs_dir.exists() and paper_trials.exists():
        for f in sorted(outputs_dir.glob("*.md")):
            display = f.stem.replace("_", " ")[:60]
            added = append_link_to_section(paper_trials, f.stem, display)
            if added:
                print(f"  + [[{f.stem}]] -> PAPER_TRIAL_RUNS.md")
                total += 1

    # ── 6. OLLAMA_STAGING/AI_BRIDGE_BUILD_PLAN → N8N_BLUEPRINT.md ────────────
    print("\n[6] AI_BRIDGE_BUILD_PLAN -> N8N_BLUEPRINT.md")
    if link_into("04_WORKFLOWS/N8N_BLUEPRINT.md", "AI_BRIDGE_BUILD_PLAN", "AI Bridge Build Plan"):
        total += 1

    # ── 7. 99_INBOX working files → DASHBOARD.md ─────────────────────────────
    print("\n[7] 99_INBOX working files -> DASHBOARD.md")
    inbox_leaves = [
        ("CHAT_EXTRACTS",   "Chat Extracts"),
        ("DECISION_LOG",    "Decision Log"),
        ("OLLAMA_RESULTS",  "Ollama Results"),
        ("RAW_IDEAS",       "Raw Ideas"),
        ("SCRATCHPAD",      "Scratchpad"),
        ("TASK_QUEUE",      "Task Queue"),
        ("TEMPLATE_DEFAULT","Template Default"),
        ("TO_REVIEW",       "To Review"),
    ]
    for stem, display in inbox_leaves:
        if link_into("DASHBOARD.md", stem, display):
            total += 1

    print(f"\n{'='*50}")
    print(f"  Links added: {total}")
    print(f"{'='*50}")


if __name__ == "__main__":
    fix()
