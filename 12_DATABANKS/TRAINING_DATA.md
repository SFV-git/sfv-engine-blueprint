---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# TRAINING DATA

Quality control training loop data.

---

## PURPOSE
Every QC outcome (approved or rejected) trains the system
to better understand what quality looks like per client.

## STRUCTURE
```
TRAINING_DATA/
├── QC_APPROVED/
│   └── [CLIENT_ID]/
│       └── [reel files + QC notes]
└── QC_REJECTED/
    └── [CLIENT_ID]/
        └── [reel files + rejection reason]
```

## WHAT GETS LOGGED PER OUTCOME
- Client ID
- Reel ID
- QC check results (pass/fail per check)
- Will's final decision (approve/reject)
- Rejection reason if rejected
- Rework required (yes/no)

## HOW IT TRAINS THE SYSTEM
Over time: system learns client-specific quality baseline.
After ~10 deliveries per client: QC accuracy improves significantly.
System proposes client-specific QC rule updates → Will approves.

## CONNECTED FILES
- [[12_DATABANKS/DATABANK_ARCHITECTURE|Databank Architecture]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
