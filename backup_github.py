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
REPO_URL = "git@github.com:jinqiang888/qiangzong3.0.git"  # GitHub备份仓库
REPO_DIR = Path.home() / ".openclaw" / "backup-repo-git"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_DIR = Path.home() / ".openclaw"

# 需要备份的文件/目录列表
BACKUP_ITEMS = [
    # 核心配置
    (OPENCLAW_DIR / "openclaw.json", "config/openclaw.json"),
    # (OPENCLAW_DIR / ".ssh", "config/.ssh"),  # 不备份SSH密钥

    # Workspace核心文件
    (WORKSPACE / "SOUL.md", "workspace/SOUL.md"),
    (WORKSPACE / "IDENTITY.md", "workspace/IDENTITY.md"),
    (WORKSPACE / "USER.md", "workspace/USER.md"),
    (WORKSPACE / "AGENTS.md", "workspace/AGENTS.md"),
    (WORKSPACE / "TOOLS.md", "workspace/TOOLS.md"),
    (WORKSPACE / "MEMORY.md", "workspace/MEMORY.md"),

    # Skills (workspace本地技能)
    (WORKSPACE / "skills", "workspace/skills"),

    # Agents配置（排除sessions，包含密钥）
    # (OPENCLAW_DIR / "agents", "agents"),  # 不备份agents目录，包含敏感信息
]

def log(msg):
    """输出日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(f"[{timestamp}] {msg}")
    except UnicodeEncodeError:
        # Windows GBK 编码问题，替换为ASCII字符
        msg = msg.replace("✅", "[OK]").replace("❌", "[FAIL]").replace("ℹ️", "[INFO]").replace("⚠️", "[WARN]")
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
    # 确保 stdout 和 stderr 是字符串
    result.stdout = result.stdout or ""
    result.stderr = result.stderr or ""
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
        run_cmd(["git", "checkout", "master"], cwd=REPO_DIR)
        run_cmd(["git", "pull", "origin", "master"], cwd=REPO_DIR)

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
        # 递归复制，排除 .git 目录
        # 使用 dirs_exist_ok=True 覆盖已存在的目录（Python 3.8+）
        ignore_patterns = shutil.ignore_patterns('.git')
        shutil.copytree(src, dst, ignore=ignore_patterns, dirs_exist_ok=True)

def backup():
    """执行备份"""
    log("开始备份...")

    # 1. 初始化仓库
    init_repo()

    # 2. 清理旧文件
    log("清理旧备份文件...")
    # 使用 git clean 清理，避免文件锁定问题
    try:
        run_cmd(["git", "clean", "-fdx"], cwd=REPO_DIR, check=False)
        # Git reset 清理已删除的文件
        run_cmd(["git", "reset", "--hard", "HEAD"], cwd=REPO_DIR)
    except subprocess.CalledProcessError as e:
        log(f"Git清理失败（可能首次运行），继续: {e.stderr[:100]}")

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
        run_cmd(["git", "push", "origin", "master"], cwd=REPO_DIR)
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
