# SFV VAULT SELF-AUDIT v2
# Zero API cost -- Ollama qwen3:14b via /api/chat
# Run: python -u C:\SFV_BLUEPRINT\99_INBOX\vault_self_audit.py

import os, json, datetime, pathlib, urllib.request

VAULT = pathlib.Path(r"C:\SFV_BLUEPRINT")
OLLAMA_MODEL = "qwen3:14b"
OLLAMA_URL = "http://localhost:11434/api/chat"

SKIP_DIRS = {
    "00_DEV_LOG", "99_INBOX", "09_PROMPTS", "11_VERSIONS",
    ".git", ".obsidian", ".smart-env", ".stfolder",
    ".claude", ".claude-engine", "Excalidraw"
}

AUDIT_OUT = VAULT / "FULL_SYSTEM_AUDIT.md"
REVAMP_OUT = VAULT / "NEEDS_REVAMP.md"
APPROVAL_OUT = VAULT / "NEEDS_APPROVAL.md"

SYS_MSG = (
    "You are a document auditor. "
    "Respond ONLY with valid JSON, nothing else. "
    "No thinking tags, no explanation, no markdown."
)

USER_TEMPLATE = (
    "Score this document 1-5:\n"
    "1=generic AI slop or wrong business model\n"
    "2=major gaps, needs full rewrite\n"
    "3=right direction but missing critical specifics\n"
    "4=solid, minor gaps, needs approval\n"
    "5=complete, specific, usable as-is\n\n"
    'Respond ONLY with: {{"score": N, "summary": "one sentence", "verdict": "one sentence"}}\n\n'
    "Path: {path}\n"
    "Content (first 800 chars):\n{content}"
)


def ollama_score(path_str, content):
    user_msg = USER_TEMPLATE.format(
        path=path_str,
        content=content[:800].replace('"', "'")
    )
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYS_MSG},
            {"role": "user", "content": user_msg}
        ],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 200}
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = json.loads(resp.read()).get("message", {}).get("content", "").strip()
            if "<think>" in raw:
                raw = raw.split("</think>")[-1].strip()
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(raw[start:end])
            return {"score": 0, "summary": "PARSE_ERROR", "verdict": raw[:80]}
    except Exception as e:
        return {"score": 0, "summary": "ERROR", "verdict": str(e)[:80]}


def collect_files():
    files = []
    for root, dirs, filenames in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                files.append(pathlib.Path(root) / f)
    return sorted(files)


def run():
    files = collect_files()
    total = len(files)
    print(f"Auditing {total} files with {OLLAMA_MODEL}...")
    print("~20-25 minutes. Leave it running.\n")

    results = []
    for i, fp in enumerate(files):
        rel = str(fp.relative_to(VAULT))
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            content = "READ ERROR: " + str(e)

        result = ollama_score(rel, content)
        result["path"] = rel
        results.append(result)

        score = result.get("score", 0)
        tag = "X" if score <= 3 else ("~" if score == 4 else "OK")
        print(f"[{i+1}/{total}] [{tag}] {score}/5  {rel}")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "---", "STATUS: FOR HUMAN REVIEW",
        f"GENERATED: {now}", f"MODEL: {OLLAMA_MODEL}",
        f"FILES_AUDITED: {total}", "---", "",
        "# SFV VAULT FULL SYSTEM AUDIT", "",
        "| Score | Path | Summary | Verdict |",
        "|---|---|---|---|"
    ]
    for r in sorted(results, key=lambda x: x.get("score", 0)):
        s = r.get("score", "?")
        lines.append(f"| {s} | {r['path']} | {r.get('summary','')} | {r.get('verdict','')} |")
    AUDIT_OUT.write_text("\n".join(lines), encoding="utf-8")

    revamp = [r for r in results if r.get("score", 0) in (1, 2, 3)]
    rlines = ["---", "STATUS: FOR HUMAN REVIEW", f"GENERATED: {now}", "---", "",
              "# NEEDS REVAMP (scores 1-3)", "", f"Total: {len(revamp)} files", ""]
    for r in sorted(revamp, key=lambda x: x.get("score", 0)):
        rlines.append(f"- **{r.get('score')}/5** `{r['path']}`")
        rlines.append(f"  {r.get('verdict', '')}")
    REVAMP_OUT.write_text("\n".join(rlines), encoding="utf-8")

    approval = [r for r in results if r.get("score", 0) == 4]
    alines = ["---", "STATUS: FOR HUMAN REVIEW", f"GENERATED: {now}", "---", "",
              "# NEEDS APPROVAL (score 4)", "", f"Total: {len(approval)} files", ""]
    for r in approval:
        alines.append(f"- `{r['path']}` -- {r.get('summary', '')}")
    APPROVAL_OUT.write_text("\n".join(alines), encoding="utf-8")

    s = [sum(1 for r in results if r.get("score") == n) for n in range(6)]
    print(f"\nDone. 1={s[1]} 2={s[2]} 3={s[3]} 4={s[4]} 5={s[5]} errors={s[0]}")
    print("Written: FULL_SYSTEM_AUDIT.md  NEEDS_REVAMP.md  NEEDS_APPROVAL.md")


if __name__ == "__main__":
    run()
