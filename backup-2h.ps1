# Force backup every 2 hours
# Regardless of whether there are changes

$workspace = "C:\Users\Administrator\.openclaw-autoclaw\workspace"
$logFile = "C:\Users\Administrator\.openclaw-autoclaw\backup.log"

function Log {
    param($msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] $msg" | Add-Content $logFile
}

Set-Location $workspace

# Always check and push
$changes = git status --porcelain 2>&1
if ($changes) {
    git add -A 2>&1 | Out-Null
    $msg = "Scheduled backup (2h) " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    git commit -m $msg 2>&1 | Out-Null
}
git push origin master 2>&1 | Out-Null
Log "[2h] Scheduled cloud backup completed"
