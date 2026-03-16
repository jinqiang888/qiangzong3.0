#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

# 设置工作目录
import os
os.chdir(current_dir)

def init_database():
    """初始化数据库"""
    print("Starting database initialization...")
    
    try:
        # 导入所有模型确保表被创建
        from backend.models import Base, BilibiliAccount, UploadRecord
        from backend.core.database import init_database, create_tables
        
        print("[OK] All models imported")
        
        # 初始化数据库
        if init_database():
            print("[OK] Database initialized")
        else:
            print("[FAIL] Database initialization failed")
            return False
        
        # 创建表
        create_tables()
        print("[OK] Database tables created")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\nDatabase initialization completed!")
        print("Ready to start the system:")
        print("1. Start services manually as described in STARTUP_GUIDE.md")
    else:
        print("\nDatabase initialization failed, please check the error message above")
        sys.exit(1)

