# Code Review — `99_INBOX/queue_dashboard.py`

- **Reviewed:** 2026-07-01
- **Reviewer:** Claude (Opus 4.8), automated code review
- **File under review:** `C:\SFV_BLUEPRINT\99_INBOX\queue_dashboard.py`
- **Scope of concern:** bugs, unsafe file operations, path traversal, writes outside `C:\SFV_BLUEPRINT`, any contact with n8n / Docker / git / live services
- **Note:** `queue_dashboard.py` was NOT modified. This is a flag-only review.

---

## VERDICT: **CLEAN**

The script is a self-contained, read-mostly reporting tool. It reads one markdown
log, scans a directory tree for filenames, and writes one draft markdown file.
All paths are derived from the script's own location (`__file__`), not from any
external or attacker-controlled input. Nothing in it invokes a shell, network,
subprocess, n8n, Docker, git, or any other live service.

No blocking issues found. The notes below are **advisory only** — none require a
fix before this script can be run safely.

---

## Safety checklist

| Concern | Result | Evidence |
|---|---|---|
| Writes outside `C:\SFV_BLUEPRINT` | **No** | Only write target is `DASHBOARD_DRAFT` = `ROOT / "VAULT_DASHBOARD_DRAFT.md"`; `ROOT` = `__file__`.parent.parent = `C:\SFV_BLUEPRINT` (line 11, 14, 124) |
| Reads outside the vault | **No** | Reads only `DECISION_LOG` (99_INBOX) and rglobs `OUTPUTS_DIR` (99_INBOX) — both `__file__`-derived (lines 12–13, 52, 60) |
| Path traversal from log content | **No** | The log's `output` field is only split to a basename and compared against a name set — never opened, read, or written (lines 40–43, 113). No filesystem call ever receives log-derived path data. |
| Touches n8n / Docker / git | **No** | No `subprocess`, `os.system`, `socket`, `requests`, or any client import anywhere in the file. |
| Network / shell / eval | **No** | Imports are only `collections`, `datetime`, `pathlib`, `re`. |
| Destructive deletes | **No** | No `unlink`, `rmtree`, `remove`, or `os.remove`. |

---

## Advisory notes (non-blocking)

**1. Line 124 — silent overwrite of `VAULT_DASHBOARD_DRAFT.md`**
`write_text` unconditionally overwrites `C:\SFV_BLUEPRINT\VAULT_DASHBOARD_DRAFT.md`
with no backup and no confirmation. This is the file's intended output and the name
signals it is a regenerable draft, so this is acceptable — just be aware any manual
edits to that draft are lost on each run. Not a safety issue (target is inside the vault).

**2. Lines 40–43 / 113 — `output_exists` matches by basename only**
A result file is reported "available" if *any* file anywhere under `OUTPUTS/` shares
its basename (case-insensitive), regardless of subdirectory. Two unrelated files with
the same name in different folders will produce a false "available". This is a
report-accuracy nuance, not a correctness or safety bug.

**3. Line 60 — `OUTPUTS_DIR.rglob("*")` may traverse symlinks**
If a symlink/junction inside `OUTPUTS/` points outside the vault, `rglob` + `is_file()`
would `stat()` targets outside `C:\SFV_BLUEPRINT`. This is metadata-only (no read/write
of contents) and requires a pre-existing malicious link inside `OUTPUTS/`, so the risk
is negligible. Worth knowing if `OUTPUTS/` is ever populated from untrusted sources.

**4. Lines 15, 84 — "Directives by Executor" table is fixed to 4 known executors**
`EXECUTORS = ("ollama", "claude", "claude_code", "codex")`. Any dispatch whose `handler`
is not one of these is counted in the **Total** (line 77) but never shown in the
per-executor table, so per-executor counts may not sum to the total. Display/reporting
gap only.

**5. Lines 17–24 — regex assumes exactly 6 pipe-delimited columns**
Rows with a different column count are silently skipped. If `DECISION_LOG.md`'s table
schema ever changes, dispatches could be under-counted with no error raised. Assumption,
not a bug in current form.

**6. Line 33 — unparseable timestamps sort as `datetime.min`**
Rows with malformed timestamps fall to the bottom of the "most recent" ordering rather
than raising. Benign and arguably desirable. All timestamps compared are naive, so there
is no naive/aware `datetime` comparison hazard.

---

## Bottom line

Safe to run as-is. It cannot write, delete, or reach outside `C:\SFV_BLUEPRINT`, and it
has no path to n8n, Docker, git, the network, or a shell. The advisory items are quality/
accuracy refinements a human may optionally address; none are required for safe execution.

## CONNECTED FILES
- [[DASHBOARD|Dashboard]]
- [[SESSION_STATE|Session State]]
