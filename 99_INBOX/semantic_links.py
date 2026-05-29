"""
SFV ENGINE — SEMANTIC LINKS
Rewrites ## CONNECTED FILES sections in every vault .md file using
Ollama (qwen3:14b) to suggest genuinely relevant cross-links.
"""

import json
import re
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

VAULT        = Path(r"C:\SFV_BLUEPRINT")
LOG_FILE     = VAULT / "00_DEV_LOG" / "SEMANTIC_LINKS_RUN.md"
OLLAMA_URL   = "http://localhost:11434/api/generate"
MODEL        = "qwen3:14b"
RATE_LIMIT   = 2        # seconds between calls
MAX_CONTENT  = 3000     # chars of file content to send (keep prompt manageable)
SKIP         = {'.git', '.obsidian', '.smart-env', '99_INBOX', 'Excalidraw', '.claude'}

SECTION_RE = re.compile(
    r'(## CONNECTED FILES|## Connected Files)(.*?)(?=\n## |\Z)',
    re.DOTALL
)


# ── helpers ──────────────────────────────────────────────────────────────────

def build_manifest(files: list[Path]) -> str:
    lines = []
    for f in files:
        rel = f.relative_to(VAULT)
        lines.append(f"{f.stem}  ({rel.as_posix()})")
    return "\n".join(lines)


def scan_vault() -> list[Path]:
    results = []
    for f in sorted(VAULT.rglob("*.md")):
        if any(s in f.parts for s in SKIP):
            continue
        results.append(f)
    return results


def call_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "").strip()
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ollama unreachable: {e}")


def parse_links(response: str) -> list[str]:
    """Extract lines that look like wikilinks: - [[...]]"""
    links = []
    for line in response.splitlines():
        line = line.strip()
        # Accept lines starting with "- [[" or just "[["
        if "[[" in line and "]]" in line:
            # Normalise to "- [[...]]" format
            match = re.search(r'\[\[.*?\]\]', line)
            if match:
                links.append(f"- {match.group()}")
    return links


def existing_links(text: str) -> set[str]:
    """Return the set of [[stems]] already present anywhere in the file."""
    return set(re.findall(r'\[\[([^\]|]+)', text))


def rewrite_section(text: str, new_links: list[str]) -> str:
    section_body = "\n".join(new_links)
    new_section = f"## CONNECTED FILES\n{section_body}\n"

    if SECTION_RE.search(text):
        return SECTION_RE.sub(new_section, text, count=1)
    else:
        return text.rstrip() + f"\n\n{new_section}"


# ── main ─────────────────────────────────────────────────────────────────────

def run():
    files = scan_vault()
    if not files:
        print("No .md files found.")
        return

    manifest = build_manifest(files)
    print(f"\nSFV ENGINE — SEMANTIC LINKS")
    print(f"Model  : {MODEL}")
    print(f"Files  : {len(files)}")
    print(f"Log    : {LOG_FILE.name}\n")

    log_lines = [
        f"# SEMANTIC LINKS RUN — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Model: {MODEL}  |  Files: {len(files)}",
        "",
        "| File | Links Added | Time (s) | Notes |",
        "|------|-------------|----------|-------|",
    ]

    total_added  = 0
    total_errors = 0

    for idx, filepath in enumerate(files, 1):
        rel = filepath.relative_to(VAULT)
        t0  = time.time()

        print(f"[{idx:03d}/{len(files)}] {rel}", end="  ", flush=True)

        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"READ ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | — | READ ERROR: {e} |")
            total_errors += 1
            continue

        content_snippet = text[:MAX_CONTENT]

        prompt = (
            f"You are a knowledge graph assistant for a media production vault called SFV Engine.\n"
            f"Here is the full list of files in the vault:\n{manifest}\n\n"
            f"Here is the content of the file [{filepath.stem}]:\n{content_snippet}\n\n"
            f"Based on the actual content, suggest 3-8 genuinely relevant wikilinks to other files "
            f"in the manifest. Only suggest files that are meaningfully related — not generic.\n"
            f"Return ONLY a list in this exact format, nothing else:\n"
            f"- [[FileNameStem|Display Name]]\n"
            f"- [[FileNameStem|Display Name]]"
        )

        try:
            response = call_ollama(prompt)
        except RuntimeError as e:
            print(f"OLLAMA ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | — | OLLAMA ERROR: {e} |")
            total_errors += 1
            time.sleep(RATE_LIMIT)
            continue

        new_links = parse_links(response)
        if not new_links:
            print("no links parsed")
            log_lines.append(f"| {filepath.name} | 0 | {time.time()-t0:.1f} | No links parsed from response |")
            time.sleep(RATE_LIMIT)
            continue

        # Deduplicate against what's already in the file (outside any section)
        present = existing_links(text)
        deduped = []
        for link in new_links:
            stem_match = re.search(r'\[\[([^\]|]+)', link)
            if stem_match and stem_match.group(1) not in present:
                deduped.append(link)
            elif stem_match:
                deduped.append(link)  # keep — rewrite replaces the whole section

        updated_text = rewrite_section(text, deduped)

        try:
            filepath.write_text(updated_text, encoding="utf-8")
        except Exception as e:
            print(f"WRITE ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | {time.time()-t0:.1f} | WRITE ERROR: {e} |")
            total_errors += 1
            time.sleep(RATE_LIMIT)
            continue

        elapsed = time.time() - t0
        print(f"{len(deduped)} links  ({elapsed:.1f}s)")
        log_lines.append(f"| {filepath.name} | {len(deduped)} | {elapsed:.1f} | OK |")
        total_added += len(deduped)

        time.sleep(RATE_LIMIT)

    # Write log
    log_lines += [
        "",
        f"**Total links written:** {total_added}",
        f"**Errors:** {total_errors}",
        f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    try:
        LOG_FILE.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        print(f"\nLog written to {LOG_FILE}")
    except Exception as e:
        print(f"\nCould not write log: {e}")

    print(f"\n{'='*50}")
    print(f"  Files processed : {len(files)}")
    print(f"  Total links     : {total_added}")
    print(f"  Errors          : {total_errors}")
    print(f"{'='*50}")


if __name__ == "__main__":
    run()
