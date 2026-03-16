#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from typing import List, Dict

# 设置UTF-8编码解决Windows emoji输出问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')


class TopicPlannerAgent:
    def __init__(self, config_path: str = "topic_planner_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "name": "选题策划Agent",
            "model": "aliyun/qwen-max",
            "skills": ["autoglm-websearch", "autoglm-deepresearch", "content-strategy", "social-content"],
            "rules": [
                "每天上午9点自动输出3-5个选题建议",
                "选题必须结合当前热点和业务方向",
                "每个选题必须附带推荐角度和至少2个参考案例链接",
                "每周一输出上周热点总结和下周选题方向",
                "所有选题必须符合目标人群画像，禁止输出无关内容"
            ],
            "business_info": {
                "product": "",
                "target_audience": "",
                "core_business": "",
                "content_platforms": ["抖音", "小红书", "视频号", "公众号", "B站"]
            },
            "output_format": {
                "选题标题": "",
                "推荐角度": [],
                "适合平台": [],
                "参考案例": [],
                "预估热度": "高/中/低"
            }
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def _load_knowledge_base(self) -> Dict:
        """加载知识库：过往爆款内容、产品信息、人群画像"""
        kb_path = "topic_knowledge_base.json"
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "past_hits": [],
            "product_info": {},
            "audience_profile": {},
            "forbidden_topics": []
        }
    
    def save_config(self):
        """保存配置"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def save_knowledge_base(self):
        """保存知识库"""
        with open("topic_knowledge_base.json", "w", encoding="utf-8") as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
    
    def set_business_info(self, product: str, target_audience: str, core_business: str, platforms: List[str] = None):
        """设置业务信息"""
        self.config["business_info"]["product"] = product
        self.config["business_info"]["target_audience"] = target_audience
        self.config["business_info"]["core_business"] = core_business
        if platforms:
            self.config["business_info"]["content_platforms"] = platforms
        self.save_config()
    
    def add_past_hit(self, title: str, platform: str, views: int, publish_date: str, tags: List[str]):
        """添加过往爆款内容"""
        self.knowledge_base["past_hits"].append({
            "title": title,
            "platform": platform,
            "views": views,
            "publish_date": publish_date,
            "tags": tags
        })
        self.save_knowledge_base()
    
    def add_forbidden_topic(self, topic: str):
        """添加禁止选题"""
        self.knowledge_base["forbidden_topics"].append(topic)
        self.save_knowledge_base()
    
    def generate_daily_topics(self) -> List[Dict]:
        """生成每日选题"""
        # 这里调用模型和搜索工具生成选题
        # 实际运行时会结合实时热点和知识库
        topics = []
        
        # 模拟生成3个选题
        for i in range(3):
            topics.append({
                "选题标题": f"选题{i+1}：{datetime.now().strftime('%Y-%m-%d')}热点结合",
                "推荐角度": ["角度1：从用户痛点切入", "角度2：结合产品优势", "角度3：对比竞品"],
                "适合平台": ["小红书", "抖音"],
                "参考案例": ["https://example.com/case1", "https://example.com/case2"],
                "预估热度": "高"
            })
        
        return topics
    
    def get_weekly_report(self) -> Dict:
        """生成周报告"""
        return {
            "上周热点总结": [],
            "下周选题方向": [],
            "重点推荐平台": []
        }

# 全局实例
topic_planner = TopicPlannerAgent()

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python agent_topic_planner.py <command> [args]")
        print("Commands:")
        print("  generate          生成今日选题")
        print("  weekly            生成周报告")
        print("  add_hit <title> <platform> <views> <date> <tags>  添加爆款案例")
        print("  config            查看配置")
        return
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        topics = topic_planner.generate_daily_topics()
        print(f"📅 {datetime.now().strftime('%Y-%m-%d')} 选题建议：")
        print("=" * 50)
        for i, topic in enumerate(topics, 1):
            print(f"\n{i}. {topic['选题标题']}")
            print(f"   推荐角度：{'、'.join(topic['推荐角度'])}")
            print(f"   适合平台：{'、'.join(topic['适合平台'])}")
            print(f"   参考案例：{'、'.join(topic['参考案例'])}")
            print(f"   预估热度：{topic['预估热度']}")
        
    elif command == "weekly":
        report = topic_planner.get_weekly_report()
        print("📊 周选题报告：")
        print("=" * 50)
        print("上周热点总结：", report["上周热点总结"])
        print("下周选题方向：", report["下周选题方向"])
        print("重点推荐平台：", report["重点推荐平台"])
        
    elif command == "add_hit":
        if len(sys.argv) < 7:
            print("参数错误：add_hit <标题> <平台> <播放量> <日期> <标签1,标签2>")
            return
        title = sys.argv[2]
        platform = sys.argv[3]
        views = int(sys.argv[4])
        date = sys.argv[5]
        tags = sys.argv[6].split(",")
        topic_planner.add_past_hit(title, platform, views, date, tags)
        print("✅ 爆款案例添加成功")
        
    elif command == "config":
        print("⚙️ 选题策划Agent配置：")
        print(json.dumps(topic_planner.config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
