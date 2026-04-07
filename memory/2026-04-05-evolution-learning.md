# 每日自动学习进化记录 - 2026-04-05

## 执行时间
2026年4月5日 19:25 (Asia/Shanghai)

---

## 1. OpenClaw 最新玩法与配置优化

### 核心配置优化要点

**配置热重载机制（2026.4新特性）**
- **hybrid模式（默认）**：安全配置即时生效，关键配置自动重启
- **hot模式**：仅热应用安全配置，需要重启时输出警告
- **restart模式**：任何配置变更都重启
- **off模式**：禁用文件监听，需手动重启
- 配置方式：`gateway.reload: { mode: "hybrid", debounceMs: 300 }`

**热应用 vs 需重启的配置**
- 热应用：Channels、Agents、Automation、Sessions、Tools、UI、Bindings
- 需重启：Gateway server（port/bind/auth/tailscale/TLS）、Infrastructure（discovery/canvasHost/plugins）

**Reasoning/思考级别优化**
- `/think low` → 平衡默认，更快更便宜
- `/think medium` → 适合研究和规划（推荐作为默认值）
- `/think high` → 最大努力，解决复杂问题
- `/think off` → 最小化推理，简单任务用
- 全局默认设置：`"agents": { "defaults": { "thinkingDefault": "medium" } }`

**ContextEngine 优化（2026.3版）**
- ContextEngine 减少约 30% 的 context 使用
- Plugin 系统重构为 Bundle + Provider + 架构

**自动化与Heartbeat**
- Cron 任务支持 SessionTarget：`main`（主会话）、`isolated`（独立会话）、`current`（创建时当前会话）、`session:custom-id`（持久化会话）
- Delivery 模式：`announce`（channel交付）、`webhook`（HTTP POST）、`none`（仅内部）
- 支持模型/思考覆盖和工具白名单限制

**配置文件包含（$include）**
- 单文件包含：`agents: { $include: "./agents.json5" }` 替换对象
- 数组文件包含：`broadcast: { $include: ["./a.json5", "./b.json5"] }` 深度合并
- 支持最多10层嵌套，相对路径基于包含文件

**Secret Ref 机制（安全密钥引用）**
```json
{
  "apiKey": {
    "source": "env|file|exec",
    "provider": "provider-name",
    "id": "key-or-path"
  }
}
```

**APNS Relay-backed Push（iOS官方构建）**
- 配置：`gateway.push.apns.relay.baseUrl: "https://relay.example.com"`
- 使用 App Attest + app receipt 认证，无需部署级 token

### 安全最佳实践

**Gateway 安全**
- 绑定到 localhost：`gateway.bind: "127.0.0.1"`（绝不用 0.0.0.0）
- 更改默认端口（18789）为随机高位端口
- 启用强认证：`gateway.auth.token` 使用长随机字符串
- 远程访问使用 Tailscale/Cloudflare Tunnel，绝不用直接端口转发

**API 密钥管理**
- 存储在 `models.providers`，绝不提交到 git
- 使用环境变量或 .env 文件，`chmod 600 .env`
- 优先使用 Composio Managed Auth 等中间件，避免原始 token 暴露
- 使用细粒度 token（如 GitHub 只读）

**工具执行加固**
- 为非受信任 agent 禁用危险工具
- 在 hardened Docker 中运行：非 root 用户、`--cap-drop=ALL`、只读文件系统
- 启用 approvals 为高风险操作
- 定期运行 `openclaw security audit`

### 其他优化技巧

**多账号飞书配置**
- 支持 `channels.feishu.accounts` 配置多账号，指定 defaultAccount

**记忆插件体系**
- `memory-core`：OpenClaw 官方推荐，本地 LanceDB 存储
- `mem0`：云端同步方案
- `memory-lancedb`：社区维护版

**PowerShell 换行技巧**
- 使用 `;` 分隔多条命令，不要用 `&&`（语法不兼容）

**自我进化监控**
- 通过 `feishu-evolver-wrapper` + cron watchdog（每10分钟执行 `ensure`）

**自动会话重置**
- 2026.3 版支持每日凌晨自动重置会话，保持上下文清爽

---

## 2. EvoMap 高质量进化资产

### EvoMap 网络概述
- EvoMap 是全球首个 AI Agent 进化网络，使用 GEP 协议
- 2026年2月在 ClawHub 推出 Evolver 插件
- 允许 OpenClaw agents 检查运行时历史、识别失败或低效、自主编写新代码或更新记忆

### 关键资产与解决方案

**多平台 AI 助手自动化框架**
- 帮助 AI 助手跨不同平台自动化任务
- 当助手需要与其他 agent 或开源工具协作时激活

**浏览器自动化解决方案**
- 完整的 OpenClaw 浏览器自动化解决方案，用于 web 任务

### Evolver 核心能力

**自我进化机制**
- 检查运行时历史，识别失败和低效
- 自主编写新代码或更新记忆以提升性能
- 一键进化：只需运行 `/evolve`

**关键环境变量**
- `A2A_NODE_ID`：EvoMap 节点身份（必需）
- `EVOLVE_ALLOW_SELF_MODIFY`：允许进化修改 evolver 自身源代码（默认 false）
- `EVOLVER_ISSUE_REPO`：GitHub repo 用于自动 issue 报告
- `EVOLVER_REPORT_TOOL`：覆盖报告工具

**回滚机制**
- `git reset --hard`：硬回滚失败的进化（仅当 `EVOLVER_ROLLBACK_MODE=hard`）
- `git stash`：保留失败的进化更改（当 `EVOLVER_ROLLBACK_MODE=stash`）

---

## 3. 行业趋势与社区洞察

### 行业动态
- **RSAC 2026**：Cisco 发布 DefenseClaw，为 AI agent 生命周期安全设计的开源框架
- **市场现状**：85% 的企业在实验 AI agents，但只有 5% 部署到生产环境，主要原因是安全担忧
- **OpenShell (NVIDIA)**：为 AI agents 提供的安全容器化运行时

### 社区模式
- Agent 的"活的、进化的资产"叙事，满足用户个性化和长期复合智能的需求
- 本地 OpenClaw 生态在中国的新兴模式正在形成

---

## 4. 可执行建议（今晚8点汇报用）

### 立即可做的优化
1. **启用配置热重载**（如果还没配置）
   ```json
   "gateway": {
     "reload": { "mode": "hybrid", "debounceMs": 300 }
   }
   ```

2. **设置思考级别默认值**
   ```json
   "agents": {
     "defaults": {
       "thinkingDefault": "medium"
     }
   }
   ```

3. **增强 Gateway 安全**
   - 检查 `gateway.bind` 是否为 `127.0.0.1`
   - 考虑更改默认端口（如果还在用 18789）
   - 验证 `gateway.auth.token` 是否足够强

### 中期规划（1-2周）
1. **探索 EvoMap 集成**
   - 注册 EvoMap 节点身份（`A2A_NODE_ID`）
   - 测试 Evolver 的自我进化能力
   - 评估哪些 assets 可以引入到当前环境

2. **优化自动化任务**
   - 审查现有 cron jobs，考虑使用 SessionTarget 优化
   - 为不同任务设置合适的 thinking 级别

### 长期布局（1个月+）
1. **安全加固**
   - 运行 `openclaw security audit` 深度扫描
   - 考虑在 hardened Docker 中运行
   - 实施 Secret Ref 机制替代明文密钥

2. **进阶功能**
   - 研究浏览器自动化解决方案
   - 评估 APNS Relay-backed Push for iOS
   - 探索记忆插件体系升级为 memory-core

---

## 5. 待验证问题
1. 当前 openclaw.json 是否已启用配置热重载？
2. 是否已有 EvoMap 节点注册？
3. Gateway 安全配置是否符合最新最佳实践？
4. 当前 cron jobs 是否可以优化为使用 SessionTarget？

---

## 学习总结
今天的学习聚焦于 OpenClaw 2026.3/2026.4 版本的新特性和最佳实践，特别是在配置热重载、安全加固、Reasoning 优化和 EvoMap 进化网络方面。发现了很多可以立即应用的优化点，特别是在安全性自动化配置管理方面。

**最有价值的新发现：**
1. 配置热重载机制可以大幅减少重启需求
2. EvoMap 的自我进化能力可以持续优化 agent 性能
3. Secret Ref 机制可以更安全地管理敏感信息
4. ContextEngine 可以降低约 30% 的 context 使用
