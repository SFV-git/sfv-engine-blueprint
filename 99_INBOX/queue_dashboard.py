"""Generate a read-only summary of dispatched directives."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
DECISION_LOG = Path(__file__).resolve().parent / "DECISION_LOG.md"
OUTPUTS_DIR = Path(__file__).resolve().parent / "OUTPUTS"
DASHBOARD_DRAFT = ROOT / "VAULT_DASHBOARD_DRAFT.md"
EXECUTORS = ("ollama", "claude", "claude_code", "codex")

ROW_RE = re.compile(
    r"\|\s*(?P<timestamp>[^|\r\n]+?)\s*"
    r"\|\s*(?P<task_id>[^|\r\n]+?)\s*"
    r"\|\s*(?P<action>[^|\r\n]+?)\s*"
    r"\|\s*(?P<handler>[^|\r\n]+?)\s*"
    r"\|\s*(?P<status>[^|\r\n]+?)\s*"
    r"\|\s*(?P<output>[^|\r\n]*?)\s*\|"
)


def parse_timestamp(value: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            pass
    return datetime.min


def markdown_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\r", " ").replace("\n", " ").strip()


def output_exists(output_value: str, output_names: set[str]) -> bool:
    normalized = output_value.strip().replace("\\", "/")
    name = normalized.rsplit("/", 1)[-1]
    return bool(name) and name.casefold() in output_names


def main() -> None:
    if not DECISION_LOG.is_file():
        raise FileNotFoundError(f"Decision log not found: {DECISION_LOG}")
    if not OUTPUTS_DIR.is_dir():
        raise FileNotFoundError(f"Outputs directory not found: {OUTPUTS_DIR}")

    log_text = DECISION_LOG.read_text(encoding="utf-8-sig")
    rows = [
        {key: value.strip() for key, value in match.groupdict().items()}
        for match in ROW_RE.finditer(log_text)
        if match.group("action").strip().casefold() == "dispatch"
    ]

    output_names = {
        path.name.casefold() for path in OUTPUTS_DIR.rglob("*") if path.is_file()
    }
    executor_counts = Counter(row["handler"].casefold() for row in rows)
    status_counts = Counter(row["status"].casefold() for row in rows)
    recent = sorted(
        enumerate(rows),
        key=lambda item: (parse_timestamp(item[1]["timestamp"]), item[0]),
        reverse=True,
    )[:10]

    lines = [
        "# Vault Queue Dashboard (Draft)",
        "",
        f"_Generated {datetime.now().astimezone().isoformat(timespec='seconds')}_",
        "",
        "## Summary",
        "",
        f"- Total directives dispatched: **{len(rows)}**",
        "",
        "## Directives by Executor",
        "",
        "| Executor | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {executor} | {executor_counts[executor]} |" for executor in EXECUTORS)

    lines.extend(
        [
            "",
            "## Directives by Status",
            "",
            "| Status | Count |",
            "|---|---:|",
        ]
    )
    if status_counts:
        lines.extend(
            f"| {markdown_cell(status)} | {count} |"
            for status, count in sorted(status_counts.items())
        )
    else:
        lines.append("| _(none)_ | 0 |")

    lines.extend(
        [
            "",
            "## 10 Most Recent Dispatches",
            "",
            "| Timestamp | Task ID | Executor | Status | Result File |",
            "|---|---|---|---|---|",
        ]
    )
    for _, row in recent:
        result = "available" if output_exists(row["output"], output_names) else "missing"
        lines.append(
            "| {timestamp} | {task_id} | {handler} | {status} | {result} |".format(
                timestamp=markdown_cell(row["timestamp"]),
                task_id=markdown_cell(row["task_id"]),
                handler=markdown_cell(row["handler"].casefold()),
                status=markdown_cell(row["status"].casefold()),
                result=result,
            )
        )

    DASHBOARD_DRAFT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DASHBOARD_DRAFT} from {len(rows)} dispatched directives.")


if __name__ == "__main__":
    main()
