# SFV ENGINE — n8n launcher
# Run this in a dedicated PowerShell terminal. Keep the window open.
# NODES_EXCLUDE=[]            → re-enables localFileTrigger (disabled by default in n8n v2)
# NODE_FUNCTION_ALLOW_BUILTIN → allows require('fs') and require('path') in Code nodes
# 127.0.0.1                  → avoids Node.js resolving localhost to ::1 (IPv6) on Windows

$env:NODES_EXCLUDE                = "[]"
$env:N8N_ENABLE_LOCAL_FILE_NODE   = "true"  # Belt-and-suspenders for future n8n upgrades
$env:OLLAMA_URL                   = "http://127.0.0.1:11434"
$env:OLLAMA_MODEL                 = "qwen3:14b"
$env:NODE_FUNCTION_ALLOW_BUILTIN  = "fs,path,os"
$env:NODE_FUNCTION_ALLOW_EXTERNAL = "*"
$env:N8N_LOG_LEVEL                = "info"

Write-Host "Starting n8n with SFV env vars..." -ForegroundColor Cyan
Write-Host "  NODES_EXCLUDE               = $env:NODES_EXCLUDE"
Write-Host "  NODE_FUNCTION_ALLOW_BUILTIN = $env:NODE_FUNCTION_ALLOW_BUILTIN"
Write-Host "  OLLAMA_URL                  = $env:OLLAMA_URL"
Write-Host ""
Write-Host "n8n UI: http://127.0.0.1:5678" -ForegroundColor Green
Write-Host "Stop:   Ctrl+C in this window"
Write-Host ""

# Run n8n directly in this shell (not a background job)
# This keeps env vars live and lets you see log output
n8n start
