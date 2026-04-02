#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw配置本地自动备份脚本
备份核心配置文件到本地目录（带时间戳）
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

# 配置
BACKUP_ROOT = Path.home() / ".openclaw" / "backups"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OPENCLAW_DIR = Path.home() / ".openclaw"

# 需要备份的文件/目录列表
BACKUP_ITEMS = [
    # 核心配置
    OPENCLAW_DIR / "openclaw.json",
    # OPENCLAW_DIR / ".ssh",  # SSH密钥通常不备份，如果需要请取消注释

    # Workspace核心文件
    WORKSPACE / "SOUL.md",
    WORKSPACE / "IDENTITY.md",
    WORKSPACE / "USER.md",
    WORKSPACE / "AGENTS.md",
    WORKSPACE / "TOOLS.md",

    # Skills (workspace本地技能)
    WORKSPACE / "skills",

    # Agents配置
    OPENCLAW_DIR / "agents",
]

def log(msg):
    """输出日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(f"[{timestamp}] {msg}")
    except:
        print(f"[{timestamp}] {msg.encode('utf-8', errors='ignore').decode('utf-8')}")

def copy_file_or_dir(src, dst, timestamp):
    """复制文件或目录"""
    if not src.exists():
        log(f"跳过不存在的源: {src}")
        return

    dst_parent = dst.parent
    dst_parent.mkdir(parents=True, exist_ok=True)

    if src.is_file():
        log(f"复制文件: {src.name}")
        shutil.copy2(src, dst)
    elif src.is_dir():
        log(f"复制目录: {src.name}")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git', '__pycache__'))

def backup():
    """执行备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / timestamp

    log("开始备份...")
    log(f"备份目录: {backup_dir}")

    # 创建备份目录
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 复制文件
    for src_path in BACKUP_ITEMS:
        relative_path = src_path.relative_to(Path.home())
        dst_path = backup_dir / relative_path
        copy_file_or_dir(src_path, dst_path, timestamp)

    # 创建ZIP压缩包
    zip_path = BACKUP_ROOT / f"openclaw_backup_{timestamp}.zip"
    log(f"创建压缩包: {zip_path.name}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(backup_dir)
                zipf.write(file_path, arcname)

    log(f"备份完成! 备份大小: {zip_path.stat().st_size / 1024:.2f} KB")
    log(f"备份路径: {zip_path}")

    # 清理旧备份（保留最近10个）
    cleanup_old_backups()

    return str(zip_path)

def cleanup_old_backups():
    """清理旧备份，保留最近10个"""
    zip_files = sorted(BACKUP_ROOT.glob("openclaw_backup_*.zip"), reverse=True)

    if len(zip_files) > 10:
        old_files = zip_files[10:]
        log(f"清理旧备份（保留最近10个，删除 {len(old_files)} 个）...")

        for old_file in old_files:
            # 删除ZIP文件
            old_file.unlink()

            # 删除对应的目录
            timestamp = old_file.stem.replace("openclaw_backup_", "")
            backup_dir = BACKUP_ROOT / timestamp
            if backup_dir.exists():
                shutil.rmtree(backup_dir)

            log(f"已删除: {old_file.name}")

def main():
    try:
        backup()
        return 0
    except Exception as e:
        log(f"备份失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
