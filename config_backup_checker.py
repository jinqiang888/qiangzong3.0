#!/usr/bin/env python3
"""
配置变更备份检查脚本
检查今天是否有配置文件变更，如果有变更则执行备份到GitHub

监控的文件包括：
- openclaw.json
- agents/*.json (agent配置)
- workspace/SOUL.md
- workspace/IDENTITY.md
- workspace/AGENTS.md
- workspace/USER.md
- workspace/TOOLS.md
- skills目录
"""

import os
import subprocess
import json
import sys
from datetime import datetime, timedelta

# 配置
WORKSPACE_DIR = r"C:\Users\Administrator\.openclaw\workspace"
OPENCLAW_DIR = r"C:\Users\Administrator\.openclaw"
STATE_FILE = os.path.join(WORKSPACE_DIR, ".config_check_state.json")

# 需要监控的文件模式
MONITORED_PATTERNS = [
    r"openclaw\.json",
    r"agents/.*\.json$",
    r"agents/.*\.json5$",
    r"workspace/SOUL\.md$",
    r"workspace/IDENTITY\.md$",
    r"workspace/AGENTS\.md$",
    r"workspace/USER\.md$",
    r"workspace/TOOLS\.md$",
    r"workspace/skills/.*",
    r".openclaw/skills/.*",
]

def run_command(cmd, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def load_state():
    """加载上次检查的状态"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"last_check": None, "file_timestamps": {}}

def save_state(state):
    """保存检查状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_file_mtime(filepath):
    """获取文件修改时间"""
    if os.path.exists(filepath):
        return os.path.getmtime(filepath)
    return None

def get_monitored_files():
    """获取所有需要监控的文件"""
    files = {}

    # openclaw.json
    openclaw_json = os.path.join(OPENCLAW_DIR, "openclaw.json")
    if os.path.exists(openclaw_json):
        files[openclaw_json] = "openclaw.json"

    # agents目录下的json文件
    agents_dir = os.path.join(OPENCLAW_DIR, "agents")
    if os.path.exists(agents_dir):
        for root, dirs, __ in os.walk(agents_dir):
            # 跳过sessions目录
            dirs[:] = [d for d in dirs if d not in ['sessions', '.sessions']]
            for file in os.listdir(root):
                if file.endswith('.json') or file.endswith('.json5'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, OPENCLAW_DIR)
                    files[filepath] = rel_path

    # workspace目录
    workspace_files = [
        "SOUL.md",
        "IDENTITY.md",
        "AGENTS.md",
        "USER.md",
        "TOOLS.md"
    ]
    for filename in workspace_files:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        if os.path.exists(filepath):
            files[filepath] = f"workspace/{filename}"

    # skills目录
    skills_dirs = [
        os.path.join(WORKSPACE_DIR, "skills"),
        os.path.join(OPENCLAW_DIR, "skills")
    ]
    for skills_dir in skills_dirs:
        if os.path.exists(skills_dir):
            for root, dirs, skill_files in os.walk(skills_dir):
                # 跳过node_modules和.git目录
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', '.package-lock.json']]
                for file in skill_files:
                    # 跳过.pyc文件
                    if file.endswith('.pyc'):
                        continue
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, OPENCLAW_DIR)
                    files[filepath] = rel_path

    return files

def check_changes():
    """检查是否有配置文件变更"""
    print(f"检查配置文件变更: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 加载上次状态
    state = load_state()
    last_check = state.get("last_check")
    old_timestamps = state.get("file_timestamps", {})

    # 获取当前所有监控文件的时间戳
    current_files = get_monitored_files()
    current_timestamps = {
        filepath: get_file_mtime(filepath)
        for filepath in current_files
    }

    # 如果是第一次运行，保存状态并返回False
    if last_check is None:
        print("首次运行，保存文件时间戳...")
        state["last_check"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        state["file_timestamps"] = current_timestamps
        save_state(state)
        return False, []

    # 检查变更
    changed_files = []

    # 检查文件修改时间变化
    for filepath, current_mtime in current_timestamps.items():
        old_mtime = old_timestamps.get(filepath)

        # 新增文件
        if old_mtime is None:
            changed_files.append({
                "file": current_files[filepath],
                "type": "新增",
                "reason": "文件不存在于上次检查"
            })
        # 修改的文件
        elif old_mtime != current_mtime:
            changed_files.append({
                "file": current_files[filepath],
                "type": "修改",
                "reason": f"修改时间变化"
            })

    # 检查删除的文件（跳过sessions）
    for filepath in old_timestamps:
        if filepath not in current_timestamps and 'sessions' not in filepath:
            changed_files.append({
                "file": filepath,
                "type": "删除",
                "reason": "文件已不存在"
            })

    # 更新状态
    state["last_check"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    state["file_timestamps"] = current_timestamps
    save_state(state)

    # 输出结果
    if changed_files:
        print(f"\n发现 {len(changed_files)} 个配置文件变更:")
        for change in changed_files[:10]:  # 只显示前10个
            print(f"  [{change['type']}] {change['file']}")
        if len(changed_files) > 10:
            print(f"  ... 还有 {len(changed_files) - 10} 个文件变更")
        return True, changed_files
    else:
        print("\n未发现配置文件变更")
        return False, []

def run_backup():
    """执行备份到GitHub"""
    print("\n开始执行备份到GitHub...")

    # 调用备份脚本
    backup_script = os.path.join(WORKSPACE_DIR, "backup_github.py")
    status, stdout, stderr = run_command(f"python {backup_script}", WORKSPACE_DIR)

    if status:
        print("备份成功！")
        return True
    else:
        print(f"备份失败: {stderr}")
        return False

def main():
    """主函数"""
    has_changes, changed_files = check_changes()

    if has_changes:
        print("\n需要执行备份到GitHub")

        # 执行备份
        backup_success = run_backup()

        if backup_success:
            # 更新最后备份时间
            state = load_state()
            state["last_backup"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_state(state)

            print(f"\n备份完成！最后备份时间: {state['last_backup']}")
            print(f"共备份了 {len(changed_files)} 个变更文件")
            return True, changed_files
        else:
            print("\n备份失败，请检查错误信息")
            return False, changed_files
    else:
        print("\n无需备份")
        return False, []

if __name__ == "__main__":
    try:
        has_changes, changes = main()
        if has_changes:
            sys.exit(0)  # 有变更但备份成功，退出码0
        else:
            sys.exit(0)  # 无变更，退出码0
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
