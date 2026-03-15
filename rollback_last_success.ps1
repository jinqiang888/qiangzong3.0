# 一键回滚到GitHub最新成功备份 (Windows PowerShell)
Write-Host "🔙 一键回滚到GitHub最新成功备份..." -ForegroundColor Cyan

# 进入工作目录
cd C:\Users\Administrator\.openclaw\workspace

# 拉取最新备份
Write-Host "📥 拉取GitHub最新备份..." -ForegroundColor Yellow
git pull origin master

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 拉取失败，请检查网络" -ForegroundColor Red
    pause
    exit 1
}

# 恢复Agent配置
Write-Host "♻️  恢复Agent配置..." -ForegroundColor Yellow
xcopy .openclaw-backup\agents\* C:\Users\Administrator\.openclaw\agents\ /E /Y /I

# 恢复所有工作空间
Write-Host "♻️  恢复工作空间..." -ForegroundColor Yellow
if (Test-Path ".openclaw-backup\workspace-qiangcehua") {
    xcopy .openclaw-backup\workspace-qiangcehua\* C:\Users\Administrator\.openclaw\workspace-qiangcehua\ /E /Y /I
    Write-Host "✅ 已恢复强策划工作空间" -ForegroundColor Green
}

# 重启网关
Write-Host "🔄 重启OpenClaw网关..." -ForegroundColor Yellow
openclaw gateway restart

Write-Host "✅ 回滚完成！网关正在重启，请稍等10秒后测试。" -ForegroundColor Green
pause
