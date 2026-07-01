# RESULT -- REVAMP-20260701-OPENWEBUI-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 15:20:43

---

```markdown
# Open WebUI Specification for SFV Engine

## 1. Purpose
Integrate **Open WebUI** as a unified interface for interacting with local LLMs on the SFV Engine. Key objectives include:
- **Centralized chat UI** for manual prompt testing and model evaluation.
- **Prompt comparison** across models (e.g., Qwen3:14b vs. MiniCPM-V:8b) via side-by-side interface.
- **Development workflow support** for iterative model tuning and error analysis.
- **Security** by isolating model interaction from external networks (see Section 5).

## 2. Deployment
### Requirements
- Docker installed on Engine Body (RTX 5080).
- Ollama endpoint running at `host.docker.internal:11434`.

### Steps
1. **Persistent Volume**: Create a Docker volume for storing user sessions and logs:
   ```bash
   docker volume create openwebui_data
   ```
2. **Container Launch**: Run Open WebUI with volume mount and Ollama endpoint:
   ```bash
   docker run -d \
     --name openwebui \
     --volume openwebui_data:/app/data \
     -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
     -p 3000:3000 \
     --restart unless-stopped \
     n8nio/openwebui:latest
   ```
3. **Verification**: Access UI at `http://localhost:3000` (see Section 5 for security).

### [UNCONFIRMED] Network Configuration
- Confirm `host.docker.internal` resolves correctly in container context.

## 3. Use Case Segmentation
| **Use Case**               | **Tool**           | **Reason**                                                                 |
|---------------------------|--------------------|----------------------------------------------------------------------------|
| Manual prompt testing     | Open WebUI         | GUI-based interaction with real-time feedback and model comparison        |
| Model evaluation (e.g., QA) | Open WebUI       | Structured prompt templates and result tracking                           |
| n8n workflow automation   | Direct Ollama API  | Lower latency, avoids overhead of WebUI routing, ensures API consistency   |
| Batch inference           | Direct Ollama API  | Optimized for high-throughput, non-interactive tasks                      |

## 4. Decision Framework for n8n Workflow Migration
### Option A: Route through Open WebUI
**Pros**:
- Unified monitoring of all model interactions.
- Potential for future feature integration (e.g., prompt library sharing).

**Cons**:
- [UNCONFIRMED] Latency impact on n8n workflows due to WebUI proxy layer.
- Risk of UI-based errors (e.g., incorrect model selection) propagating to workflows.

### Option B: Maintain Direct Ollama API
**Pros**:
- Minimal latency for automation-critical tasks.
- Full control over request formatting and error handling in n8n.

**Cons**:
- No centralized visibility into model usage patterns.

### Recommendation
**Keep n8n workflows on direct Ollama API**.  
**Rationale**: Automation workflows require deterministic behavior and low-latency responses. Open WebUI is better suited for exploratory tasks where UI-based feedback (e.g., model comparison) is valuable. Migrating n8n would introduce unnecessary complexity and risk of performance degradation.

## 5. Access/Security
- **Default**: Open WebUI binds to `0.0.0.0:3000` but requires **localhost-only access** for security.
- **Tailscale Exposure** (if required):
  - Use Tailscale's `--advertise-expose` flag to securely expose the service.
  - Implement **OAuth2 authentication** via Tailscale's identity provider.
  - [UNCONFIRMED] Confirm Tailscale integration with Open WebUI's authentication system.
- **Docker Security**: Ensure `--read-only` flag is applied to container filesystem where possible.

## 6. Monitoring & Maintenance
- **Logs**: Persisted in `openwebui_data` volume (inspect via `docker logs openwebui`).
- **Updates**: Pull new Open WebUI images monthly; test compatibility with Ollama endpoint.
- **Backup**: Include `openwebui_data` volume in SFV's disaster recovery plan.
```
