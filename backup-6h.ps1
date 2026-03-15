# Incremental backup script (every 6 hours)
# Only does git commit + push, no full archive

$workspace = "C:\Users\Administrator\.openclaw-autoclaw\workspace"
$logFile = "C:\Users\Administrator\.openclaw-autoclaw\backup.log"

function Log {
    param($msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] $msg" | Add-Content $logFile
}

Set-Location $workspace
$changes = git status --porcelain 2>&1

if ($changes) {
    Log "[6h] Changes detected, backing up..."
    git add -A 2>&1 | Out-Null
    $msg = "Auto backup (6h) " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    git commit -m $msg 2>&1 | Out-Null
    git push origin master 2>&1 | Out-Null
    Log "[6h] Backup completed"
}
