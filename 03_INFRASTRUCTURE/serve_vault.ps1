# SFV Engine — Vault Website Server
# Builds vault from C:\SFV_BLUEPRINT and serves on port 8080.
#
# LOCAL:     http://localhost:8080
# TAILSCALE: http://100.118.181.52:8080  (Engine Body Tailscale IP)
#
# Run this before you leave. Keep the window open. Access from phone/laptop via Tailscale.
# To rebuild after vault changes: Ctrl+C, run this script again.

$quartzDir = "C:\SFV_QUARTZ"
$vaultDir  = "C:\SFV_BLUEPRINT"
$publicDir = "C:\SFV_QUARTZ\public"
$port      = 8080

Write-Host ""
Write-Host "=== SFV VAULT SERVER ===" -ForegroundColor White
Write-Host ""
Write-Host "Building..." -ForegroundColor Cyan
Set-Location $quartzDir
& npx quartz build --directory $vaultDir

Write-Host ""
Write-Host "BUILD COMPLETE" -ForegroundColor Green
Write-Host ""
Write-Host "  Local:     http://localhost:$port" -ForegroundColor White
Write-Host "  Tailscale: http://100.118.181.52:$port" -ForegroundColor White
Write-Host ""
Write-Host "Serving. Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

python -m http.server $port --directory $publicDir
