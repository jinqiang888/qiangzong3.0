# LEARNINGS.md - Continuous Learning Log

## [LRN-20260317-001] OpenClaw 配置优化最佳实践

**Logged**: 2026-03-17T18:00:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
整理了搜索到的OpenClaw最新配置优化、安全最佳实践

### Details
从公开学习资源整理获得以下关键知识：

1. **核心配置文件优化**
   - 直接编辑 `~/.openclaw/SOUL.md` `IDENTITY.md` `USER.md` 塑造个性行为
   - `MEMORY.md` + 日常记忆文件：定期修剪，保持上下文精简
   - `openclaw.json` 关键配置：
     - gateway 绑定 127.0.0.1，修改默认端口，启用强token认证
     - agents.defaults 配置默认模型、温度、思考级别
     - models.providers 存放API key，绝不提交到git

2. **思考/推理级别配置**
   - 全局默认设置 `agents.defaults.thinkingDefault: "medium"`
   - 聊天中可随时切换：`/think low/medium/high/xhigh/off`
   - 简单任务用low/off，省钱更快；复杂深度分析用high

3. **上下文与并发优化**
   - 用qmd等技能总结长线程/研究，减少上下文占用
   - 简单任务路由到本地模型（Ollama），重推理路由到云端Claude/GPT
   - 配置Brave Search API key，默认网络搜索走Brave

4. **自动化与 proactive 特性**
   - cron做定期任务，比如每周一9点研究主题发总结
   - heartbeat 做日常检查，自动git pull更新
   - 定期执行 `openclaw update` 更新技能和工具

5. **安全加固最佳实践**
   - API key 用环境变量或 `.env` 文件，权限设为 600
   - 网关绝不绑0.0.0.0，远程访问用Tailscale/Cloudflare Tunnel/SSH反向隧道
   - 对非信任agent禁用高风险工具（shell、文件写、browser）
   - 定期运行 `openclaw security audit` 检查
   - 敏感数据用隔离VPS本地模式，不接入云端模型

6. **Telegram使用技巧**
   - DM做私有CLI控制，群聊做共享任务
   - 群聊需要@机器人触发（可配置 `requireMention: false`）
   - 支持流式回复，实时编辑消息

### Suggested Action
将这些最佳实践更新到 `TOOLS.md` 或 `AGENTS.md`，日常执行中遵循

### Metadata
- Source: web search (dreamsaicanbuy.com)
- Related Files: openclaw.json, SOUL.md, AGENTS.md
- Tags: openclaw, configuration, optimization, security
- See Also:
- Pattern-Key: openclaw.configuration-optimization
- Recurrence-Count: 1
- First-Seen: 2026-03-17
- Last-Seen: 2026-03-17

---
