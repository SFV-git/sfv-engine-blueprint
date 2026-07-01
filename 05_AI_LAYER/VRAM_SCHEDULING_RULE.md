**VRAM Scheduling Rule for Roles 3 and 5 (12GB Ceiling)**  
This rule ensures exclusive access to VRAM for large models (Role 3 and Role 5) and prevents concurrent loading of these roles, while adhering to a 12GB VRAM ceiling.

---

### **1. Role-Specific Co-Load Prevention Rule**  
**Rule:**  
> *"When scheduling a task, if the task is **Role 3** or **Role 5**, check if any existing task is also **Role 3** or **Role 5**. If true, **defer the new task** until the existing task completes. This ensures **Role 3 and Role 5 never co-load**."*

**Implementation Details:**  
- Use a **task queue** or **scheduler** that tracks active tasks by role.  
- Before initiating a new task, verify the role of all currently running tasks.  
- If a conflict is detected (e.g., Role 3 is running, and a new Role 5 task is requested), the new task is placed in a **waiting queue** until the existing task completes.  

---

### **2. Ollama Single-Large-Model-at-a-Time Rule (12GB Ceiling)**  
**Rule:**  
> *"For any task requiring **VRAM > 6GB**, enforce a **single-model-at-a-time** policy. Only one such model may be loaded simultaneously, even if the total VRAM usage is below 12GB. This ensures the 12GB ceiling is not exceeded by overlapping large models."*

**Implementation Details:**  
- Define **large models** as those requiring **>6GB VRAM** (e.g., Role 3 and Role 5).  
- When a large model is loaded, **block all other tasks** (including other large models) until it completes.  
- Smaller models (≤6GB) may run concurrently with large models **only if the total VRAM usage remains below 12GB**.  

---

### **3. Combined Enforcement in Ollama**  
**Configuration Example (Ollama):**  
```yaml
scheduling:
  vrampolicy:
    ceiling: 12GB
    roles:
      - role3:
          vram: 10GB
          priority: high
          exclusivity: true
      - role5:
          vram: 11GB
          priority: high
          exclusivity: true
    co_load_prevention:
      - role3
      - role5
```

**Key Ollama Features to Leverage:**  
- **Priority queues** for high-priority roles (Role 3/5).  
- **VRAM usage tracking** to enforce the 12GB ceiling.  
- **Exclusive task locks** for large models (Role 3/5) to prevent co-loading.  

---

### **4. Additional Notes**  
- **Testing:** Validate that Role 3 and Role 5 tasks are never scheduled simultaneously, even if their combined VRAM is ≤12GB.  
- **Fallback:** If a task exceeds the VRAM ceiling, it must be **rejected** or **deferred** until resources are available.  
- **Monitoring:** Log co-load attempts and enforce penalties (e.g., retries, alerts) for violations.  

This rule ensures optimal VRAM utilization, prevents resource contention, and aligns with Ollama’s design for single-model inference.

## CONNECTED FILES
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]

## OVERNIGHT DRAFT — UNREVIEWED (codex merge 2026-07-01, directive MERGE-20260701-P14-VRAM-SCHEDULING-001)

**VRAM Scheduling Rule for Roles 3 and 5 (12GB Ceiling)**  
This rule ensures exclusive access to VRAM for large models (Role 3 and Role 5) and prevents concurrent loading of these roles, while adhering to a 12GB VRAM ceiling.

---

### **1. Role-Specific Co-Load Prevention Rule**  
**Rule:**  
> *"When scheduling a task, if the task is **Role 3** or **Role 5**, check if any existing task is also **Role 3** or **Role 5**. If true, **defer the new task** until the existing task completes. This ensures **Role 3 and Role 5 never co-load**."*

**Implementation Details:**  
- Use a **task queue** or **scheduler** that tracks active tasks by role.  
- Before initiating a new task, verify the role of all currently running tasks.  
- If a conflict is detected (e.g., Role 3 is running, and a new Role 5 task is requested), the new task is placed in a **waiting queue** until the existing task completes.  

---

### **2. Ollama Single-Large-Model-at-a-Time Rule (12GB Ceiling)**  
**Rule:**  
> *"For any task requiring **VRAM > 6GB**, enforce a **single-model-at-a-time** policy. Only one such model may be loaded simultaneously, even if the total VRAM usage is below 12GB. This ensures the 12GB ceiling is not exceeded by overlapping large models."*

**Implementation Details:**  
- Define **large models** as those requiring **>6GB VRAM** (e.g., Role 3 and Role 5).  
- When a large model is loaded, **block all other tasks** (including other large models) until it completes.  
- Smaller models (≤6GB) may run concurrently with large models **only if the total VRAM usage remains below 12GB**.  

---

### **3. Combined Enforcement in Ollama**  
**Configuration Example (Ollama):**  
```yaml
scheduling:
  vrampolicy:
    ceiling: 12GB
    roles:
      - role3:
          vram: 10GB
          priority: high
          exclusivity: true
      - role5:
          vram: 11GB
          priority: high
          exclusivity: true
    co_load_prevention:
      - role3
      - role5
```

**Key Ollama Features to Leverage:**  
- **Priority queues** for high-priority roles (Role 3/5).  
- **VRAM usage tracking** to enforce the 12GB ceiling.  
- **Exclusive task locks** for large models (Role 3/5) to prevent co-loading.  

---

### **4. Additional Notes**  
- **Testing:** Validate that Role 3 and Role 5 tasks are never scheduled simultaneously, even if their combined VRAM is ≤12GB.  
- **Fallback:** If a task exceeds the VRAM ceiling, it must be **rejected** or **deferred** until resources are available.  
- **Monitoring:** Log co-load attempts and enforce penalties (e.g., retries, alerts) for violations.  

This rule ensures optimal VRAM utilization, prevents resource contention, and aligns with Ollama’s design for single-model inference.
