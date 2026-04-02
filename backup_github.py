#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw配置自动备份脚本
备份核心配置文件到GitHub仓库
"""

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# 配置
REPO_URL = "git@github.com:YOUR_USERNAME/openclaw-config-backup.git"  # 请修改为你的GitHub仓库
REPO_DIR = Path.home() / ".openclaw" / "backup-repo"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_DIR = Path.home() / ".openclaw"

# 需要备份的文件/目录列表
BACKUP_ITEMS = [
    # 核心配置
    (OPENCLAW_DIR / "openclaw.json", "config/openclaw.json"),
    (OPENCLAW_DIR / ".ssh", "config/.ssh"),

    # Workspace核心文件
    (WORKSPACE / "SOUL.md", "workspace/SOUL.md"),
    (WORKSPACE / "IDENTITY.md", "workspace/IDENTITY.md"),
    (WORKSPACE / "USER.md", "workspace/USER.md"),
    (WORKSPACE / "AGENTS.md", "workspace/AGENTS.md"),
    (WORKSPACE / "TOOLS.md", "workspace/TOOLS.md"),

    # Skills (workspace本地技能)
    (WORKSPACE / "skills", "workspace/skills"),

    # Agents配置
    (OPENCLAW_DIR / "agents", "agents"),
]

def log(msg):
    """输出日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_cmd(cmd, cwd=None, check=True):
    """执行命令"""
    log(f"执行: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=isinstance(cmd, str)
    )
    if check and result.returncode != 0:
        log(f"命令失败: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    return result

def init_repo():
    """初始化Git仓库"""
    log("初始化备份仓库...")
    REPO_DIR.mkdir(parents=True, exist_ok=True)

    if not (REPO_DIR / ".git").exists():
        log("克隆仓库...")
        run_cmd(f"git clone {REPO_URL} {REPO_DIR}")
    else:
        log("仓库已存在，拉取最新...")
        run_cmd(["git", "fetch", "origin"], cwd=REPO_DIR)
        run_cmd(["git", "checkout", "main"], cwd=REPO_DIR)
        run_cmd(["git", "pull", "origin", "main"], cwd=REPO_DIR)

def copy_file_or_dir(src, dst):
    """复制文件或目录"""
    if not src.exists():
        log(f"跳过不存在的源: {src}")
        return

    dst_parent = dst.parent
    dst_parent.mkdir(parents=True, exist_ok=True)

    if src.is_file():
        log(f"复制文件: {src} -> {dst}")
        shutil.copy2(src, dst)
    elif src.is_dir():
        log(f"复制目录: {src} -> {dst}")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

def backup():
    """执行备份"""
    log("开始备份...")

    # 1. 初始化仓库
    init_repo()

    # 2. 清理旧文件
    log("清理旧备份文件...")
    for item in BACKUP_ITEMS:
        dst = REPO_DIR / item[1]
        if dst.exists():
            if dst.is_file():
                dst.unlink()
            elif dst.is_dir():
                shutil.rmtree(dst)

    # 3. 复制新文件
    log("复制新文件...")
    for src, dst in BACKUP_ITEMS:
        copy_file_or_dir(src, REPO_DIR / dst)

    # 4. 提交并推送
    log("提交更改...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"配置备份 - {timestamp}"

    try:
        run_cmd(["git", "add", "-A"], cwd=REPO_DIR, check=False)
        run_cmd(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=False)
        run_cmd(["git", "push", "origin", "main"], cwd=REPO_DIR)
        log("✅ 备份成功！")
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in str(e.stdout + e.stderr):
            log("ℹ️  没有需要提交的更改")
        else:
            log(f"⚠️  Git操作失败: {e}")
            raise

def main():
    try:
        backup()
    except Exception as e:
        log(f"❌ 备份失败: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
