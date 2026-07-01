# Specification for Training Data Automation: QC File Handling and Logging

## **Overview**
This specification outlines an automation system that moves training data files to either `QC_APPROVED` or `QC_REJECTED` directories based on Will's decision, logs the outcome, and provides feedback for **Role 5**. The system supports implementation via **Python** (e.g., Flask + `shutil`) or **n8n** (workflow automation tool).

---

## **Components**
1. **Trigger**: Event to initiate the workflow (e.g., user submission, file upload).
2. **Decision Logic**: Rule to determine `QC_APPROVED` or `QC_REJECTED` based on Will's input.
3. **File Handling**: Move files to appropriate directories.
4. **Logging**: Record decisions, timestamps, and metadata for **Role 5** feedback.

---

## **Trigger Definition**

### **Option 1: Python (Flask/Webhook)**
- **Trigger Type**: HTTP POST request to a Flask endpoint.
- **Input Payload**:
  ```json
  {
    "filename": "example_data.csv",
    "decision": "QC_APPROVED",  // or "QC_REJECTED"
    "user": "Will"
  }
  ```
- **Code Snippet**:
  ```python
  from flask import Flask, request
  import shutil
  import os
  import logging

  app = Flask(__name__)
  LOG_FILE = "qc_log.json"
  APPROVED_DIR = "/path/to/QC_APPROVED"
  REJECTED_DIR = "/path/to/QC_REJECTED"

  logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

  @app.route("/submit_decision", methods=["POST"])
  def handle_decision():
      data = request.json
      filename = data["filename"]
      decision = data["decision"]
      user = data["user"]

      # Move file
      src_path = f"/path/to/uploaded_files/{filename}"
      dest_dir = APPROVED_DIR if decision == "QC_APPROVED" else REJECTED_DIR
      dest_path = os.path.join(dest_dir, filename)
      shutil.move(src_path, dest_path)

      # Log outcome
      log_entry = {
          "filename": filename,
          "decision": decision,
          "timestamp": datetime.now().isoformat(),
          "user": user
      }
      logging.info(str(log_entry))

      return {"status": "success", "message": "File processed and logged."}
  ```

---

### **Option 2: n8n Workflow**
- **Trigger Node**:  
  - **Type**: `HTTP Request` (Webhook)  
  - **Configuration**:  
    - **Method**: POST  
    - **URL**: `/api/submit_decision`  
    - **Expected JSON Payload**:
      ```json
      {
        "filename": "example_data.csv",
        "decision": "QC_APPROVED",
        "user": "Will"
      }
      ```

- **Action Nodes**:  
  1. **Move File**:  
     - **Type**: `File` → `Move File`  
     - **Configuration**:  
       - **Source Path**: `{{ $json.filename }}` (from uploaded files directory).  
       - **Destination Path**:  
         ```plaintext
         {{ $json.decision == "QC_APPROVED" ? "QC_APPROVED/{{ $json.filename }}" : "QC_REJECTED/{{ $json.filename }}" }}
         ```
  2. **Log Outcome**:  
     - **Type**: `Function` (Custom JavaScript)  
     - **Code**:
       ```javascript
       const logEntry = {
         filename: $json.filename,
         decision: $json.decision,
         timestamp: new Date().toISOString(),
         user: $json.user
       };
       console.log(JSON.stringify(logEntry)); // Logs to n8n's debug console or external logging service
       ```

---

## **Automation Logic**
1. **Trigger**: A POST request is sent to the system with the filename, decision (`QC_APPROVED`/`QC_REJECTED`), and user (`Will`).  
2. **Validation**:  
   - Ensure `filename` exists in the source directory.  
   - Validate `decision` is one of the allowed values.  
3. **File Movement**:  
   - Move the file to `QC_APPROVED` or `QC_REJECTED` based on the decision.  
   - If the file cannot be moved (e.g., permissions), log an error.  
4. **Logging**:  
   - Store a JSON log entry in a file (e.g., `qc_log.json`) or database with:  
     - `filename`, `decision`, `timestamp`, `user`, and optional `error` field.  

---

## **Logging Format (Example)**
```json
{
  "filename": "example_data.csv",
  "decision": "QC_REJECTED",
  "timestamp": "2023-10-05T14:30:00Z",
  "user": "Will",
  "error": "File had missing labels"  // Optional
}
```

---

## **Role 5 Feedback**
- **Access**: Role 5 users can review the `qc_log.json` file or query a database for:  
  - Approval/rejection trends.  
  - Files requiring rework (e.g., `QC_REJECTED` entries).  
  - Timestamps to audit decision timelines.  

---

## **Error Handling**
- **File Not Found**: Log an error and notify Will.  
- **Permission Issues**: Retry or alert administrators.  
- **Invalid Decision**: Reject the request and log the invalid input.  

---

## **Technology Stack**
- **Python**: Flask (web server), `shutil` (file operations), `logging` (log entries).  
- **n8n**: HTTP Request, File, and Function nodes.  

---

## **Example Use Case**
1. Will reviews `example_data.csv` and submits a decision via a web form.  
2. The system moves the file to `QC_APPROVED` and logs the outcome.  
3. Role 5 accesses the log to verify the decision and ensure compliance.  

--- 

This specification ensures seamless automation, traceability, and feedback for training data quality control.

## CONNECTED FILES
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]

## OVERNIGHT DRAFT — UNREVIEWED (codex merge 2026-07-01, directive MERGE-20260701-P18-TRAINING-DATA-001)

# Specification for Training Data Automation: QC File Handling and Logging

## **Overview**
This specification outlines an automation system that moves training data files to either `QC_APPROVED` or `QC_REJECTED` directories based on Will's decision, logs the outcome, and provides feedback for **Role 5**. The system supports implementation via **Python** (e.g., Flask + `shutil`) or **n8n** (workflow automation tool).

---

## **Components**
1. **Trigger**: Event to initiate the workflow (e.g., user submission, file upload).
2. **Decision Logic**: Rule to determine `QC_APPROVED` or `QC_REJECTED` based on Will's input.
3. **File Handling**: Move files to appropriate directories.
4. **Logging**: Record decisions, timestamps, and metadata for **Role 5** feedback.

---

## **Trigger Definition**

### **Option 1: Python (Flask/Webhook)**
- **Trigger Type**: HTTP POST request to a Flask endpoint.
- **Input Payload**:
  ```json
  {
    "filename": "example_data.csv",
    "decision": "QC_APPROVED",  // or "QC_REJECTED"
    "user": "Will"
  }
  ```
- **Code Snippet**:
  ```python
  from flask import Flask, request
  import shutil
  import os
  import logging

  app = Flask(__name__)
  LOG_FILE = "qc_log.json"
  APPROVED_DIR = "/path/to/QC_APPROVED"
  REJECTED_DIR = "/path/to/QC_REJECTED"

  logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

  @app.route("/submit_decision", methods=["POST"])
  def handle_decision():
      data = request.json
      filename = data["filename"]
      decision = data["decision"]
      user = data["user"]

      # Move file
      src_path = f"/path/to/uploaded_files/{filename}"
      dest_dir = APPROVED_DIR if decision == "QC_APPROVED" else REJECTED_DIR
      dest_path = os.path.join(dest_dir, filename)
      shutil.move(src_path, dest_path)

      # Log outcome
      log_entry = {
          "filename": filename,
          "decision": decision,
          "timestamp": datetime.now().isoformat(),
          "user": user
      }
      logging.info(str(log_entry))

      return {"status": "success", "message": "File processed and logged."}
  ```

---

### **Option 2: n8n Workflow**
- **Trigger Node**:  
  - **Type**: `HTTP Request` (Webhook)  
  - **Configuration**:  
    - **Method**: POST  
    - **URL**: `/api/submit_decision`  
    - **Expected JSON Payload**:
      ```json
      {
        "filename": "example_data.csv",
        "decision": "QC_APPROVED",
        "user": "Will"
      }
      ```

- **Action Nodes**:  
  1. **Move File**:  
     - **Type**: `File` → `Move File`  
     - **Configuration**:  
       - **Source Path**: `{{ $json.filename }}` (from uploaded files directory).  
       - **Destination Path**:  
         ```plaintext
         {{ $json.decision == "QC_APPROVED" ? "QC_APPROVED/{{ $json.filename }}" : "QC_REJECTED/{{ $json.filename }}" }}
         ```
  2. **Log Outcome**:  
     - **Type**: `Function` (Custom JavaScript)  
     - **Code**:
       ```javascript
       const logEntry = {
         filename: $json.filename,
         decision: $json.decision,
         timestamp: new Date().toISOString(),
         user: $json.user
       };
       console.log(JSON.stringify(logEntry)); // Logs to n8n's debug console or external logging service
       ```

---

## **Automation Logic**
1. **Trigger**: A POST request is sent to the system with the filename, decision (`QC_APPROVED`/`QC_REJECTED`), and user (`Will`).  
2. **Validation**:  
   - Ensure `filename` exists in the source directory.  
   - Validate `decision` is one of the allowed values.  
3. **File Movement**:  
   - Move the file to `QC_APPROVED` or `QC_REJECTED` based on the decision.  
   - If the file cannot be moved (e.g., permissions), log an error.  
4. **Logging**:  
   - Store a JSON log entry in a file (e.g., `qc_log.json`) or database with:  
     - `filename`, `decision`, `timestamp`, `user`, and optional `error` field.  

---

## **Logging Format (Example)**
```json
{
  "filename": "example_data.csv",
  "decision": "QC_REJECTED",
  "timestamp": "2023-10-05T14:30:00Z",
  "user": "Will",
  "error": "File had missing labels"  // Optional
}
```

---

## **Role 5 Feedback**
- **Access**: Role 5 users can review the `qc_log.json` file or query a database for:  
  - Approval/rejection trends.  
  - Files requiring rework (e.g., `QC_REJECTED` entries).  
  - Timestamps to audit decision timelines.  

---

## **Error Handling**
- **File Not Found**: Log an error and notify Will.  
- **Permission Issues**: Retry or alert administrators.  
- **Invalid Decision**: Reject the request and log the invalid input.  

---

## **Technology Stack**
- **Python**: Flask (web server), `shutil` (file operations), `logging` (log entries).  
- **n8n**: HTTP Request, File, and Function nodes.  

---

## **Example Use Case**
1. Will reviews `example_data.csv` and submits a decision via a web form.  
2. The system moves the file to `QC_APPROVED` and logs the outcome.  
3. Role 5 accesses the log to verify the decision and ensure compliance.  

--- 

This specification ensures seamless automation, traceability, and feedback for training data quality control.
