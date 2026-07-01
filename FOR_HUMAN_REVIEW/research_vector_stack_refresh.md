# Vector Stack Refresh — Research Notes

**Scope:** Local RAG / vault-search stack for a solo creative studio (small, single-node, not enterprise).
**Stack:** Qdrant (self-hosted via Docker) + `nomic-embed-text` embeddings served through Ollama.
**Date compiled:** 2026-07-01
**Status:** Research only — nothing installed, run, or changed. For human review before any action.

---

## 1. Qdrant — recommended Docker image / version

- **Latest stable line is v1.17.x** (v1.17.1 was the current stable release as of late March 2026). The **v1.18** line also exists and is available for self-hosted testing; the community Helm chart is already published at v1.18.2. For a small studio deployment, **pin to a specific v1.17.x tag** and only move to v1.18 after a deliberate test. ([QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/), [GitHub releases](https://github.com/qdrant/qdrant/releases), [Artifact Hub helm 1.18.2](https://artifacthub.io/packages/helm/qdrant/qdrant))
- **Image:** `qdrant/qdrant` on Docker Hub. Official docs show the canonical run pattern. ([Docker Hub](https://hub.docker.com/r/qdrant/qdrant), [Qdrant Installation](https://qdrant.tech/documentation/installation/))
- **Do NOT use the `latest` tag** in a persistent deployment — pin an explicit version and add a restart policy so a host/daemon reboot brings Qdrant back up. ([QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/), [Markaicode persistence guide](https://markaicode.com/howto/how-to-run-qdrant-docker-production/))

**Canonical run command (from official docs):**
```bash
docker run -p 6333:6333 \
    -v $(pwd)/path/to/data:/qdrant/storage \
    qdrant/qdrant
```
Source: [Qdrant Installation](https://qdrant.tech/documentation/installation/)

**Ports:**
- `6333` — HTTP REST API (and web dashboard at `/dashboard`)
- `6334` — gRPC API
- `6335` — cluster/peer communication (only needed for distributed setups — **not needed here**)

Sources: [Qdrant Installation](https://qdrant.tech/documentation/installation/), [Docker Hub](https://hub.docker.com/r/qdrant/qdrant)

**Supported architectures:** x86_64/amd64 and AArch64/arm64. Docs recommend SSD/NVMe if vectors are offloaded to disk (mmap). Some deployment guides note a practical requirement for a modern CPU with the `avx2` flag, though the official install page does not list a hard AVX requirement. ([Qdrant Installation](https://qdrant.tech/documentation/installation/), [QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/))

---

## 2. Resource requirements — small single-node deployment

- **Floor:** Qdrant can run on as little as **0.5 CPU / 1 GB RAM**. Real needs scale with vector count and dimension. ([Capacity Planning](https://qdrant.tech/documentation/guides/capacity-planning/))
- **In-memory sizing formula** (all vectors in RAM, optimal latency):
  `memory ≈ num_vectors × dimensions × 4 bytes × 1.5`
  (the ×1.5 covers indexes, point versions, and temporary segments during optimization).
  - Worked example for this stack: 100,000 chunks × 768 dims × 4 bytes × 1.5 ≈ **~440 MB** of vector RAM. A vault of even a few hundred thousand chunks stays comfortably within a few GB.
  Source: [Minimal RAM to serve a million vectors](https://qdrant.tech/articles/memory-consumption/)
- **Memory-mapped (mmap) mode:** ~1M vectors can be served with as little as **135 MB RAM**, but search latency suffers at that floor — fine as a disk-offload option, not for hot-path search. ([Memory consumption](https://qdrant.tech/articles/memory-consumption/))
- **Quantization** (e.g. scalar/binary) is the single highest-impact optimization if memory ever gets tight: ~4× memory reduction with minimal recall loss. Likely unnecessary at studio scale but worth knowing. ([Antryk production guide](https://www.antryk.com/blog/how-to-deploy-qdrant-in-production-the-complete-guide-2026), [Markaicode config guide](https://markaicode.com/best/best-qdrant-configuration-production-guide/))

**Practical recommendation for a solo studio vault:** ~1–2 CPU cores and 2–4 GB RAM allocated to the Qdrant container is generous for tens-to-hundreds of thousands of chunks; SSD-backed storage. Add a memory alert around 85% of the container limit if you want a safety net. ([QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/))

---

## 3. `nomic-embed-text` via Ollama — how to invoke

- **Model:** `nomic-embed-text` — download size **~274 MB**, context length **~2K tokens**, output **768 dimensions**. Requires **Ollama 0.1.26 or later**. Embedding-only (cannot chat). ([Ollama library](https://ollama.com/library/nomic-embed-text), [Ollama embedding blog](https://ollama.com/blog/embedding-models))
- Pull once with `ollama pull nomic-embed-text` (no run/install performed here — for reference only).

**Two API endpoints exist — note the different JSON field names:**

Modern endpoint `/api/embed` (uses `input`, supports batching):
```bash
curl http://localhost:11434/api/embed -d '{
  "model": "nomic-embed-text",
  "input": "search_document: Rayleigh scattering makes the sky blue."
}'
# -> { "embeddings": [[ ... 768 floats ... ]] }
```

Legacy endpoint `/api/embeddings` (uses `prompt`, single input):
```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "search_document: Rayleigh scattering makes the sky blue."
}'
# -> { "embedding": [ ... 768 floats ... ] }
```
**Prefer `/api/embed`** for new code (batching + the `embeddings` array shape). Sources: [Ollama library](https://ollama.com/library/nomic-embed-text), [Ollama API guide](https://oneuptime.com/blog/post/2026-02-02-ollama-api/view), [Chroma cookbook](https://cookbook.chromadb.dev/integrations/ollama/embeddings/)

**Python / JS SDK:**
```python
import ollama
r = ollama.embed(model='nomic-embed-text', input='search_document: ...')
vec = r.embeddings          # list of 768-float vectors
```
```js
const r = await ollama.embed({ model: 'nomic-embed-text', input: 'search_document: ...' });
// r.embeddings
```
Source: [Ollama embedding models blog](https://ollama.com/blog/embedding-models)

---

## 4. Known gotchas

### 4a. `nomic-embed-text` REQUIRES a task-instruction prefix (biggest correctness trap)
Every input must be prepended with a task prefix, or embedding quality degrades badly:
- **`search_document:`** — for anything you store in Qdrant (your vault chunks).
- **`search_query:`** — for the user's search text at query time.
- (also `classification:` and `clustering:` for other tasks.)

For vault search: index chunks as `search_document: <text>` and embed the search box input as `search_query: <text>`. Mismatched or omitted prefixes produce poor retrieval. This asymmetry is easy to forget and hard to notice — results are simply mediocre rather than broken.
Sources: [Qdrant × Nomic docs](https://qdrant.tech/documentation/embeddings/nomic/), [nomic-embed-text-v1.5 model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5), [nomic-embed-text-v1 model card](https://huggingface.co/nomic-ai/nomic-embed-text-v1)

### 4b. Qdrant collection vector size must be exactly 768
Create the collection with `size: 768` and a distance metric (Cosine is the usual choice for these embeddings). A mismatch between the model's 768 dims and the collection config causes insert/search errors. ([Qdrant × Nomic docs](https://qdrant.tech/documentation/embeddings/nomic/), [Ollama library](https://ollama.com/library/nomic-embed-text))

### 4c. Docker persistence — the classic "vectors vanished on restart"
The most common Qdrant+Docker mistake is a missing/broken volume mount → data gone after a container restart. Always mount `/qdrant/storage` and verify it persists.
Sources: [Markaicode persistence guide](https://markaicode.com/howto/how-to-run-qdrant-docker-production/), [Markaicode 3-step stack](https://markaicode.com/integrate/qdrant-with-docker/)

### 4d. Windows-specific volume caveat
Docker Desktop / WSL bind mounts on Windows have known filesystem quirks that can cause data loss. On Windows, **prefer a named Docker volume** (e.g. `-v qdrant_data:/qdrant/storage`) over a bind-mounted host folder. (On Linux, a bind-mounted host dir owned by root isn't writable — fix with `chown -R 1000:1000` — not applicable on Windows.)
Sources: [QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/), [Markaicode persistence guide](https://markaicode.com/howto/how-to-run-qdrant-docker-production/), [Qdrant Installation](https://qdrant.tech/documentation/installation/)

### 4e. Upgrade path caution (v1.15 → v1.17)
v1.17 removed RocksDB in favor of Gridstore; a direct jump from v1.15.x to v1.17.x is **not** supported — go through the intermediate version. Relevant only if adopting an existing older deployment; a fresh v1.17.x install is unaffected.
Source: [QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/)

### 4f. Restart policy
Add `--restart unless-stopped` (or `always`) so a reboot/daemon restart doesn't leave Qdrant down. Easy to omit; annoying to diagnose.
Source: [QWE AI guide](https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/), [Markaicode persistence guide](https://markaicode.com/howto/how-to-run-qdrant-docker-production/)

### 4g. Ollama embedding throughput
`nomic-embed-text` is small (~274 MB) and CPU-friendly, so no GPU is required for a studio-scale vault. For initial bulk indexing of many chunks, batch requests via `/api/embed` rather than one HTTP call per chunk to keep indexing time reasonable. ([Ollama embedding blog](https://ollama.com/blog/embedding-models), [Ollama library](https://ollama.com/library/nomic-embed-text))

---

## 5. Quick fit assessment for this use case

- Both components are **well within** small/single-node territory — the studio vault will not stress either service.
- Total resident footprint is modest: Qdrant a few hundred MB–few GB of RAM depending on vault size, plus the ~274 MB Ollama model.
- The **two things most likely to cause silent quality/data problems**: (1) forgetting the `search_document:` / `search_query:` prefixes (§4a), and (2) a misconfigured Docker volume on Windows (§4c/4d). Get those right and the rest is routine.

---

## Sources
- Qdrant Installation (official): https://qdrant.tech/documentation/installation/
- Qdrant Docker Hub image: https://hub.docker.com/r/qdrant/qdrant
- Qdrant GitHub releases: https://github.com/qdrant/qdrant/releases
- Qdrant — Minimal RAM to serve a million vectors: https://qdrant.tech/articles/memory-consumption/
- Qdrant Capacity Planning: https://qdrant.tech/documentation/guides/capacity-planning/
- Qdrant × Nomic embeddings docs: https://qdrant.tech/documentation/embeddings/nomic/
- Ollama nomic-embed-text library page: https://ollama.com/library/nomic-embed-text
- Ollama embedding models blog: https://ollama.com/blog/embedding-models
- Ollama API guide (2026): https://oneuptime.com/blog/post/2026-02-02-ollama-api/view
- Chroma cookbook — Ollama embeddings: https://cookbook.chromadb.dev/integrations/ollama/embeddings/
- nomic-embed-text-v1.5 model card (task prefixes): https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
- nomic-embed-text-v1 model card: https://huggingface.co/nomic-ai/nomic-embed-text-v1
- QWE AI — Deploy Qdrant v1.17 in Docker [2026 Guide]: https://www.qwe.edu.pl/ai-tools/best-vector-db-qdrant-deployment-guide/
- Markaicode — Qdrant Docker persistence: https://markaicode.com/howto/how-to-run-qdrant-docker-production/
- Markaicode — Qdrant + Docker 3-step stack: https://markaicode.com/integrate/qdrant-with-docker/
- Antryk — Deploy Qdrant in Production (2026): https://www.antryk.com/blog/how-to-deploy-qdrant-in-production-the-complete-guide-2026
- Artifact Hub — Qdrant Helm 1.18.2: https://artifacthub.io/packages/helm/qdrant/qdrant
</content>
</invoke>

## CONNECTED FILES
- [[DASHBOARD|Dashboard]]
- [[SESSION_STATE|Session State]]
