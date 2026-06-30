# RESULT -- BLUEPRINT-LOOP-20260630-192506-P9-QC-CHECKLIST-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-06-30 19:36:03

---

# QC_CHECKLIST.md  
**Quality Control System Specification for User-Generated Content (UGC)**  

---

## **Overview**  
This document defines the quality control (QC) checklist for validating UGC across text, image, and video content. The system uses the **Ollama API** for initial checks, escalates complex cases to **Claude API** for resolution, and applies auto-fixes where permissible.  

---

## **Quality Check Items**  

### **1. Toxicity Detection**  
**Description**: Identify harmful, offensive, or abusive language.  
- **Pass/Fail Threshold**:  
  - **Pass**: Toxicity score ≤ 0.3 (on a 0–1 scale).  
  - **Fail**: Toxicity score > 0.3.  
- **Ollama Model**: `llama3:8b`  
- **Prompt**:  
  ```  
  Rate the toxicity of the following text on a scale from 0 (completely neutral) to 1 (extremely toxic). Provide only the numerical score.  
  ```  
- **Output Format**: JSON with fields: `check_name`, `score`, `pass`, `auto_fix_applied`.  
- **Escalation Trigger**:  
  - If score > 0.7 → Escalate to Claude API for manual review.  

---

### **2. PII (Personally Identifiable Information) Detection**  
**Description**: Identify and redact sensitive data (e.g., names, addresses, phone numbers).  
- **Pass/Fail Threshold**:  
  - **Pass**: No PII detected.  
  - **Fail**: PII detected.  
- **Ollama Model**: `llama3:8b` (fine-tuned for PII detection).  
- **Prompt**:  
  ```  
  Identify all instances of PII in the text (e.g., names, addresses, phone numbers). List them in a JSON array.  
  ```  
- **Output Format**: JSON with fields: `check_name`, `pii_found`, `auto_redacted`.  
- **Escalation Trigger**:  
  - If PII is ambiguous or cannot be auto-redacted → Escalate to Claude API for manual redaction.  

---

### **3. Grammar and Coherence Check**  
**Description**: Validate grammatical correctness and logical flow.  
- **Pass/Fail Threshold**:  
  - **Pass**: Grammar score ≥ 0.8 (on a 0–1 scale).  
  - **Fail**: Grammar score < 0.8.  
- **Ollama Model**: `llama3:8b`  
- **Prompt**:  
  ```  
  Rate the grammatical correctness and coherence of the text on a scale from 0 (completely incoherent) to 1 (perfectly written). Provide only the numerical score.  
  ```  
- **Output Format**: JSON with fields: `check_name`, `score`, `pass`, `auto_fix_applied`.  
- **Escalation Trigger**:  
  - If grammar score < 0.5 → Escalate to Claude API for rewrite suggestions.  

---

### **4. Image Content Moderation**  
**Description**: Detect explicit, violent, or NSFW imagery.  
- **Pass/Fail Threshold**:  
  - **Pass**: No explicit content detected.  
  - **Fail**: Explicit content detected.  
- **Ollama Model**: `llava:7b` (multimodal vision-language model).  
- **Prompt**:  
  ```  
  Describe the content of the image. Identify any explicit, violent, or NSFW elements. Provide only a JSON array of detected elements.  
  ```  
- **Output Format**: JSON with fields: `check_name`, `explicit_content_found`, `auto_flagged`.  
- **Escalation Trigger**:  
  - If content is ambiguous or requires context → Escalate to Claude API for manual review.  

---

### **5. Copyright Infringement Check**  
**Description**: Detect unauthorized use of copyrighted material (text, images).  
- **Pass/Fail Threshold**:  
  - **Pass**: No copyright violations detected.  
  - **Fail**: Copyright violation detected.  
- **Ollama Model**: `llama3:8b` (fine-tuned for copyright detection).  
- **Prompt**:  
  ```  
  Determine if the provided content (text/image) contains unauthorized use of copyrighted material. Respond with "Yes" or "No".  
  ```  
- **Output Format**: JSON with fields: `check_name`, `copyright_violation`, `auto_flagged`.  
- **Escalation Trigger**:  
  - If uncertainty about copyright status → Escalate to Claude API for legal review.  

---

## **Auto-Fix Scope**  
Auto-fixes are limited to **low-risk, high-confidence scenarios**:  
- **Text**:  
  - Replace profanity with asterisks (`***`).  
  - Redact PII (e.g., `[REDACTED]`).  
  - Correct minor grammar errors (e.g., subject-verb agreement).  
- **Images**:  
  - Auto-flag NSFW content with a watermark.  
  - Blur explicit regions (if safe).  
- **Exclusions**:  
  - No auto-fix for context-sensitive language (e.g., culturally sensitive terms).  
  - No auto-fix for complex logical errors or nuanced content disputes.  

---

## **Escalation Procedures**  
When a check fails and auto-fixes are insufficient:  
1. **Trigger Claude API**:  
   - **Endpoint**: `https://api.anthropic.com/v1/messages`  
   - **Parameters**:  
     - `model`: `claude-3-sonnet`  
     - `max_tokens`: 1000  
     - `temperature`: 0.2  
     - `system_prompt`: "You are a content moderator. Provide a detailed resolution for the flagged UGC."  
     - `user_prompt`: Include the original UGC, QC results, and auto-fix attempts.  
2. **Manual Review**: Escalated content is flagged for human review if Claude’s response is inconclusive.  

---

## **Output Format (Standardized)**  
All QC results must follow this JSON schema:  
```json  
{  
  "check_name": "Toxicity Detection",  
  "score": 0.25,  
  "pass": true,  
  "auto_fix_applied": false,  
  "escalated": false,  
  "timestamp": "2023-10-05T14:30:00Z"  
}  
```  

---

## **Notes**  
- **Model Tuning**: Ollama models may require periodic retraining on domain-specific UGC datasets.  
- **Prompt Safety**: All prompts must avoid bias or ethical risks (e.g., avoid prompts that could generate harmful outputs).  
- **Compliance**: Auto-fixes and escalations must comply with local laws (e.g., GDPR, COPPA).  

---  
**End of Document**
