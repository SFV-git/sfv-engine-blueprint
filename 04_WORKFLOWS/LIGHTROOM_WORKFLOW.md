---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-29
CREATED_BY: loop directive BLUEPRINT-20260629-P5-LIGHTROOM-001
LAST_UPDATED: 2026-06-29
PURPOSE: Blueprint the Lightroom Classic preset + catalog + export workflow per branch.
  Closes MASTER GAP LIST P5 (BLUEPRINT_COVERAGE_MAP.md) — "Lightroom preset + catalog
  per-branch workflow: MISSING as a doc; battle-tested in practice." Promotes the
  Morning Walk / Shamar export recipe out of chat/memory and resolves the EXPORT.md
  "specs TBD" hole where the vault records a real number.
---

# LIGHTROOM CLASSIC WORKFLOW — PER BRANCH

> **Read this label key before trusting any line below.**
>
> - **CANON** — locked in a CANON doc (cited inline).
> - **CANON-in-practice** — battle-tested and executed in the real pipeline (Morning Walk
>   May 28 / Shamar June 6), recorded in memory and `MISSING_REFERENCED_FILES.md §3`, but
>   **never previously written into the vault**. Real, but not yet ratified as CANON here.
> - **UNCONFIRMED** — inferred from adjacent docs, or genuinely undecided. Not a settled fact.
> - **FOR HUMAN REVIEW (FHR)** — Will must ratify before it becomes CANON.
> - **MISSING** — nothing exists in the vault for this; no recipe in practice either.
>
> **Rule honored:** no settings were invented. Where the vault does not record a number,
> this doc says UNCONFIRMED rather than guessing one.

This doc covers Lightroom Classic only (photo edit). Video/Reel editing (Premiere Pro) is a
separate, still-MISSING gap (MASTER GAP LIST **P2**) and is out of scope here.

---

## 0. WHERE THIS SITS IN THE PIPELINE

```
CAPTURE → INGEST → CULL → [ LIGHTROOM CLASSIC: import → edit/sync → export ] → DELIVER → ARCHIVE
                                         ▲ this doc
```

Upstream handoff is from [[INGEST]] / [[CULLING]]; downstream handoff is to [[EXPORT]] →
[[DELIVERY]] (Pixieset for STUDIO) / [[EVENTS_ZENFOLIO_DELIVERY]] (Zenfolio for EVENTS).

---

## 1. CATALOG STRUCTURE

**STATUS: UNCONFIRMED — nothing in the vault records the LR catalog model.**

| Question | Vault answer | Verdict |
|---|---|---|
| One master catalog vs per-branch catalogs? | Not recorded anywhere. | **UNCONFIRMED — FHR** |
| Where does the catalog file (`.lrcat`) live — `C:\` or `D:\`? | Not recorded. Active media lives on `D:\SFV_ACTIVE\BRANCHES\[BRANCH]\` (INGEST.md, CANON), which is the strongest hint the catalog *should* sit beside it on `D:\`, but this is inference only. | **UNCONFIRMED — FHR** |
| Catalog backup cadence / location? | Not recorded. | **UNCONFIRMED — FHR** |
| Smart Previews on/off (offline editing once media is archived)? | Not recorded. Relevant because ARCHIVE moves media ACTIVE→WARM→COLD ([[ARCHIVE]]); without Smart Previews, archived shoots lose their LR previews. | **UNCONFIRMED — FHR** |

**Inference (flagged, not adopted):** INGEST.md step 7 points Lightroom at
`D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528\` per shoot. That pattern is consistent
with *one catalog* that imports per-shoot folders off `D:\`, but it is equally consistent
with a per-branch catalog. **Will to decide.**

---

## 2. IMPORT INTO LIGHTROOM (handoff from INGEST / CULLING)

**The handoff point is the open question here — two vault docs describe two different cull models.**

- **INGEST.md (CANON)** ends at: files renamed and moved to
  `D:\SFV_ACTIVE\BRANCHES\[BRANCH]\INGEST\[YYYYMMDD]\`, then step 7: *"Open Lightroom → point
  to [that folder]"*, step 8: *"Cull, sync preset, export."* → This implies **Will culls
  inside Lightroom** (flag/pick in LR), folder-based import.
- **CULLING.md (UNCONFIRMED)** describes a **file-system** cull: AI blur/exposure flagging →
  `REJECTS/` and `REVIEW/` folders → Will picks → `SELECTS/` folder → then (presumably) LR
  imports `SELECTS/` only.

These two are **not reconciled in the vault.** BLUEPRINT_COVERAGE_MAP.md confirms it:
*"Creative selects (how Will culls in LR) — none — MISSING."*

| Item | Verdict |
|---|---|
| Import source folder: `…\INGEST\[YYYYMMDD]\` (cull in LR) **or** `…\SELECTS\` (cull on disk first)? | **UNCONFIRMED — FHR.** Pick one and make the other doc point to it. |
| Folder import vs LR Collection per shoot/event? | **UNCONFIRMED.** The job naming (`[YYYYMMDD]_[EVENT/CLIENT]/`, NAMING_CONVENTIONS CANON) suggests one Collection (or folder) per shoot, but the vault never states LR's organizational unit. |
| Copy/Add/Move on import? | **UNCONFIRMED.** INGEST already did the copy+verify+rename, so LR should **Add** (not re-copy). Inference only. |
| Apply preset on import vs after? | STUDIO applies preset as a **batch sync** (see §3); whether it's an import preset or a post-import sync is not stated. **UNCONFIRMED.** |

**Recommended handoff to ratify (FHR):** INGEST writes the renamed files → LR **Adds** the
per-shoot folder → Will flags picks in LR → develop + sync → export. If the on-disk
`SELECTS/` model in CULLING.md is the real one instead, say so and retire the LR-cull
language in INGEST.md.

---

## 3. PER-BRANCH PRESETS

### SFV_STUDIO — **CANON** (most documented branch)

From `SFV_STUDIO.md` (CANON), EDITING APPROACH:
- **Lightroom Classic batch export with sync presets.** (CANON)
- Same lighting/settings per session ⇒ **minimal variations off the preset.** (CANON)
- **No individual retouching** needed for bulk shoots. (CANON)

Operational read (Morning Walk stress test, SFV_STUDIO.md): 50+ models × 3 shots = 150+
photos, one collective Pixieset gallery, **same-day delivery**. The whole point of the sync
preset is volume: develop one frame, sync the corrected develop settings across the set,
export the batch. **CANON** that the method is batch-sync; the **specific develop preset name
and its slider values are UNCONFIRMED** (not recorded in any vault doc).

### SFV_EVENTS — **CANON-in-practice** (the Morning Walk / Shamar recipe)

> ⚠️ This recipe was **executed** for Morning Walk (May 28) and Shamar (June 6) and is recorded
> in memory + `MISSING_REFERENCED_FILES.md §3`. It was **NOT previously in the vault** — EXPORT.md
> still reads "specs TBD / UNCONFIRMED." Labeled **CANON-in-practice**; promote to CANON once
> Will ratifies it here.

The battle-tested EVENTS portrait edit:
1. **Adaptive Portrait preset** as the base develop. *(CANON-in-practice; exact slider values
   not recorded — UNCONFIRMED at the slider level.)*
2. **AI-mask sync** — Lightroom AI masks (subject / face / sky etc.) developed on one frame
   and **synced** across the batch. *(CANON-in-practice — see §5.)*
3. **Generative Remove** for distractions/cleanup. *(CANON-in-practice — see §5.)*
4. **Export: sRGB, quality 80–85, long edge 2560 px.** *(CANON-in-practice — see §6; this is
   the one hard, recorded number set.)*

This is a **per-subject portrait** approach (Adaptive Portrait + AI masks per face), distinct
from STUDIO's uniform batch sync — consistent with EVENTS being "the most professional-looking
branch" doing "on-site professional portrait sessions" (SFV_EVENTS.md, CANON).

### SFV_ARCHIVE — **THIN / UNCONFIRMED**

EXPORT.md (UNCONFIRMED) lists ARCHIVE under "Full res + social specs" and names Lightroom
Classic as its export tool. **No develop/preset approach is documented.** The coverage map
rates "Lightroom edit — EVENTS, ARCHIVE" as THIN against EXPORT.md only. → **Edit approach
UNCONFIRMED; FHR.**

### SFV_LIVE — **UNCONFIRMED (likely minimal / not a real LR branch)**

EXPORT.md: *"SFV_LIVE: Minimal processing, square format, basically untouched."* That suggests
LIVE may barely touch Lightroom at all. **No LR preset documented.** → **UNCONFIRMED whether
LIVE uses LR; if it does, the approach is MISSING.**

### SFV_ATHLETICS / SFV_WORLD / SFV_404 / MYTHOLOGY — **MISSING**

BLUEPRINT_COVERAGE_MAP.md: *"Lightroom edit — LIVE, ATHLETICS, WORLD, 404, MYTHOLOGY —
none — MISSING [INFERENCE that they use LR at all]."* MYTHOLOGY/WORLD ingest is
phone-sourced (INGEST.md), so they may not be LR branches at all. → **MISSING. No LR approach
documented; not even confirmed these branches use Lightroom.**

| Branch | LR edit approach | Source / verdict |
|---|---|---|
| SFV_STUDIO | Batch develop + **sync preset**, no retouch | SFV_STUDIO.md — **CANON** (preset name UNCONFIRMED) |
| SFV_EVENTS | Adaptive Portrait + AI-mask sync + Generative Remove | memory / §3 — **CANON-in-practice** (was not in vault) |
| SFV_ARCHIVE | Full res + social; develop approach not stated | EXPORT.md — **UNCONFIRMED / FHR** |
| SFV_LIVE | "Minimal, basically untouched, square" | EXPORT.md — **UNCONFIRMED** (may bypass LR) |
| SFV_ATHLETICS | — | **MISSING** |
| SFV_WORLD | — | **MISSING** (phone-sourced) |
| SFV_404 | — | **MISSING** |
| MYTHOLOGY | — | **MISSING** (phone-sourced; may not use LR) |

---

## 4. PRESET MANAGEMENT (.xmp storage, sync, version control)

**STATUS: UNCONFIRMED — nothing in the vault records how presets are stored, synced, or versioned.**

| Question | Vault answer | Verdict |
|---|---|---|
| Where do `.xmp` develop presets live on disk? | Not recorded. LR default is `…\AppData\Roaming\Adobe\CameraRaw\Settings\` and the LR `Develop Presets` store — but the vault does not say whether SFV keeps them there or in the vault/`D:\`. | **UNCONFIRMED — FHR** |
| Synced between machines? (Morning Walk involves multiple shooters; EVENTS runs **3 laptops / 1 account**, EVENTS_ZENFOLIO_DELIVERY) | Not recorded. Syncthing is LIVE on both nodes (coverage map D), so a Syncthing-shared preset folder is *plausible*, but unstated. | **UNCONFIRMED — FHR** (preset parity across the 3 event laptops is an operational risk worth a decision) |
| Version controlled? | Not recorded. | **UNCONFIRMED — FHR** |
| Adobe Creative Cloud preset sync used? | Not recorded. | **UNCONFIRMED — FHR** |

**Note (real risk, not invented):** EVENTS runs the QR workflow across **3 laptops on 1
Zenfolio account**. If the Adaptive Portrait preset + AI-mask recipe is to be applied
consistently across those 3 machines, preset distribution needs a defined mechanism. Today
that mechanism is **undocumented.**

---

## 5. AI MASKING + GENERATIVE REMOVE

**Source:** Morning Walk / Shamar recipe (memory + `MISSING_REFERENCED_FILES.md §3`).
**Verdict: CANON-in-practice for SFV_EVENTS; not documented for any other branch.**

| Feature | Where used | Verdict |
|---|---|---|
| **AI-mask sync** (LR AI subject/face masks developed once, synced across batch) | SFV_EVENTS portrait edit | **CANON-in-practice** |
| **Generative Remove** (distraction/object cleanup) | SFV_EVENTS portrait edit | **CANON-in-practice** |
| AI masking in SFV_STUDIO | STUDIO is "no individual retouching, minimal variations off preset" (CANON) — implies AI masking is **not** part of the bulk STUDIO flow | **UNCONFIRMED** (likely not used; not stated) |
| AI masking / Generative Remove in ARCHIVE, LIVE, ATHLETICS, WORLD, 404, MYTHOLOGY | Not recorded | **MISSING / UNCONFIRMED** |

> These are **Lightroom Classic** AI features (local Adobe cloud-assisted), distinct from the
> SFV R&D Terminal Ollama vision models used for *technical* culling ([[CULLING]]). Do not
> conflate the two AI layers.

---

## 6. EXPORT SETTINGS PER BRANCH

This section **resolves the EXPORT.md "specs TBD" hole for SFV_EVENTS** with the recorded
recipe, and honestly flags every other branch as UNCONFIRMED.

### SFV_EVENTS — **CANON-in-practice (the one recorded number set)**

| Setting | Value | Source |
|---|---|---|
| Color space | **sRGB** | memory / §3 |
| Quality | **80–85 (JPEG)** | memory / §3 |
| Dimension | **2560 px long edge** | memory / §3 |
| Sharpening | **UNCONFIRMED** (not recorded) | — |
| Output sharpening for screen / metadata / watermark | **UNCONFIRMED** | — |

> This is sized for **web gallery delivery (Zenfolio)** — sRGB + 2560px + q80–85 is a
> screen-delivery spec, not a print/full-res spec. Whether EVENTS *also* exports a separate
> full-res master (for archive or print upsell) is **UNCONFIRMED** — EXPORT.md mentions
> "Full res for Pixieset + social specs" but that line is about a Pixieset/STUDIO-style flow,
> and EVENTS delivers via **Zenfolio**, not Pixieset (see §7 contradiction note).

### SFV_STUDIO — **UNCONFIRMED at the number level**

Method is CANON (batch export, sync presets — SFV_STUDIO.md). The **export numbers are not
recorded.** EXPORT.md only lists generic SPEC tags (FULLRES / 1080SQ / 1080×1350 / 1920×1080)
under an UNCONFIRMED banner. Delivery is a Pixieset collective gallery (CANON), which implies
at least a full-res-ish web export, but **resolution / color space / quality / sharpening are
all UNCONFIRMED.** A reasonable starting point would mirror the EVENTS sRGB recipe, but **do
not adopt that without Will's confirmation.**

### Other branches

| Branch | Resolution | Color space | Quality | Sharpening | Verdict |
|---|---|---|---|---|---|
| SFV_EVENTS | 2560px long edge | sRGB | 80–85 | UNCONFIRMED | **CANON-in-practice** |
| SFV_STUDIO | UNCONFIRMED | UNCONFIRMED | UNCONFIRMED | UNCONFIRMED | method CANON, numbers **UNCONFIRMED** |
| SFV_ARCHIVE | "Full res + social specs" (tags only) | UNCONFIRMED | UNCONFIRMED | UNCONFIRMED | **UNCONFIRMED** |
| SFV_LIVE | square, "basically untouched" | UNCONFIRMED | UNCONFIRMED | UNCONFIRMED | **UNCONFIRMED** (may not use LR) |
| ATHLETICS / WORLD / 404 / MYTHOLOGY | — | — | — | — | **MISSING** |

> Generic IG SPEC tags (1080SQ, 1080×1350, 1920×1080) from EXPORT.md are **naming/aspect
> conventions**, not confirmed LR export presets. They are carried here for reference only and
> remain **UNCONFIRMED** as actual export settings.

---

## 7. HANDOFF TO DELIVERY

### Export destination (staging)

From SFV_STUDIO.md (CANON) OUTPUT PATH and INGEST.md (CANON) branch tree, exports land on
`D:\` under the branch:

```
D:\SFV_ACTIVE\BRANCHES\[BRANCH]\EXPORT\      ← LR export target (staging)
D:\SFV_ACTIVE\BRANCHES\[BRANCH]\DELIVERY\    ← STUDIO also has a DELIVERY path
```

*(Branch docs use the `%BRANCHES_ROOT%\…` variable; INGEST.md resolves `%BRANCHES_ROOT%` to
`D:\SFV_ACTIVE\BRANCHES\`. Note the `%SFV_ROOT%` ambiguity flagged in
MISSING_REFERENCED_FILES.md §4 — `%BRANCHES_ROOT%` is the safe one to use here.)*

**Verdict:** EXPORT/DELIVERY folders on `D:\` are **CANON** for STUDIO; EVENTS has an EXPORT
path (CANON) but **no DELIVERY path** in SFV_EVENTS.md — **UNCONFIRMED** whether EVENTS exports
straight to a Zenfolio upload folder or stages first.

### Export file naming

Per NAMING_CONVENTIONS.md (CANON), photo exports:

```
[BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[SPEC]_[####]
EVENTS_20250606_SHAMAR_2560_0001        ← (SPEC token for the EVENTS recipe — see note)
STUDIO_20250528_MORNINGWALK_FULLRES_0001
STUDIO_20250528_MORNINGWALK_1080SQ_0001
```

> **Naming gap (FHR):** NAMING_CONVENTIONS.md gives SPEC examples (`FULLRES`, `1080SQ`) but has
> **no SPEC token for the 2560px EVENTS web export.** Proposed token `2560` shown above is a
> suggestion, **not CANON** — Will should ratify the SPEC token so the recipe and the naming
> doc agree.

### Delivery platform per branch

| Branch | Platform | Verdict |
|---|---|---|
| SFV_STUDIO | **Pixieset** collective gallery, subjects self-claim | **CANON** (SFV_STUDIO.md, DELIVERY.md) |
| SFV_EVENTS | **Zenfolio** Sports & Events (Advanced), QR workflow | **CANON in DELIVERY.md / EVENTS_ZENFOLIO_DELIVERY.md (FHR doc)** — see contradiction ⚠️ |
| SFV_ARCHIVE / LIVE / ATHLETICS / WORLD / 404 / MYTHOLOGY | Direct-to-Instagram, no client delivery | **CANON** (DELIVERY.md "all other branches") |

> ⚠️ **Known contradiction (carried, not resolved here):** SFV_EVENTS.md (CANON) still says
> delivery = *"Pixieset (like Studio) or different? UNCONFIRMED"*, while DELIVERY.md and
> EVENTS_ZENFOLIO_DELIVERY.md lock **Zenfolio**. This is the same contradiction flagged in
> BLUEPRINT_COVERAGE_MAP.md (Domain A flags) and MASTER GAP LIST **P7**. For Lightroom export
> purposes, **treat EVENTS delivery as Zenfolio** (the operational decision), and the EVENTS
> web export recipe (sRGB/2560/q80–85) is sized for Zenfolio, not Pixieset. SFV_EVENTS.md
> needs its delivery line corrected — out of scope for this doc, tracked under P7.

---

## 8. CONSOLIDATED OPEN-DECISIONS TABLE

| # | Open decision | Current state | Owner | Blocks |
|---|---|---|---|---|
| L1 | One master catalog vs per-branch catalogs | UNCONFIRMED | WILL | Catalog backup, archive offline editing |
| L2 | Catalog location — `C:\` vs `D:\` (beside active media) | UNCONFIRMED (D:\ inferred) | WILL | DR / backup plan |
| L3 | Smart Previews on/off (editing after ARCHIVE moves media to WARM/COLD) | UNCONFIRMED | WILL | [[ARCHIVE]] interplay |
| L4 | Cull handoff: cull **in LR** (INGEST.md) vs on-disk **SELECTS/** (CULLING.md) | **Contradiction, UNCONFIRMED** | WILL | Reconcile INGEST.md ↔ CULLING.md |
| L5 | LR import unit: folder vs Collection per shoot; Add vs Copy | UNCONFIRMED (Add inferred) | WILL | — |
| L6 | SFV_STUDIO develop preset — name + slider values | Method CANON, values UNCONFIRMED | WILL | Reproducibility |
| L7 | **Ratify EVENTS recipe to CANON** (Adaptive Portrait + AI-mask sync + Generative Remove + sRGB/2560/q80–85) | **CANON-in-practice**, not yet vault-CANON | WILL | Promote into EXPORT.md, close P5 |
| L8 | EVENTS export sharpening value | UNCONFIRMED | WILL | Complete the recipe |
| L9 | Does EVENTS also export a full-res master (print/archive upsell)? | UNCONFIRMED | WILL | Archive + upsell |
| L10 | SFV_STUDIO export numbers (res/space/quality/sharpening) | UNCONFIRMED | WILL | Pixieset spec |
| L11 | SFV_ARCHIVE edit + export approach | UNCONFIRMED | WILL | — |
| L12 | Do LIVE / ATHLETICS / WORLD / 404 / MYTHOLOGY use Lightroom at all? | MISSING / UNCONFIRMED | WILL | Scope of this doc |
| L13 | Preset (.xmp) storage location | UNCONFIRMED | WILL | L14 |
| L14 | Preset sync across machines (esp. EVENTS 3-laptop event rig) | UNCONFIRMED (Syncthing plausible) | WILL | Event-day consistency |
| L15 | Preset version control | UNCONFIRMED | WILL | — |
| L16 | SPEC token in NAMING_CONVENTIONS for the 2560px EVENTS export | No token exists (proposed `2560`) | WILL | Naming ↔ recipe parity |
| L17 | EVENTS export staging path (EXPORT/ vs direct Zenfolio upload folder) | UNCONFIRMED (no DELIVERY path in SFV_EVENTS.md) | WILL | Handoff clarity |
| L18 | Fix SFV_EVENTS.md delivery line (says Pixieset/UNCONFIRMED; reality = Zenfolio) | Contradiction (tracked under P7) | WILL | Branch-doc integrity |

---

## CONNECTED FILES
- [[02_BRANCHES/SFV_STUDIO|SFV_STUDIO]]
- [[02_BRANCHES/SFV_EVENTS|SFV_EVENTS]]
- [[04_WORKFLOWS/EXPORT|Export]]
- [[04_WORKFLOWS/DELIVERY|Delivery]]
- [[04_WORKFLOWS/INGEST|Ingest]]
- [[04_WORKFLOWS/CULLING|Culling]]
- [[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]
- [[04_WORKFLOWS/EVENTS_ZENFOLIO_DELIVERY|Events Zenfolio Delivery]]
- [[08_TESTS/BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[00_DEV_LOG/MISSING_REFERENCED_FILES|Missing / Referenced Files]]
- [[02_BRANCHES/SFV_ARCHIVE|SFV_ARCHIVE]]
- [[04_WORKFLOWS/ARCHIVE|Archive]]
