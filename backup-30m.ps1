# Check and backup if there are changes
# Runs every 30 minutes

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
    Log "[30m] Changes detected, backing up to cloud..."
    git add -A 2>&1 | Out-Null
    $msg = "Auto backup " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    git commit -m $msg 2>&1 | Out-Null
    git push origin master 2>&1 | Out-Null
    Log "[30m] Cloud backup completed"
}
