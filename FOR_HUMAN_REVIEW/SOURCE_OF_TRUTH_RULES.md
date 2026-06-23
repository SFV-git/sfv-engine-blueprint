---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple, Prompt A)
---

# SOURCE OF TRUTH RULES — FOR ALL LATER SESSIONS AND MODELS

How any model (Fable, Sonnet, Gemini, qwen, future foreman) resolves conflicting
information when working from this transfer package or the vault. These extend —
never override — 01_CANON_RULES/RULES.md and the .claude/rules set.

## PRECEDENCE LADDER (highest wins)

1. **Will's explicit, current-session statement.** Beats everything, including CANON files.
   Log it to the vault immediately (PROPOSALS or decision record) so rule 2 inherits it.
2. **Recorded Will decisions** — DECISIONS.md entries, QUESTIONS_FOR_WILL resolved lines,
   PROPOSALS approved/deferred/rejected blocks, SESSION_STATE "DECISIONS LOCKED" lists.
   Newest dated decision wins on the same topic.
3. **STATUS: CANON vault docs.** Within CANON, newer LAST_UPDATED wins on overlapping claims.
   CANON-vs-CANON conflict → do NOT silently resolve. Add a row to CONTRADICTION_MATRIX,
   flag FOR HUMAN REVIEW, proceed only on the non-conflicting parts.
4. **Live system state** (n8n UI, `ollama list`, Task Scheduler, git remote) is RUNTIME truth.
   When vault and runtime disagree, runtime is what's real and the vault is what's wrong —
   the fix is a vault write-back, never pretending the vault is right. From a remote/MacBook
   session, runtime is [UNVERIFIABLE FROM SNAPSHOT]; say so, don't guess.
5. **Vault workflow JSONs** are IMPORT-SOURCE truth (what to load), never RUNTIME-IDENTITY
   truth. JSON `id` fields ≠ live n8n workflow IDs. Live IDs come from the n8n UI only.
6. **FOR HUMAN REVIEW / UNCONFIRMED / DRAFT docs** — advisory. Can inform analysis, can never
   be built from, can never override a CANON claim.
7. **RESEARCH-status docs** (10_REFERENCES) — reference only. Never built from (canon-control rule).
8. **Derived packages** (this transfer set, MYTHOS outputs, Antigravity reports, Fable audits) —
   advisory analysis of the layers above. Integration path is PROPOSALS → Will → vault edit.
   ANTIGRAVITY/MYTHOS/FABLE OUTPUT ≠ WILL'S APPROVAL — standing rule, restated.
9. **Model memory / chat history** — lowest tier. Anything load-bearing gets verified against
   files before use. Memory is a hint, never a citation.

## SPECIFIC TIE-BREAKS ALREADY NEEDED IN THIS SNAPSHOT

| Conflict class | Rule |
|---|---|
| SESSION_STATE session blocks disagree (06-03 vs later) | SESSION_STATE is append-style history; treat the NEWEST block as intended-current, but its own [UNCONFIRMED] flags stand until A6 runtime verification. |
| Stale CANON inline tags vs newer resolved decisions (e.g. SFV_404 IG [UNCONFIRMED] vs Q001 resolved) | The decision record (rule 2) wins; the stale inline tag is a mechanical-fix candidate, not an open question. |
| Doc vs implementation (CONFIDENCE_LOGIC vs workflow1 JSON think-strip) | Code that Will validated end-to-end (06-03 confirmation) outranks the doc's "pending" framing; doc gets updated, code doesn't get reverted to match a stale doc. |
| Schema definitions | JOB_ENVELOPE_SPEC.md is the single envelope source once promoted; until then, Blueprint §4 base + SPEC extensions, and no doc may re-define fields inline. |
| Decision ledger fragmentation | Until Will designates one ledger, a "decision exists" claim must cite file + date. Unsourced "we decided" = [UNCONFIRMED]. |

## RULES FOR THIS PACKAGE'S OWN OUTPUTS

- Every generated doc carries STATUS: FOR HUMAN REVIEW and CREATED_BY.
- Generated docs cite source files for material claims; short excerpts only.
- Later Fable sessions treat `01_SOURCE_SNAPSHOT` (the zip) as authoritative over
  earlier-session generated docs. Raw source loads before derivatives, always.
- If a later session finds this package contradicting the snapshot: snapshot wins,
  package gets corrected, correction noted in DELIVERABLE_COMPLETENESS_AUDIT at the end.

## SNAPSHOT-SPECIFIC CAVEATS

- Snapshot timestamp: files zipped 2026-06-10 (latest mtimes 06-10 05:29–06:20 vault-time).
  Anything done on Engine Body after the zip is invisible here.
- `.git/` was excluded from this analysis — commit history, remote, and uncommitted-change
  state are all [UNVERIFIABLE FROM SNAPSHOT].
- Live secrets file rode along in the zip (audit S1). Future snapshot command must add:
  `--exclude 'n8n_env.ps1' --exclude '.claude*/settings.local.json'` (the latter is
  machine-local allow-lists, not secrets, but has no business traveling).
