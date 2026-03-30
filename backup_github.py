#!/usr/bin/env python3
import os
import subprocess
import time
from datetime import datetime

# 配置
WORKSPACE_DIR = r"C:\Users\Administrator\.openclaw\workspace"
WORKSPACE_QIANGCEHUA = r"C:\Users\Administrator\.openclaw\workspace-qiangcehua"
AGENTS_DIR = r"C:\Users\Administrator\.openclaw\agents"
GIT_REMOTE = "git@github.com:jinqiang888/qiangzong3.0.git"
BACKUP_MESSAGE = f"自动备份 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def run_command(cmd, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, encoding='utf-8', errors='replace')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def sync_directory(src_dir, dest_dir):
    """同步目录到备份位置，跳过包含秘密信息的文件"""
    import shutil
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # 需要跳过的文件和目录模式
    skip_patterns = [
        "sessions",
        ".env",
        ".env.",
        ".jsonl",
        ".DS_Store",
        "Thumbs.db",
        ".git",
        "node_modules"
    ]
    
    for item in os.listdir(src_dir):
        # 检查是否需要跳过该项目
        if any(pattern in item for pattern in skip_patterns):
            continue
            
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        
        if os.path.isdir(s):
            # 如果是目录，递归同步，但检查是否是需要跳过的目录
            if "sessions" not in s:
                sync_directory(s, d)
        else:
            # 如果是文件，检查是否包含需要跳过的模式
            if not any(pattern in item for pattern in skip_patterns):
                # 复制文件，覆盖已存在的
                shutil.copy2(s, d)

def backup_to_github():
    """备份到GitHub"""
    print(f"开始备份: {datetime.now()}")
    
    # 创建临时备份目录结构
    backup_root = os.path.join(WORKSPACE_DIR, ".openclaw-backup")
    agents_backup = os.path.join(backup_root, "agents")
    qiangcehua_backup = os.path.join(backup_root, "workspace-qiangcehua")
    
    # 同步强策划工作空间
    print("同步强策划工作空间...")
    sync_directory(WORKSPACE_QIANGCEHUA, qiangcehua_backup)
    
    # 同步agents配置
    print("同步agents配置...")
    sync_directory(AGENTS_DIR, agents_backup)
    
    # 进入工作目录
    os.chdir(WORKSPACE_DIR)
    
    # 检查git仓库
    if not os.path.exists(".git"):
        print("初始化git仓库...")
        run_command("git init")
        run_command(f"git remote add origin {GIT_REMOTE}")
        # 尝试重命名分支为main，如果失败用master
        run_command("git branch -M main || git branch -M master")
    
    # 获取当前分支
    print("获取当前分支...")
    _, branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
    current_branch = branch.strip() or "master"
    print(f"当前分支: {current_branch}")
    
    # 拉取最新代码
    print("拉取最新代码...")
    run_command(f"git pull origin {current_branch}")
    
    # 添加所有文件（包括备份目录）
    print("添加文件...")
    run_command("git add .")
    run_command("git add -f .openclaw-backup/")
    
    # 提交
    print("提交更改...")
    status, _, _ = run_command(f'git commit -m "{BACKUP_MESSAGE}"')
    if not status:
        print("没有更改需要提交")
        return True
    
    # 推送
    print(f"推送到GitHub origin/{current_branch}...")
    status, stdout, stderr = run_command(f"git push -u origin {current_branch}")
    if status:
        print("备份成功！包含：")
        print("  - 主工作区 (workspace)")
        print("  - 强策划工作区 (workspace-qiangcehua)")
        print("  - 所有Agent配置 (agents)")
        
        # 更新最后备份时间戳
        backup_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(".github_last_backup.txt", "w", encoding='utf-8') as f:
            f.write(backup_time)
        print(f"最后备份时间: {backup_time}")
        
        return True
    else:
        print(f"备份失败: {stderr}")
        return False

if __name__ == "__main__":
    backup_to_github()
