---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-09
CREATED_BY: Claude Chat
MERGE_INTO: STANDALONE
---

# MYTHOS PROTOCOL — FULL-VAULT AUDIT ROLE

> Defines when and how the 1M-context model (Google AI Studio / "MYTHOS" role) is used
> against the vault. First run executed 2026-06-09 via Claude Chat + Desktop Commander
> (direct vault access made the external paste unnecessary).

---

## ROLE

Full-vault, single-pass analysis that session-based tools cannot do without fragmentation:
1. Cross-doc contradiction sweep (IPs, statuses, decisions)
2. UNCONFIRMED / FOR HUMAN REVIEW inventory
3. Open decisions with no resolution logged
4. Broken references (missing files, dead wikilinks, stale paths)
5. Architectural gaps not blueprinted anywhere

## ROUTING RULE

| Condition | Tool |
|---|---|
| Claude Chat has Desktop Commander access to vault | Claude runs the audit directly — preferred (writes fixes immediately) |
| No vault access / second opinion wanted | Google AI Studio (1M context) — paste full vault dump |

## VAULT DUMP COMMAND (for external run)

```powershell
Get-ChildItem C:\SFV_BLUEPRINT -Recurse -Filter "*.md" |
  Where-Object { $_.FullName -notmatch '\\.git|\\.obsidian|\\.smart-env' } |
  ForEach-Object { "=== $($_.FullName) ===`n" + (Get-Content $_.FullName -Raw) + "`n`n" } |
  Set-Clipboard
```

## OUTPUT RULES

- Findings only — one line per finding, file + issue, severity 🔴/🟡/🟢
- No summaries, no system re-explanation
- External (AI Studio) outputs are FINDINGS ONLY — never written to vault directly. Claude verifies against actual files, then patches. MYTHOS output ≠ Will's approval (same rule as Antigravity).

## CADENCE

[FOR HUMAN REVIEW]: Proposed — run before each phase gate (pre-PostgreSQL, pre-Docker, pre-workflow3 build) and after any multi-session burst that touched 5+ docs. Will confirms.

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[PROPOSALS|Proposals]]
- [[RATE_LIMITS|Rate Limits]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
