# REVIEW — UGC Pre-Production Intake Scaffold

- **Reviewed:** `C:\SFV_BLUEPRINT\99_INBOX\PROTOTYPES\ugc_pre_production\index.html`
- **Spec compared against:** `04_WORKFLOWS\UGC_PRE_PRODUCTION.md` (§5 INTAKE FORM)
- **Reviewer:** Claude (Opus 4.8) — read-only review, no files in the prototype folder modified
- **Date:** 2026-07-01

---

## VERDICT: CLEAN

The prototype is a single self-contained `index.html` (HTML + CSS + one inline
IIFE script; no other files in the folder). It is a **client-only** intake form:
all state lives in `localStorage`, there is no backend, network call, `eval`,
or `document.write`. It is safe to open locally and, on its own, safe if served
statically. The minor items below are polish, not blockers.

---

## 1. XSS / Injection — no issues found

- The **only** `innerHTML` sink is in `addHook()` (line ~249). It writes a
  **static template literal with no user data interpolated**. The hook's value
  is applied on the next line via `row.querySelector("input").value = value`
  (a DOM property assignment, which does not parse HTML). ✅ Safe.
- All other user-supplied data is rendered via `textContent`
  (`updateSummary` ~L333, `renumberHooks` ~L270) or written to form control
  `.value` (`populate`). None of these are HTML-parsing sinks. ✅ Safe.
- `localStorage` is read through `JSON.parse` inside a `try/catch` that clears
  a corrupt draft (L389–394). A maliciously crafted draft still cannot reach an
  HTML sink, so it cannot achieve DOM XSS. ✅ Safe.
- No `eval`, `Function`, `document.write`, `innerHTML +=` on user data,
  `srcdoc`, or `on*` attribute construction anywhere.

**Forward-looking caveat (not a defect in this file):** the saved/exported
JSON is untrusted free-text. When the real app, the PDF generator (jsPDF /
react-pdf), or the planned n8n hook later *consume* this data, they must escape
it at their own output boundaries. This prototype does not create that risk; the
downstream consumers will own it.

## 2. Field match vs. UGC_PRE_PRODUCTION.md §5 — complete

All 13 spec'd intake fields are present and correctly modeled:

| Spec field | In form | Notes |
|---|---|---|
| Brand / Client (dropdown) | ✅ `brand` | Sample options, hint notes future Client DB |
| Shoot date | ✅ `shootDate` | `required` |
| Location (dropdown) | ✅ `location` | Sample options, hint notes future Location DB |
| Shooter (dropdown, Will only) | ✅ `shooter` | Single option "Will" |
| Deliverables (Reels/Stories/Stills/BTS) | ✅ `deliverables` | Multi-select checkboxes; ≥1 enforced |
| Number of looks / outfits | ✅ `looks` | number, min 1 |
| Key products / services | ✅ `products` → `productsOrServices` | mapped in collectData |
| Tone / vibe | ✅ `tone` | freeform |
| Hooks (min 3) | ✅ `hookList` | ≥3 non-empty enforced in `validateBrief` |
| Talking points (bullet list) | ✅ `talkingPoints` | split per-line into array |
| CTA | ✅ `cta` | |
| References | ✅ `references` | |
| Special requirements | ✅ `requirements` → `specialRequirements` | mapped in collectData |

Also consistent with the SHOOT entity: auto-generated Shoot ID
(`SHOOT-<date>-<ts>`) and a `status: "PLANNED"` stamp. Deliverable label casing
("Stills" vs spec "stills") is cosmetic and matches intent.

## 3. Bugs — none functional

No correctness defects found. Logic that was checked and is sound:
minimum-3-hook enforcement (remove button hidden at `<= 3`), draft
load/populate round-trip, per-line talking-point parsing, and the
`T12:00:00`-anchored date display (deliberately avoids timezone off-by-one).

## 4. Minor observations (optional polish, non-blocking)

1. **Redundant save/summary calls.** Form-level `input`/`change` listeners
   (L348–349) already cover hook fields via bubbling, yet `addHook` also adds
   per-input `input` listeners (L260) that call `updateSummary()` +
   `saveDraftSilently()`. Harmless double-invocation; could be simplified.
2. **`looks` lower bound.** `Number(fields.looks) || 1` coerces `0` (and blank)
   to `1`. Fine as a default, just note it silently rewrites a `0` entry.
3. **Select value vs. saved draft.** `brand`/`location` options have no explicit
   `value` attributes, so the option text *is* the value. If a sample option is
   later renamed/removed, a previously-saved draft's selection will silently
   fall back to empty. Acceptable for a prototype backed by placeholder data.
4. **Accessibility nit.** Dynamically added hook `<input>`s have a placeholder
   and an `aria-label` on the remove button, but no associated `<label>`. Low
   priority for a prototype.

## Scope note

Reviewed only the prototype file and the workflow spec, both read-only. No
changes were made anywhere. n8n, Docker, git, and live services were not
touched.
