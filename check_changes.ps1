$todayDate = Get-Date
$hasChanges = 0
$changedFiles = @()

$files = @(
    'C:\Users\Administrator\.openclaw\openclaw.json',
    'C:\Users\Administrator\.openclaw\workspace\SOUL.md',
    'C:\Users\Administrator\.openclaw\workspace\IDENTITY.md'
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $lastWrite = (Get-Item $file).LastWriteTime
        $daysDiff = ($todayDate - $lastWrite).Days
        if ($daysDiff -lt 1) {
            $hasChanges = 1
            $changedFiles += "$file | Modified: $lastWrite"
        }
    }
}

$agentsDir = 'C:\Users\Administrator\.openclaw\workspace\agents'
if (Test-Path $agentsDir) {
    Get-ChildItem -Path $agentsDir -Filter '*.json' -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        $daysDiff = ($todayDate - $_.LastWriteTime).Days
        if ($daysDiff -lt 1) {
            $hasChanges = 1
            $changedFiles += "$($_.FullName) | Modified: $($_.LastWriteTime)"
        }
    }
}

Write-Host "HAS_CHANGES=$hasChanges"
if ($hasChanges -eq 1) {
    Write-Host "Changed files found today:"
    foreach ($item in $changedFiles) {
        Write-Host $item
    }
} else {
    Write-Host "No configuration changes today"
}
