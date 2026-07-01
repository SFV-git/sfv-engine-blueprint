# Code Review — BOM-Strip Fix in "Read Task" node

**File reviewed:** `C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json`
**Node:** `Read Task` (`n8n-nodes-base.code`, id `2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e`)
**Reviewer:** Claude (Opus 4.8)
**Date:** 2026-07-01
**Scope:** Correctness-only check of the BOM-stripping fix from the unsupervised codex run. No files were modified. This is a vault copy, not the live n8n DB — no live services touched.

---

## VERDICT: ✅ CLEAN

The BOM-stripping fix is present, is syntactically valid JavaScript, correctly handles both BOM and non-BOM input without breaking normal parsing, and the surrounding JSON file is intact and un-corrupted.

One out-of-scope advisory is noted at the end — it does **not** affect this verdict but is worth knowing.

---

## What the fix looks like

Inside the `Read Task` node's `jsCode`, the file read now strips a leading UTF-8 BOM before parsing:

```js
const content = fs.readFileSync(filePath, 'utf8').replace(/^﻿/, '');
task = JSON.parse(content);
```

(The whole block is wrapped in `try { ... } catch(e) { return []; }`, so a genuinely malformed file still fails safely.)

---

## Verification performed

All checks were run against the actual bytes in the file (extracted via `JSON.parse` of the workflow, then re-checked), not by eye.

| # | Check | Method | Result |
|---|-------|--------|--------|
| 1 | Fix actually present | Extracted `Read Task.parameters.jsCode`, grepped for the BOM strip | ✅ Present: `.replace(/^﻿/, '')` sits between `readFileSync(...,'utf8')` and `JSON.parse(content)` |
| 2 | Syntactically valid JS | Wrote the full node code to disk, ran `node --check` | ✅ PASS (no syntax errors in the whole node body) |
| 3a | Handles BOM input | Fed `'﻿' + validJSON` through the exact expression | ✅ BOM removed, `JSON.parse` succeeds |
| 3b | Doesn't break non-BOM input | Fed plain JSON through the expression | ✅ String returned unchanged (`output === input`), parses normally |
| 3c | Only strips a *leading* BOM | Fed JSON with a U+FEFF in the middle of a value | ✅ Anchored `^` means the interior BOM is preserved — no accidental corruption of legitimate content |
| 3d | Fix is actually necessary | Parsed BOM-prefixed JSON *without* the strip | ✅ Confirmed it throws `SyntaxError` without the fix, so the strip is doing real work |
| 4 | Rest of JSON still valid | Full-file `JSON.parse` | ✅ Parses cleanly; all 6 nodes present, `connections` graph intact, no truncation or trailing-comma damage from the edit |

### Notes on correctness details
- **Regex is correct.** `/^﻿/` matches exactly one code unit U+FEFF at string start. This is the canonical, minimal BOM strip.
- **In the JSON encoding** the escape appears as `\\uFEFF` (PowerShell `ConvertTo-Json` escaped the backslash). That decodes to the two-character JS source `﻿` inside a regex literal — i.e. the BOM character, **not** a literal backslash. Verified by running the extracted source, not just reading it.
- **Ordering is right:** the strip is applied to the `readFileSync` result *before* `JSON.parse`, which is the only order that works.
- **`utf8` decode + `^﻿`** is the correct pairing. Reading as `'utf8'` turns the 3 BOM bytes (`EF BB BF`) into the single character U+FEFF, which is exactly what the regex targets.

---

## Advisory (OUT OF SCOPE — verdict remains CLEAN)

This is **not** a defect in the reviewed fix and requires no action to accept it. Flagging only for completeness:

Two downstream nodes re-read the **same task file** and call `JSON.parse` **without** the BOM strip:

- `Write + Log` node: `const taskData = JSON.parse(fs.readFileSync(task.file_path, 'utf8'));`
- `Non-Ollama Handler` node: `const taskData = JSON.parse(fs.readFileSync(task.file_path, 'utf8'));`

Because `Read Task` strips the BOM only in memory (it never rewrites the source file), a task file that *actually* ships with a BOM would be re-read with its BOM still on disk by these later nodes and would throw a `SyntaxError` there — meaning the end-to-end path for a genuinely BOM'd task is still not fully hardened.

This does not change the correctness of the `Read Task` fix itself, which was the item under review. If you want full BOM resilience across the workflow, apply the same `.replace(/^﻿/, '')` to those two reads. Recommend as a follow-up, not a blocker.

---

## Bottom line

The `Read Task` BOM-strip fix is correct, safe, and non-destructive. JSON file is uncorrupted. **Accept the fix.** Optionally schedule the two downstream reads for the same treatment.

## CONNECTED FILES
- [[DASHBOARD|Dashboard]]
- [[SESSION_STATE|Session State]]
