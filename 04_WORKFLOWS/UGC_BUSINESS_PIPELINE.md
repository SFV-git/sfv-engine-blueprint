---
STATUS: FOR HUMAN REVIEW
VERSION: v2.0.0
OWNER: WILL
LAST_UPDATED: 2026-07-01
REWRITTEN_BY: Claude Chat (autonomous, web-researched against 2026 UGC market data)
SUPERSEDES: v1 (scored 1/5 by Perplexity — described a B2B martech agency campaign pipeline
  using Salesforce/Tableau/TINT/Hootsuite/Upland, entirely wrong business model. All removed.)
GROUND_TRUTH: [[SFV_UGC_SEED|SFV UGC Seed]]
---

# UGC BUSINESS PIPELINE

SFV_UGC is a solo creator/shooter selling short-form video content directly to brands on retainer.
SFV IS the content producer — not an agency aggregating consumer content. Pipeline:
outreach → pitch → brief → shoot → edit → deliver → invoice → repeat.

Market benchmarks below verified against 2026 UGC industry data (Fueler, Influee, InfluenceFlow,
DesignRevision, Billo). All specific SFV numbers remain [FOR HUMAN REVIEW] until Will locks them —
these are industry-standard defaults to price against, not SFV's confirmed rates.

## 1. LEAD INTAKE / CLIENT ACQUISITION
Channels (from SFV_UGC_SEED — Will-confirmed):
1. Direct outreach to known contacts already doing UGC for brands (warm, first channel)
2. Scraper bot → find local UGC service providers → get in same rooms → pitch in person
3. Sales team → US + other-province brand outreach
4. Website → brands book a digital rebrand (full AIO pipeline) + web-dev partner bundle

Intake tracking: lightweight CRM. HubSpot free tier is sufficient for solo/retainer volume.
DO NOT use Salesforce (enterprise, wrong scale). Log: brand, contact, source channel, stage,
budget signal, follow-up date.

Outreach cadence benchmark: pitch 5-10 brands/week, 10-20% response rate is normal early on.
Before pitching: 15 min researching the brand's existing TikTok/IG, reference a specific recent
post, explain how SFV's style complements their current marketing.

## 2. BRIEF INTAKE
Required from brand BEFORE any shoot (build as a form — Tally/Typeform, feeds the n8n intake):
- Product + key talking points
- Hook direction / angle (testimonial, unboxing, demo, lifestyle)
- Visual references
- Aspect ratios required (9:16, 1:1, 4:5, 16:9)
- Posting date / deadline
- Edited deliverable vs raw footage?
- Usage scope: organic only, or paid ads / whitelisting? (determines pricing — see §4)

n8n hook: brief form submitted → task dropped to Hermes queue → Telegram notification to Will.

## 3. RATE CARD STRUCTURE (industry defaults — [FOR HUMAN REVIEW, Will sets final])
Keep it simple: one base rate + clear add-ons. Complex rate cards kill deals.

Base rate tiers (2026 US market, single 15-60s video):
- Beginner (0-1yr): $150-300
- Mid-tier (1-3yr, proven portfolio): $400-800
- Top-tier (proven ROAS data): $1,000-3,000+
- 2026 market average: ~$212/deliverable

Add-ons (separate creation fee from usage fee — always):
- Extra 15s hook variation: +$50-100 each
- Raw footage access: +30-50% of base
- 48hr rush delivery: +25-50%
- Additional revision round (beyond included): +$25-200
- Product return/handling: +$25-50 + shipping

Usage rights (the biggest money lever — base rate covers organic only, 30-90 days):
- Paid ad usage: +30-50% of base per 30-day period
- Whitelisting (brand runs ads through creator's own handle): +20-50%/month
- 90-day exclusivity: +25-35% | 6-month: +40-60% | perpetual: 2x+
- Full-year digital ad usage: +50-100% of base

Bundle discount: 10-20% off for packages of 5+ videos (standard, builds recurring).

## 4. SFV RETAINER MODEL (from SFV_UGC_SEED — Will-confirmed direction)
- Monthly recurring fee for ongoing content production
- One-time fee for full media revamp (website build by web-dev partner)
- Increased monthly rate for maintenance on top of shoot fees
- Retainer = monthly content package (8-12 pieces) at per-piece discount, guaranteed recurring income
- Exact SFV numbers: [FOR HUMAN REVIEW — NOT YET SET]

## 5. CONTRACT / SCOPE PROTECTION
Every project needs written scope BEFORE work starts (prevents scope creep — the #1 profit killer):
- Deliverables itemized (count, length, aspect ratios)
- Revisions: "Includes up to 2 rounds of minor edits addressing creative direction. Additional
  rounds $X each. Technical fixes (audio sync, color) unlimited within 5 days of delivery."
- Revision requests must come within 5 days of delivery
- Usage rights explicitly stated: "Rate includes 90-day organic usage license for brand's owned
  TikTok/IG channels. Paid ad usage billed separately." (Silence = brand assumes perpetual/unlimited = lost income.)
- Scope changes ("redo the thumbnail", "film an alternate version") = new deliverable, billed separately, in writing first.

Tools: contract templates (DocuSign/PandaDoc for e-sign — NOT Canva, Canva can't collect signatures).

## 6. PAYMENT TERMS
- Standard: 50% upfront, 50% on delivery. NOT Net-30 (that's agency terms, wrong for solo).
- Invoicing: [FOR HUMAN REVIEW — Will's locked invoicing tool goes here. v1 recommended 3 tools as if undecided.]
- Client-ghost-after-delivery protection: upfront 50% covers the shoot; final files released only on final payment.

## 7. DELIVERY
- Method: [FOR HUMAN REVIEW — Google Drive / WeTransfer / Frame.io / Dropbox — Will to lock]
- See [[UGC_DELIVERY|UGC Delivery]] for the delivery workflow spec.
- Deliverable specs: burned-in captions per §8 of [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]], correct aspect ratios per brief.
- Deliver 24h early when possible — "reliable creator" = repeat bookings.

## 8. PERFORMANCE / REPORTING
Reality check: a UGC creator usually does NOT have access to the brand's ad analytics.
SFV delivers the asset; the brand runs it and owns performance data.
SFV's "reporting" = delivery confirmation + usage-rights summary, NOT a campaign analytics dashboard.
(v1 assumed access to brand social metrics — incorrect for this model.)
Exception: if whitelisting through SFV's own handle, SFV sees that ad's metrics — can report those.

## 9. n8n AUTOMATION HOOKS (the actual stack value)
- Brief form submitted → task to Hermes queue + Telegram ping
- Invoice sent → Telegram notification
- Delivery confirmed → archive trigger ([[ARCHIVE|Archive Workflow]])
- Retainer client → monthly recurring task auto-created on billing date
Client comms channel: Telegram (locked) — NOT Slack/Teams (v1 recommended those, wrong).

## CONNECTED FILES
- [[SFV_UGC_SEED|SFV UGC Seed]]
- [[SFV_UGC|SFV UGC Branch]]
- [[UGC_PRE_PRODUCTION|UGC Pre-Production]]
- [[UGC_DELIVERY|UGC Delivery]]
- [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]]
- [[SAAS_CONVERSION_PLAN|SaaS Conversion Plan]]
