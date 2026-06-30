"""
SFV ENGINE — SEMANTIC LINKS WORKER
Parallel worker variant — processes a specific slice of vault files.
Usage: python semantic_links_worker.py <worker_id> <file1> <file2> ...
"""

import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

VAULT      = Path(r"C:\SFV_BLUEPRINT")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen3:14b"
SKIP       = {'.git', '.obsidian', '.smart-env', '99_INBOX', 'Excalidraw', '.claude'}
MAX_CONTENT = 3000

SECTION_RE = re.compile(
    r'(## CONNECTED FILES|## Connected Files)(.*?)(?=\n## |\Z)',
    re.DOTALL
)


def build_manifest() -> str:
    lines = []
    for f in sorted(VAULT.rglob("*.md")):
        if any(s in f.parts for s in SKIP):
            continue
        rel = f.relative_to(VAULT)
        lines.append(f"{f.stem}  ({rel.as_posix()})")
    return "\n".join(lines)


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
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
        return data.get("response", "").strip()


def parse_links(response: str) -> list[str]:
    links = []
    for line in response.splitlines():
        line = line.strip()
        if "[[" in line and "]]" in line:
            match = re.search(r'\[\[.*?\]\]', line)
            if match:
                links.append(f"- {match.group()}")
    return links


def rewrite_section(text: str, new_links: list[str]) -> str:
    section_body = "\n".join(new_links)
    new_section = f"## CONNECTED FILES\n{section_body}\n"
    if SECTION_RE.search(text):
        return SECTION_RE.sub(new_section, text, count=1)
    return text.rstrip() + f"\n\n{new_section}"


def run(worker_id: str, file_paths: list[Path]):
    log_path = VAULT / "00_DEV_LOG" / f"SEMANTIC_LINKS_WORKER_{worker_id}.md"
    manifest = build_manifest()

    print(f"\n[Worker {worker_id}] Starting — {len(file_paths)} files")

    log_lines = [
        f"# SEMANTIC LINKS WORKER {worker_id} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Model: {MODEL}  |  Files: {len(file_paths)}",
        "",
        "| File | Links | Time (s) | Status |",
        "|------|-------|----------|--------|",
    ]

    total_links  = 0
    total_errors = 0

    for idx, filepath in enumerate(file_paths, 1):
        rel = filepath.relative_to(VAULT)
        t0  = time.time()
        print(f"  [{worker_id}:{idx:02d}/{len(file_paths)}] {rel}", end="  ", flush=True)

        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"READ ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | — | READ ERROR |")
            total_errors += 1
            continue

        prompt = (
            f"You are a knowledge graph assistant for a media production vault called SFV Engine.\n"
            f"Here is the full list of files in the vault:\n{manifest}\n\n"
            f"Here is the content of the file [{filepath.stem}]:\n{text[:MAX_CONTENT]}\n\n"
            f"Based on the actual content, suggest 3-8 genuinely relevant wikilinks to other files "
            f"in the manifest. Only suggest files that are meaningfully related — not generic.\n"
            f"Return ONLY a list in this exact format, nothing else:\n"
            f"- [[FileNameStem|Display Name]]\n"
            f"- [[FileNameStem|Display Name]]"
        )

        try:
            response = call_ollama(prompt)
        except Exception as e:
            print(f"OLLAMA ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | {time.time()-t0:.1f} | OLLAMA ERROR |")
            total_errors += 1
            continue

        new_links = parse_links(response)
        if not new_links:
            print("no links parsed")
            log_lines.append(f"| {filepath.name} | 0 | {time.time()-t0:.1f} | no links |")
            continue

        updated = rewrite_section(text, new_links)
        try:
            filepath.write_text(updated, encoding="utf-8")
        except Exception as e:
            print(f"WRITE ERROR: {e}")
            log_lines.append(f"| {filepath.name} | — | {time.time()-t0:.1f} | WRITE ERROR |")
            total_errors += 1
            continue

        elapsed = time.time() - t0
        print(f"{len(new_links)} links  ({elapsed:.1f}s)")
        log_lines.append(f"| {filepath.name} | {len(new_links)} | {elapsed:.1f} | OK |")
        total_links += len(new_links)

    log_lines += [
        "",
        f"**Total links written:** {total_links}",
        f"**Errors:** {total_errors}",
        f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"\n[Worker {worker_id}] Done -- {total_links} links, {total_errors} errors -> {log_path.name}")
    return total_links, total_errors


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: semantic_links_worker.py <worker_id> <file1> <file2> ...")
        sys.exit(1)
    worker_id = sys.argv[1]
    paths = [Path(p) for p in sys.argv[2:]]
    run(worker_id, paths)

# CONNECTED FILES
# - [[SFV Engine|SFV Engine]]
# - [[TASK_QUEUE|Task Queue]]
# - [[SESSION_STATE|Session State]]
# - [[USAGE_OPTIMIZATION|Usage Optimization]]
# - [[MASTER_CONTEXT|Master Context]]
# - [[TEMPLATE_DEFAULT|Template Default]]
