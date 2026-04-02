#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw配置自动备份脚本
将关键配置文件备份到GitHub（排除敏感信息）
"""

import os
import sys
import json
import subprocess
import shutil
import re
from pathlib import Path
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置
OPENCLAW_DIR = Path("C:/Users/Administrator/.openclaw")
BACKUP_DIR = OPENCLAW_DIR / "workspace" / "backups" / "github"
TODAY = datetime.now().strftime("%Y-%m-%d")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# 需要备份的文件列表
FILES_TO_BACKUP = [
    "openclaw.json",
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
    "TOOLS.md",
    "MEMORY.md",
    "backup_github.py",
]

# 需要备份的目录列表
DIRS_TO_BACKUP = [
    "agents",
    "skills",
]

# 敏感词模式（用于检测和替换）
SECRET_PATTERNS = [
    r'["\']?api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?',
    r'["\']?token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?',
    r'["\']?secret["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?',
    r'["\']?password["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{10,}["\']?',
    r'sk-[a-zA-Z0-9]{48}',  # OpenAI API key
    r'Bearer [a-zA-Z0-9_-]{20,}',
    r'ghp_[a-zA-Z0-9]{36}',  # GitHub personal access token
]

# 备份目录
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def redact_secrets(content):
    """检测并替换敏感情息"""
    if not isinstance(content, str):
        return content

    for pattern in SECRET_PATTERNS:
        content = re.sub(pattern, '[REDACTED_SECRET]', content, flags=re.IGNORECASE)
    return content

def is_safe_to_backup(filepath):
    """检查文件是否包含敏感情息"""
    try:
        # 跳过二进制文件和非常大的文件
        if not filepath.is_file():
            return True

        # 跳过已知敏感情文件类型
        skip_patterns = ['.key', '.pem', '.crt', '.der', '.p12', '.pfx']
        if any(filepath.suffix.lower() in skip_patterns):
            return False

        # 跳过文件名包含敏感情词的文件
        skip_keywords = ['secret', 'key', 'password', 'token', 'credential']
        if any(keyword.lower() in filepath.name.lower() for keyword in skip_keywords):
            return False

        # 对于文本文件，检查内容
        try:
            with open(filepath, as f):
                content = f.read()
            # 检查是否包含API密钥等敏感情模式
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, content, flags=re.IGNORECASE):
                    print(f"  ⚠️  跳过包含敏感情息的文件: {filepath.name}")
                    return False
        except:
            # 如果无法读取，假设不安全
            return False

        return True
    except:
        return False

def copy_file_to_backup(file_path, dest_dir):
    """复制单个文件到备份目录"""
    src = OPENCLAW_DIR / file_path
    if not src.exists():
        print(f"  ⚠️  文件不存在: {file_path}")
        return False

    # 检查是否安全
    if not is_safe_to_backup(src):
        print(f"  🔒 跳过敏感情文件: {file_path}")
        return False

    dest = dest_dir / file_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    # 如果是JSON文件，先清理敏感情息
    if src.suffix.lower() == '.json':
        try:
            with open(src, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            # 清理敏感情息
            cleaned_content = redact_secrets(content)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"  ✅ 已备份（已清理）: {file_path}")
            return True
        except Exception as e:
            print(f"  ⚠️  处理JSON失败: {file_path} - {e}")
            return False
    else:
        shutil.copy2(src, dest)
        print(f"  ✅ 已备份: {file_path}")
        return True

def copy_dir_with_exclude(src, dest, exclude_dirs=None):
    """复制目录（递归），排除指定子目录和敏感情文件"""
    if not src.exists() or not src.is_dir():
        return 0, 0

    # 默认排除的目录
    excluded = {'.git', 'node_modules', '__pycache__', 'sessions', '.openclaw-backup'}
    if exclude_dirs:
        excluded.update(exclude_dirs)

    # 删除目标目录（如果存在）
    if dest.exists():
        try:
            shutil.rmtree(dest)
        except (PermissionError, OSError) as e:
            try:
                for item in dest.iterdir():
                    if item.name not in excluded:
                        try:
                            if item.is_dir():
                                shutil.rmtree(item)
                            else:
                                item.unlink()
                        except (PermissionError, OSError):
                            pass
            except:
                pass

    dest.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    skipped_count = 0

    # 手动复制，排除指定目录和敏感情文件
    for item in src.iterdir():
        # 直接排除 sessions 目录
        if item.name == 'sessions':
            skipped_count += 1
            continue

        if item.name in excluded:
            skipped_count += 1
            continue

        # 跳过敏感情文件
        if item.is_file() and not is_safe_to_backup(item):
            skipped_count += 1
            continue

        dest_item = dest / item.name
        if item.is_dir():
            # 递归复制子目录
            sub_copkted, sub_skipped = copy_dir_with_exclude(item, dest_item, exclude_dirs=list(excluded))
            copied_count += sub_copied
            skipped_count += sub_skipped
        else:
            dest_item.parent.mkdir(parents=True, exist_ok=True)
            # 如果是JSON文件，先清理敏感情息
            if item.suffix.lower() == '.json':
                try:
                    with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    cleaned_content = redact_secrets(content)
                    with open(dest_item, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    copied_count += 1
                except:
                    pass
            else:
                shutil.copy2(item, dest_item)
                copied_count += 1

    print(f"  ✅ 已备份目录: {src.name} (已复制{copied_count}个文件, 跳过{skipped_count}个)")
    return copied_count, skipped_count

def check_git_repo():
    """检查是否是git仓库"""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=BACKUP_DIR,
            capture_output=True,
            check=True
        )
        return True
    except:
        return False

def init_git_repo():
    """初始化git仓库"""
    subprocess.run(["git", "init"], cwd=BACKUP_DIR, check=True)

    # 配置 .gitignore
    gitignore = BACKUP_DIR / ".gitignore"
    gitignore_content = """# Node modules - 不需要备份
**/node_modules/
node_modules/

# NPM 缓存
.npm/
package-lock.json

# Python 缓存
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 备份文件
*.bak
*.backup
*.swp
*.tmp
*~

# 日志
*.log
logs/

# 操作系统
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# 临时文件
tmp/
temp/

# OpenClaw 会话和敏感情据（跳过所有jsonl文件）
**/*.jsonl
**/*.jsonl.*

# OpenClaw 备份目录
/.openclaw-backup/

# agents 下的所有 sessions 目录
**/agents/*/sessions/**
"""

    with open(gitignore, "w", encoding='utf-8') as f:
        f.write(gitignore_content)

    print("  ✅ Git仓库已初始化")

def git_commit():
    """提交变更到git"""
    subprocess.run(["git", "add", "."], cwd=BACKUP_DIR, check=True)

    # 检查是否有变更
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=BACKUP_DIR,
        capture_output=True,
        text=True
    )

    if not status_result.stdout.strip():
        print("  ⚠️  没有新内容需要提交")
        return False

    commit_msg = f"配置自动备份 - {TIMESTAMP}"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=BACKUP_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"  ✅ 已提交到本地Git: {commit_msg}")
        return True
    else:
        print(f"  ⚠️  提交失败: {result.stderr}")
        return False

def get_current_branch():
    """获取当前分支名称"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=BACKUP_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return "master"

def git_push():
    """推送到GitHub"""
    # 获取当前分支名称
    branch = get_current_branch()
    print(f"  📍 当前分支: {branch}")

    # 检查remote配置
    try:
        result = subprocess.run(
            ["git", "remote", "-v"],
            cwd=BACKUP_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"  📌 当前remote配置:\n{result.stdout}")
    except subprocess.CalledProcessError:
        print("  ⚠️  未配置remote，无法推送到GitHub")
        print("  💡 提示: 运行以下命令添加GitHub仓库:")
        print(f"     cd {BACKUP_DIR}")
        print("     git remote add origin <你的GitHub仓库URL>")
        return False

    # 尝试推送
    try:
        subprocess.run(
            ["git", "push", "origin", branch],
            cwd=BACKUP_DIR,
            check=True,
            timeout=60
        )
        print(f"  ✅ 已推送到GitHub (分支: {branch})")
        return True
    except subprocess.TimeoutExpired:
        print("  ⚠️  推送超时（60秒），可能网络较慢")
        return False
    except subprocess.CalledProcessError as e:
        print(f"  ❌ 推送失败: {e}")
        print("  💡 提示: 检查GitHub仓库URL、认证或网络连接")
        return False

def main():
    print(f"\n{'='*60}")
    print(f"OpenClaw配置自动备份 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 1. 创建今日备份目录
    today_backup = BACKUP_DIR / TODAY
    today_backup.mkdir(parents=True, exist_ok=True)
    print(f"📁 备份目录: {today_backup}\n")

    # 2. 备份文件
    print("📄 备份配置文件...")
    backup_success = True
    for file in FILES_TO_BACKUP:
        if not copy_file_to_backup(file, today_backup):
            backup_success = False

    # 3. 备份目录
    print("\n📁 备份配置目录...")
    total_copied = 0
    total_skipped = 0
    for dir_name in DIRS_TO_BACKUP:
        src = OPENCLAW_DIR / dir_name
        dest = today_backup / dir_name
        copied, skipped = copy_dir_with_exclude(src, dest)
        total_copied += copied
        total_skipped += skipped

    print(f"\n📊 备份统计: 复制{total_copied}个文件, 跳过{total_skipped}个文件")

    if not backup_success:
        print("\n⚠️  部分文件/目录备份失败，但继续执行Git操作")

    # 4. Git操作
    print("\n🔧 Git操作...")
    if not check_git_repo():
        print("  初始化Git仓库...")
        init_git_repo()

    committed = git_commit()

    # 5. 推送到GitHub（可选）
    print("\n🚀 推送到GitHub...")
    push_result = git_push()

    # 6. 生成备份报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "backup_dir": str(today_backup),
        "files_backed": FILES_TO_BACKUP,
        "dirs_backed": DIRS_TO_BACKUP,
        "git_commit": committed,
        "git_push": push_result if committed else None,
        "statistics": {
            "copied_files": total_copied,
            "skipped_files": total_skipped
        }
    }

    report_file = BACKUP_DIR / f"report_{TIMESTAMP}.json"
    with open(report_file, "w", encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 备份报告已保存: {report_file}")
    print(f"{'='*60}\n")

    return 0

if __name__ == "__main__":
    exit(main())
