# SFV Engine — n8n environment config
# Run this before starting n8n: . .\n8n_env.ps1
# Never hardcode these values in any n8n workflow node

$env:OLLAMA_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "qwen3:14b"
$env:OLLAMA_MODEL_FAST = "qwen3:14b"
$env:VAULT_PATH = "C:\SFV_BLUEPRINT"
$env:ACTIVE_STORAGE = "D:\SFV_ACTIVE"
$env:FIELD_INGEST_PATH = "E:\"
$env:TAVILY_API_KEY = "tvly-FILL_IN_BEFORE_USE"
$env:PERPLEXITY_API_KEY = "pplx-FILL_IN_BEFORE_USE"
$env:DECISION_LOG = "C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md"
$env:QUEUE_PATH = "C:\SFV_BLUEPRINT\99_INBOX\QUEUE"
$env:OUTPUTS_PATH = "C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS"
$env:HANDOFFS_PATH = "C:\SFV_BLUEPRINT\99_INBOX\HANDOFFS"

# Start n8n after vars are set
# npx n8n
