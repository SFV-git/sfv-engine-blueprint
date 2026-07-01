import json
from pathlib import Path


input_path = Path(__file__).with_name("fake_tasks.json")
tasks = json.loads(input_path.read_text(encoding="utf-8"))
pending_count = sum(task["status"] == "PENDING" for task in tasks)

print(pending_count)
