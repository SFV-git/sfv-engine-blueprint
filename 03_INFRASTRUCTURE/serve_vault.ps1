# SFV Engine — Vault Website Server
# Builds vault from C:\SFV_BLUEPRINT and serves on port 8080.
#
# LOCAL:     http://localhost:8080
# TAILSCALE: http://100.118.181.52:8080
#
# Keep this window open. Ctrl+C to stop.

$quartzDir = "C:\SFV_QUARTZ"
$vaultDir  = "C:\SFV_BLUEPRINT"

Write-Host ""
Write-Host "=== SFV VAULT SERVER ===" -ForegroundColor White
Write-Host ""
Write-Host "Building..." -ForegroundColor Cyan
Set-Location $quartzDir
& npx quartz build --directory $vaultDir

Write-Host ""
Write-Host "  Local:     http://localhost:8080" -ForegroundColor Green
Write-Host "  Tailscale: http://100.118.181.52:8080" -ForegroundColor Green
Write-Host ""
Write-Host "Serving. Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

python C:\SFV_QUARTZ\serve.py
