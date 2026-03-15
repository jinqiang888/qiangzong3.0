#!/usr/bin/env python3
import json
import os
from typing import Dict, List, Any

class AgentScheduler:
    def __init__(self, config_path: str = "agent_config.json"):
        self.config = self._load_config(config_path)
        self.main_agent = self.config["主Agent"]
        self.sub_agents = {agent["id"]: agent for agent in self.config["子Agent列表"]}
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _classify_task(self, user_query: str) -> str:
        """分类任务类型，返回对应的子Agent ID"""
        query = user_query.lower()
        
        # 代码相关
        code_keywords = ["代码", "写代码", "编程", "开发", "bug", "调试", "部署", "运维", "服务器", "数据库", "git", "python", "java", "javascript", "前端", "后端", "接口"]
        if any(keyword in query for keyword in code_keywords):
            return "code-agent"
            
        # 设计相关
        design_keywords = ["设计", "UI", "UX", "界面", "原型", "美工", "作图", "画图", "生成图片", "前端页面", "样式"]
        if any(keyword in query for keyword in design_keywords):
            return "design-agent"
            
        # 研究相关
        research_keywords = ["研究", "调研", "查资料", "搜索", "报告", "分析", "竞品", "行业", "论文", "资料", "文献"]
        if any(keyword in query for keyword in research_keywords):
            return "research-agent"
            
        # 内容相关
        content_keywords = ["文案", "写作", "内容", "营销", "运营", "公众号", "微博", "小红书", "抖音", "SEO", "推广", "方案"]
        if any(keyword in query for keyword in content_keywords):
            return "content-agent"
            
        # 客服相关
        service_keywords = ["客服", "回复", "消息", "咨询", "售后", "解答", "问题"]
        if any(keyword in query for keyword in service_keywords):
            return "service-agent"
            
        # 通用任务，主Agent自己处理
        return "main"
    
    def _spawn_sub_agent(self, agent_id: str, task: str) -> str:
        """派生子Agent执行任务"""
        agent = self.sub_agents[agent_id]
        print(f"📤 派任务给 [{agent['name']}]，使用模型: {agent['model']}")
        print(f"任务内容: {task}")
        
        # 这里调用OpenClaw的sessions_spawn接口派生子Agent
        # 实际运行时会替换为真实的工具调用
        result = f"[{agent['name']}] 完成任务: {task}\n模拟返回结果..."
        return result
    
    def process_query(self, user_query: str) -> str:
        """处理用户查询"""
        task_type = self._classify_task(user_query)
        
        if task_type == "main":
            # 主Agent自己处理
            return f"我来处理这个任务: {user_query}"
        else:
            # 派给子Agent
            result = self._spawn_sub_agent(task_type, user_query)
            return f"任务已完成，结果如下:\n{result}"
    
    def get_agent_list(self) -> List[Dict]:
        """获取所有子Agent列表"""
        return self.config["子Agent列表"]
    
    def add_agent(self, agent_config: Dict) -> bool:
        """添加新的子Agent"""
        if agent_config["id"] in self.sub_agents:
            return False
        self.config["子Agent列表"].append(agent_config)
        self.sub_agents[agent_config["id"]] = agent_config
        # 保存配置
        with open("agent_config.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        return True

# 全局调度器实例
scheduler = AgentScheduler()

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python agent_scheduler.py <user_query>")
        print("示例: python agent_scheduler.py '帮我写一个Python爬虫'")
        return
    
    user_query = sys.argv[1]
    result = scheduler.process_query(user_query)
    print(result)

if __name__ == "__main__":
    main()
