# RESULT -- REVAMP-20260701-MODELROUTING-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 15:21:08

---

# Model Routing Policy for SFV Engine  
**Purpose:** Define routing rules for model/executor selection based on task type, cost tier, and signal-based decision logic.  

---

## Tier Table with Decision Rules  

| **Model**         | **Tier**       | **Use Case**                                      | **Decision Rules**                                                                 | **Notes**                                                                 |
|-------------------|----------------|---------------------------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| **ollama (local qwen3:14b)** | **Free**       | Cheap mechanical work (inventories, classification, summaries, stubs, doc drafts) | - Token estimate < 1,000<br>- Single file input<br>- No web/current facts needed<br>- No judgment required | Default for all tasks unless signals override                                 |
| **devstral-small-2 (local, 24B)** | **Free (Under Evaluation)** | Potential replacement for claude_code tier (multi-file blueprint authoring) | - Token estimate 1,000–5,000<br>- Multi-file input<br>- Complex reasoning needed<br>- No web/current facts required | [FOR HUMAN REVIEW] Not adopted yet; agentic harness required               |
| **codex (ChatGPT sub)**      | **Paid**       | Narrow coding tasks with locked specs (write-enabled in vault)                   | - Token estimate < 1,000<br>- Locked API/protocol specs<br>- No judgment required | Write-enabled only in vault; no web access                                  |
| **claude_code (cloud)**      | **Paid**       | Real multi-file blueprint authoring                                                | - Token estimate > 5,000<br>- Multi-file input<br>- Complex reasoning needed<br>- Web/current facts required | Default escalation tier for tasks exceeding free-tier capacity            |
| **claude (cloud)**           | **Paid**       | Hard one-shot judgment (legal, ethical, high-stakes decisions)                   | - Token estimate < 1,000<br>- Single file input<br>- High complexity<br>- Judgment required | No mechanical execution; used only for final approval                     |

---

## Escalation Path  
1. **Start with free local models**:  
   - Route to **ollama** for all tasks unless signals (token count, file count, judgment need) require escalation.  
2. **Escalate to devstral-small-2** (if under evaluation):  
   - Only if **ollama fails** and task requires multi-file reasoning (e.g., complex blueprint drafts).  
3. **Escalate to paid tiers**:  
   - **codex** for narrow coding tasks with locked specs.  
   - **claude_code** for multi-file blueprints requiring web/current facts.  
   - **claude** for hard one-shot judgment tasks (no mechanical execution).  

---

## Worked Examples  

### Example 1: **Inventory classification**  
- **Task**: Classify 500 items into categories (e.g., "tools", "consumables").  
- **Routing**: **ollama**  
  - Signals: Token estimate ~300, single file, no judgment or web facts needed.  

### Example 2: **Architectural blueprint authoring**  
- **Task**: Generate a 10-page blueprint for a modular home design.  
- **Routing**: **devstral-small-2** (if under evaluation) → **claude_code** (if devstral fails)  
  - Signals: Token estimate ~4,000, multi-file input, complex reasoning, no web facts.  

### Example 3: **Ethical review of AI deployment**  
- **Task**: Judge whether a proposed AI system complies with GDPR.  
- **Routing**: **claude**  
  - Signals: Token estimate ~200, single file, high complexity, judgment required.  

---

## Logging of Routing Decisions  
All routing decisions are logged with the following metadata:  
- **Task ID**  
- **Model used** (e.g., "ollama", "claude_code")  
- **Signal triggers** (token count, file count, judgment need, web access)  
- **Success/failure status** (for free-tier models)  
- **Escalation path taken** (if any)  
- **Timestamp**  
- **Human review flag** (set to `true` for tasks routed to devstral-small-2 or claude)  

Logs are stored in a structured format (e.g., JSON) in the **ROUTING_AUDIT** database table.  

---  

**Note:** Devstral-small-2 is marked [FOR HUMAN REVIEW] until evaluation completes.
