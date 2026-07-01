---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# DATABANK ARCHITECTURE

## PURPOSE
Maps every databank in the SFV system.
Blueprint vault documents structure. Engine holds actual data.

## TWO LAYERS
```
SFV_BLUEPRINT/12_DATABANKS/    ← architecture docs (this vault)
SFV_ENGINE/DATABANKS/           ← actual data (built in v2.x+)
```

## DATABANK TYPES

### CONTENT BANKS
Hooks, CTAs, script templates, content map templates.
Fed by: UGC production sessions, successful content analysis.
Used by: Claude API (caption generation), n8n (content map builder).

### TASTE BANKS
Visual references, grade references, edit style per branch.
Fed by: Will's selections, are.na research, R&D terminal trend research.
Used by: Archive curation support, QC audit visual baseline.

### CLIENT BANKS
Client profiles, briefs, feedback, memory per client.
Fed by: each UGC client session, QC outcomes.
Used by: monthly content map generation, brief generation.

### BRAND BANKS
SFV visual language, caption style per branch.
Fed by: Will's decisions, design sessions.
Used by: all AI calls involving SFV brand voice.

### RESEARCH BANKS
Trend research, platform insights.
Fed by: R&D terminal continuous research (24/7).
Used by: content map generation, template updates.

### TRAINING DATA
QC approved and rejected reels.
Fed by: every UGC delivery outcome.
Used by: QC system training, improving accuracy over time.

## CONNECTED FILES
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[CLAUDE_API|Claude API]]
- [[RD_TERMINAL_ARCHITECTURE|RD Terminal Architecture]]
- [[BRANCH_OUTPUTS|Branch Outputs]]
- [[QUALITY_CONTROL|Quality Control]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[DEEP_RESEARCH_FINDINGS|Deep Research Findings]]

## OVERNIGHT DRAFT — UNREVIEWED (codex merge 2026-07-01, directive MERGE-20260701-P10-BANKS-WIRING-001)


### **Blueprint for Wiring CONTENT_BANKS and CLIENT_BANKS into Pre-Production**  
This blueprint outlines the integration of **CONTENT_BANKS** (repository of content assets) and **CLIENT_BANKS** (client-specific data) into a pre-production environment, mapping **CLIENT_BANKS** memory fields to an **intake app schema** and defining how **hooks/scripts** surface in the user interface (form).  

---

## **1. System Overview**  
### **Key Components**  
- **CONTENT_BANKS**: Centralized storage for media, templates, and content assets (e.g., images, videos, text snippets).  
- **CLIENT_BANKS**: Client-specific data repository (e.g., user profiles, preferences, contracts, and metadata).  
- **Intake App**: Front-end application for data collection, configured to pull from **CONTENT_BANKS** and **CLIENT_BANKS**.  
- **Hooks/Scripts**: Automated workflows or custom logic triggered during form interactions (e.g., validation, dynamic field population, or API calls).  

---

## **2. Data Mapping: CLIENT_BANKS to Intake App Schema**  
### **Objective**  
Map **CLIENT_BANKS** memory fields (e.g., `client_id`, `preferred_language`, `contract_expiry`) into the **intake app schema** (e.g., form fields, database tables).  

### **Mapping Rules**  
| **CLIENT_BANKS Field**       | **Intake App Schema Field**         | **Data Type** | **Description** |  
|-----------------------------|------------------------------------|---------------|------------------|  
| `client_id`                 | `form.client_id`                   | String        | Unique client identifier. |  
| `preferred_language`        | `form.language_preference`         | Enum (ISO 639-1) | e.g., `en`, `es`. |  
| `contract_expiry`           | `form.contract_expiry_date`        | Date          | Expiry date of client contract. |  
| `client_segment`            | `form.segment`                     | Enum (e.g., "VIP", "Standard") | Client categorization. |  
| `custom_metadata`           | `form.additional_info`             | JSON          | Free-form client-specific data. |  

### **Implementation Details**  
- **Data Source**: Use API endpoints or database queries to fetch **CLIENT_BANKS** data.  
- **Schema Alignment**:  
  - Map `client_id` to a hidden field in the form for internal tracking.  
  - Use `preferred_language` to dynamically load localized content from **CONTENT_BANKS**.  
  - Validate `contract_expiry` against current date using **hooks/scripts** (see Section 3).  
- **Security**:  
  - Encrypt `custom_metadata` if sensitive.  
  - Use role-based access control (RBAC) to restrict access to **CLIENT_BANKS**.  

---

## **3. Hooks/Scripts in the Form**  
### **Purpose**  
Automate workflows, enforce business rules, or dynamically update form behavior based on **CLIENT_BANKS** or **CONTENT_BANKS** data.  

### **Types of Hooks/Scripts**  
1. **On-Load Scripts**  
   - **Function**: Populate form fields with pre-loaded **CLIENT_BANKS** data.  
   - **Example**:  
     ```javascript  
     // Auto-fill client name on form load  
     document.getElementById("client_name").value = getClientData().name;  
     ```  
   - **Integration**: Triggered via a `DOMContentLoaded` event or framework-specific lifecycle hooks (e.g., React `useEffect`).  

2. **Validation Hooks**  
   - **Function**: Validate form inputs against **CLIENT_BANKS** rules (e.g., contract expiry date).  
   - **Example**:  
     ```javascript  
     function validateContractExpiry(date) {  
       const clientExpiry = getClientData().contract_expiry;  
       return date <= clientExpiry ? "Valid" : "Expiry date must be after contract end.";  
     }  
     ```  

3. **Dynamic Content Population**  
   - **Function**: Fetch content from **CONTENT_BANKS** based on user input.  
   - **Example**:  
     ```javascript  
     // Load template from CONTENT_BANKS when user selects a category  
     async function loadTemplate(category) {  
       const template = await fetchContentBank(`templates/${category}`);  
       document.getElementById("content_preview").innerHTML = template;  
     }  
     ```  

4. **Pre-Submit Scripts**  
   - **Function**: Enrich form data with **CLIENT_BANKS** metadata before submission.  
   - **Example**:  
     ```javascript  
     function preSubmitHandler(formData) {  
       const clientData = getClientData();  
       formData.additional_info = { ...formData.additional_info, client_segment: clientData.segment };  
       return formData;  
     }  
     ```  

---

## **4. Integration Blueprint**  
### **Architecture Diagram (Textual Representation)**  
```
[CLIENT_BANKS]       [CONTENT_BANKS]  
     |                   |  
     | Fetch via API     | Fetch via API  
     v                   v  
[Intake App] <-----> [Form Engine]  
     |                   |  
     | Use Hooks/Scripts | Use Hooks/Scripts  
     v                   v  
[Database]           [Content Cache]  
```  

### **Key Integration Points**  
- **API Endpoints**:  
  - `GET /client-data/{client_id}` → Fetches **CLIENT_BANKS** data.  
  - `GET /content/{type}/{id}` → Fetches **CONTENT_BANKS** assets.  
- **Form Engine**:  
  - Binds **CLIENT_BANKS** fields to form inputs.  
  - Triggers hooks/scripts on user interactions (e.g., input change, submit).  
- **Caching**:  
  - Cache **CONTENT_BANKS** assets locally for faster access.  
  - Invalidate cache when **CONTENT_BANKS** data is updated.  

---

## **5. Pre-Production Configuration**  
### **Steps**  
1. **Environment Setup**:  
   - Provision staging servers for **CLIENT_BANKS** and **CONTENT_BANKS**.  
   - Configure API gateways for secure access.  

2. **Schema Sync**:  
   - Align **CLIENT_BANKS** memory fields with the **intake app schema** using migration scripts.  

3. **Hook/Script Testing**:  
   - Unit test hooks/scripts for edge cases (e.g., invalid dates, missing **CLIENT_BANKS** data).  

4. **User Acceptance Testing (UAT)**:  
   - Validate dynamic content population and validation rules with end-users.  

5. **Security Hardening**:  
   - Enable HTTPS for API calls.  
   - Audit permissions for **CLIENT_BANKS** access.  

---

## **6. Error Handling & Logging**  
- **Data Mapping Errors**:  
  - Log mismatches between **CLIENT_BANKS** and **intake app schema** (e.g., missing fields).  
- **Hook/Script Failures**:  
  - Display user-friendly error messages (e.g., "Failed to load template").  
  - Log errors to a centralized system (e.g., Sentry, ELK Stack).  
- **Fallback Behavior**:  
  - Use default **CONTENT_BANKS** assets if dynamic content fails to load.  

---

## **7. Post-Pre-Production**  
- **Monitor Performance**: Track API latency for **CLIENT_BANKS** and **CONTENT_BANKS** queries.  
- **Iterate**: Refine hooks/scripts based on user feedback.  

--- 

This blueprint ensures seamless integration of **CONTENT_BANKS** and **CLIENT_BANKS** into the **intake app**, with clear data mapping and extensible hooks/scripts for dynamic form behavior.
