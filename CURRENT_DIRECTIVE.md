---
STATUS: ACTIVE
DIRECTIVE_ID: BLUEPRINT-20260629-P2-VIDEO-EDIT-001
EXECUTOR: claude_code
---

Read the following vault files before writing anything:
- C:\SFV_BLUEPRINT\08_TESTS\BLUEPRINT_COVERAGE_MAP.md (§P2 and Domain B §8 for context)
- C:\SFV_BLUEPRINT\01_BRANCHES\SFV_UGC.md
- C:\SFV_BLUEPRINT\01_BRANCHES\SFV_LIVE.md
- C:\SFV_BLUEPRINT\01_BRANCHES\SFV_EVENTS.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\DELIVERY.md
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\NAMING_CONVENTIONS.md

Then write a new file: C:\SFV_BLUEPRINT\04_WORKFLOWS\VIDEO_EDIT_WORKFLOW.md

This doc blueprints the Premiere Pro / video-edit workflow for SFV Engine. It must cover:

1. Tool decision: Premiere Pro as primary editor. Flag CapCut and Aditor.ai as UNCONFIRMED candidates for UGC reels — mark the final tool choice FOR HUMAN REVIEW.
2. Per-branch edit approach (one section per branch that has video):
   - SFV_UGC: reel assembly, hook-first structure, caption handoff, client revision loop
   - SFV_LIVE: highlight reel, event recap, multi-cam if applicable
   - SFV_EVENTS: short-form recap delivery
   - SFV_ATHLETICS: action highlight, slow-mo usage
   - SFV_STUDIO: product/portrait video if applicable
   - SFV_ARCHIVE: preservation edits only (no stylistic changes)
3. Audio workflow: sync, music licensing approach (UNCONFIRMED — flag), levels target
4. Color: LUT or Premiere Lumetri approach per branch (flag as UNCONFIRMED where unknown)
5. Caption/subtitle handoff: where Whisper (R&D Terminal) output feeds into the edit
6. Export presets: per-branch output spec — codec, resolution, bitrate, container. Flag anything not yet confirmed as UNCONFIRMED.
7. FFmpeg post-export step: any repackaging or validation pass before delivery
8. Handoff to delivery: file naming, staging path (D:\), delivery workflow

Rules:
- Label everything honestly: CANON where it's locked practice, UNCONFIRMED where it's inferred or undecided, FOR HUMAN REVIEW where Will needs to ratify.
- Do NOT invent tool decisions that aren't in the vault — flag open decisions explicitly.
- STATUS of the finished doc: FOR HUMAN REVIEW
- Include standard frontmatter: STATUS, VERSION v0.1.0, OWNER WILL, CREATED 2026-06-29, CREATED_BY loop directive BLUEPRINT-20260629-P2-VIDEO-EDIT-001
- End the doc with a CONNECTED FILES section linking to: SFV_UGC, SFV_LIVE, SFV_EVENTS, DELIVERY, NAMING_CONVENTIONS, EXPORT, MEDIA_PIPELINE