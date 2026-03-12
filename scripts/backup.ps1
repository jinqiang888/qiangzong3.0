# 智能备份脚本
param(
    [string]$commitMsg = "auto backup"
)

Set-Location "C:\Users\Administrator\.openclaw\workspace"

# 检查是否有变更
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to backup"
    exit 0
}

# 提交变更
git add .
git commit -m "$commitMsg"
git push origin master

Write-Host "Backup completed successfully: $commitMsg"
