# RESULT -- DRAFT-20260701-THEORY-RUNS-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:11:18

---

# Theory Runs Protocol for SFV Engine (n8n + Ollama + Claude AI)  

---

## 1. What is a Theory Run and Why It Exists  

A **Theory Run** is a controlled, dry-run test of the SFV Engine’s workflow pipeline, designed to validate system integrity, identify bottlenecks, and ensure reliability without exposing live client data or workflows to risk. It simulates task envelopes being processed through the full system stack (n8n, Ollama, Claude AI) under predefined scenarios, with manual observation and logging of each step.  

**Purpose**:  
- Validate end-to-end task processing.  
- Identify configuration errors, latency issues, or failover gaps.  
- Ensure compliance with workflow logic and AI integration.  
- Provide a baseline for troubleshooting live issues.  

---

## 2. Scenario Types and Observation Checklists  

### **Scenario A: Basic Queue Processor Round-Trip**  
**Objective**: Validate a single task envelope’s journey through the system from ingestion to output.  

**Steps for Observation**:  
1. **Envelope Ingestion**:  
   - Confirm task envelope is dropped into the n8n queue (via CLI or API).  
   - Verify queue status (e.g., `n8n queue status`).  
2. **n8n Processing**:  
   - Observe execution of nodes (e.g., metadata extraction, format conversion).  
   - Check for errors in n8n logs (`n8n logs`).  
3. **Ollama Integration**:  
   - Confirm Ollama model is invoked (e.g., prompt generation, image captioning).  
   - Verify model output is correctly parsed and passed to next node.  
4. **Claude AI Integration**:  
   - Ensure Claude AI is triggered for tasks requiring LLM processing (e.g., caption refinement, metadata tagging).  
   - Check for response accuracy and error handling.  
5. **Output Storage**:  
   - Confirm processed task is stored in designated output bucket (e.g., S3, local FS).  
   - Verify checksum or hash matches input envelope.  

**PASS**: Task completes without errors, output matches expectations.  
**FAIL**: Any step fails (e.g., queue timeout, Ollama/Claude error, output mismatch).  

---

### **Scenario B: R&D Terminal / Node B Failover**  
**Objective**: Test system resilience when Node B (e.g., Ollama or Claude AI) fails, ensuring fallback to backup systems (e.g., Tavily, local cache).  

**Steps for Observation**:  
1. **Trigger Failover**:  
   - Simulate Node B failure (e.g., terminate Ollama container, block Claude API).  
   - Confirm failure is logged in system monitoring (e.g., Prometheus, Grafana).  
2. **Failover Route Activation**:  
   - Observe fallback to Tavily or local cache for research/data retrieval.  
   - Check logs for "failover triggered" and "backup route activated" messages.  
3. **Task Continuation**:  
   - Verify task envelope continues processing via fallback route.  
   - Confirm output is generated (even if degraded) and stored.  
4. **Post-Failover Recovery**:  
   - Re-enable Node B.  
   - Ensure system reverts to primary route without data loss.  

**PASS**: Failover occurs seamlessly, task completes via backup route, and recovery is automatic.  
**FAIL**: Failover fails, task stalls, or output is incomplete/incorrect.  

---

### **Scenario C: RESEARCH Route via Tavily**  
**Objective**: Validate the system’s ability to route tasks requiring external research (e.g., image attribution, historical context) through Tavily.  

**Steps for Observation**:  
1. **Trigger Research Task**:  
   - Drop a task envelope with a "RESEARCH" flag (e.g., "Find historical context for this image").  
   - Confirm flag is parsed by n8n’s routing logic.  
2. **Tavily Integration**:  
   - Observe Tavily API invocation (e.g., `tavily search` command).  
   - Check for successful retrieval of web results.  
3. **Data Processing**:  
   - Verify Ollama/Claude AI processes Tavily results (e.g., summarization, metadata extraction).  
   - Confirm output is appended to task envelope.  
4. **Final Output**:  
   - Ensure task is stored with research data intact.  
   - Check for redundancy (e.g., original data + research findings).  

**PASS**: Research route is triggered, Tavily returns valid data, and output is correctly merged.  
**FAIL**: Tavily fails, data is incomplete, or routing logic misfires.  

---

## 3. PASS vs FAIL Definitions  

| **Status** | **Definition**                                                                 |
|------------|-------------------------------------------------------------------------------|
| **PASS**   | Task completes all steps without errors, output meets expectations, logs are clean. |
| **FAIL**   | Any step fails (e.g., timeout, incorrect output, unhandled error), or logs indicate anomalies. |

---

## 4. Logging Results  

**Location**: All Theory Run results must be logged to the **SFV Archive Internal Log Repository** (`https://sfv-logs.archive/`).  

**Format**:  
- **Filename**: `theory_run_<scenario>_<date>_<time>.md` (e.g., `theory_run_A_20231015_1430.md`).  
- **Content**:  
  ```markdown
  ## Scenario: A  
  **Status**: PASS / FAIL  
  **Observations**:  
  - Step 1: [Details]  
  - Step 2: [Details]  
  **Issues Identified**: [List issues if FAIL]  
  **Resolution Plan**: [If FAIL, steps to resolve]  
  ```  

**Owners**: Logs must be reviewed by the **SFV Engine Lead** and **AI Integration Team** within 24 hours of submission.  

---  

**End of Document**
