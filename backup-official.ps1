# Enhanced backup using official openclaw backup command
# Combines git push + official backup archive

$ErrorActionPreference = "Continue"
$stateDir = "C:\Users\Administrator\.openclaw-autoclaw"
$workspace = "$stateDir\workspace"
$logFile = "$stateDir\backup.log"
$backupDir = "C:\Users\Administrator\OpenClaw_Backups"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Log {
    param($msg)
    "[$timestamp] $msg" | Add-Content $logFile
}

Log "========== Backup Started =========="

# 1. Git backup (workspace to GitHub)
Log "[1/3] Git backup to GitHub..."
Set-Location $workspace
$changes = git status --porcelain 2>&1
if ($changes) {
    git add -A 2>&1 | Out-Null
    $msg = "Auto backup $timestamp"
    git commit -m $msg 2>&1 | Out-Null
    git push origin master 2>&1 | Out-Null
    Log "  Git backup completed"
} else {
    Log "  No changes to backup"
}

# 2. Official openclaw backup (full state)
Log "[2/3] Official backup archive..."
$archiveName = "openclaw-backup-$(Get-Date -Format 'yyyy-MM-dd-HHmm').tar.gz"
$archivePath = "$backupDir\$archiveName"

# Create backup dir if needed
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

# Use official backup command
$env:OPENCLAW_STATE_DIR = $stateDir
openclaw backup create --output $backupDir --verify 2>&1 | ForEach-Object { Log "  $_" }

# 3. Cleanup old archives (keep 30 days)
Log "[3/3] Cleanup old archives..."
$oldArchives = Get-ChildItem $backupDir -Filter "*.tar.gz" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
if ($oldArchives) {
    $oldArchives | Remove-Item -Force
    Log "  Removed $($oldArchives.Count) old archives"
}

Log "========== Backup Complete =========="
Log ""
