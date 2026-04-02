#!/bin/bash
# 简单版备份脚本 - 使用git命令直接操作

REPO_URL="git@github.com:YOUR_USERNAME/openclaw-config-backup.git"
REPO_DIR="$HOME/.openclaw/backup-repo"
WORKSPACE="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"

echo "[$(date)] 开始备份..."

# 检查是否已初始化仓库
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "初始化备份仓库..."
    mkdir -p "$REPO_DIR"
    cd "$REPO_DIR"
    git init
    git remote add origin "$REPO_URL"
    echo "请先手动运行: cd '$REPO_DIR' && git pull origin main"
    exit 1
fi

cd "$REPO_DIR"
echo "拉取最新..."
git pull origin main 2>/dev/null || echo "(首次运行，忽略pull失败)"

# 清理旧文件
echo "清理旧文件..."
rm -rf config workspace agents

# 复制新文件
echo "复制配置文件..."
mkdir -p config
cp "$OPENCLAW_DIR/openclaw.json" config/ 2>/dev/null

echo "复制workspace文件..."
mkdir -p workspace
cp "$WORKSPACE/SOUL.md" workspace/ 2>/dev/null
cp "$WORKSPACE/IDENTITY.md" workspace/ 2>/dev/null
cp "$WORKSPACE/USER.md" workspace/ 2>/dev/null
cp "$WORKSPACE/AGENTS.md" workspace/ 2>/dev/null
cp "$WORKSPACE/TOOLS.md" workspace/ 2>/dev/null

if [ -d "$WORKSPACE/skills" ]; then
    echo "复制skills目录..."
    cp -r "$WORKSPACE/skills" workspace/
fi

echo "复制agents目录..."
if [ -d "$OPENCLAW_DIR/agents" ]; then
    cp -r "$OPENCLAW_DIR/agents" .
fi

# 提交并推送
echo "提交更改..."
git add -A
git commit -m "配置备份 - $(date)" 2>/dev/null || echo "(没有更改需要提交)"
git push origin main

echo "[$(date)] 备份完成！"
