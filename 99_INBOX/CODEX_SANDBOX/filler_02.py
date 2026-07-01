import json
from pathlib import Path


tasks = [
    {"id": 1, "task_type": "IMPORT", "status": "PENDING"},
    {"id": 2, "task_type": "EXPORT", "status": "COMPLETE"},
    {"id": 3, "task_type": "REVIEW", "status": "PENDING"},
    {"id": 4, "task_type": "ARCHIVE", "status": "FAILED"},
    {"id": 5, "task_type": "SYNC", "status": "PENDING"},
]

output_path = Path(__file__).with_name("fake_tasks.json")
output_path.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
