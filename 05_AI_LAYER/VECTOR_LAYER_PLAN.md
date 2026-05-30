---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# VECTOR LAYER PLAN — Qdrant + Embeddings

> In scope for ultraplan (confirmed 2026-05-29).
> Currently marked FUTURE in AI_STACK_ARCHITECTURE_BLUEPRINT §8.
> This doc defines what gets embedded, when, and what queries the store.

---

## PURPOSE IN THE SFV STACK

The vector layer enables three distinct capabilities:

| Capability | What it solves |
|---|---|
| **Semantic search** | Find files/notes by meaning, not filename. "Find the brief about Brandon Bellotti" without knowing the filename. |
| **Deduplication** | Detect near-duplicate content across branches (photo descriptions, captions, briefs). Catches semantic duplicates that MD5 misses. |
| **RAG (retrieval-augmented generation)** | When Claude or Ollama answers a question, the vector layer surfaces the most relevant vault docs as context — without loading the entire vault. |

---

## WHAT GETS EMBEDDED

Priority order:

**Phase 1 — embed first:**
- All vault `.md` files in `05_AI_LAYER/`, `03_INFRASTRUCTURE/`, `04_WORKFLOWS/` — the blueprint core
- `SESSION_STATE.md`, `COMPRESSED_CONTEXT.md` — always-relevant context files
- All `OUTPUTS/` files — searchable results from Ollama/Claude

**Phase 2 — add when stable:**
- Branch files in `01_BRANCHES/`
- `FOR_HUMAN_REVIEW/PROPOSALS.md` and `00_DEV_LOG/` files
- Captions and scripts in `OLLAMA_PROMPTS/`

**Do not embed:**
- JSON workflow files in `03_INFRASTRUCTURE/n8n_workflows/` — not human-language content
- `.gitignore`, `n8n_env.ps1`, binary files
- Individual task queue JSON files — ephemeral, no long-term value

---

## EMBEDDING MODEL

**Model:** `nomic-embed-text` via Ollama
**Dimensions:** 768
**Location:** Run on Node A (Engine Body) — embedding is fast, no GPU required
**Pull command:** `ollama pull nomic-embed-text`

This is the same Ollama instance already running. No new service required.

---

## QDRANT DEPLOYMENT

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v C:/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

**Port:** 6333 (localhost only — do not expose to LAN)
**Storage:** `C:\qdrant_storage\` — SSD, per AI_STACK_ARCHITECTURE_BLUEPRINT §2 (vector search latency demands SSD)

---

## WHEN EMBEDDING RUNS

**Trigger:** vault_watcher.py already monitors the vault for new `.md` files. Extend it to:
1. Detect new or modified `.md` files
2. Call `nomic-embed-text` via Ollama API for each file
3. Upsert the vector into Qdrant with metadata (file path, STATUS, last modified)

**Schedule:** Continuous (vault_watcher handles this). No separate cron needed.

**Batch backfill:** One-time script to embed all existing vault files on initial setup. Run once, then vault_watcher maintains incrementally.

---

## WHAT QUERIES THE VECTOR STORE

| Query source | Use case |
|---|---|
| Claude Code | "Find vault files related to [topic]" — surfaces relevant docs before writing a new one |
| Antigravity | Vault audit — find orphaned or near-duplicate docs across the vault |
| n8n workflow | SUMMARIZE tasks can pull related prior outputs as context before running Ollama |
| Will (via Open WebUI) | Ad-hoc semantic search: "what did we decide about Docker?" |

**Query interface:** Python script or n8n HTTP Request node → `POST http://localhost:6333/collections/sfv_vault/points/search`

---

## COLLECTION SCHEMA

```json
{
  "collection_name": "sfv_vault",
  "vectors": {
    "size": 768,
    "distance": "Cosine"
  },
  "payload_schema": {
    "file_path": "keyword",
    "status": "keyword",
    "last_modified": "datetime",
    "file_type": "keyword"
  }
}
```

---

## RAG INTEGRATION SPEC

For RAG use in n8n workflows:

1. Receive task with prompt
2. Embed the prompt via `nomic-embed-text`
3. Query Qdrant for top-5 most similar vault documents
4. Inject retrieved content as context prefix to the Ollama/Gemini/Claude prompt
5. Send enriched prompt to model

This allows Ollama to answer questions about SFV specifics without being fine-tuned.

---

## IMPLEMENTATION ORDER

| Phase | Action |
|---|---|
| Pre-req | Docker installed |
| Pre-req | `ollama pull nomic-embed-text` |
| Step 1 | Deploy Qdrant container |
| Step 2 | Create `sfv_vault` collection |
| Step 3 | Write backfill script (embed all existing vault `.md` files) |
| Step 4 | Extend vault_watcher.py with Qdrant upsert on file change |
| Step 5 | Test: search for a known topic, verify top results are relevant |
| Step 6 | Add RAG prefix to workflow1 Ollama calls for CLASSIFY/SUMMARIZE |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §8]]
- [[LOCAL_MODELS|Local Models]]
- [[DOCKER_INSTALL_CHECKLIST|Docker Install Checklist]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[OPEN_WEBUI_SPEC|Open WebUI Spec]]
