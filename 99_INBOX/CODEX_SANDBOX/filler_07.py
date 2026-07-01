def parse_frontmatter(markdown: str) -> dict[str, str]:
    """Extract selected keys from a Markdown YAML-style frontmatter block."""
    result: dict[str, str] = {}
    lines = markdown.splitlines()

    if not lines or lines[0].strip() != "---":
        return result

    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"STATUS", "DIRECTIVE_ID", "EXECUTOR"}:
            result[key] = value.strip()

    return result


samples = [
    (
        """---
STATUS: READY
DIRECTIVE_ID: DIR-001
EXECUTOR: codex
---
# First sample
""",
        {"STATUS": "READY", "DIRECTIVE_ID": "DIR-001", "EXECUTOR": "codex"},
    ),
    (
        """---
EXECUTOR: python-worker
IGNORED: value
STATUS: COMPLETE
DIRECTIVE_ID: DIR-002
---
Body text.
""",
        {
            "STATUS": "COMPLETE",
            "DIRECTIVE_ID": "DIR-002",
            "EXECUTOR": "python-worker",
        },
    ),
    (
        """---
STATUS: BLOCKED
DIRECTIVE_ID: DIR:003
EXECUTOR: manual
---
""",
        {"STATUS": "BLOCKED", "DIRECTIVE_ID": "DIR:003", "EXECUTOR": "manual"},
    ),
]


for index, (markdown, expected) in enumerate(samples, start=1):
    actual = parse_frontmatter(markdown)
    print(f"Sample {index}: {'PASS' if actual == expected else 'FAIL'}")
