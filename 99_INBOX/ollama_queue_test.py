r"""
SFV ENGINE — QUEUE PROCESSOR SIMULATION
Simulates n8n Workflow 1 — Queue Processor Switch node routing.

Routes by task_type field in each QUEUE/*.json:
  CLASSIFY | SUMMARIZE | COMPRESS  →  Ollama (with confidence routing)
  RESEARCH                         →  DEFERRED_TO_N8N (no HTTP call)
  BLUEPRINT | CODE                 →  Handoff written directly for Claude

Reads:  99_INBOX/QUEUE/*.json  (status=PENDING)
Writes: 99_INBOX/OUTPUTS/      (completed tasks)
        99_INBOX/HANDOFFS/     (escalations to Claude)
Logs:   99_INBOX/DECISION_LOG.md  (appends markdown table rows)

USAGE:
  python C:\SFV_BLUEPRINT\99_INBOX\ollama_queue_test.py
"""

import json
import re
import requests
import sys
from pathlib import Path
from datetime import datetime

VAULT        = Path(r"C:\SFV_BLUEPRINT")
QUEUE_DIR    = VAULT / "99_INBOX" / "QUEUE"
OUTPUT_DIR   = VAULT / "99_INBOX" / "OUTPUTS"
HANDOFFS_DIR = VAULT / "99_INBOX" / "HANDOFFS"
DECISION_LOG = VAULT / "99_INBOX" / "DECISION_LOG.md"
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_TAGS  = "http://localhost:11434/api/tags"
MODEL        = "qwen3:14b"
FALLBACK     = "qwen3"

OLLAMA_TYPES   = {"CLASSIFY", "SUMMARIZE", "COMPRESS"}
HANDOFF_TYPES  = {"BLUEPRINT", "CODE"}
RESEARCH_TYPES = {"RESEARCH"}

HIGH_CONFIDENCE_KEYWORDS = [
    "certain", "confident", "clear", "definitive", "branch is", "classification is",
    "confidence: high",
]

SYSTEM = (
    "You are a task processor for SFV Engine, a media operating system for a photography brand.\n"
    "Rules:\n"
    "- Complete only the specific task given\n"
    "- Never make creative or canon decisions\n"
    "- Output only what is asked — no preamble, no sign-off\n"
    "- Be specific. No generic advice.\n"
    "- If asked to classify, output: BRANCH, CONFIDENCE (high/medium/low), REASON"
)


# --- Ollama helpers ---

def check_ollama():
    try:
        requests.get(OLLAMA_TAGS, timeout=5)
        return True
    except Exception:
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


def ask_ollama(prompt, model):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": f"{SYSTEM}\n\nTASK:\n{prompt}", "stream": False},
            timeout=300,
        )
        r.raise_for_status()
        return r.json().get("response", "ERROR: Empty response").strip()
    except Exception as e:
        return f"ERROR: {e}"


def detect_confidence(response):
    lower = response.lower()
    if any(w in lower for w in ("unsure", "uncertain", "not sure", "unclear")):
        return "LOW"
    if any(kw in lower for kw in HIGH_CONFIDENCE_KEYWORDS):
        return "HIGH"
    return "LOW"


# --- Queue helpers ---

def load_pending_tasks():
    tasks = []
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("status", "").upper() == "PENDING":
                tasks.append((f, data))
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return tasks


def update_task_status(task_file, task_data, new_status, output_path):
    task_data["status"] = new_status
    task_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_data["output_written_to"] = str(output_path)
    task_file.write_text(json.dumps(task_data, indent=2), encoding="utf-8")


# --- Output writers ---

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


def _extract_summary(response):
    sentences = re.split(r"(?<=[.!?])\s+", response.strip())
    return " ".join(sentences[:3])


def write_handoff(task_id, task_file, ollama_response, reason):
    summary = _extract_summary(ollama_response) if ollama_response else "No Ollama response — direct handoff."
    handoff = {
        "handoff_id": f"{task_id}-HANDOFF",
        "task_type": "REASONING",
        "priority": "NORMAL",
        "source_task": str(task_file),
        "context_budget_tokens": 1500,
        "summary": summary,
        "key_findings": [],
        "unresolved": [ollama_response] if ollama_response else [],
        "relevant_files": [],
        "do_not_include": [],
        "ollama_confidence": "LOW",
        "escalation_reason": reason,
    }
    HANDOFFS_DIR.mkdir(parents=True, exist_ok=True)
    handoff_path = HANDOFFS_DIR / f"{task_id}_HANDOFF.json"
    handoff_path.write_text(json.dumps(handoff, indent=2), encoding="utf-8")
    return handoff_path


# --- Decision log (markdown table rows only) ---

def log_decision(task_id, action, handler, result_path, status):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path_display = str(result_path).replace(str(VAULT), "%VAULT%")
    row = f"| {ts} | {task_id} | {action} | {handler} | {status} | {path_display} |\n"
    with open(DECISION_LOG, "a", encoding="utf-8") as f:
        f.write(row)


# --- Switch node routing ---

def route_task(task_file, task_data, model):
    task_id       = task_data.get("task_id", task_file.stem)
    topic         = task_data.get("topic", "unknown")
    prompt        = task_data.get("prompt", "")
    task_type     = task_data.get("task_type", "CLASSIFY").upper()
    output_target = task_data.get("output_target", "")

    print(f"  [{task_type}] {task_id} — {topic}")

    if task_type in RESEARCH_TYPES:
        # n8n Workflow 3 (Tavily) handles this — not built yet
        log_decision(task_id, "DEFERRED_TO_N8N", "N8N_TAVILY", task_file, "DEFERRED")
        update_task_status(task_file, task_data, "DEFERRED", task_file)
        print("  Routed: DEFERRED_TO_N8N (build Workflow 3 in n8n UI)\n")

    elif task_type in HANDOFF_TYPES:
        # Skip Ollama — write handoff directly for Claude
        reason = f"task_type={task_type} requires Claude — direct handoff, Ollama not consulted"
        handoff_path = write_handoff(task_id, task_file, "", reason)
        update_task_status(task_file, task_data, "ESCALATED", handoff_path)
        log_decision(task_id, f"DIRECT_HANDOFF ({task_type})", "CLAUDE", handoff_path, "ESCALATED")
        print(f"  Handoff written: {handoff_path}\n")

    else:
        # CLASSIFY / SUMMARIZE / COMPRESS → Ollama with confidence routing
        result     = ask_ollama(prompt, model)
        confidence = detect_confidence(result)
        print(f"  Confidence: {confidence}")

        if confidence == "HIGH":
            out_path = write_output(task_id, topic, result, output_target)
            update_task_status(task_file, task_data, "COMPLETE", out_path)
            log_decision(task_id, f"OLLAMA_{task_type} (HIGH CONFIDENCE)", "OLLAMA", out_path, "COMPLETE")
            print(f"  Output: {out_path}\n")
        else:
            reason = "ollama_confidence=LOW — escalated to Claude"
            handoff_path = write_handoff(task_id, task_file, result, reason)
            update_task_status(task_file, task_data, "ESCALATED", handoff_path)
            log_decision(task_id, "ESCALATE_TO_CLAUDE (LOW CONFIDENCE)", "CLAUDE", handoff_path, "ESCALATED")
            print(f"  Handoff: {handoff_path}\n")


# --- Main ---

def run():
    print("\nSFV ENGINE — QUEUE PROCESSOR SIMULATION")
    print(f"Queue:    {QUEUE_DIR}")
    print(f"Outputs:  {OUTPUT_DIR}")
    print(f"Handoffs: {HANDOFFS_DIR}\n")

    if not check_ollama():
        print("ERROR: Ollama not running. Check: http://localhost:11434")
        sys.exit(1)
    print("Ollama: OK")

    model = get_model()
    print(f"Model:  {model}\n")

    tasks = load_pending_tasks()
    if not tasks:
        print("No PENDING tasks found in QUEUE/")
        print("Add a .json file to QUEUE/ with status=PENDING and task_type=(CLASSIFY|SUMMARIZE|COMPRESS|RESEARCH|BLUEPRINT|CODE)")
        sys.exit(0)

    print(f"Found {len(tasks)} task(s)\n")

    for task_file, task_data in tasks:
        route_task(task_file, task_data, model)

    print("Queue processor simulation complete.")
    print(f"Decision log: {DECISION_LOG}")


if __name__ == "__main__":
    run()

# CONNECTED FILES
# - [[DECISION_LOG|Decision Log]]
# - [[OLLAMA|Ollama]]
# - [[CLAUDE|Claude]]
