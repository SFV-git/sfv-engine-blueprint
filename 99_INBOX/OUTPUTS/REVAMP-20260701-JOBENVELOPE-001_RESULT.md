# RESULT -- REVAMP-20260701-JOBENVELOPE-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 15:21:42

---

# Job Envelope Specification for SFV Engine

This document defines the standardized structure and lifecycle of a "job envelope" used across the SFV Engine's Hermes loop and n8n execution pipeline.

---

## 1. Core Fields in a Job Envelope

Every job envelope contains the following fields:

| Field                  | Type             | Description                                                                 |
|-----------------------|------------------|-----------------------------------------------------------------------------|
| `id`                  | string           | Unique identifier for the job (e.g., `DIRECTIVE_ID`)                       |
| `type`                | enum             | Task type: `"mechanical"` (e.g., Ollama) or `"judgment"` (e.g., Claude)   |
| `executor`            | string           | Executor service name (e.g., `"ollama"`, `"claude"`, `"hermes"`)          |
| `priority`            | integer (1-5)    | Task priority (1=lowest, 5=highest)                                        |
| `status`              | enum             | Lifecycle state: `"pending"`, `"active"`, `"complete"`, `"error"`, `"reviewed"`, `"ratified"` |
| `created_at`          | datetime         | ISO 8601 timestamp of job creation                                         |
| `source`              | string           | Originating system or user ID                                              |
| `payload/body`        | string/object    | Input data for the task (e.g., prompt, document, query)                   |
| `output_target`       | string           | File path or endpoint for storing results (e.g., `{DIRECTIVE_ID}_RESULT.md`) |
| `confidence`          | float (0.0-1.0)  | Confidence score for judgment tasks (optional)                             |
| `review_required_by`  | datetime         | Deadline for review (if `review_required` is true)                         |
| `canon_approval_required_by` | datetime | Deadline for canon approval (if required)                                |

---

## 2. Field Definitions and Allowed Values

- **`id`**: Must match the `DIRECTIVE_ID` in Hermes frontmatter (e.g., `"directive_1234"`).
- **`type`**: `"mechanical"` for deterministic tasks (e.g., text generation), `"judgment"` for analytical tasks (e.g., classification).
- **`executor`**: Must be a registered executor in the system (e.g., `"ollama"`, `"claude"`, `"hermes"`).
- **`priority`**: Integer 1-5; higher values are processed first.
- **`status`**: Reflects the job's lifecycle state (see Section 3).
- **`created_at`**: Must be in ISO 8601 format (e.g., `"2024-03-20T14:23:00Z"`).
- **`source`**: Typically a user ID, system name, or task origin (e.g., `"user_456"`, `"importer_v2"`).
- **`payload/body`**: For mechanical tasks, this is the input prompt or data. For judgment tasks, this includes the query and context.
- **`output_target`**: File path follows `{DIRECTIVE_ID}_RESULT.md` format, or an API endpoint.
- **`confidence`**: Optional for judgment tasks; ranges from 0.0 (no confidence) to 1.0 (certain).
- **`review_required_by`**: Only set if `review_required` is true; must be a future timestamp.
- **`canon_approval_required_by`**: Only set if canon approval is required; must be a future timestamp.

---

## 3. Job Lifecycle States

Jobs progress through these states:

1. **Pending**: Created but not yet assigned to an executor.
2. **Active**: Executor has started processing the task.
3. **Complete/Errored**: Task has finished successfully or failed.
4. **Reviewed**: Judgment task has been reviewed by a human or system.
5. **Ratified**: Final approval given (e.g., canon approval).

**Transitions**:
- `pending` → `active` (executor assigned)
- `active` → `complete`/`error` (task finishes)
- `complete` → `reviewed` (if review is required)
- `reviewed` → `ratified` (approval granted)

---

## 4. Example Job Envelopes

### Example 1: Ollama Mechanical Task (Text Generation)

```yaml
---
id: "directive_7890"
type: "mechanical"
executor: "ollama"
priority: 5
status: "active"
created_at: "2024-03-20T14:23:00Z"
source: "user_456"
payload: "Generate a 500-word article about quantum computing."
output_target: "directive_7890_RESULT.md"
confidence: 0.0
review_required_by: null
canon_approval_required_by: null
---
```

### Example 2: Claude Judgment Task (Classification)

```yaml
---
id: "directive_1122"
type: "judgment"
executor: "claude"
priority: 3
status: "pending"
created_at: "2024-03-20T10:15:00Z"
source: "importer_v2"
payload: 
  query: "Is this document compliant with GDPR?"
  context: "Document contains user email addresses and IP logs."
output_target: "directive_1122_RESULT.md"
confidence: 0.85
review_required_by: "2024-03-21T17:00:00Z"
canon_approval_required_by: "2024-03-22T12:00:00Z"
---
```

---

## 5. Mapping to Hermes Directive Frontmatter

The Hermes directive frontmatter maps directly to the job envelope:

| Hermes Field         | Job Envelope Field     | Description                                  |
|----------------------|------------------------|----------------------------------------------|
| `STATUS`             | `status`               | Current lifecycle state                      |
| `DIRECTIVE_ID`       | `id`                   | Unique job identifier                        |
| `EXECUTOR`           | `executor`             | Target executor service                      |
| `BODY`               | `payload/body`         | Input data for the task                      |

The Hermes loop uses the `DIRECTIVE_ID` to write results to `{DIRECTIVE_ID}_RESULT.md` and logs a row to `DECISION_LOG.md` upon completion.

--- 

This specification ensures consistency across task execution, logging, and approval workflows in the SFV Engine.
