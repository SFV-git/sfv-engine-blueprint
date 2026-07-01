### n8n WF3 RESEARCH Handler Structural Specification  
**Objective:** Define the architecture, data flow, and integration logic for the n8n WF3 RESEARCH handler, ensuring alignment between `RESEARCH_ROUTE_SPEC` and `N8N_BLUEPRINT` trigger mechanisms while leveraging the Tavily API.  

---

### **1. Handler Overview**  
**Name:** `RESEARCH_HANDLER`  
**Purpose:** Execute research tasks via the Tavily API, route results according to `RESEARCH_ROUTE_SPEC`, and interface with n8n workflows via `N8N_BLUEPRINT` triggers.  

---

### **2. Integration with Tavily API**  
**Authentication:**  
- **Key Source:** Tavily API key (assumed available in n8n credentials manager under `TAVILY_API_KEY`).  
- **Usage:** Injected into HTTP headers (`Authorization: Bearer <TAVILY_API_KEY>`) for Tavily API requests.  

**Supported Operations:**  
- **`search`**: Query Tavily for information (e.g., `GET https://api.tavily.com/search?query={query}`).  
- **`analyze`**: Process structured data (e.g., `POST https://api.tavily.com/analyze`).  
- **Error Handling:**  
  - Retry on transient errors (e.g., 5xx responses).  
  - Log and halt on Tavily API rate limits or invalid keys.  

---

### **3. Input/Output Parameters**  
**Inputs (from `N8N_BLUEPRINT` triggers):**  
- `query`: String (research query or topic).  
- `config`: Object (Tavily-specific parameters, e.g., `max_results`, `search_depth`).  
- `context`: Object (metadata for routing, e.g., `workflow_id`, `user_id`).  

**Outputs (to `N8N_BLUEPRINT` nodes):**  
- `results`: Structured data from Tavily API (e.g., `{ "summary": "...", "sources": [...]}`).  
- `error`: Error object (if Tavily API fails or route spec validation fails).  
- `metadata`: Contextual data for downstream routing (e.g., `{"route": "next_node"}`).  

---

### **4. RESEARCH_ROUTE_SPEC Alignment**  
**Routing Logic:**  
- **Step 1: Validate Input**  
  - Check if `query` and `config` are provided.  
  - If invalid, trigger `N8N_BLUEPRINT` error node with `error.code = "INVALID_INPUT"`.  

- **Step 2: Execute Tavily API Call**  
  - Use `query` and `config` to call Tavily API.  
  - If API returns data, proceed to Step 3.  
  - If API fails, trigger `N8N_BLUEPRINT` error node with `error.code = "TAVILY_API_FAILURE"`.  

- **Step 3: Route Results**  
  - Based on `RESEARCH_ROUTE_SPEC` rules:  
    - **Rule A:** If `results.summary.length > 1000`, route to `SUMMARY_TRUNCATION_NODE`.  
    - **Rule B:** If `results.sources.length == 0`, route to `NO_SOURCES_NODE`.  
    - **Default:** Route to `RESEARCH_OUTPUT_NODE`.  

**Conflict Resolution with `N8N_BLUEPRINT`:**  
- Ensure `RESEARCH_ROUTE_SPEC` conditions are mapped to `N8N_BLUEPRINT` conditional triggers (e.g., `if {{results.summary.length}} > 1000 then trigger SUMMARY_TRUNCATION_NODE`).  
- Use n8n’s `set` node to inject `metadata.route` for downstream routing.  

---

### **5. N8N_BLUEPRINT Trigger Compatibility**  
**Trigger Mechanisms:**  
- **Trigger Type:** `http` (for external requests) or `manual` (for user-initiated workflows).  
- **Data Format:** Inputs must conform to `{"query": "...", "config": {...}, "context": {...}}`.  
- **Output Handling:**  
  - Success: Pass `results` and `metadata` to next node.  
  - Failure: Pass `error` to `N8N_BLUEPRINT` error handling node.  

**Key Reconciliation Points:**  
- **Data Flow Consistency:** Ensure `RESEARCH_ROUTE_SPEC` rules (e.g., `if sources.length == 0`) are mirrored in `N8N_BLUEPRINT` conditional triggers.  
- **Error Propagation:** Map Tavily API errors to `N8N_BLUEPRINT` error codes for centralized handling.  

---

### **6. Example Workflow**  
1. **Trigger:** User submits a query via `N8N_BLUEPRINT` HTTP trigger.  
2. **Handler:**  
   - Validates input.  
   - Calls Tavily API with `query` and `config`.  
   - Routes results to `SUMMARY_TRUNCATION_NODE` if summary is too long.  
3. **Output:** Truncated summary sent to downstream nodes (e.g., email or database).  

---

### **7. Configuration Requirements**  
- **Tavily API Key:** Stored securely in n8n credentials manager.  
- **Environment Variables:**  
  - `TAVILY_API_KEY`: Required for API authentication.  
- **n8n Nodes:**  
  - `RESEARCH_HANDLER` node (custom code).  
  - `set` node for metadata injection.  
  - Conditional triggers for routing.  

---

### **8. Error Handling**  
- **Tavily API Errors:**  
  - Retry up to 3 times on 5xx errors.  
  - Log to n8n’s execution history.  
- **Invalid Input:**  
  - Trigger `N8N_BLUEPRINT` error node with user-friendly message.  
- **Routing Failures:**  
  - Default to `RESEARCH_OUTPUT_NODE` if no route matches.  

---

### **9. Testing & Validation**  
- **Unit Tests:**  
  - Mock Tavily API responses (e.g., empty sources, large summaries).  
  - Validate route spec conditions.  
- **Integration Tests:**  
  - Simulate `N8N_BLUEPRINT` triggers with valid/invalid inputs.  
  - Confirm outputs match expected routing and data formats.  

---

**Conclusion:** This spec ensures seamless integration between `RESEARCH_ROUTE_SPEC` and `N8N_BLUEPRINT` by aligning data flow, error handling, and conditional triggers, while leveraging Tavily for research tasks.

## CONNECTED FILES
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]

## OVERNIGHT DRAFT — UNREVIEWED (codex merge 2026-07-01, directive MERGE-20260701-P8-WF3-RESEARCH-001)

### n8n WF3 RESEARCH Handler Structural Specification  
**Objective:** Define the architecture, data flow, and integration logic for the n8n WF3 RESEARCH handler, ensuring alignment between `RESEARCH_ROUTE_SPEC` and `N8N_BLUEPRINT` trigger mechanisms while leveraging the Tavily API.  

---

### **1. Handler Overview**  
**Name:** `RESEARCH_HANDLER`  
**Purpose:** Execute research tasks via the Tavily API, route results according to `RESEARCH_ROUTE_SPEC`, and interface with n8n workflows via `N8N_BLUEPRINT` triggers.  

---

### **2. Integration with Tavily API**  
**Authentication:**  
- **Key Source:** Tavily API key (assumed available in n8n credentials manager under `TAVILY_API_KEY`).  
- **Usage:** Injected into HTTP headers (`Authorization: Bearer <TAVILY_API_KEY>`) for Tavily API requests.  

**Supported Operations:**  
- **`search`**: Query Tavily for information (e.g., `GET https://api.tavily.com/search?query={query}`).  
- **`analyze`**: Process structured data (e.g., `POST https://api.tavily.com/analyze`).  
- **Error Handling:**  
  - Retry on transient errors (e.g., 5xx responses).  
  - Log and halt on Tavily API rate limits or invalid keys.  

---

### **3. Input/Output Parameters**  
**Inputs (from `N8N_BLUEPRINT` triggers):**  
- `query`: String (research query or topic).  
- `config`: Object (Tavily-specific parameters, e.g., `max_results`, `search_depth`).  
- `context`: Object (metadata for routing, e.g., `workflow_id`, `user_id`).  

**Outputs (to `N8N_BLUEPRINT` nodes):**  
- `results`: Structured data from Tavily API (e.g., `{ "summary": "...", "sources": [...]}`).  
- `error`: Error object (if Tavily API fails or route spec validation fails).  
- `metadata`: Contextual data for downstream routing (e.g., `{"route": "next_node"}`).  

---

### **4. RESEARCH_ROUTE_SPEC Alignment**  
**Routing Logic:**  
- **Step 1: Validate Input**  
  - Check if `query` and `config` are provided.  
  - If invalid, trigger `N8N_BLUEPRINT` error node with `error.code = "INVALID_INPUT"`.  

- **Step 2: Execute Tavily API Call**  
  - Use `query` and `config` to call Tavily API.  
  - If API returns data, proceed to Step 3.  
  - If API fails, trigger `N8N_BLUEPRINT` error node with `error.code = "TAVILY_API_FAILURE"`.  

- **Step 3: Route Results**  
  - Based on `RESEARCH_ROUTE_SPEC` rules:  
    - **Rule A:** If `results.summary.length > 1000`, route to `SUMMARY_TRUNCATION_NODE`.  
    - **Rule B:** If `results.sources.length == 0`, route to `NO_SOURCES_NODE`.  
    - **Default:** Route to `RESEARCH_OUTPUT_NODE`.  

**Conflict Resolution with `N8N_BLUEPRINT`:**  
- Ensure `RESEARCH_ROUTE_SPEC` conditions are mapped to `N8N_BLUEPRINT` conditional triggers (e.g., `if {{results.summary.length}} > 1000 then trigger SUMMARY_TRUNCATION_NODE`).  
- Use n8n’s `set` node to inject `metadata.route` for downstream routing.  

---

### **5. N8N_BLUEPRINT Trigger Compatibility**  
**Trigger Mechanisms:**  
- **Trigger Type:** `http` (for external requests) or `manual` (for user-initiated workflows).  
- **Data Format:** Inputs must conform to `{"query": "...", "config": {...}, "context": {...}}`.  
- **Output Handling:**  
  - Success: Pass `results` and `metadata` to next node.  
  - Failure: Pass `error` to `N8N_BLUEPRINT` error handling node.  

**Key Reconciliation Points:**  
- **Data Flow Consistency:** Ensure `RESEARCH_ROUTE_SPEC` rules (e.g., `if sources.length == 0`) are mirrored in `N8N_BLUEPRINT` conditional triggers.  
- **Error Propagation:** Map Tavily API errors to `N8N_BLUEPRINT` error codes for centralized handling.  

---

### **6. Example Workflow**  
1. **Trigger:** User submits a query via `N8N_BLUEPRINT` HTTP trigger.  
2. **Handler:**  
   - Validates input.  
   - Calls Tavily API with `query` and `config`.  
   - Routes results to `SUMMARY_TRUNCATION_NODE` if summary is too long.  
3. **Output:** Truncated summary sent to downstream nodes (e.g., email or database).  

---

### **7. Configuration Requirements**  
- **Tavily API Key:** Stored securely in n8n credentials manager.  
- **Environment Variables:**  
  - `TAVILY_API_KEY`: Required for API authentication.  
- **n8n Nodes:**  
  - `RESEARCH_HANDLER` node (custom code).  
  - `set` node for metadata injection.  
  - Conditional triggers for routing.  

---

### **8. Error Handling**  
- **Tavily API Errors:**  
  - Retry up to 3 times on 5xx errors.  
  - Log to n8n’s execution history.  
- **Invalid Input:**  
  - Trigger `N8N_BLUEPRINT` error node with user-friendly message.  
- **Routing Failures:**  
  - Default to `RESEARCH_OUTPUT_NODE` if no route matches.  

---

### **9. Testing & Validation**  
- **Unit Tests:**  
  - Mock Tavily API responses (e.g., empty sources, large summaries).  
  - Validate route spec conditions.  
- **Integration Tests:**  
  - Simulate `N8N_BLUEPRINT` triggers with valid/invalid inputs.  
  - Confirm outputs match expected routing and data formats.  

---

**Conclusion:** This spec ensures seamless integration between `RESEARCH_ROUTE_SPEC` and `N8N_BLUEPRINT` by aligning data flow, error handling, and conditional triggers, while leveraging Tavily for research tasks.
