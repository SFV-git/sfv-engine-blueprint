# RESULT -- RESEARCH-20260701-IG-SCHEDULER-001

- Executor: claude_code
- Status: complete
- Dispatched: 2026-07-01 01:48:45

---

Done. I created **`C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\research_ig_scheduler_comparison.md`** (new file only — nothing else touched, no n8n/Docker/git/live services involved).

## What the research found

**The decisive factor for your setup is API/automation access, and neither tool is clean:**

- **Later** has **no public API** for its scheduling product at all. Its "Later Influence" product has a *reporting-only* API, gated behind an account manager — useless for scheduling automation. There's no realistic n8n path without unofficial browser-automation hacks.
- **Buffer** just launched a **public GraphQL API (public beta, 2026)** with personal API keys — callable from n8n's HTTP Request node. But its old REST API is closed to new registrations, and third-party OAuth isn't enabled yet. It's the only *officially documented* programmatic surface between the two, but it's beta.

**Pricing for ~8 accounts:**
- **Buffer:** per-channel → ~$40/mo (Essentials, annual) or ~$80/mo (Team).
- **Later:** ~$18.75/mo *if* all 8 fit in one "social set" — but that's a real question mark (see below).

**Two caveats I flagged rather than glossed over:**
1. **⚠️ Later "social set" ambiguity** — a social set is "up to 8 profiles," but historically oriented as one-per-network, not 8 separate Instagram accounts. Whether your 8 branded accounts fit one Starter set is unclear and **swings the cost from ~$18.75 to ~$82.50/mo**. Confirm with Later directly before buying.
2. **API risk both ways** — I added a note suggesting you also glance at API-first schedulers (Ayrshare, Postiz, Meta's own Content Publishing API) as a parallel option, since a *stable* n8n integration is non-negotiable for you.

Carousels and Reels are effectively a tie (both auto-publish, subject to Meta's account-type permissions).

I deliberately did **not** pick a winner — the file lays out "lean Buffer if…" / "lean Later if…" with the tradeoffs, and all claims are cited with source URLs at the bottom. The n8n requirement is the thing I'd weight most heavily in your decision.
