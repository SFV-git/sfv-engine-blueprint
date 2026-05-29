# Start n8n with required env vars for SFV_BLUEPRINT workflows.
# NODES_EXCLUDE=[] re-enables localFileTrigger (disabled by default in n8n v2).
# 127.0.0.1 avoids Node.js resolving localhost to ::1 (IPv6) on Windows.

$env:NODES_EXCLUDE = "[]"
$env:OLLAMA_URL    = "http://127.0.0.1:11434"
$env:OLLAMA_MODEL  = "qwen3:14b"

# Start n8n in background so we can activate workflows after it's ready
$logFile = "$env:TEMP\n8n.log"
$job = Start-Job -ScriptBlock {
    $env:NODES_EXCLUDE = "[]"
    $env:OLLAMA_URL    = "http://127.0.0.1:11434"
    $env:OLLAMA_MODEL  = "qwen3:14b"
    n8n start *> $using:logFile
}

# Wait up to 60s for n8n to respond
$ready = $false
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep 3
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
}

if (-not $ready) { exit 1 }

# Read API key from Claude Code settings
$settings = Get-Content "$env:USERPROFILE\.claude\settings.json" -Raw | ConvertFrom-Json
$apiKey   = $settings.env.N8N_API_KEY

# Activate workflow1 (queue processor)
$headers = @{ "X-N8N-API-KEY" = $apiKey; "Content-Type" = "application/json" }
try {
    Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/FwTeEPL7w5vlPwO7/activate" `
        -Method Post -Headers $headers -ErrorAction Stop | Out-Null
} catch {}

# Keep job alive so n8n keeps running
Wait-Job $job
