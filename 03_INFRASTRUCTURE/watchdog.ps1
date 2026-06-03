# SFV Engine — Watchdog
# Checks n8n + Ollama every 5 minutes. Auto-restarts if either is down.
# Logs to C:\SFV_BLUEPRINT\00_DEV_LOG\WATCHDOG_LOG.md
# Run in a dedicated PowerShell terminal. Keep window open overnight.

$logFile  = "C:\SFV_BLUEPRINT\00_DEV_LOG\WATCHDOG_LOG.md"
$n8nUrl   = "http://127.0.0.1:5678/healthz"
$ollamaUrl = "http://127.0.0.1:11434"
$intervalSec = 300

function Write-Log($msg) {
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $line = "| $ts | $msg |"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Test-Service($url) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        return $r.StatusCode -eq 200
    } catch { return $false }
}

function Start-N8N {
    $running = Get-Process -Name "node" -ErrorAction SilentlyContinue
    if ($running) { return $false }
    Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\start_n8n.ps1`"" -WindowStyle Normal
    return $true
}

function Start-Ollama {
    $running = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
    if ($running) { return $false }
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Minimized
    return $true
}

# Ensure log file exists with header
if (-not (Test-Path $logFile)) {
    New-Item -ItemType File -Path $logFile -Force | Out-Null
    Set-Content -Path $logFile -Value "| Timestamp | Event |`n|-----------|-------|" -Encoding UTF8
}

Write-Log "WATCHDOG START — interval=${intervalSec}s, n8n=$n8nUrl, ollama=$ollamaUrl"

while ($true) {
    $n8nOk    = Test-Service $n8nUrl
    $ollamaOk = Test-Service $ollamaUrl

    if ($n8nOk -and $ollamaOk) {
        Write-Log "OK — n8n UP, Ollama UP"
    } else {
        if (-not $n8nOk) {
            $restarted = Start-N8N
            Write-Log "ALERT — n8n DOWN — restart attempted: $restarted"
        }
        if (-not $ollamaOk) {
            $restarted = Start-Ollama
            Write-Log "ALERT — Ollama DOWN — restart attempted: $restarted"
        }
    }

    Start-Sleep -Seconds $intervalSec
}
