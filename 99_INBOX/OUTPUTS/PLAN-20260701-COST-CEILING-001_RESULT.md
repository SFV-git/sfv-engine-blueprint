# RESULT -- PLAN-20260701-COST-CEILING-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:56:19

---

```markdown
# Cost Ceiling Policy for AI Automation Stack

## 1. **Metered API Usage Soft-Cap**
- **Monthly Soft-Cap**: $50 USD (subject to adjustment quarterly based on project scope).
- **Alert Threshold**: 75% of soft-cap ($37.50) triggers a non-disruptive alert (email/in-app notification) to review usage.
- **No Auto-Shutoff**: Exceeding the soft-cap does not interrupt workflows but requires manual intervention to address.

## 2. **Metered API Usage Policy**
- **Allowed APIs**: Direct calls to Anthropic (non-CLI) and OpenAI (non-CLI) APIs are permitted only for tasks not covered by Claude Code CLI or Codex CLI.
- **Usage Tracking**: All metered API calls must be logged in the format below.
- **Preferred Tools**: Prioritize local Ollama, Claude Code CLI, and Codex CLI to avoid metered usage.

## 3. **Usage Logging Format**
Logs must be maintained in a plain-text or CSV file with the following fields:
```
date,task,executor,estimated_cost
2023-10-05,generate_code,Codex CLI,0.00
2023-10-05,analyze_data,Anthropic API,12.34
```
- **Date**: ISO 8601 format (YYYY-MM-DD).
- **Task**: Brief description of the task (e.g., "generate_code", "analyze_data").
- **Executor**: Tool/API used (e.g., "Codex CLI", "Anthropic API").
- **Estimated Cost**: Approximate USD cost of the API call (rounded to two decimal places).

## 4. **Review and Compliance**
- **Monthly Review**: Audit logs to ensure adherence to the soft-cap and identify optimization opportunities.
- **Cost Optimization**: Reallocate tasks to non-metered tools if usage exceeds $25/month.
- **Exceptions**: Any intentional exceedance of the soft-cap must be documented with a justification and approved by the studio owner.
```
