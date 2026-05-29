# Start n8n with required env vars for SFV_BLUEPRINT workflows.
# NODES_EXCLUDE=[] re-enables localFileTrigger (disabled by default in n8n v2).
# 127.0.0.1 avoids Node.js resolving localhost to ::1 (IPv6) on Windows.

$env:NODES_EXCLUDE = "[]"
$env:OLLAMA_URL    = "http://127.0.0.1:11434"
$env:OLLAMA_MODEL  = "qwen3:14b"

n8n start
