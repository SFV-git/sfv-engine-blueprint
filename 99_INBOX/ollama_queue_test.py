r"""
SFV ENGINE — OLLAMA QUEUE BRIDGE TEST
Reads structured JSON tasks from 99_INBOX/QUEUE/
Processes via Ollama daemon-compatible request
Writes output to 99_INBOX/OUTPUTS/
Logs status to 99_INBOX/DECISION_LOG.md

TEST SCOPE: No production media. One task. Prove the loop works.

USAGE: python C:\SFV_BLUEPRINT\99_INBOX\ollama_queue_test.py
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

VAULT       = Path(r"C:\SFV_BLUEPRINT")
QUEUE_DIR    = VAULT / "99_INBOX" / "QUEUE"
OUTPUT_DIR   = VAULT / "99_INBOX" / "OUTPUTS"
HANDOFFS_DIR = VAULT / "99_INBOX" / "HANDOFFS"
DECISION_LOG = VAULT / "99_INBOX" / "DECISION_LOG.md"
OLLAMA_URL  = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"
MODEL       = "qwen3:14b"
FALLBACK    = "qwen3"

SYSTEM = (
    "You are a task processor for SFV Engine, a media operating system for a photography brand.\n"
    "Rules:\n"
    "- Complete only the specific task given\n"
    "- Never make creative or canon decisions\n"
    "- Output only what is asked — no preamble, no sign-off\n"
    "- Be specific. No generic advice.\n"
    "- If asked to classify, output: BRANCH, CONFIDENCE (high/medium/low), REASON"
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
            return FALLBACK
        print("ERROR: No model found. Run: ollama pull qwen3:14b")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

def load_pending_tasks():
    tasks = []
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("status", "").upper() == "PENDING" and data.get("assigned_to", "").upper() == "OLLAMA":
                tasks.append((f, data))
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return tasks

def ask_ollama(prompt, model):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": f"{SYSTEM}\n\nTASK:\n{prompt}", "stream": False},
            timeout=300
        )
        r.raise_for_status()
        return r.json().get("response", "ERROR: Empty response").strip()
    except Exception as e:
        return f"ERROR: {e}"

def write_output(task_id, topic, result, output_target):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"---\n"
        f"TASK_ID: {task_id}\n"
        f"DATE: {ts}\n"
        f"PROCESSED_BY: OLLAMA\n"
        f"STATUS: DRAFT\n"
        f"REVIEW_REQUIRED: YES\n"
        f"---\n\n"
        f"# OUTPUT — {topic}\n\n"
        f"{result}\n"
    )
    out_path = Path(output_target) if output_target else OUTPUT_DIR / f"{task_id}_OLLAMA_OUTPUT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path

def log_decision(task_id, action, result_path, status):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## {ts} | {task_id}\n"
        f"- ACTION: {action}\n"
        f"- ASSIGNED_TO: OLLAMA\n"
        f"- STATUS: {status}\n"
        f"- OUTPUT: {result_path}\n\n"
        f"---"
    )
    with open(DECISION_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def update_task_status(task_file, task_data, new_status, output_path):
    task_data["status"] = new_status
    task_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_data["output_written_to"] = str(output_path)
    task_file.write_text(json.dumps(task_data, indent=2), encoding="utf-8")

def run():
    print("\nSFV ENGINE — OLLAMA QUEUE BRIDGE TEST")
    print(f"Queue: {QUEUE_DIR}")
    print(f"Output: {OUTPUT_DIR}\n")

    if not check_ollama():
        print("ERROR: Ollama not running. Check: http://localhost:11434")
        sys.exit(1)
    print("Ollama: OK")

    model = get_model()
    print(f"Model: {model}\n")

    tasks = load_pending_tasks()
    if not tasks:
        print("No PENDING tasks assigned to OLLAMA found in QUEUE/")
        print("Add a .json task file with: assigned_to=OLLAMA, status=PENDING")
        sys.exit(0)

    print(f"Found {len(tasks)} task(s)\n")

    for task_file, task_data in tasks:
        task_id = task_data.get("task_id", task_file.stem)
        topic = task_data.get("topic", "unknown")
        prompt = task_data.get("prompt", "")
        output_target = task_data.get("output_target", "")

        print(f"  Processing: {task_id} — {topic}")
        result = ask_ollama(prompt, model)

        out_path = write_output(task_id, topic, result, output_target)
        update_task_status(task_file, task_data, "COMPLETE", out_path)
        log_decision(task_id, "PROCESS_AND_WRITE", out_path, "COMPLETE")

        print(f"  Output: {out_path}")
        print(f"  Status updated: COMPLETE\n")

    print("Queue bridge test complete.")
    print(f"Review outputs in: {OUTPUT_DIR}")
    print(f"Decision log: {DECISION_LOG}")

HIGH_CONFIDENCE_KEYWORDS = [
    "certain", "confident", "clear", "definitive", "branch is", "classification is"
]

def detect_confidence(response):
    lower = response.lower()
    if "unsure" in lower:
        return "LOW"
    for kw in HIGH_CONFIDENCE_KEYWORDS:
        if kw in lower:
            return "HIGH"
    return "LOW"

def extract_summary(response):
    import re
    sentences = re.split(r'(?<=[.!?])\s+', response.strip())
    return " ".join(sentences[:3])

def write_handoff(task_id, task_file, response):
    summary = extract_summary(response)
    handoff = {
        "handoff_id": f"{task_id}-HANDOFF",
        "task_type": "REASONING",
        "priority": "NORMAL",
        "source_task": str(task_file),
        "context_budget_tokens": 1500,
        "summary": summary,
        "key_findings": [],
        "unresolved": [response],
        "relevant_files": [],
        "do_not_include": [],
        "ollama_confidence": "LOW",
        "escalation_reason": "Confidence below threshold — escalated to Claude"
    }
    HANDOFFS_DIR.mkdir(parents=True, exist_ok=True)
    handoff_path = HANDOFFS_DIR / f"{task_id}_HANDOFF.json"
    handoff_path.write_text(json.dumps(handoff, indent=2), encoding="utf-8")
    return handoff_path

def run_with_handoff():
    print("\nSFV ENGINE — OLLAMA QUEUE BRIDGE (CONFIDENCE ROUTING MODE)")
    print(f"Queue: {QUEUE_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Handoffs: {HANDOFFS_DIR}\n")

    if not check_ollama():
        print("ERROR: Ollama not running. Check: http://localhost:11434")
        sys.exit(1)
    print("Ollama: OK")

    model = get_model()
    print(f"Model: {model}\n")

    tasks = load_pending_tasks()
    if not tasks:
        print("No PENDING tasks assigned to OLLAMA found in QUEUE/")
        print("Add a .json task file with: assigned_to=OLLAMA, status=PENDING")
        sys.exit(0)

    print(f"Found {len(tasks)} task(s)\n")

    for task_file, task_data in tasks:
        task_id = task_data.get("task_id", task_file.stem)
        topic = task_data.get("topic", "unknown")
        prompt = task_data.get("prompt", "")
        output_target = task_data.get("output_target", "")

        print(f"  Processing: {task_id} — {topic}")
        result = ask_ollama(prompt, model)

        confidence = detect_confidence(result)
        print(f"  Confidence: {confidence}")

        if confidence == "HIGH":
            out_path = write_output(task_id, topic, result, output_target)
            update_task_status(task_file, task_data, "COMPLETE", out_path)
            log_decision(task_id, "PROCESS_AND_WRITE (HIGH CONFIDENCE)", out_path, "COMPLETE")
            print(f"  Output: {out_path}")
            print(f"  Status updated: COMPLETE\n")
        else:
            handoff_path = write_handoff(task_id, task_file, result)
            update_task_status(task_file, task_data, "ESCALATED", handoff_path)
            log_decision(task_id, "ESCALATE_TO_CLAUDE (LOW/MEDIUM CONFIDENCE)", handoff_path, "ESCALATED")
            print(f"  Handoff written: {handoff_path}")
            print(f"  Status updated: ESCALATED\n")

    print("Handoff routing complete.")
    print(f"Outputs: {OUTPUT_DIR}")
    print(f"Handoffs: {HANDOFFS_DIR}")
    print(f"Decision log: {DECISION_LOG}")

if __name__ == "__main__":
    print("1. run() — standard mode")
    print("2. run_with_handoff() — confidence routing mode")
    choice = input("Select: ")
    if choice == "2":
        run_with_handoff()
    else:
        run()
