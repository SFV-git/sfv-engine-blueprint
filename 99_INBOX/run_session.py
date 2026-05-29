import os
import subprocess
import urllib.request
import urllib.error
import json
import time
import datetime

vault = r"C:\SFV_BLUEPRINT"
os.chdir(vault)

report = []
def log(msg):
    print(msg)

def add_report(task, status, info):
    line = f"{task}: {status} - {info}"
    report.append(line)
    log(line)

# TASK 1
try:
    subprocess.run(["git", "add", "."], check=True)
    status_out = subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
    if not status_out:
        add_report("TASK 1", "SKIPPED", "Git already clean")
    else:
        subprocess.run(["git", "commit", "-m", "feat: node networking live, n8n workflows rebuilt, Syncthing configured, Claude Code installed"], check=True)
        hash_out = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        add_report("TASK 1", "DONE", f"Committed: {hash_out}")
except Exception as e:
    add_report("TASK 1", "FAILED", str(e))

# TASK 2
sync_file = os.path.join(vault, "SYNC_TEST.txt")
if os.path.exists(sync_file):
    try:
        os.remove(sync_file)
        add_report("TASK 2", "DONE", "Deleted SYNC_TEST.txt")
    except Exception as e:
        add_report("TASK 2", "FAILED", str(e))
else:
    add_report("TASK 2", "SKIPPED", "Already gone")

# TASK 3
wf_ids = []
wf1_id = None
wfs = [
    r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json",
    r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow4_output_monitor.json"
]
for wf in wfs:
    try:
        with open(wf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        req = urllib.request.Request("http://localhost:5678/api/v1/workflows", 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            wid = res.get('id')
            add_report("TASK 3", "DONE", f"Imported {os.path.basename(wf)} ID: {wid}")
            wf_ids.append(wid)
            if "workflow1" in wf: wf1_id = wid
    except Exception as e:
        add_report("TASK 3", "FAILED", f"Error importing {os.path.basename(wf)}: {str(e)}")

# TASK 4
if wf1_id:
    try:
        req = urllib.request.Request(f"http://localhost:5678/api/v1/workflows/{wf1_id}",
            data=json.dumps({"active": True}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}, method='PATCH')
        with urllib.request.urlopen(req) as response:
            pass # activated
        
        test_file = os.path.join(vault, "99_INBOX", "QUEUE", "TEST_CLAUDE_CODE_RUN.json")
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump({"task_id": "CC-TEST-001", "task_type": "OLLAMA", "status": "PENDING", "prompt": "Reply with exactly: WORKFLOW1 CONFIRMED", "model": "qwen3:14b", "created": "2026-05-29"}, f, indent=2)
            
        found = False
        out_dir = os.path.join(vault, "99_INBOX", "OUTPUTS")
        os.makedirs(out_dir, exist_ok=True)
        
        start = time.time()
        while time.time() - start < 60:
            for fn in os.listdir(out_dir):
                if "CC-TEST-001" in fn:
                    found = True
                    break
            if found: break
            time.sleep(2)
            
        if found: add_report("TASK 4", "DONE", "Output appeared")
        else: add_report("TASK 4", "FAILED", "Timeout waiting for output")
    except Exception as e:
        add_report("TASK 4", "FAILED", str(e))
else:
    add_report("TASK 4", "SKIPPED", "No workflow1 ID")

# TASK 5
tool_script = r"C:\SFV_BLUEPRINT\99_INBOX\review_tool.py"
tool_code = '''import os
vault = r"C:\SFV_BLUEPRINT"
targets = ["UNCONFIRMED", "FOR HUMAN REVIEW", "FOR_HUMAN_REVIEW", "🔴"]
res = {}
c = 0
for r, d, files in os.walk(vault):
    for f in files:
        if f.endswith('.md') and f != "PENDING_REVIEW.md":
            fp = os.path.join(r, f)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    lines = fh.readlines()
                    for i, l in enumerate(lines):
                        if any(t in l for t in targets):
                            if fp not in res: res[fp] = []
                            res[fp].append((i+1, l.strip()))
                            c += 1
            except: pass
out_path = os.path.join(vault, "00_DEV_LOG", "PENDING_REVIEW.md")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as out:
    import datetime
    out.write(f"Total items found: {c}\\nDate run: {datetime.datetime.now().strftime('%Y-%m-%d')}\\n\\n")
    for fp, items in res.items():
        out.write(f"### {fp}\\n")
        for idx, text in items:
            out.write(f"{idx}. Line {idx}: {text}\\n")
        out.write("\\n")
print(f"Found {c} items")
'''
try:
    with open(tool_script, 'w', encoding='utf-8') as f:
        f.write(tool_code)
    output = subprocess.check_output(["python", tool_script], text=True).strip()
    items = output.split()[1] if 'Found' in output else "0"
    add_report("TASK 5", "DONE", f"Found {items} FOR_HUMAN_REVIEW items")
except Exception as e:
    add_report("TASK 5", "FAILED", str(e))

# Write Report
report_path = os.path.join(vault, "00_DEV_LOG", "CLAUDE_CODE_SESSION_2026-05-29.md")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
try:
    with open(report_path, 'w', encoding='utf-8') as f:
        for r in report:
            f.write(r + "\\n")
except Exception as e:
    log(f"Failed to write report: {e}")
