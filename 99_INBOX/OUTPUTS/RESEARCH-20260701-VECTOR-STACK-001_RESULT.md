# RESULT -- RESEARCH-20260701-VECTOR-STACK-001

- Executor: claude_code
- Status: complete
- Dispatched: 2026-07-01 01:52:57

---

Done. Wrote findings to `C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\research_vector_stack_refresh.md` (new file only — nothing else touched, nothing installed or run).

## Key takeaways

**Qdrant (Docker):**
- Pin to a **v1.17.x** tag of `qdrant/qdrant` (v1.17.1 was current stable; v1.18 exists but only adopt after a deliberate test). **Never use `latest`** for a persistent deployment.
- Ports **6333** (HTTP/dashboard) and **6334** (gRPC); mount `/qdrant/storage`; add `--restart unless-stopped`.

**Resources (studio scale):** trivially small. Floor is 0.5 CPU / 1 GB RAM. Your vault at 768-dim vectors: ~440 MB of vector RAM per 100k chunks. Allocating ~1–2 cores and 2–4 GB is generous. No GPU needed.

**nomic-embed-text via Ollama:** ~274 MB model, **768 dims**, ~2K context, needs Ollama ≥ 0.1.26. Use the modern `POST /api/embed` endpoint (field `input`, returns `embeddings[]`); the legacy `/api/embeddings` uses `prompt` and returns `embedding`.

**Biggest gotchas** (both cause *silent* problems):
1. **Task prefixes are mandatory** — index chunks as `search_document: …` and embed the search box as `search_query: …`. Omitting them quietly degrades retrieval quality rather than erroring.
2. **Docker volume persistence** — the classic "vectors vanished on restart." On **Windows specifically**, prefer a **named Docker volume** over a bind-mounted host folder (WSL bind mounts can lose data).
3. Collection vector size must be exactly **768** with a distance metric (Cosine typical).

All source URLs are cited inline and in a Sources list at the bottom of the file. One caveat worth flagging: several deployment specifics (v1.17 details, Windows volume advice) come from third-party 2026 guides rather than official docs — verify the exact current version tag on Docker Hub before pinning.
