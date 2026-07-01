from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent

documents = [
    (
        "placeholder_01.md",
        "DRAFT",
        "DIR-FAKE-001",
        "2026-07-01",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed tempor incididunt ut labore et dolore magna aliqua.",
    ),
    (
        "placeholder_02.md",
        "PENDING",
        "DIR-FAKE-002",
        "2026-07-01",
        "Vestibulum fictum neque, blandit vel tempor sit amet, cursus vitae sapien; nulla facilisi proin varius.",
    ),
    (
        "placeholder_03.md",
        "ARCHIVED",
        "DIR-FAKE-003",
        "2026-07-01",
        "Praesent commodo lorem at ipsum feugiat, vitae malesuada erat tincidunt, donec posuere sem vel urna.",
    ),
]

for filename, status, directive_id, created, paragraph in documents:
    content = (
        "---\n"
        f"STATUS: {status}\n"
        f"DIRECTIVE_ID: {directive_id}\n"
        f"CREATED: {created}\n"
        "---\n\n"
        f"{paragraph}\n"
    )
    (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")

print(f"Created {len(documents)} Markdown files in {OUTPUT_DIR}")
