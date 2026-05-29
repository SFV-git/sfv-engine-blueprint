import os
import json
import sys
import requests

BASE_URL = "http://localhost:5678/api/v1"
API_KEY = os.environ.get("N8N_API_KEY")

if not API_KEY:
    print("ERROR: N8N_API_KEY not set in environment.")
    sys.exit(1)

HEADERS = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json",
}

WORKFLOWS = [
    ("workflow1_queue_processor", r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json"),
    ("workflow4_output_monitor",  r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow4_output_monitor.json"),
]

imported_ids = {}

for name, path in WORKFLOWS:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    payload.pop("id", None)
    payload.pop("versionId", None)

    resp = requests.post(f"{BASE_URL}/workflows", headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        wf_id = resp.json().get("id")
        imported_ids[name] = wf_id
        print(f"IMPORTED  {name}  id={wf_id}")
    elif resp.status_code == 400 and "already exists" in resp.text.lower():
        print(f"SKIPPED   {name}  (already exists)")
    else:
        print(f"FAILED    {name}  status={resp.status_code}  body={resp.text[:300]}")

# Activate workflow1
wf1_id = imported_ids.get("workflow1_queue_processor")
if wf1_id:
    act = requests.patch(
        f"{BASE_URL}/workflows/{wf1_id}",
        headers=HEADERS,
        json={"active": True},
    )
    if act.status_code == 200:
        print(f"ACTIVATED workflow1 id={wf1_id}")
    else:
        print(f"ACTIVATE FAILED  status={act.status_code}  body={act.text[:200]}")
else:
    print("SKIPPED activation — workflow1 id not captured (may already exist).")
