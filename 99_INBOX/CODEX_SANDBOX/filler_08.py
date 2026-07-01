from pathlib import Path


OUTPUT_PATH = Path(__file__).with_name("mock_decision_log.md")

rows = [
    ("2026-07-01T09:00:00-03:00", "DIR-001", "Initialize mock workspace", "completed"),
    ("2026-07-01T09:15:00-03:00", "DIR-002", "Review placeholder requirements", "completed"),
    ("2026-07-01T09:30:00-03:00", "DIR-003", "Draft sample schema", "completed"),
    ("2026-07-01T09:45:00-03:00", "DIR-004", "Generate mock records", "completed"),
    ("2026-07-01T10:00:00-03:00", "DIR-005", "Validate table formatting", "completed"),
    ("2026-07-01T10:15:00-03:00", "DIR-006", "Check directive ordering", "completed"),
    ("2026-07-01T10:30:00-03:00", "DIR-007", "Mark sample review", "pending"),
    ("2026-07-01T10:45:00-03:00", "DIR-008", "Archive mock decision log", "planned"),
]

lines = [
    "# Mock Decision Log",
    "",
    "| timestamp | directive_id | action | status |",
    "|---|---|---|---|",
]
lines.extend(f"| {timestamp} | {directive_id} | {action} | {status} |" for timestamp, directive_id, action, status in rows)

OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
