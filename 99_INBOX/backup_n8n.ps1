# SFV Engine — n8n SQLite Backup
# Copies .n8n SQLite DB to D:\SFV_ACTIVE\BACKUPS\n8n\ daily.
# Run via Windows Task Scheduler — independent of n8n (survives n8n crash).
# After PostgreSQL migration: replace with pg_dump command (see POSTGRES_MIGRATION.md).
#
# Task Scheduler setup:
#   Action: powershell.exe -NonInteractive -File "C:\SFV_BLUEPRINT\99_INBOX\backup_n8n.ps1"
#   Trigger: Daily 03:00
#   Run whether user logged on or not

$source    = "$env:USERPROFILE\.n8n\database.sqlite"
$backupDir = "D:\SFV_ACTIVE\BACKUPS\n8n"
$retention = 7
$logFile   = "C:\SFV_BLUEPRINT\00_DEV_LOG\WATCHDOG_LOG.md"

function Write-Log($msg) {
    $ts   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $line = "| $ts | $msg |"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

if (-not (Test-Path $source)) {
    Write-Log "N8N_BACKUP FAILED -- source not found: $source"
    exit 1
}

$stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$dest  = "$backupDir\n8n_sqlite_$stamp.sqlite"
try {
    Copy-Item -Path $source -Destination $dest -ErrorAction Stop
    $sizeMB = [math]::Round((Get-Item $dest).Length / 1MB, 2)
    Write-Log "N8N_BACKUP OK -- $dest ($sizeMB MB)"
} catch {
    Write-Log "N8N_BACKUP FAILED -- $_"
    exit 1
}

Get-ChildItem -Path $backupDir -Filter "*.sqlite" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$retention) } |
    ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Log "N8N_BACKUP PRUNED -- $($_.Name)"
    }
