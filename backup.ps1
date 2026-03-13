# Enhanced Auto Backup Script for OpenClaw
# Backs up entire state directory, not just workspace
# Run daily at 3:00 AM via Windows Task Scheduler

$ErrorActionPreference = "Continue"
$stateDir = "C:\Users\Administrator\.openclaw-autoclaw"
$workspace = "$stateDir\workspace"
$logFile = "$stateDir\backup.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Log {
    param($msg)
    "[$timestamp] $msg" | Add-Content $logFile
}

Log "========== Backup Started =========="

# 1. Memory flush reminder (write any pending memories)
Log "Step 1: Memory files check..."
$memoryFiles = Get-ChildItem "$workspace\memory" -Filter "*.md" -ErrorAction SilentlyContinue
Log "  Found $($memoryFiles.Count) memory files"

# 2. Git backup (workspace only to GitHub)
Log "Step 2: Git backup to GitHub..."
Set-Location $workspace

$changes = git status --porcelain 2>&1
if ($changes) {
    Log "  Changes detected, committing..."
    git add -A 2>&1 | ForEach-Object { Log "    $_" }
    $commitMsg = "Auto backup $timestamp"
    git commit -m $commitMsg 2>&1 | ForEach-Object { Log "    $_" }
    git push origin master 2>&1 | ForEach-Object { Log "    $_" }
    Log "  Git backup completed!"
} else {
    Log "  No changes to backup"
}

# 3. Full state archive (weekly, keep 7 days)
$dayOfWeek = (Get-Date).DayOfWeek
if ($dayOfWeek -eq "Sunday") {
    Log "Step 3: Weekly full archive..."
    $archiveDir = "C:\Users\Administrator\OpenClaw_Backups"
    $archiveName = "openclaw-full-$(Get-Date -Format 'yyyy-MM-dd').zip"
    
    # Create archive directory if not exists
    if (-not (Test-Path $archiveDir)) {
        New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
    }
    
    # Create zip archive
    Compress-Archive -Path "$stateDir\workspace", "$stateDir\agents", "$stateDir\identity", "$stateDir\openclaw.json" -DestinationPath "$archiveDir\$archiveName" -Force
    
    # Clean old archives (keep 30 days)
    Get-ChildItem $archiveDir -Filter "*.zip" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force
    
    Log "  Archive created: $archiveName"
    
    # Clean old archives
    $oldArchives = Get-ChildItem $archiveDir -Filter "*.zip" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
    if ($oldArchives) {
        $oldArchives | Remove-Item -Force
        Log "  Cleaned $($oldArchives.Count) old archives"
    }
} else {
    Log "Step 3: Skipped (not Sunday)"
}

# 4. Summary
Log "========== Backup Complete =========="
Log ""
