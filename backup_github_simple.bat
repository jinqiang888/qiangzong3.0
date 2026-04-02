@echo off
REM 简单版备份脚本 - 使用git命令直接操作
setlocal

set REPO_URL=git@github.com:YOUR_USERNAME/openclaw-config-backup.git
set REPO_DIR=%USERPROFILE%\.openclaw\backup-repo
set WORKSPACE=%USERPROFILE%\.openclaw\workspace
set OPENCLAW_DIR=%USERPROFILE%\.openclaw

echo [%DATE% %TIME%] 开始备份...

REM 检查是否已初始化仓库
if not exist "%REPO_DIR%\.git" (
    echo 初始化备份仓库...
    mkdir "%REPO_DIR%" 2>nul
    cd /d "%REPO_DIR%"
    git init
    git remote add origin %REPO_URL%
    echo 请先手动运行: cd "%REPO_DIR%" ^&^& git pull origin main
    exit /b 1
)

cd /d "%REPO_DIR%"
echo 拉取最新...
git pull origin main 2>nul || echo (首次运行，忽略pull失败)

REM 清理旧文件
echo 清理旧文件...
if exist "config" rmdir /s /q "config"
if exist "workspace" rmdir /s /q "workspace"
if exist "agents" rmdir /s /q "agents"

REM 复制新文件
echo 复制配置文件...
mkdir "config" 2>nul
copy /Y "%OPENCLAW_DIR%\openclaw.json" "config\" 2>nul

echo 复制workspace文件...
mkdir "workspace" 2>nul
copy /Y "%WORKSPACE%\SOUL.md" "workspace\" 2>nul
copy /Y "%WORKSPACE%\IDENTITY.md" "workspace\" 2>nul
copy /Y "%WORKSPACE%\USER.md" "workspace\" 2>nul
copy /Y "%WORKSPACE%\AGENTS.md" "workspace\" 2>nul
copy /Y "%WORKSPACE%\TOOLS.md" "workspace\" 2>nul

if exist "%WORKSPACE%\skills" (
    echo 复制skills目录...
    xcopy "%WORKSPACE%\skills" "workspace\skills\" /E /I /Y
)

echo 复制agents目录...
if exist "%OPENCLAW_DIR%\agents" (
    xcopy "%OPENCLAW_DIR%\agents" "agents\" /E /I /Y
)

REM 提交并推送
echo 提交更改...
git add -A
git commit -m "配置备份 - %DATE% %TIME%" 2>nul || echo (没有更改需要提交)
git push origin main

echo [%DATE% %TIME%] 备份完成！
end