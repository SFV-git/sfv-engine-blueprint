---
STATUS: ACTIVE
DIRECTIVE_ID: BLUEPRINT-20260629-P5-LIGHTROOM-001
EXECUTOR: claude_code
---

UNICODE REGRESSION MARKER (this body intentionally contains: arrow -> char \u2192, em-dash \u2014, smart quotes \u201cx\u201d). If you can read this, the encoding fix holds.

Read the following vault files before writing anything:
- C:\SFV_BLUEPRINT\08_TESTS\BLUEPRINT_COVERAGE_MAP.md (section P5, and the Domain A Lightroom rows)
- C:\SFV_BLUEPRINT\02_BRANCHES\SFV_STUDIO.md
- C:\SFV_BLUEPRINT\02_BRANCHES\SFV_EVENTS.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\EXPORT.md (read if it exists)
- C:\SFV_BLUEPRINT\00_DEV_LOG\MISSING_REFERENCED_FILES.md (section 3 references the battle-tested Morning Walk / Shamar Lightroom recipe)
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\NAMING_CONVENTIONS.md

Then write ONE new file: C:\SFV_BLUEPRINT\04_WORKFLOWS\LIGHTROOM_WORKFLOW.md

This doc blueprints the Lightroom Classic preset + catalog + export workflow per branch. The coverage audit (P5) notes this is MISSING as a doc but battle-tested in practice. Capture the real recipe where the vault records it, and flag everything unknown. Cover:

1. CATALOG STRUCTURE: one catalog vs per-branch catalogs. Where catalogs live (C:\ or D:\). Flag UNCONFIRMED if not recorded.

2. IMPORT INTO LIGHTROOM: how culled selects land in LR (handoff from INGEST/CULLING). Folder vs collection. Flag the handoff point.

3. PER-BRANCH PRESETS:
   - SFV_STUDIO: batch edit + sync preset (this is the most documented - capture what SFV_STUDIO.md says)
   - SFV_EVENTS: portrait edit approach. Capture the battle-tested Morning Walk / Shamar recipe from MISSING_REFERENCED_FILES section 3 if present (Adaptive Portrait preset, AI-mask sync, Generative Remove, sRGB q80-85 2560px). Label it CANON-in-practice but note it was not previously in the vault.
   - SFV_ARCHIVE: edit approach
   - LIVE / ATHLETICS / WORLD / 404 / MYTHOLOGY: mark MISSING/UNCONFIRMED where no LR approach is documented

4. PRESET MANAGEMENT: where preset files (.xmp) are stored, how synced between machines, version control. Flag UNCONFIRMED.

5. AI MASKING + GENERATIVE REMOVE: where used (the Shamar recipe uses AI-mask sync + Generative Remove). Per-branch applicability.

6. EXPORT SETTINGS PER BRANCH: resolution, color space, quality, sharpening. Capture the sRGB q80-85 2560px spec for EVENTS. Flag others UNCONFIRMED. Resolve the EXPORT.md "specs TBD" hole where you can.

7. HANDOFF TO DELIVERY: export destination path (D:\ staging), naming per NAMING_CONVENTIONS, which delivery platform per branch (Pixieset for STUDIO, Zenfolio for EVENTS).

Rules:
- Label honestly: CANON where locked in a CANON doc, CANON-in-practice for the battle-tested recipe (with a note it was not previously documented), UNCONFIRMED where inferred/undecided, FOR HUMAN REVIEW where Will must ratify, MISSING where nothing exists.
- Do not invent settings. Where a number is not in the vault, say UNCONFIRMED.
- End with a consolidated open-decisions table.
- Doc STATUS: FOR HUMAN REVIEW
- Frontmatter: STATUS, VERSION v0.1.0, OWNER WILL, CREATED 2026-06-29, CREATED_BY loop directive BLUEPRINT-20260629-P5-LIGHTROOM-001
- CONNECTED FILES linking to: SFV_STUDIO, SFV_EVENTS, EXPORT, DELIVERY, INGEST, CULLING, NAMING_CONVENTIONS, EVENTS_ZENFOLIO_DELIVERY