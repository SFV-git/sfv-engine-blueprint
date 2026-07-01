# Code Review — `99_INBOX/merge_reviewer.py`

**Reviewed:** 2026-07-01
**Reviewer:** Claude (Opus 4.8), read-only audit
**Scope:** bugs, unsafe file operations, path traversal, accidental modification of
scanned files, and any interaction with n8n / Docker / git / live services.
**Note:** `merge_reviewer.py` was NOT modified during this review (flag-only, per instructions).

---

## VERDICT: CLEAN

The script is safe to run against `C:\SFV_BLUEPRINT`. It reads `.md` files only,
never writes to or modifies any scanned file, has no path-traversal exposure, and
never invokes a subprocess, shell, network call, or anything touching n8n, Docker,
git, or any live service. The findings below are **advisory robustness notes only** —
none are blocking.

---

## Safety checklist (the specific concerns raised)

| Concern | Result | Evidence |
|---|---|---|
| Could it modify a scanned file instead of only reading? | **No** | Scanned files are opened only via `path.read_text(...)` (line 36), which is read-only. The single write in the program is `OUTPUT.write_text(...)` (line 71), and `OUTPUT` is a fixed, separate path. |
| Path traversal risk | **None** | `ROOT` is a hardcoded constant (line 8). No user/CLI/env input feeds any path. `os.walk` stays inside `ROOT`; symlinks are NOT followed (default `followlinks=False`), so it cannot escape the tree. `relative_to(ROOT)` (lines 32, 66) is display-only. |
| Unsafe file operations | **None** | No `os.remove`, `shutil`, `os.rename`, `open(..., "w")` on scanned files, no globs with deletion, no temp-file races. Only one deliberate write to the output file. |
| Touches n8n / Docker / git | **No** | No `subprocess`, `os.system`, `os.popen`, sockets, or HTTP anywhere. `.git` (plus `.obsidian`, `.smart-env`) is excluded from the walk (line 11); even if it weren't, the script only ever *reads* `.md` files. |

---

## Advisory notes (non-blocking)

1. **Line 36 — unhandled read exceptions abort the whole run.**
   `path.read_text(...)` has no `try/except`. If any `.md` file under the tree is
   locked (open in another app), permission-denied, or removed mid-walk, the
   exception propagates and the entire scan fails with no partial output. This is a
   robustness/availability issue, not a safety one — it can only *fail to write*,
   never corrupt a scanned file. Consider wrapping the read and skipping unreadable
   files with a warning.

2. **Line 71 — `OUTPUT` is overwritten unconditionally every run.**
   `REVIEW_QUEUE.md` in `99_INBOX` is clobbered each invocation. That is the intended
   behavior for a generated queue file, but if a human ever hand-edits that file, the
   edits are lost silently on the next run. Acceptable as designed; just be aware it
   is a generated artifact, not a hand-maintained one.

3. **Output file lives inside the scanned tree.**
   `OUTPUT` (`99_INBOX/REVIEW_QUEUE.md`) is itself a `.md` file under `ROOT`, so it is
   re-scanned on subsequent runs. This is harmless: the generated content
   (`# Overnight Merge Review Queue`, path bullets, the summary count) never contains
   the literal target heading `OVERNIGHT DRAFT — UNREVIEWED` as an ATX/setext heading,
   so it cannot self-match or inflate the count. No action needed; noted for clarity.

4. **Walk scope covers the entire tree except three dirs.**
   Only `.git`, `.obsidian`, `.smart-env` are excluded (line 11). If large or foreign
   `.md`-bearing directories exist under `SFV_BLUEPRINT` (e.g. `node_modules`, backups,
   Docker bind-mount contents), they will all be read. Read-only, so no safety impact —
   purely a performance consideration.

5. **Encoding handling is safe.**
   `encoding="utf-8-sig", errors="replace"` (line 36) means BOM-prefixed and
   malformed-byte files won't crash the reader — good. The em-dash (U+2014) in
   `TARGET` matches correctly as long as this source file is saved as UTF-8.

---

## Bottom line

No bugs that risk data, no unsafe writes, no traversal, no accidental modification of
scanned files, and zero contact with n8n / Docker / git / live services. Safe to run.
The only real-world failure mode is that a locked/unreadable `.md` file (note 1) would
abort the run without producing output — a resilience nit, not a hazard.
