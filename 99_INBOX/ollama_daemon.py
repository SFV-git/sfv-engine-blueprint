"""
SFV ENGINE — OLLAMA DAEMON v2
Runs continuously. Reads TASK_QUEUE.md every 30 seconds.
Processes tasks using local Ollama model.
Writes results to OLLAMA_RESULTS.md.

SETUP (run these first, once only):
    pip install requests

USAGE (two terminal tabs required):
    Tab 1: ollama serve
    Tab 2: python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py

ADD TASKS:
    Edit C:\SFV_BLUEPRINT\99_INBOX\TASK_QUEUE.md
    Add task text between --- separators
    Daemon picks up automatically
"""

import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# ── CONFIG ────────────────────────────────────
VAULT        = Path(r"C:\SFV_BLUEPRINT")
TASK_QUEUE   = VAULT / "99_INBOX" / "TASK_QUEUE.md"
RESULTS      = VAULT / "99_INBOX" / "OLLAMA_RESULTS.md"
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_TAGS  = "http://localhost:11434/api/tags"
MODEL        = "qwen3:14b"
FALLBACK     = "qwen3"
INTERVAL     = 30  # seconds

# ── SYSTEM PROMPT ─────────────────────────────
SYSTEM = (
    "You are a task assistant for SFV Engine, a photography and content production system.\n"
    "Rules:\n"
    "- Complete only the specific task given\n"
    "- Never make creative or canon decisions\n"
    "- If unsure about anything, output exactly: UNSURE\n"
    "- Output only what is asked — no preamble, no sign-off\n"
    "- Be specific. No generic advice."
)

# ── STARTUP CHECKS ────────────────────────────
def check_ollama():
    """Verify Ollama is running."""
    try:
        requests.get(OLLAMA_TAGS, timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False

def get_model():
    """Return best available model."""
    try:
        tags = requests.get(OLLAMA_TAGS, timeout=5).json()
        names = [m["name"] for m in tags.get("models", [])]
        if any(MODEL in n for n in names):
            return MODEL
        if any(FALLBACK in n for n in names):
            print(f"  {MODEL} not found. Using {FALLBACK}.")
            return FALLBACK
        print(f"  ERROR: No usable model found. Pull one with: ollama pull qwen3:14b")
        sys.exit(1)
    except Exception as e:
        print(f"  ERROR checking models: {e}")
        sys.exit(1)

# ── CONTEXT ───────────────────────────────────
def load_context():
    """Load compressed vault context."""
    parts = []
    for fname in ["COMPRESSED_CONTEXT.md", "SESSION_STATE.md"]:
        f = VAULT / fname
        if f.exists():
            # Strip frontmatter (--- blocks at top)
            text = f.read_text(encoding="utf-8")
            lines = text.split("\n")
            # Skip lines between first two --- markers
            in_front = False
            front_count = 0
            clean = []
            for line in lines:
                if line.strip() == "---" and front_count < 2:
                    front_count += 1
                    in_front = front_count == 1
                    continue
                if front_count >= 2:
                    clean.append(line)
            parts.append("\n".join(clean).strip())
    return "\n\n---\n\n".join(parts)

# ── OLLAMA CALL ───────────────────────────────
def ask(task, context, model):
    prompt = f"{SYSTEM}\n\nSFV CONTEXT:\n{context}\n\nTASK:\n{task}"
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180
        )
        r.raise_for_status()
        return r.json().get("response", "ERROR: Empty response").strip()
    except requests.exceptions.ConnectionError:
        return "ERROR: Lost connection to Ollama. Is 'ollama serve' still running?"
    except requests.exceptions.Timeout:
        return "ERROR: Ollama timed out (180s). Task may be too complex."
    except Exception as e:
        return f"ERROR: {e}"

# ── TASK PARSING ──────────────────────────────
def parse_tasks(content):
    """
    Extract tasks from TASK_QUEUE.md.
    Tasks are separated by --- and don't start with #
    """
    tasks = []
    # Split on standalone --- lines only
    blocks = content.split("\n---\n")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            continue
        # Skip the header paragraph (contains instructions)
        if "Daemon picks them up" in block or "Separate tasks with" in block:
            continue
        tasks.append(block)
    return tasks

# ── RESULTS WRITER ────────────────────────────
def write_result(task, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## {ts}\n"
        f"**TASK:** {task[:200]}\n\n"
        f"**RESULT:**\n{result}\n\n"
        f"---"
    )
    with open(RESULTS, "a", encoding="utf-8") as f:
        f.write(entry)

# ── QUEUE RESET ───────────────────────────────
def clear_queue():
    TASK_QUEUE.write_text(
        "# TASK QUEUE\n"
        "Add tasks below separated by ---\n"
        "Daemon checks every 30 seconds.\n\n",
        encoding="utf-8"
    )

# ── MAIN LOOP ─────────────────────────────────
def run():
    print("\n SFV ENGINE — OLLAMA DAEMON")
    print(f" Vault   : {VAULT}")
    print(f" Queue   : {TASK_QUEUE.name}")
    print(f" Results : {RESULTS.name}")
    print(f" Interval: {INTERVAL}s\n")

    print(" Checking Ollama...")
    if not check_ollama():
        print(" ERROR: Ollama not running.")
        print(" Fix: open a new terminal tab and run: ollama serve")
        sys.exit(1)
    print(" Ollama OK")

    model = get_model()
    print(f" Model: {model}\n")

    print(" Loading vault context...")
    context = load_context()
    print(f" Context: {len(context)} chars loaded")
    print("\n Running. Edit TASK_QUEUE.md to add tasks.")
    print(" Press Ctrl+C to stop.\n")

    context_timer = time.time()

    while True:
        try:
            # Reload context every 10 minutes
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
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {len(tasks)} task(s) found")
                for i, task in enumerate(tasks, 1):
                    print(f"  [{i}/{len(tasks)}] {task[:80]}...")
                    result = ask(task, context, model)
                    write_result(task, result)
                    print(f"  Done → written to OLLAMA_RESULTS.md")
                clear_queue()
                print(f"  Queue cleared.\n")

            time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print("\n\n Daemon stopped by user.")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
