# SFV Engine — n8n environment config TEMPLATE
# Copy this to n8n_env.ps1, fill in real values, then run: . .\n8n_env.ps1
# n8n_env.ps1 is gitignored — never commit the live file.

$env:OLLAMA_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "qwen3:14b"
$env:OLLAMA_MODEL_FAST = "qwen3:14b"
$env:VAULT_PATH = "C:\SFV_BLUEPRINT"
$env:ACTIVE_STORAGE = "D:\SFV_ACTIVE"
$env:FIELD_INGEST_PATH = "E:\"
$env:TAVILY_API_KEY = "tvly-FILL_IN_BEFORE_USE"
$env:PERPLEXITY_API_KEY = "NOT_USED — Perplexity via web only, API billed separately from Pro"
$env:DECISION_LOG = "C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md"
$env:QUEUE_PATH = "C:\SFV_BLUEPRINT\99_INBOX\QUEUE"
$env:OUTPUTS_PATH = "C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS"
$env:HANDOFFS_PATH = "C:\SFV_BLUEPRINT\99_INBOX\HANDOFFS"

# Allow n8n Code nodes to use Node.js built-in fs module
# Required by Workflow 4 (Output Monitor) Code nodes
$env:NODE_FUNCTION_ALLOW_BUILTIN = "fs,path"

# Start n8n after vars are set
# npx n8n
