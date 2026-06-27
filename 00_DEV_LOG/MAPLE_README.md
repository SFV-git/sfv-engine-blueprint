---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple — transfer package build)
SOURCE: Full read of SFV_BLUEPRINT.zip snapshot (220 files, zipped 2026-06-10 ~22:41)
---

# READ ME FIRST — SFV ENGINE TRANSFER PACKAGE

This package is the output of the Fable runbook sessions executed 2026-06-10 against a
snapshot of the vault (`E:\SFV_BLUEPRINT` copy, uploaded as zip). It is NOT the vault.
Nothing in here is CANON. Every file is FOR HUMAN REVIEW until Will integrates it.

## PACKAGE STRUCTURE

```
SFV_ENGINE_TRANSFER_2026-06-10/
├── 00_CONTROL/          ← read first. Manifest, missing-files list, source-of-truth rules.
│   ├── README_FIRST.md                  (this file)
│   ├── local_file_inventory.txt         (every file in the snapshot, byte sizes)
│   ├── BLUEPRINT_MANIFEST.md            (every doc: purpose, status, stage, confidence, dependents)
│   ├── MISSING_REFERENCED_FILES.md      (referenced-but-absent, empty stubs, unformalized specs)
│   └── SOURCE_OF_TRUTH_RULES.md         (precedence ladder for resolving conflicts)
├── 02_AUDITS/           ← Session Maple Prompt B output.
│   ├── ARCHITECTURE_AUDIT.md            (findings, severity-tagged, source-cited)
│   ├── CONTRADICTION_MATRIX.md          (every cross-doc conflict found, one row each)
│   ├── DEPENDENCY_GRAPH.mmd             (Mermaid — blocking edges, critical path)
│   └── CRITICAL_PATH.md                 (ordered next-actions to first new milestone)
└── (later sessions add: 03_ROADMAP, 07_CORE_SPECS, stage blueprints, etc.)
```

## SAVE CONVENTION

Drop the folders from this package onto the SSD transfer root beside `01_SOURCE_SNAPSHOT/`.
Later Fable sessions (Cedar, Granite, Forge, Studio, Handoff) re-upload the vault zip PLUS
this package's prior outputs per the runbook attachment register.

## STAGE VOCABULARY USED IN THIS PACKAGE

The runbook says MVP/v2/v3. Mapped onto SFV's actual phase reality:

| Label | Meaning in SFV terms |
|---|---|
| NOW | Live or required for current operational core (queue processor era) |
| P1 | Unlocked by PostgreSQL + Docker (Open WebUI, n8n-MCP, workflow3, Gemini route, queue-mode prep) |
| P2 | Vector layer, monitoring stack, media pipeline, Redis queue mode |
| FUTURE | Scaling: operators, NAS, multi-node, commercial engine (v7.x+) |
| SHARED | Rules, schemas, naming, conventions inherited by everything |

## HARD RULES THIS PACKAGE FOLLOWS

1. Snapshot files are source of truth; this package never silently resolves a contradiction —
   conflicts go to CONTRADICTION_MATRIX.md with Will's name on the decision.
2. Everything not verifiable from the snapshot is tagged [UNCONFIRMED] or [INFERENCE].
3. Live-system state (n8n UI, ollama list, git remote) could NOT be verified from a MacBook —
   those items are explicitly flagged [UNVERIFIABLE FROM SNAPSHOT].
4. ANTIGRAVITY/MYTHOS/FABLE OUTPUTS ≠ WILL'S APPROVAL. Including this package.

## ONE URGENT ITEM BEFORE ANYTHING ELSE

`03_INFRASTRUCTURE/n8n_env.ps1` — the gitignored live-secrets file — IS IN THIS SNAPSHOT ZIP.
It traveled off the Engine Body onto the SSD, the MacBook, and an upload. Per SECRETS_POLICY
this counts as suspected exposure. See ARCHITECTURE_AUDIT.md finding S1. Short version:
rotate the Tavily key, and exclude `n8n_env.ps1` from every future snapshot/zip.

## CONNECTED FILES
- [[BLUEPRINT_MANIFEST|Blueprint Manifest]]
- [[MISSING_REFERENCED_FILES|Missing Referenced Files]]
- [[SOURCE_OF_TRUTH_RULES|Source of Truth Rules]]
- [[ARCHITECTURE_AUDIT|Architecture Audit]]
- [[CONTRADICTION_MATRIX|Contradiction Matrix]]
- [[CRITICAL_PATH|Critical Path]]
