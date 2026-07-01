---
STATUS: FOR HUMAN REVIEW
TYPE: SESSION HANDOFF
DATE: 2026-07-01
SESSION: Claude Chat (autonomous doc revamp)
---

# HANDOFF — 2026-07-01 AUTONOMOUS DOC REVAMP

## WHAT WILL ASKED
Run the low-scoring blueprint docs back through a fix pass using the web search tool (Perplexity-style
fact-checking) instead of local-model guessing, so they'd actually score 4-5 on a Perplexity re-audit.
Full autonomy granted, minimize token use, don't text until done.

## WHAT WAS ACTUALLY WRONG (important context)
The FULL_SYSTEM_AUDIT.md showed ~100 files at "0/5" — those are NOT real scores, they're PARSE_ERRORs.
qwen3:14b was fighting Aider for VRAM during the audit run and returned malformed/empty JSON on most
files. Only ~26 files (the ones scored after Aider stopped) got clean scores: 9× 3/5, 7× 4/5.
So the real work was NOT "half the vault is slop" — it was a handful of genuinely weak docs plus the
2 Perplexity-confirmed disasters. **A clean re-audit is still needed** (release VRAM first).

## DOCS REWRITTEN THIS SESSION (all web-researched, all FOR HUMAN REVIEW)
1. **VIDEO_EDIT_WORKFLOW.md v2.0** (was 1.5/5) — removed every hallucinated Premiere feature Perplexity
   caught (Content-Aware Fill, Keylight, "Audio Sync Tool", fake Preferences>Export). Rebuilt on verified
   Premiere 2026 facts: Pancake timeline, Auto Reframe, Ultra Key, Media Browser, waveform multicam sync,
   loudness specs, correct export/ProRes handling. Added SaaS-resale licensing section.
2. **UGC_BUSINESS_PIPELINE.md v2.0** (was 1/5) — deleted the entire wrong-business-model martech stack.
   Rebuilt as a real solo-creator pipeline on verified 2026 UGC market data: rate tiers, usage-rights
   pricing, revision policy, 50/50 payment terms, brief intake, scope protection, n8n hooks.
3. **SCHEDULING_WORKFLOW.md v2.0** (was 3/5) — killed the invented foreign-timezone "Branch A-H" and
   fake team roles. Rebuilt for solo/Halifax/Atlantic-time reality. Surfaced a REAL cost decision:
   8 IG accounts exceed Later's 6-set Advanced tier — Will must pick add-on sets vs consolidation vs
   alternative tool.
4. **SFV_UGC.md** (was 3/5) — not slop, just thin + UNCONFIRMED placeholders. Cross-linked to the new
   pipeline spec, left name/handle/pricing as Will-only decisions (did not invent them).
5. **SFV_UGC_SEED.md** (new, earlier this session) — Will's actual business ground truth.

## STILL OPEN — NEEDS WILL, NOT AI
- **SFV_UGC_SEED.md holes**: rate card $, delivery method, revision policy, payment tool. 5 min of Will's
  input unlocks final pricing across all UGC docs. Every "[FOR HUMAN REVIEW]" $ figure waits on this.
- **Later account cost fork** (SCHEDULING §2): 8 accounts vs 6-set tier. Real recurring-cost decision.
- **Per-branch LUT files** (VIDEO_EDIT §7): the actual color deliverable doesn't exist yet.
- **Caption voice per branch** (QUESTIONS_FOR_WILL #12).

## NOT TOUCHED (deliberately)
Remaining 3/5 docs — OPEN_WEBUI_SPEC, POSTGRES_MIGRATION, HERMES_LOOP, JOB_ENVELOPE_SPEC, MODEL_ROUTING,
RULES — are internal-stack technical docs. Web research can't fix them; they need Will's architectural
decisions. Filling them with invented detail risks contradicting the real setup. Left for a working
session with Will, not autonomous guessing.

## NEXT STEPS (recommended order)
1. Re-run Perplexity audit on the 4 rewritten docs to confirm they now score 4-5.
2. Will fills SFV_UGC_SEED.md holes → re-run UGC pricing docs.
3. Clean vault re-audit: release qwen3 VRAM (`release_qwen.ps1`), then run vault_self_audit.py with
   nothing else hitting the GPU.
4. Decide the Later account-cost fork.

## STACK STATE AT SESSION END
- Hermes: healthy (deps restored after Aider conflict). Nous auth expires 14:30 AT today — re-auth needed.
- Ollama: running. qwen3:14b + devstral-small-2 both pulled. Can't co-reside in 16GB VRAM.
- Aider: installed CLEAN in isolated venv C:\SFV_TOOLS\aider-venv (NOT in Hermes venv — that broke it once, fixed).
- n8n: healthy (200).
- CURRENT_DIRECTIVE.md: still holds the Fable UGC audit directive (EXECUTOR: claude), unrun.

## CONNECTED FILES
- [[SFV_UGC_SEED|SFV UGC Seed]]
- [[UGC_BUSINESS_PIPELINE|UGC Business Pipeline]]
- [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]]
- [[SCHEDULING_WORKFLOW|Scheduling Workflow]]
