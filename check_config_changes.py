# -*- coding: utf-8 -*-
"""
配置文件变更检查脚本
检测今天是否有配置文件变更，返回退出码：
- 0: 无变更
- 1: 有变更
"""
import os
from datetime import datetime, timedelta
from pathlib import Path

# 设置
WORKSPACE = r"C:\Users\Administrator\.openclaw\workspace"
REPO = r"C:\Users\Administrator\.openclaw"
TODAY = datetime.now().strftime("%Y-%m-%d")
TODAY_DT = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def check_file_modified_today(filepath):
    """检查文件今天是否被修改过"""
    if not os.path.exists(filepath):
        return False
    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    mod_date = mod_time.strftime("%Y-%m-%d")
    return mod_date == TODAY

def main():
    has_changes = False
    changed_files = []

    print("=== 配置变更检查 ===")
    print(f"检查日期: {TODAY}")
    print("")

    # 检查核心配置文件
    print("【核心配置文件】")
    core_files = [
        (os.path.join(REPO, "openclaw.json"), "openclaw.json"),
        (os.path.join(WORKSPACE, "SOUL.md"), "SOUL.md"),
        (os.path.join(WORKSPACE, "IDENTITY.md"), "IDENTITY.md")
    ]

    for filepath, name in core_files:
        if os.path.exists(filepath):
            if check_file_modified_today(filepath):
                print(f"  ✓ 变更: {name}")
                has_changes = True
                changed_files.append(filepath)
            else:
                print(f"  - 未变: {name}")
        else:
            print(f"  ! 不存在: {name}")

    # 检查 agents/*.json
    print("")
    print("【Agent配置文件】")
    agents_dir = os.path.join(WORKSPACE, "agents")
    if os.path.exists(agents_dir):
        json_count = 0
        changed_count = 0
        for root, dirs, files in os.walk(agents_dir):
            for file in files:
                if file.endswith('.json'):
                    json_count += 1
                    filepath = os.path.join(root, file)
                    if check_file_modified_today(filepath):
                        changed_count += 1
                        has_changes = True
                        changed_files.append(filepath)
                        print(f"  ✓ 变更: {file(os.path.relpath(filepath, agents_dir))}")

        if json_count == 0:
            print("  - (无JSON文件)")
        elif changed_count == 0:
            print(f"  - 检查了 {json_count} 个文件，无变更")
    else:
        print("  - agents目录不存在")

    # 输出结果
    print("")
    if has_changes:
        print(f"【结果】检测到 {len(changed_files)} 个文件变更")
        print("需要执行备份")
        sys.exit(1)
    else:
        print("【结果】今天没有检测到配置文件变更")
        sys.exit(0)

if __name__ == "__main__":
    import sys
    main()
