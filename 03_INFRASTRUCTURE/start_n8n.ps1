# SFV ENGINE - n8n launcher
# Run this in a dedicated PowerShell terminal. Keep the window open.
# All env vars live in n8n_env.ps1 (single source of truth). This script only
# dot-sources that file, then starts n8n so it inherits every var.

. "$PSScriptRoot\n8n_env.ps1"

Write-Host "Starting n8n with SFV env vars (from n8n_env.ps1)..." -ForegroundColor Cyan
Write-Host "  NODES_EXCLUDE                = $env:NODES_EXCLUDE"
Write-Host "  N8N_ENABLE_LOCAL_FILE_NODE   = $env:N8N_ENABLE_LOCAL_FILE_NODE"
Write-Host "  NODE_FUNCTION_ALLOW_BUILTIN  = $env:NODE_FUNCTION_ALLOW_BUILTIN"
Write-Host "  DB_TYPE                      = $env:DB_TYPE"
Write-Host "  OLLAMA_URL                   = $env:OLLAMA_URL"
Write-Host ""
Write-Host "n8n UI: http://127.0.0.1:5678" -ForegroundColor Green
Write-Host "Stop:   Ctrl+C in this window"
Write-Host ""

# Run n8n directly in this shell (not a background job)
# This keeps env vars live and lets you see log output
n8n start
