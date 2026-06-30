"""
SFV ENGINE — SEMANTIC LINKS FOR PYTHON FILES
Adds # CONNECTED FILES comment blocks to .py files in the vault.
"""

import json
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

VAULT      = Path(r"C:\SFV_BLUEPRINT")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "qwen3:14b"
SKIP       = {'.git', '.obsidian', '.smart-env', 'Excalidraw'}
MAX_CONTENT = 3000

SECTION_MARKER = "# CONNECTED FILES"


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
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read()).get("response", "").strip()


def parse_links(response: str) -> list[str]:
    links = []
    for line in response.splitlines():
        if "[[" in line and "]]" in line:
            match = re.search(r'\[\[.*?\]\]', line)
            if match:
                links.append(match.group())
    return links


def has_section(text: str) -> bool:
    return SECTION_MARKER in text


def rewrite_py(text: str, links: list[str]) -> str:
    comment_block = SECTION_MARKER + "\n" + "\n".join(f"# - {l}" for l in links)

    # Replace existing block
    pattern = re.compile(
        r'# CONNECTED FILES\n(?:# - \[\[.*?\]\]\n?)*',
        re.MULTILINE
    )
    if pattern.search(text):
        return pattern.sub(comment_block + "\n", text, count=1)

    # Append before last newline
    return text.rstrip() + "\n\n" + comment_block + "\n"


def run(worker_id: str = "", explicit_files: list[Path] | None = None):
    if explicit_files is not None:
        py_files = explicit_files
    else:
        py_files = [
            f for f in sorted(VAULT.rglob("*.py"))
            if not any(s in f.parts for s in SKIP)
        ]
    tag = f" [{worker_id}]" if worker_id else ""
    manifest = build_manifest()

    print(f"\nSFV ENGINE - SEMANTIC LINKS FOR PYTHON FILES{tag}")
    print(f"Model : {MODEL}  |  Files: {len(py_files)}\n")

    log_lines = [
        f"# SEMANTIC LINKS — PYTHON FILES{tag} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Model: {MODEL}  |  Files: {len(py_files)}",
        "",
        "| File | Links | Time (s) | Status |",
        "|------|-------|----------|--------|",
    ]

    total_links = 0
    for idx, filepath in enumerate(py_files, 1):
        rel = filepath.relative_to(VAULT)
        t0  = time.time()
        print(f"[{idx:02d}/{len(py_files)}] {rel}", end="  ", flush=True)

        try:
            text = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"READ ERROR: {e}")
            log_lines.append(f"| {filepath.name} | - | - | READ ERROR |")
            continue

        prompt = (
            f"You are a knowledge graph assistant for a media production vault called SFV Engine.\n"
            f"Here is the full list of documentation files in the vault:\n{manifest}\n\n"
            f"Here is a Python script [{filepath.name}]:\n{text[:MAX_CONTENT]}\n\n"
            f"Based on what this script does, suggest 3-6 vault documentation files that are "
            f"directly relevant to this script's purpose. Only suggest genuinely related files.\n"
            f"Return ONLY a list in this exact format, nothing else:\n"
            f"- [[FileNameStem|Display Name]]\n"
            f"- [[FileNameStem|Display Name]]"
        )

        try:
            response = call_ollama(prompt)
        except Exception as e:
            print(f"OLLAMA ERROR: {e}")
            log_lines.append(f"| {filepath.name} | - | {time.time()-t0:.1f} | OLLAMA ERROR |")
            continue

        links = parse_links(response)
        if not links:
            print("no links")
            log_lines.append(f"| {filepath.name} | 0 | {time.time()-t0:.1f} | no links |")
            continue

        updated = rewrite_py(text, links)
        try:
            filepath.write_text(updated, encoding="utf-8")
        except Exception as e:
            print(f"WRITE ERROR: {e}")
            log_lines.append(f"| {filepath.name} | - | {time.time()-t0:.1f} | WRITE ERROR |")
            continue

        elapsed = time.time() - t0
        print(f"{len(links)} links  ({elapsed:.1f}s)")
        log_lines.append(f"| {filepath.name} | {len(links)} | {elapsed:.1f} | OK |")
        total_links += len(links)

    log_lines += ["", f"**Total:** {total_links} links",
                  f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    suffix = f"_{worker_id}" if worker_id else ""
    log_path = VAULT / "00_DEV_LOG" / f"SEMANTIC_LINKS_PYTHON{suffix}.md"
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"\nDone -- {total_links} links -> {log_path.name}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        wid   = sys.argv[1]
        paths = [Path(p) for p in sys.argv[2:]]
        run(worker_id=wid, explicit_files=paths)
    else:
        run()

# CONNECTED FILES
# - [[SFV Engine|SFV Engine]]
# - [[TASK_QUEUE|Task Queue]]
# - [[TEMPLATE_DEFAULT|Template Default]]
# - [[USAGE_OPTIMIZATION|Usage Optimization]]
# - [[MASTER_CONTEXT|Master Context]]
