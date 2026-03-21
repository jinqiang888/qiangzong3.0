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
   - **2026.3新增特性：每日凌晨自动重置会话**，保持上下文清爽

5. **安全加固最佳实践**
   - API key 用环境变量或 `.env` 文件，权限设为 600
   - 网关绝不绑0.0.0.0，远程访问用Tailscale/Cloudflare Tunnel/SSH反向隧道
   - 对非信任agent禁用高风险工具（shell、文件写、browser）
   - 定期运行 `openclaw security audit` 检查
   - 敏感数据用隔离VPS本地模式，不接入云端模型

6. **多账号飞书配置（2026.3新增）**
   - 支持同一个飞书开放平台下多个应用在不同频道使用
   - 通过 `channels.feishu.accounts` 配置多账号，指定defaultAccount
   - 多账号之间完全隔离，互不干扰

7. **记忆插件体系（2026.3新增）**
   - 支持 `mem0`、`memory-core`、`memory-lancedb` 多种向量记忆后端
   - 在 `plugins` 配置启用，按需选择适合自己的方案
   - `memory-core` 是OpenClaw官方推荐的本地优先方案，基于LanceDB，自带场景隔离防污染

8. **Telegram使用技巧**
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
- Recurrence-Count: 2
- First-Seen: 2026-03-17
- Last-Seen: 2026-03-22

## [LRN-20260321-001] Windows PowerShell 命令分隔符兼容性

**Logged**: 2026-03-21T02:10:00Z
**Priority**: medium
**Status**: resolved
**Area**: config, infra

### Summary
Windows PowerShell 不支持 `&&` 分隔多条命令，必须使用 `;` 分隔。这会导致多行命令执行失败。

### Details
之前执行 `cd xxx && node xxx` 报错，PowerShell 语法不支持 `&&` 操作符，必须改用 `cd xxx; node xxx`。

### Suggested Action
在后续执行多命令时，使用 `;` 代替 `&&`。

### Metadata
- Source: self-experience
- Related Files: (dynamic commands)
- Tags: openclaw, windows, powershell, compatibility
- See Also: LRN-20260317-001
- Pattern-Key: openclaw.windows-powershell-command-separator
- Recurrence-Count: 1
- First-Seen: 2026-03-21
- Last-Seen: 2026-03-21

## [LRN-20260322-001] EvoMap服务可用性

**Logged**: 2026-03-22T02:15:00Z
**Priority**: medium
**Status**: observed
**Area**: infra, evolution

### Summary
EvoMap搜索和fetch接口偶发500/503错误，心跳接口正常，积分功能可用。

### Details
- 心跳、状态查询、任务列表接口工作正常，当前节点状态active
- `search` 和 `fetch` 接口返回5xx服务器错误，无法获取资产内容
- 推测是EvoMap服务端正在维护或流量高峰，非客户端配置问题

### Suggested Action
- 等待服务端恢复后再尝试批量拉取高质量资产
- 本地已有知识足够整理本次每日学习汇报，不影响进度

### Metadata
- Source: EvoMap API
- Related Files: evomap_client.py, evomap_config.json
- Tags: evomap, api, availability
- Pattern-Key: evomap.api-outage
- Recurrence-Count: 1
- First-Seen: 2026-03-22
- Last-Seen: 2026-03-22

## [LRN-20260322-002] OpenClaw更新后模块缺失问题

**Logged**: 2026-03-22T02:25:00Z
**Priority**: high
**Status**: pending
**Area**: openclaw, update

### Summary
`openclaw update` 更新后出现模块缺失错误：`Cannot find module .../openclaw/openclaw.mjs`

### Details
- 更新流程显示全局npm包更新成功（49s）
- 但在 `openclaw doctor` 检查阶段报错，找不到入口文件
- 推测更新过程中构建步骤未完成或文件损坏
- 需要后续重新安装修复

### Suggested Action
下次维护时执行 `npm uninstall -g openclaw && npm install -g openclaw` 完整重新安装

### Metadata
- Source: self-experience
- Related Files: openclaw update log
- Tags: openclaw, update, bug
- Pattern-Key: openclaw.update-module-missing
- Recurrence-Count: 1
- First-Seen: 2026-03-22
- Last-Seen: 2026-03-22

---
