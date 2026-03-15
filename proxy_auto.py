#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import threading
from queue import Queue

# 配置
PROXY_HOST = "127.0.0.1"
PROXY_PORT = "34743"
PROXY_URL = f"http://{PROXY_HOST}:{PROXY_PORT}"

# 国内域名后缀，这些不走代理
CN_DOMAINS = [
    '.cn', '.com.cn', '.net.cn', '.org.cn', '.gov.cn', '.edu.cn',
    '.baidu.com', '.qq.com', '.taobao.com', '.tmall.com', '.jd.com',
    '.pinduoduo.com', '.douyin.com', '.kuaishou.com', '.bilibili.com',
    '.weibo.com', '.xiaohongshu.com', '.zhihu.com', '.csdn.net',
    '.jianshu.com', '.oschina.net', '.gitee.com', '.aliyun.com',
    '.tencent.com', '.huawei.com', '.163.com', '.126.com', '.sina.com',
    '.sohu.com', '.ifeng.com', '.xinhuannet.com', '.people.com.cn',
    '.gmw.cn', '.cctv.com', '.feishu.cn', '.larksuite.com',
    '.volcengine.com', '.bytedance.com', '.douban.com', '.meituan.com',
    '.ele.me', '.didi.cn', '.ctrip.com', '.qunar.com', '.12306.cn',
    '.apple.com.cn', '.microsoft.com', '.office.com', '.windows.com'
]

# 需要走代理的域名
PROXY_DOMAINS = [
    '.github.com', '.githubusercontent.com', '.gitlab.com',
    '.google.com', '.googleapis.com', '.gstatic.com', '.youtube.com',
    '.twitter.com', '.x.com', '.facebook.com', '.instagram.com',
    '.linkedin.com', '.medium.com', '.dev.to', '.stackoverflow.com',
    '.stackexchange.com', '.npmjs.com', '.npmjs.org', '.yarnpkg.com',
    '.docker.com', '.docker.io', '.k8s.io', '.kubernetes.io',
    '.aws.amazon.com', '.amazon.com', '.azure.com', '.cloudflare.com',
    '.openai.com', '.anthropic.com', '.huggingface.co', '.hf.co',
    '.pypi.org', '.python.org', '.rust-lang.org', '.golang.org',
    '.npmjs.org', '.wikipedia.org', '.mozilla.org', '.debian.org',
    '.ubuntu.com', '.centos.org', '.redhat.com', '.fedoraproject.org',
    '.archlinux.org', '.gentoo.org', '.freebsd.org', '.netflix.com',
    '.spotify.com', '.discord.com', '.slack.com', '.notion.so',
    '.figma.com', '.dropbox.com', '.box.com', '.trello.com',
    '.atlassian.com', '.bitbucket.org', '.zoom.us', '.salesforce.com',
    '.heroku.com', '.vercel.com', '.netlify.app', '.render.com',
    '.fly.io', '.supabase.com', '.planetscale.com', '.mongodb.com',
    '.postgresql.org', '.mysql.com', '.oracle.com', '.ibm.com',
    '.intel.com', '.amd.com', '.nvidia.com', '.steamcommunity.com',
    '.steampowered.com', '.epicgames.com', '.ubisoft.com', '.ea.com',
    '.blizzard.com', '.riotgames.com', '.valvesoftware.com'
]

class ProxyManager:
    def __init__(self):
        self.proxy_enabled = False
        self.queue = Queue()
        self.lock = threading.Lock()
        self._check_initial_status()
        
    def _check_initial_status(self):
        """检查初始代理状态"""
        try:
            git_proxy = subprocess.check_output(
                ["git", "config", "--global", "http.proxy"], 
                text=True, 
                stderr=subprocess.DEVNULL
            ).strip()
            self.proxy_enabled = git_proxy == PROXY_URL
        except:
            self.proxy_enabled = False
    
    def _set_proxy(self):
        """开启代理"""
        with self.lock:
            if self.proxy_enabled:
                return
                
            # 设置环境变量
            os.environ['HTTP_PROXY'] = PROXY_URL
            os.environ['HTTPS_PROXY'] = PROXY_URL
            os.environ['ALL_PROXY'] = PROXY_URL
            os.environ['NO_PROXY'] = "localhost,127.0.0.1,localaddress,.local," + ",".join(CN_DOMAINS)
            
            # 配置git代理
            subprocess.run(
                ["git", "config", "--global", "http.proxy", PROXY_URL], 
                capture_output=True, 
                shell=True
            )
            subprocess.run(
                ["git", "config", "--global", "https.proxy", PROXY_URL], 
                capture_output=True, 
                shell=True
            )
            
            # 配置npm代理
            try:
                subprocess.run(
                    ["npm", "config", "set", "proxy", PROXY_URL], 
                    capture_output=True, 
                    shell=True
                )
                subprocess.run(
                    ["npm", "config", "set", "https-proxy", PROXY_URL], 
                    capture_output=True, 
                    shell=True
                )
            except:
                pass
            
            self.proxy_enabled = True
            print(f"Proxy enabled: {PROXY_URL}")
    
    def _remove_proxy(self):
        """关闭代理"""
        with self.lock:
            if not self.proxy_enabled:
                return
                
            # 清除环境变量
            for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY']:
                if key in os.environ:
                    del os.environ[key]
            
            # 清除git代理
            subprocess.run(
                ["git", "config", "--global", "--unset", "http.proxy"], 
                capture_output=True, 
                shell=True
            )
            subprocess.run(
                ["git", "config", "--global", "--unset", "https.proxy"], 
                capture_output=True, 
                shell=True
            )
            
            # 清除npm代理
            try:
                subprocess.run(
                    ["npm", "config", "delete", "proxy"], 
                    capture_output=True, 
                    shell=True
                )
                subprocess.run(
                    ["npm", "config", "delete", "https-proxy"], 
                    capture_output=True, 
                    shell=True
                )
            except:
                pass
            
            self.proxy_enabled = False
            print("Proxy disabled")
    
    def _needs_proxy(self, url):
        """判断URL是否需要走代理"""
        if not url:
            return False
            
        url = url.lower()
        
        # 先检查是否是国内域名
        for domain in CN_DOMAINS:
            if domain in url:
                return False
                
        # 再检查是否是需要代理的域名
        for domain in PROXY_DOMAINS:
            if domain in url:
                return True
                
        # 未知域名默认直连，安全第一
        return False
    
    def auto_switch(self, url=None):
        """根据URL自动切换代理"""
        if url and self._needs_proxy(url):
            self._set_proxy()
        else:
            # 没有URL或者不需要代理，默认关闭
            self._remove_proxy()
    
    def get_status(self):
        """查看代理状态"""
        print("\nProxy Status Check")
        print("=" * 50)
        
        # 检查环境变量
        http_proxy = os.environ.get('HTTP_PROXY', 'Not set')
        print(f"HTTP_PROXY: {http_proxy}")
        
        # 检查git代理
        try:
            git_proxy = subprocess.check_output(
                ["git", "config", "--global", "http.proxy"], 
                text=True, 
                stderr=subprocess.DEVNULL
            ).strip()
        except:
            git_proxy = 'Not set'
        print(f"Git proxy: {git_proxy}")
        
        # 检查npm代理
        try:
            npm_proxy = subprocess.check_output(
                ["npm", "config", "get", "proxy"], 
                text=True, 
                shell=True,
                stderr=subprocess.DEVNULL
            ).strip()
            if npm_proxy == 'undefined':
                npm_proxy = 'Not set'
        except:
            npm_proxy = 'Not available'
        print(f"NPM proxy: {npm_proxy}")
        
        print("=" * 50)
        
        if self.proxy_enabled:
            print("Proxy is ENABLED")
        else:
            print("Proxy is DISABLED")
        print()

# 全局代理管理器
proxy_manager = ProxyManager()

def run_with_auto_proxy(command, url=None):
    """自动切换代理后运行命令"""
    try:
        # 自动切换代理
        proxy_manager.auto_switch(url)
        
        # 运行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # 命令执行完后关闭代理
        proxy_manager.auto_switch()
        
        return result
    except Exception as e:
        proxy_manager.auto_switch()
        raise e

def main():
    if len(sys.argv) < 2:
        action = 'status'
    else:
        action = sys.argv[1].lower()
    
    if action == 'on':
        proxy_manager._set_proxy()
    elif action == 'off':
        proxy_manager._remove_proxy()
    elif action == 'status':
        proxy_manager.get_status()
    elif action == 'run':
        if len(sys.argv) < 3:
            print("Usage: python proxy_auto.py run <command> [url]")
            sys.exit(1)
        command = sys.argv[2]
        url = sys.argv[3] if len(sys.argv) > 3 else None
        result = run_with_auto_proxy(command, url)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    else:
        print("Usage: python proxy_auto.py [on|off|status|run]")
        print("  on         Force enable proxy")
        print("  off        Force disable proxy")
        print("  status     Check proxy status")
        print("  run        Run command with auto proxy (usage: run <command> [url])")
        print("             Example: run 'git clone https://github.com/xxx/xxx' github.com")
        sys.exit(1)

if __name__ == "__main__":
    main()
