$today = (Get-Date).Date
$hasChanges = $false

Write-Host "=== 检查今天的配置文件变更 ===" -ForegroundColor Cyan
Write-Host "Date: $($today.ToString('yyyy-MM-dd'))`n" -ForegroundColor Gray

# Check core config files
$coreFiles = @("openclaw.json", "SOUL.md", "IDENTITY.md", "USER.md", "AGENTS.md", "MEMORY.md")

foreach ($file in $coreFiles) {
    if ($file -eq "openclaw.json") {
        $path = "$env:USERPROFILE\.openclaw\openclaw.json"
    } elseif ($file -eq "MEMORY.md") {
        $path = "$env:USERPROFILE\.openclaw\workspace\MEMORY.md"
    } else {
        $path = "$env:USERPROFILE\.openclaw\workspace\$file"
    }

    if (Test-Path $path) {
        $lastMod = (Get-Item $path).LastWriteTime
        if ($lastMod.Date -eq $today) {
            Write-Host "  [$($lastMod.ToString('HH:mm:ss'))] $file" -ForegroundColor Green
            $hasChanges = $true
        }
    }
}

# Check agents directory
$agentsDir = "$env:USERPROFILE\.openclaw\agents"
if (Test-Path $agentsDir) {
    $agentFiles = Get-ChildItem $agentsDir -Filter "*.json" -Recurse -ErrorAction SilentlyContinue
    foreach ($af in $agentFiles) {
        if ($af.LastWriteTime.Date -eq $today) {
            $relPath = $af.FullName.Replace("$agentsDir\", "")
            Write-Host "  [$($af.LastWriteTime.ToString('HH:mm:ss'))] agents\$relPath" -ForegroundColor Green
            $hasChanges = $true
        }
    }
}

# Check skills directory
$skillsDir = "$env:USERPROFILE\.openclaw\skills"
if (Test-Path $skillsDir) {
    $skillFiles = Get-ChildItem $skillsDir -Recurse -File -ErrorAction SilentlyContinue
    foreach ($sf in $skillFiles) {
        if ($sf.LastWriteTime.Date -eq $today) {
            Write-Host "  [$($sf.LastWriteTime.ToString('HH:mm:ss'))] skills\$($sf.Name)" -ForegroundColor Green
            $hasChanges = $true
            break
        }
    }
}

Write-Host ""

if ($hasChanges) {
    Write-Host "[OK] Config changes detected today, running full backup..." -ForegroundColor Yellow
    python backup_github.py
} else {
    Write-Host "[OK] No config changes today, skipping backup" -ForegroundColor Gray
}
