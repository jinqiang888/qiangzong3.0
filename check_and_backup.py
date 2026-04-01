# -*- coding: utf-8 -*-
"""
配置变更检查与自动备份脚本
检查今天是否有配置文件变更，如果有则执行备份到GitHub
"""
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# 设置
WORKSPACE = r"C:\Users\Administrator\.openclaw\workspace"
REPO = r"C:\Users\Administrator\.openclaw"
BACKUP_SCRIPT = os.path.join(WORKSPACE, "backup_github.py")
TODAY = datetime.now().strftime("%Y-%m-%d")

def check_file_modified_today(filepath):
    """检查文件今天是否被修改过"""
    if not os.path.exists(filepath):
        return False
    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    mod_date = mod_time.strftime("%Y-%m-%d")
    return mod_date == TODAY

def check_for_changes():
    """检查是否有配置文件变更"""
    has_changes = False

    # 检查核心配置文件
    core_files = [
        os.path.join(REPO, "openclaw.json"),
        os.path.join(WORKSPACE, "SOUL.md"),
        os.path.join(WORKSPACE, "IDENTITY.md")
    ]

    for filepath in core_files:
        if os.path.exists(filepath):
            if check_file_modified_today(filepath):
                has_changes = True
                print(f"[变更] {os.path.basename(filepath)}")

    # 检查 agents/*.json
    agents_dir = os.path.join(WORKSPACE, "agents")
    if os.path.exists(agents_dir):
        for root, dirs, files in os.walk(agents_dir):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    if check_file_modified_today(filepath):
                        has_changes = True
                        print(f"[变更] {os.path.relpath(filepath, WORKSPACE)}")

    return has_changes

def run_backup():
    """执行备份脚本"""
    if not os.path.exists(BACKUP_SCRIPT):
        print(f"错误: 备份脚本不存在: {BACKUP_SCRIPT}")
        return False

    print("执行备份到 GitHub...")
    try:
        result = subprocess.run(
            ["python", BACKUP_SCRIPT],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"备份失败: {e}")
        return False

def main():
    """主函数"""
    print(f"=== 配置变更检查与自动备份 ===")
    print(f"时间: {TODAY} {datetime.now().strftime('%H:%M:%S')}")
    print("")

    if check_for_changes():
        print("")
        print("检测到配置变更，执行备份...")
        success = run_backup()
        if success:
            print("备份完成！")
            sys.exit(0)
        else:
            print("备份失败！")
            sys.exit(1)
    else:
        print("未检测到配置变更，跳过备份")
        sys.exit(0)

if __name__ == "__main__":
    main()
