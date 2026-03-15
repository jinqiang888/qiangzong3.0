#!/usr/bin/env python3
import sys
import os
import subprocess

PROXY_HOST = "127.0.0.1"
PROXY_PORT = "34743"
PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"

def set_proxy():
    """开启代理"""
    # 设置环境变量
    os.environ['HTTP_PROXY'] = PROXY_URL
    os.environ['HTTPS_PROXY'] = PROXY_URL
    os.environ['ALL_PROXY'] = PROXY_URL
    os.environ['NO_PROXY'] = "localhost,127.0.0.1,localaddress,.local,.cn,.com.cn"
    
    # 配置git代理
    subprocess.run(["git", "config", "--global", "http.proxy", PROXY_URL], capture_output=True, shell=True)
    subprocess.run(["git", "config", "--global", "https.proxy", PROXY_URL], capture_output=True, shell=True)
    
    # 配置npm代理（如果npm存在）
    try:
        subprocess.run(["npm", "config", "set", "proxy", PROXY_URL], capture_output=True, shell=True)
        subprocess.run(["npm", "config", "set", "https-proxy", PROXY_URL], capture_output=True, shell=True)
    except:
        pass
    
    print(f"Proxy enabled: {PROXY_URL}")
    print(f"NO_PROXY: {os.environ['NO_PROXY']}")

def remove_proxy():
    """关闭代理"""
    # 清除环境变量
    for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY']:
        if key in os.environ:
            del os.environ[key]
    
    # 清除git代理
    subprocess.run(["git", "config", "--global", "--unset", "http.proxy"], capture_output=True, shell=True)
    subprocess.run(["git", "config", "--global", "--unset", "https.proxy"], capture_output=True, shell=True)
    
    # 清除npm代理（如果npm存在）
    try:
        subprocess.run(["npm", "config", "delete", "proxy"], capture_output=True, shell=True)
        subprocess.run(["npm", "config", "delete", "https-proxy"], capture_output=True, shell=True)
    except:
        pass
    
    print("Proxy disabled")

def get_status():
    """查看代理状态"""
    print("\nProxy Status Check")
    print("------------------------")
    
    # 检查环境变量
    http_proxy = os.environ.get('HTTP_PROXY', 'Not set')
    print(f"HTTP_PROXY: {http_proxy}")
    
    # 检查git代理
    try:
        git_proxy = subprocess.check_output(["git", "config", "--global", "http.proxy"], text=True).strip()
    except:
        git_proxy = 'Not set'
    print(f"Git proxy: {git_proxy}")
    
    # 检查npm代理（如果npm存在）
    try:
        npm_proxy = subprocess.check_output(["npm", "config", "get", "proxy"], text=True, shell=True).strip()
        if npm_proxy == 'undefined':
            npm_proxy = 'Not set'
    except:
        npm_proxy = 'Not available'
    print(f"NPM proxy: {npm_proxy}")
    
    print("------------------------")
    
    if http_proxy != 'Not set' and git_proxy != 'Not set' and npm_proxy != 'Not set':
        print("Proxy is working properly")
    else:
        print("Proxy is not enabled")
    print()

def main():
    if len(sys.argv) < 2:
        action = 'status'
    else:
        action = sys.argv[1].lower()
    
    if action == 'on':
        set_proxy()
    elif action == 'off':
        remove_proxy()
    elif action == 'status':
        get_status()
    else:
        print("Usage: python proxy.py [on|off|status]")
        print("  on     Enable proxy")
        print("  off    Disable proxy")
        print("  status Check proxy status")
        sys.exit(1)

if __name__ == "__main__":
    main()
