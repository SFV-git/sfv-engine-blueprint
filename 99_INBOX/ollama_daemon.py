r"""
SFV ENGINE — OLLAMA DAEMON v3
Auto-reads vault files referenced in tasks. No more UNSURE on file tasks.

SETUP: pip install requests
USAGE: python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py

TASK FORMAT:
  Option A — auto file inject (add READ: line before your instruction):
    READ: 04_WORKFLOWS/INGEST.md
    TASK: Find missing steps. Output numbered list only.
    ---
  Option B — inline content (paste content directly in task)

Daemon checks every 30 seconds. Ctrl+C to stop.
"""

import sys, time, requests
from pathlib import Path
from datetime import datetime

VAULT       = Path(r"C:\SFV_BLUEPRINT")
TASK_QUEUE  = VAULT / "99_INBOX" / "TASK_QUEUE.md"
RESULTS     = VAULT / "99_INBOX" / "OLLAMA_RESULTS.md"
OLLAMA_URL  = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"
MODEL       = "qwen3:14b"
FALLBACK    = "qwen3"
INTERVAL    = 30
MAX_FILE_CHARS = 6000

SYSTEM = (
    "You are a task assistant for SFV Engine, a photography and content production system.\n"
    "Rules:\n"
    "- Complete only the specific task given\n"
    "- Never make creative or canon decisions\n"
    "- If provided file content is empty or missing, output: FILE_NOT_FOUND\n"
    "- Output only what is asked — no preamble, no sign-off\n"
    "- Be specific. No generic advice."
)

def check_ollama():
    try:
        requests.get(OLLAMA_TAGS, timeout=5)
        return True
    except:
        return False

def get_model():
    try:
        tags = requests.get(OLLAMA_TAGS, timeout=5).json()
        names = [m["name"] for m in tags.get("models", [])]
        if any(MODEL in n for n in names):
            return MODEL
        if any(FALLBACK in n for n in names):
            print(f"  Using fallback: {FALLBACK}")
            return FALLBACK
        print("  ERROR: No model found. Run: ollama pull qwen3:14b")
        sys.exit(1)
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)

def load_context():
    parts = []
    for fname in ["COMPRESSED_CONTEXT.md", "SESSION_STATE.md"]:
        f = VAULT / fname
        if f.exists():
            text = f.read_text(encoding="utf-8")
            lines = text.split("\n")
            count = 0
            clean = []
            for line in lines:
                if line.strip() == "---" and count < 2:
                    count += 1
                    continue
                if count >= 2:
                    clean.append(line)
            parts.append("\n".join(clean).strip())
    return "\n\n---\n\n".join(parts)

def resolve_file_refs(task_text):
    """
    Detect READ: lines, load the file, inject content into task.
    Handles both forward and back slashes — fixes Windows path separator issue.
    """
    import os
    lines = task_text.split("\n")
    instruction_lines = []
    file_blocks = []
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("READ:"):
            raw = stripped[5:].strip()
            # Normalize: try both slash styles so watcher-generated paths always resolve
            normalized = raw.replace("/", os.sep).replace("\\", os.sep)
            candidates = [
                VAULT / normalized,          # vault-relative, normalized
                VAULT / raw,                 # vault-relative, as-is
                Path(normalized),            # absolute, normalized
                Path(raw),                   # absolute, as-is
            ]
            found = False
            for candidate in candidates:
                try:
                    if candidate.exists():
                        content = candidate.read_text(encoding="utf-8", errors="ignore")
                        if len(content) > MAX_FILE_CHARS:
                            content = content[:MAX_FILE_CHARS] + "\n...[TRUNCATED]"
                        file_blocks.append(f"FILE: {raw}\n---\n{content}\n---")
                        found = True
                        break
                except Exception:
                    continue
            if not found:
                # Debug: show what was tried so Will can diagnose
                tried = str(VAULT / normalized)
                file_blocks.append(f"FILE: {raw}\n---\nFILE NOT FOUND\nTried: {tried}\n---")
        else:
            instruction_lines.append(line)
    task_instruction = "\n".join(instruction_lines).strip()
    if file_blocks:
        return task_instruction + "\n\nFILE CONTENTS:\n" + "\n\n".join(file_blocks)
    return task_instruction

def ask(task, context, model):
    resolved = resolve_file_refs(task)
    prompt = f"{SYSTEM}\n\nSFV CONTEXT:\n{context}\n\nTASK:\n{resolved}"
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=300
        )
        r.raise_for_status()
        return r.json().get("response", "ERROR: Empty response").strip()
    except requests.exceptions.ConnectionError:
        return "ERROR: Lost connection to Ollama."
    except requests.exceptions.Timeout:
        return "ERROR: Timeout (300s). Split the task into smaller pieces."
    except Exception as e:
        return f"ERROR: {e}"

def parse_tasks(content):
    tasks = []
    blocks = content.split("\n---\n")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            continue
        if "Daemon checks every" in block or "Add tasks below" in block:
            continue
        tasks.append(block)
    return tasks

def write_result(task, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    short_task = task.split("\n")[0][:200]
    entry = (
        f"\n## {ts}\n"
        f"**TASK:** {short_task}\n\n"
        f"**RESULT:**\n{result}\n\n"
        f"---"
    )
    with open(RESULTS, "a", encoding="utf-8") as f:
        f.write(entry)

def clear_queue():
    TASK_QUEUE.write_text(
        "# TASK QUEUE\n"
        "Add tasks below separated by ---\n"
        "Daemon checks every 30 seconds.\n\n"
        "To read a vault file: add READ: path/relative/to/vault.md\n"
        "before your instruction.\n\n",
        encoding="utf-8"
    )

def run():
    print("\n SFV ENGINE — OLLAMA DAEMON v3")
    print(f" Vault: {VAULT} | Interval: {INTERVAL}s\n")

    print(" Checking Ollama...")
    if not check_ollama():
        print(" ERROR: Ollama not running. Check: http://localhost:11434")
        sys.exit(1)
    print(" Ollama OK")

    model = get_model()
    print(f" Model: {model}")

    print(" Loading context...")
    context = load_context()
    print(f" Context: {len(context)} chars loaded")
    print("\n Running. Ctrl+C to stop.\n")

    context_timer = time.time()

    while True:
        try:
            if time.time() - context_timer > 600:
                context = load_context()
                context_timer = time.time()

            if not TASK_QUEUE.exists():
                TASK_QUEUE.touch()

            content = TASK_QUEUE.read_text(encoding="utf-8")
            tasks = parse_tasks(content)

            if not tasks:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting...", end="\r")
            else:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {len(tasks)} task(s)")
                for i, task in enumerate(tasks, 1):
                    print(f"  [{i}/{len(tasks)}] {task.split(chr(10))[0][:80]}...")
                    result = ask(task, context, model)
                    write_result(task, result)
                    print(f"  Done → OLLAMA_RESULTS.md")
                clear_queue()
                print("  Queue cleared.\n")

            time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print("\n\n Daemon stopped.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            time.sleep(INTERVAL)

if __name__ == "__main__":
    run()

# CONNECTED FILES
# - [[OLLAMA|Ollama Integration]]
# - [[OLLAMA_SETUP|Ollama Setup]]
# - [[NAMING_CONVENTIONS|Naming Conventions]]
