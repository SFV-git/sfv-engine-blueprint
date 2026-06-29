---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
CREATED: 2026-06-29
CREATED_BY: loop directive BLUEPRINT-20260629-P2-VIDEO-EDIT-001
LAST_UPDATED: 2026-06-29
PURPOSE: Blueprint the Premiere Pro / video-edit workflow for SFV Engine — per-branch edit
  approach, audio, color, caption hand-off, export presets, FFmpeg post-export, and delivery
  hand-off. Closes MASTER GAP LIST P2 (BLUEPRINT_COVERAGE_MAP.md §6).
---

# VIDEO EDIT WORKFLOW

> This doc fills the single biggest craft-layer hole identified in the coverage audit:
> **there was no video-editing (Premiere Pro) workflow doc at all** (BLUEPRINT_COVERAGE_MAP.md
> §1 row "Video / Reel edit" = MISSING; §2 step 8 = MISSING; ranked **P2** in §6).
>
> It affects six branches that produce video: **UGC** (revenue), **LIVE**, **EVENTS**,
> **ATHLETICS**, **STUDIO**, and **ARCHIVE**.

**STATUS legend (inline labels used throughout this doc)**
- **CANON** — locked, battle-tested practice already established in another CANON vault doc.
- **UNCONFIRMED** — inferred from adjacent docs, or a decision that has not been made.
- **FOR HUMAN REVIEW (FHR)** — Will must ratify before this becomes operational practice.

> **Whole-doc STATUS: FOR HUMAN REVIEW.** Nothing here is locked practice except where it
> explicitly cites an existing CANON doc. The video-edit craft has not been blueprinted before,
> so most of this is first-draft inference awaiting Will's ratification.

---

## 1. TOOL DECISION

### 1.1 Primary editor — Premiere Pro
- **Adobe Premiere Pro is the primary / default video editor for all branches.** *(CANON-by-stack —
  per BLUEPRINT_COVERAGE_MAP.md §1 and §2: "Premiere Pro is the only editor in the stack.")*
- All timeline assembly, multi-clip sequencing, color (Lumetri), and master export originate in
  Premiere unless a branch section below states otherwise.

### 1.2 UGC reel candidates — UNDECIDED
- **CapCut** — **UNCONFIRMED.** Listed in this directive as a candidate, but note for honesty:
  **CapCut is never mentioned anywhere in the vault** (per coverage map §2: "CapCut never
  mentioned"). It is a candidate *introduced by this directive only*, not an existing SFV decision.
- **Aditor.ai** — **UNCONFIRMED.** Coverage map §2 records it as status **RESEARCHING** for UGC reels.
- **Captions (app)** — **UNCONFIRMED / RESEARCHING.** Tracked in `TOOL_STATUS.md` as a caption/
  subtitle tool under research; relevant if caption burn-in moves out of Premiere (see §5).

> ### ⚑ FOR HUMAN REVIEW — final UGC reel tool choice
> Will must ratify whether UGC reels are cut in **Premiere Pro only**, or whether **CapCut** and/or
> **Aditor.ai** supplement/replace Premiere for fast-turnaround social reels. Per coverage map §2,
> *"whether CapCut/Aditor.ai supplement it is undecided — this is the single biggest UGC gap."*
> **Do not treat any supplemental tool as adopted until this block is resolved.**

---

## 2. PER-BRANCH EDIT APPROACH

> Engine Levels below are quoted from each branch's CANON branch-definition file. Higher level =
> more engine automation, less manual Will involvement.

### 2.1 SFV_UGC — reel assembly *(branch doc: UNCONFIRMED; Engine Level 6.5)*
The revenue branch. Most automated account in the system.

- **Structure: hook-first.** *(UNCONFIRMED as a written rule — inferred from the UGC niche
  (trainer/athlete reels) and the existence of a HOOK_BANK in CONTENT_BANKS.md. The hook-first
  ordering is standard short-form practice but is **not yet codified** in any CANON SFV doc.)*
- **Reel assembly:** ingest selects → lay hook on first 1–3s → body clips → CTA tail. Pull hook/
  script candidates from `CONTENT_BANKS.md` (HOOK_BANK / CTA_BANK / SCRIPT_TEMPLATES) and client
  memory from `CLIENT_BANKS.md` (both currently **UNCONFIRMED**, not yet wired into the edit).
- **Client revision loop *(CANON naming, UNCONFIRMED process):***
  - Draft export named per `NAMING_CONVENTIONS.md`:
    `UGC_[YYYYMMDD]_[CLIENT]_REEL_[###]_DRAFT`
  - AI self-audit (brand alignment, no typos/misplaced overlays, technical QC) — per `SFV_UGC.md`
    QUALITY CONTROL section. → see `QUALITY_CONTROL.md`.
  - Will reviews before delivery (CANON: "Will reviews before posting").
  - On client feedback, re-version: `..._REEL_[###]_REJECTED` → new cut → `..._REEL_[###]_APPROVED`.
  - Approved/rejected outcome trains the engine over time (CANON, SFV_UGC.md).
  - Client-facing deliverable renamed at hand-off: `[CLIENT_ID]_[YYYYMMDD]_REEL_v[##]`
    (e.g. `PROEDGE_20250601_REEL_v01`). *(CANON, NAMING_CONVENTIONS.md.)*
- **Caption handoff:** Whisper transcript feeds caption/subtitle generation — see §5.
- **Revision-round count / SLA per service tier:** **UNCONFIRMED** (packages still undecided,
  SFV_UGC.md PACKAGES = UNCONFIRMED). **FHR.**

### 2.2 SFV_LIVE — highlight reel / event recap *(branch doc: CANON; Engine Level 3.5)*
- **Engine Level 3.5 = rough assembly + schedules; Will reviews selects before posting.** *(CANON.)*
- **Deliberately raw.** SFV_LIVE.md (CANON): reels are *"patched together clips, raw feeling"*,
  *"no video-heavy content — feels like a magazine on digitals"*, *"shot with cheapest lens for
  authenticity."* → **Minimal stylization is the brand. Do not over-polish.**
- **Edit approach:** quick highlight / event-recap assembly from event coverage clips. Light cut,
  music bed optional, little-to-no color grade (see §4). Magazine-on-digitals feel preserved.
- **Multi-cam:** **UNCONFIRMED.** No multi-cam rig is documented for LIVE; single cheap-lens capture
  is the stated style. Treat multi-cam as not-in-scope unless Will confirms. **FHR.**
- Output path: `%BRANCHES_ROOT%\SFV_LIVE\EXPORT\`. No client-portal delivery (IG next-day).

### 2.3 SFV_EVENTS — short-form recap delivery *(branch doc: CANON; Engine Level 5–6.5)*
- **Most professional-looking branch** (on-site portrait sessions). Reels = *"service showcase
  [implied]"* per SFV_EVENTS.md (the "[implied]" is the branch doc's own hedge → **UNCONFIRMED**
  that reels are a formal EVENTS deliverable).
- **Edit approach:** short-form **recap** of the event/session — backdrop shots + b-roll cut to a
  tight social recap. Higher polish than LIVE (this branch is the professional shop window).
- **Photo vs video split:** EVENTS' primary deliverable is portraits (Zenfolio QR delivery, see
  EVENTS_ZENFOLIO_DELIVERY); the recap reel is a marketing artifact, not the paid deliverable.
  **UNCONFIRMED** whether recap reels are delivered to the event owner or only posted to SFV_EVENTS IG.
- Note the standing contradiction (coverage map §1): SFV_EVENTS.md still says delivery is
  "Pixieset or different? UNCONFIRMED" while Zenfolio is locked in EVENTS_ZENFOLIO_DELIVERY. Video
  recap delivery channel inherits this ambiguity. **FHR.**

### 2.4 SFV_ATHLETICS — action highlight / slow-mo *(branch doc: CANON; Engine Level 3.5)*
- **Engine Level 3.5 = rough edit with more polish than LIVE, + schedules.** *(CANON.)*
- **Edit approach:** action-highlight assembly — non-traditional sports coverage (SFV_ATHLETICS.md:
  *"captures games and athletic disciplines in non-traditional ways"*; primary background basketball).
- **Slow-motion usage:** **UNCONFIRMED.** Slow-mo is requested by this directive and is idiomatic for
  athletics highlights, but it is **not documented anywhere in the vault** — no capture frame-rate
  spec (e.g. 120/240 fps), no conform/retime rule. Treat slow-mo as a proposed technique pending:
  (a) confirmation the camera captures high-fps source, (b) a retime/conform standard. **FHR.**
- Not a money branch — taste display. No client delivery; IG only.

### 2.5 SFV_STUDIO — product/portrait video *(branch doc: CANON; Engine Level 5.5)*
- **Primarily a photo branch.** SFV_STUDIO.md EDITING APPROACH is **Lightroom Classic batch export**
  with sync presets — *no video workflow is described.* Reels are *"possibly showcase work [implied]"*
  (the branch doc's own hedge).
- **Video status: UNCONFIRMED whether SFV_STUDIO produces video at all.** If it does, the likely form
  is a short portrait/comp-card showcase reel (stills-to-motion or behind-the-scenes), cut in Premiere.
  - Product/portrait motion video: **UNCONFIRMED — not an established STUDIO deliverable.** **FHR.**
- If no video is produced here, this section is N/A and STUDIO drops out of the video-branch list.

### 2.6 SFV_ARCHIVE — ⚑ DIRECTIVE CONTRADICTS THE VAULT
> **This directive instructed: "SFV_ARCHIVE — preservation edits only (no stylistic changes)."**
> **The vault says the opposite.** `SFV_ARCHIVE.md` (CANON) defines SFV_ARCHIVE as *Will's creative
> portfolio account — best work across all disciplines, music videos, brand shoots, creative shoots…
> Reels: yes — creative showpieces*, with **human-final curation** ("AI never makes final curation
> decisions for Archive. Human review always final for this branch.")
>
> This looks like a conflation of two different "archive" concepts:
> - **SFV_ARCHIVE the branch** = creative portfolio / showpiece reels (CANON, stylistic, high craft).
> - **The data-archive workflow** (`ARCHIVE.md`, ACTIVE→WARM→COLD storage tiers) = literal file
>   preservation, **no editing at all** — that is a storage process, not a video edit.
>
> **FOR HUMAN REVIEW — Will must disambiguate which "archive" this directive meant.** Until then,
> both readings are documented below; **do not act on either.**

- **Reading A — SFV_ARCHIVE branch (per vault, CANON):** highest-standard **creative showpiece**
  edits in Premiere. Stylistic grade encouraged. Will adds the final creative touch before posting
  (Engine Level 3.5 = rough edit + Will's creative pass). Content may be promoted here from any
  branch. **This is stylistic, not preservation.**
- **Reading B — data-archive (per directive wording):** **preservation only, no stylistic changes.**
  If a clip is being archived for cold storage, it is **not edited** — it is repackaged/validated for
  longevity (see §7 FFmpeg) and filed under `ARCHIVE.md` naming
  (`[BRANCH]_[YYYYMMDD]_[PROJECT]_[####]_ARCHIVE`). No Premiere step.

---

## 3. AUDIO WORKFLOW

- **Sync:** if dual-system audio (external recorder + camera) is used, sync in Premiere
  (waveform / Merge Clips). **UNCONFIRMED** — no external-audio rig is documented; most branches
  appear to be single-source camera audio. **FHR** whether dual-system audio is in scope.
- **Music / licensing approach:** **UNCONFIRMED — flag.** No music-licensing source, library, or
  policy exists anywhere in the vault (no Epidemic Sound / Artlist / Premiere Stock / royalty-free
  decision recorded). For a revenue branch (UGC) delivering client-facing reels, **licensed music is
  a legal/commercial requirement** — this is an open decision that must be made before paid delivery.
  > **⚑ FOR HUMAN REVIEW:** choose and record a music-licensing source + a per-branch usage rule
  > (commercial-cleared for UGC/EVENTS client work; looser for IG-only LIVE/ATHLETICS/ARCHIVE).
- **Levels target:** **UNCONFIRMED.** Proposed starting standard pending ratification:
  - Integrated loudness **−14 LUFS** (Instagram/social target), true peak **≤ −1 dBTP**.
  - Dialogue/voiceover seated around −12 to −16 LUFS short-term; music bed ducked ~ −18 to −22 LUFS
    under speech.
  - These are **proposed defaults, not locked.** **FHR** to confirm or override.

---

## 4. COLOR

Default: **Premiere Lumetri** for all in-Premiere grading. LUT usage is per-branch and mostly
unconfirmed (no LUT pack is recorded in the vault).

| Branch | Color approach | Status |
|---|---|---|
| SFV_UGC | Lumetri — clean, brand-aligned, consistent per client | **UNCONFIRMED** — no per-client LUT/look recorded; client BRAND_BANKS may define this later |
| SFV_LIVE | Minimal / near-untouched — "raw feeling", magazine-on-digitals | **CANON-aligned** (raw look is the brand) — exact settings UNCONFIRMED |
| SFV_EVENTS | Lumetri — clean professional grade (shop-window polish) | **UNCONFIRMED** |
| SFV_ATHLETICS | Lumetri — punchier "more polish than LIVE" | **UNCONFIRMED** |
| SFV_STUDIO | Match the Lightroom stills look if video exists | **UNCONFIRMED** (video itself unconfirmed) |
| SFV_ARCHIVE | Reading A: stylistic creative grade (LUT/Lumetri). Reading B: none (preservation) | **FHR** (see §2.6) |

- **No SFV LUT pack / shared `.cube` library is documented.** If a house LUT is desired, it must be
  created and stored (proposed: `03_INFRASTRUCTURE/` or a `LUTS/` asset folder). **FHR.**
- Photo color recipes (e.g. the battle-tested Morning Walk / Shamar Lightroom Adaptive Portrait
  preset) live in the photo pipeline, not here — see the P5 Lightroom workflow gap. Video grades are
  a separate, currently-undefined asset set.

---

## 5. CAPTION / SUBTITLE HANDOFF

This is where the **R&D Terminal (Node B) Whisper output** feeds the edit. Pipeline already
specified in `MEDIA_PIPELINE.md` (FHR) — this section maps its output into the video edit.

```
Premiere export OR pre-edit source
        │  (drop video/audio job envelope, task_type = MEDIA)
        ▼
C:\SFV_BLUEPRINT\99_INBOX\QUEUE\           ← n8n Local File Trigger (Node A)
        │  FFmpeg extracts 16kHz mono WAV  (MEDIA_PIPELINE §4)
        ▼
Node B (R&D Terminal) — Whisper transcribe (serial, 1 job at a time; 12GB VRAM ceiling)
        ▼
C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\
        ├─ YYYYMMDD-###_[topic]_TRANSCRIPT.md        (markdown transcript)
        └─ YYYYMMDD-###_[topic]_TRANSCRIPT_RAW.json  (word-level timestamps, if available)
        │
        ▼
Caption authoring into the reel:
        → import transcript/segments → captions track in Premiere (or candidate tool, §1.2)
        → style + position per branch → burn-in or sidecar .srt
```

- **Feed point:** the `_RAW.json` sidecar (word-level timestamps) is the useful artifact for
  caption timing; the `.md` is the human-readable transcript. *(CANON from MEDIA_PIPELINE.md §6.)*
- **Caption authoring tool:** **UNCONFIRMED.** Options: (a) Premiere built-in captions / Text panel
  importing the SRT/segments; (b) the **Captions** app or **Aditor.ai** (both RESEARCHING, §1.2).
  Resolve alongside the §1.2 tool decision. **FHR.**
- **Whisper install status:** Whisper is **approved but not yet installed** (coverage map §2 step 9);
  port/endpoint on Node B are still `[INFERENCE]` in MEDIA_PIPELINE.md §5. **Caption handoff is not
  operational until Whisper is live on Node B.**
- **Burn-in vs sidecar:** UGC client reels likely need burned-in captions (social autoplay/muted);
  whether to also deliver an `.srt` is **UNCONFIRMED. FHR.**

---

## 6. EXPORT PRESETS (PER-BRANCH OUTPUT SPEC)

> **Everything in this section is UNCONFIRMED.** `EXPORT.md` (UNCONFIRMED) lists video specs as
> "[UNCONFIRMED]" / "[TBD]" and the coverage map marks Video/Reel export specs as **MISSING / TBD**.
> The table below is a **proposed first-draft standard** to give Will something concrete to ratify —
> **not locked practice.**

**Proposed master reel preset (all social reels) — UNCONFIRMED:**
| Param | Proposed value | Status |
|---|---|---|
| Resolution | 1080 × 1920 (9:16) | UNCONFIRMED (EXPORT.md lists 1080x1920 as the Reels spec) |
| Frame rate | match source (24/30; 60 for ATHLETICS action) | UNCONFIRMED |
| Codec | H.264 (High profile) | UNCONFIRMED |
| Bitrate | VBR 2-pass, ~12–16 Mbps target / 20 Mbps max | UNCONFIRMED |
| Container | .mp4 | UNCONFIRMED (matches MEDIA_PIPELINE "primary ingest format") |
| Audio | AAC 320 kbps, 48 kHz, −14 LUFS (see §3) | UNCONFIRMED |
| Color | Rec.709 | UNCONFIRMED |

**Per-branch deltas — all UNCONFIRMED:**
| Branch | Aspect / extra outputs | Notes | Status |
|---|---|---|---|
| SFV_UGC | 9:16 reel; per-client spec possible | EXPORT.md: "Reel format, per client spec" — some clients may want 1:1 or 4:5 too | UNCONFIRMED |
| SFV_LIVE | 9:16 reel; possibly 1:1 | raw look; low-stakes encode | UNCONFIRMED |
| SFV_EVENTS | 9:16 recap reel | full-res photo path is separate (Zenfolio) | UNCONFIRMED |
| SFV_ATHLETICS | 9:16; 60fps for action / retimed slow-mo | depends on high-fps capture (§2.4) | UNCONFIRMED |
| SFV_STUDIO | 9:16 and/or 1:1 if video exists | video existence unconfirmed (§2.5) | UNCONFIRMED |
| SFV_ARCHIVE | Reading A: high-bitrate showpiece master (consider higher Mbps / possible 4K). Reading B: preservation master (see §7) | depends on §2.6 disambiguation | FHR |

- **1080x1080 (square)** and **1080x1350 (4:5)** are listed in EXPORT.md as additional video specs —
  produce only if a branch/client requires. **UNCONFIRMED** which branches need them.
- **Export engine:** Premiere's built-in encoder (Adobe Media Encoder) for the master. A second
  FFmpeg pass is described in §7. **UNCONFIRMED** whether AME or FFmpeg is the final encoder of record.

> **⚑ FOR HUMAN REVIEW — ratify the export matrix above** (codec, bitrate, fps, container, per-branch
> aspect ratios). This also resolves the EXPORT.md "[UNCONFIRMED]/[TBD]" video rows.

---

## 7. FFMPEG POST-EXPORT STEP

FFmpeg already exists in the stack on **Node A** (used for Whisper audio extraction —
MEDIA_PIPELINE.md §4; installation is `[INFERENCE]`, confirm `ffmpeg -version`).

**Proposed post-export pass — UNCONFIRMED:**
1. **Validation / integrity probe** — `ffprobe` the Premiere master to confirm codec, resolution,
   duration, audio stream, and loudness sanity before it leaves the building.
   ```bash
   ffprobe -v error -show_format -show_streams "[master].mp4"
   ```
2. **Repackaging (faststart for web/social)** — remux so the moov atom is at the front (streaming-
   friendly) without re-encoding:
   ```bash
   ffmpeg -i "[master].mp4" -c copy -movflags +faststart "[delivery].mp4"
   ```
3. **Loudness normalization (optional)** — if the master misses the −14 LUFS target (§3), a
   one-pass `loudnorm` correction. **UNCONFIRMED** whether to normalize in FFmpeg or fix in Premiere.
4. **Preservation transcode (ARCHIVE Reading B only)** — for cold-storage preservation, transcode to
   a long-term mezzanine/lossless container **with no stylistic change** (see §2.6 / ARCHIVE.md).
   Format **UNCONFIRMED. FHR.**

- **Is a post-export FFmpeg pass even wanted?** **UNCONFIRMED.** Premiere/AME can output faststart
  MP4 directly. The FFmpeg pass earns its place mainly for (a) automated validation and (b)
  preservation transcodes. **FHR** whether to standardize it or skip it for simple social reels.
- **Automation:** could be wired as an n8n Execute Command node on export (EXPORT.md lists
  "n8n: orchestrate export triggers [FUTURE]"). Not built. **UNCONFIRMED.**

---

## 8. HANDOFF TO DELIVERY

### 8.1 File naming *(CANON — NAMING_CONVENTIONS.md)*
- Working/review reels:
  `[BRANCH]_[YYYYMMDD]_[CLIENT]_REEL_[###]_[STATUS]`
  (`STATUS` ∈ DRAFT / APPROVED / REJECTED) — e.g. `UGC_20250601_PROEDGE_REEL_001_APPROVED`.
- Client-facing deliverable (renamed at hand-off):
  `[CLIENT_ID]_[YYYYMMDD]_[DELIVERABLE]_v[##]` — e.g. `PROEDGE_20250601_REEL_v01`.
- No `final_final_v2`, no spaces, dates `YYYYMMDD`, status always last. *(CANON.)*

### 8.2 Staging path (D:\) *(UNCONFIRMED exact path)*
- Active production lives on the **D:\ working drive**. MEDIA_PIPELINE.md references
  `D:\SFV_ACTIVE\[branch]\...` for source media, and the telemetry tree is `D:\SFV_ACTIVE\LOGS\`.
- **Proposed video staging/export paths** (mapping the branch docs' `%BRANCHES_ROOT%` to D:\):
  - Master/export: `D:\SFV_ACTIVE\[BRANCH]\EXPORT\`
  - Client staging (UGC/STUDIO have a DELIVERY subtree): `D:\SFV_ACTIVE\[BRANCH]\DELIVERY\`
  - The branch docs list `%BRANCHES_ROOT%\SFV_UGC\EXPORT\` and `...\DELIVERY\`; the literal D:\
    resolution of `%BRANCHES_ROOT%` is **UNCONFIRMED** — confirm against STORAGE_ARCHITECTURE.md. **FHR.**

### 8.3 Delivery workflow → `DELIVERY.md` *(UNCONFIRMED)*
- **UGC:** delivery platform is **UNCONFIRMED** (DELIVERY.md: "direct download, Drive link, or
  portal?"). **Current method is WeTransfer (stop-gap), to be replaced.** Will reviews before
  delivery; AI self-audit (QC) runs first. Client notification path = **MISSING** (coverage map §2 step 16).
- **EVENTS:** portrait deliverables go via **Zenfolio QR** (EVENTS_ZENFOLIO_DELIVERY, locked);
  recap-reel delivery channel is **UNCONFIRMED** (§2.3).
- **STUDIO:** Pixieset collective gallery (CANON) — for photos; video delivery (if any) unconfirmed.
- **LIVE / ATHLETICS / ARCHIVE:** no client delivery — content goes directly to Instagram (CANON,
  DELIVERY.md "All other branches").
- **IG scheduling** (the post-delivery step for all branches) is a separate MISSING workflow (tool
  undecided: Later vs Buffer) — see coverage map P4. Out of scope for this doc.

---

## OPEN DECISIONS — CONSOLIDATED (FOR HUMAN REVIEW)

| # | Decision | §  | Status |
|---|---|---|---|
| 1 | Final UGC reel tool: Premiere only vs + CapCut / Aditor.ai | 1.2 | FHR |
| 2 | UGC hook-first ordering — codify as a rule? | 2.1 | UNCONFIRMED |
| 3 | UGC revision-round count / SLA per tier | 2.1 | FHR |
| 4 | LIVE multi-cam in scope? | 2.2 | UNCONFIRMED |
| 5 | EVENTS recap reel — delivered or IG-only? | 2.3 | UNCONFIRMED |
| 6 | ATHLETICS slow-mo: high-fps capture + retime standard | 2.4 | FHR |
| 7 | STUDIO — does it produce video at all? | 2.5 | FHR |
| 8 | **ARCHIVE — directive ("preservation only") contradicts vault ("creative showpieces"); disambiguate** | 2.6 | **FHR** |
| 9 | Music licensing source + per-branch usage rule | 3 | FHR |
| 10 | Audio loudness target (−14 LUFS proposed) | 3 | UNCONFIRMED |
| 11 | House LUT pack — create + store? | 4 | FHR |
| 12 | Caption authoring tool (Premiere vs Captions/Aditor.ai); burn-in vs .srt | 5 | FHR |
| 13 | Full export matrix (codec/bitrate/fps/container/aspect) | 6 | FHR |
| 14 | Final encoder of record: Adobe Media Encoder vs FFmpeg | 6 | UNCONFIRMED |
| 15 | Standardize the FFmpeg post-export pass, or skip for simple reels? | 7 | FHR |
| 16 | D:\ resolution of `%BRANCHES_ROOT%` for video paths | 8.2 | FHR |
| 17 | UGC delivery platform (replace WeTransfer) + notification path | 8.3 | UNCONFIRMED / MISSING |

**Prerequisites that gate this workflow becoming operational:**
Whisper installed + port/endpoint confirmed on Node B (caption handoff) · FFmpeg confirmed on Node A ·
EXPORT.md video specs ratified · STORAGE_ARCHITECTURE.md path confirmation.

---

## CONNECTED FILES
- [[SFV_UGC|SFV_UGC]]
- [[SFV_LIVE|SFV_LIVE]]
- [[SFV_EVENTS|SFV_EVENTS]]
- [[DELIVERY|Delivery Workflow]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[EXPORT|Export Workflow]]
- [[MEDIA_PIPELINE|Media Pipeline — Whisper Transcription]]
