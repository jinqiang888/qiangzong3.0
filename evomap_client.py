#!/usr/bin/env python3
import json
import time
import hashlib
import requests
import os
from datetime import datetime
from typing import Dict, List, Any

class EvoMapClient:
    def __init__(self, config_path: str = "evomap_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.base_url = "https://evomap.ai"
        self.session = requests.Session()
        
        if self.config.get("node_secret"):
            self.session.headers.update({
                "Authorization": f"Bearer {self.config['node_secret']}"
            })
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _generate_message_id(self) -> str:
        """生成唯一消息ID"""
        timestamp = int(time.time())
        random_hex = hashlib.sha256(os.urandom(8)).hexdigest()[:8]
        return f"msg_{timestamp}_{random_hex}"
    
    def _get_iso_timestamp(self) -> str:
        """获取ISO格式时间戳"""
        return datetime.utcnow().isoformat() + "Z"
    
    def _compute_asset_id(self, asset: Dict) -> str:
        """计算asset_id：SHA256(canonical_json(asset_without_asset_id))"""
        # 移除asset_id字段
        asset_copy = {k: v for k, v in asset.items() if k != "asset_id"}
        # 序列化排序key的JSON
        canonical_json = json.dumps(asset_copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
        # 计算SHA256
        return "sha256:" + hashlib.sha256(canonical_json).hexdigest()
    
    def register_node(self) -> Dict:
        """注册节点，获取node_id和node_secret"""
        url = f"{self.base_url}/a2a/hello"
        
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "hello",
            "message_id": self._generate_message_id(),
            "timestamp": self._get_iso_timestamp(),
            "payload": {
                "capabilities": {},
                "model": "aliyun/qwen-max",
                "env_fingerprint": {
                    "platform": "windows",
                    "arch": "x64"
                }
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # 保存配置
        self.config.update({
            "node_id": result["payload"]["your_node_id"],
            "node_secret": result["payload"]["node_secret"],
            "claim_code": result["payload"]["claim_code"],
            "claim_url": result["payload"]["claim_url"],
            "hub_node_id": result["payload"]["hub_node_id"],
            "heartbeat_interval_ms": result["payload"]["heartbeat_interval_ms"]
        })
        self._save_config()
        
        # 更新请求头
        self.session.headers.update({
            "Authorization": f"Bearer {self.config['node_secret']}"
        })
        
        return result
    
    def send_heartbeat(self) -> Dict:
        """发送心跳，保持在线"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        url = f"{self.base_url}/a2a/heartbeat"
        payload = {
            "node_id": self.config["node_id"],
            "worker_enabled": True,
            "worker_domains": ["strategy", "coding", "design", "research", "operation"],
            "max_load": 5
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def fetch_promoted_assets(self, asset_type: str = "Capsule", include_tasks: bool = False) -> Dict:
        """获取已推广的资产"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        url = f"{self.base_url}/a2a/fetch"
        
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "fetch",
            "message_id": self._generate_message_id(),
            "sender_id": self.config["node_id"],
            "timestamp": self._get_iso_timestamp(),
            "payload": {
                "asset_type": asset_type,
                "include_tasks": include_tasks
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def publish_bundle(self, 
                      gene_category: str,
                      gene_signals: List[str],
                      gene_summary: str,
                      capsule_trigger: List[str],
                      capsule_summary: str,
                      capsule_content: str,
                      confidence: float = 0.9,
                      blast_radius: Dict = None,
                      outcome_score: float = 0.9) -> Dict:
        """发布Gene + Capsule + EvolutionEvent bundle"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        if blast_radius is None:
            blast_radius = {"files": 1, "lines": 10}
        
        # 构建Gene
        gene = {
            "type": "Gene",
            "schema_version": "1.5.0",
            "category": gene_category,
            "signals_match": gene_signals,
            "summary": gene_summary
        }
        gene["asset_id"] = self._compute_asset_id(gene)
        
        # 构建Capsule
        capsule = {
            "type": "Capsule",
            "schema_version": "1.5.0",
            "trigger": capsule_trigger,
            "gene": gene["asset_id"],
            "summary": capsule_summary,
            "content": capsule_content,
            "confidence": confidence,
            "blast_radius": blast_radius,
            "outcome": {
                "status": "success",
                "score": outcome_score
            },
            "env_fingerprint": {
                "platform": "windows",
                "arch": "x64"
            },
            "success_streak": 1
        }
        capsule["asset_id"] = self._compute_asset_id(capsule)
        
        # 构建EvolutionEvent
        evolution_event = {
            "type": "EvolutionEvent",
            "intent": gene_category,
            "capsule_id": capsule["asset_id"],
            "genes_used": [gene["asset_id"]],
            "outcome": {
                "status": "success",
                "score": outcome_score
            },
            "mutations_tried": 1,
            "total_cycles": 1
        }
        evolution_event["asset_id"] = self._compute_asset_id(evolution_event)
        
        # 发布
        url = f"{self.base_url}/a2a/publish"
        payload = {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "publish",
            "message_id": self._generate_message_id(),
            "sender_id": self.config["node_id"],
            "timestamp": self._get_iso_timestamp(),
            "payload": {
                "assets": [gene, capsule, evolution_event]
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def search_assets(self, signals: str, asset_type: str = "Capsule") -> Dict:
        """搜索资产"""
        url = f"{self.base_url}/a2a/assets/search?signals={signals}&type={asset_type}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_asset_detail(self, asset_id: str) -> Dict:
        """获取资产详情"""
        url = f"{self.base_url}/a2a/assets/{asset_id}?detailed=true"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def list_tasks(self, min_reputation: int = 0, min_bounty: int = 0) -> Dict:
        """获取可用任务"""
        url = f"{self.base_url}/task/list?min_reputation={min_reputation}&min_bounty={min_bounty}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def claim_task(self, task_id: str) -> Dict:
        """认领任务"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        url = f"{self.base_url}/task/claim"
        payload = {
            "task_id": task_id,
            "node_id": self.config["node_id"]
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def complete_task(self, task_id: str, asset_id: str) -> Dict:
        """完成任务"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        url = f"{self.base_url}/task/complete"
        payload = {
            "task_id": task_id,
            "asset_id": asset_id,
            "node_id": self.config["node_id"]
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_node_status(self) -> Dict:
        """获取节点状态和信誉"""
        if not self.config.get("node_id"):
            raise Exception("Node not registered. Call register_node() first.")
            
        url = f"{self.base_url}/a2a/nodes/{self.config['node_id']}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# 全局客户端实例
evomap = EvoMapClient()

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python evomap_client.py <command> [args]")
        print("Commands:")
        print("  register          注册节点")
        print("  heartbeat         发送心跳")
        print("  fetch [type]      获取资产，默认Capsule")
        print("  search <signals>  搜索资产")
        print("  tasks             列出可用任务")
        print("  status            查看节点状态")
        return
    
    command = sys.argv[1].lower()
    
    if command == "register":
        result = evomap.register_node()
        print("节点注册成功！")
        print(f"Node ID: {result['payload']['your_node_id']}")
        print(f"Claim URL: {result['payload']['claim_url']}")
        print("请访问上面的链接绑定你的EvoMap账户，领取200初始积分。")
        
    elif command == "heartbeat":
        result = evomap.send_heartbeat()
        print("心跳发送成功")
        print(f"节点状态: {result['node_status']}")
        print(f"积分余额: {result['credit_balance']}")
        if result.get('available_work'):
            print(f"可用任务: {len(result['available_work'])}个")
            
    elif command == "fetch":
        asset_type = sys.argv[2] if len(sys.argv) > 2 else "Capsule"
        result = evomap.fetch_promoted_assets(asset_type)
        print(f"获取到 {len(result['payload'].get('assets', []))} 个{asset_type}资产")
        
    elif command == "search":
        if len(sys.argv) < 3:
            print("请输入搜索关键词，例如: python evomap_client.py search python,timeout")
            return
        signals = sys.argv[2]
        result = evomap.search_assets(signals)
        print(f"搜索到 {len(result.get('assets', []))} 个相关资产")
        
    elif command == "tasks":
        result = evomap.list_tasks()
        print(f"获取到 {len(result.get('tasks', []))} 个可用任务")
        
    elif command == "status":
        result = evomap.get_node_status()
        print(f"节点ID: {result['node_id']}")
        print(f"信誉分: {result.get('reputation', 0)}")
        print(f"积分余额: {result.get('credit_balance', 0)}")
        print(f"已发布资产: {result.get('capsule_count', 0)}个")
        
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
