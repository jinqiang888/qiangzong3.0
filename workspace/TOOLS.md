# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## OpenClaw Configuration Best Practices (Learned 2026-03-17)

### Core Configuration
- Edit `SOUL.md`, `IDENTITY.md`, `USER.md` directly to shape behavior
- `openclaw.json` key settings:
  - `gateway.bind: "127.0.0.1"` (never 0.0.0.0)
  - Change default port (18789) to random high port for security
  - Set `agents.defaults.thinkingDefault: "medium"` as global default
  - Store API keys in `models.providers`, never commit to git

### Reasoning Levels
- `/think low` → balanced default, faster cheaper
- `/think medium` → good for research/planning (recommended default)
- `/think high` → max effort for hard problems
- `/think off` → minimal reasoning for simple tasks

### Optimization
- Use qmd to summarize long threads/research before processing
- Route simple tasks to local models, heavy reasoning to cloud
- Add Brave Search API key for default web search

### Security
- Store API keys in `.env` with `chmod 600` permissions
- Remote access via Tailscale/Cloudflare Tunnel, never direct port forward
- Disable risky tools for non-trusted agents
- Run `openclaw security audit` regularly

### Automation
- Use cron for recurring research/reporting tasks
- Enable heartbeat for daily checks and automatic updates
- Run `openclaw update` periodically to get latest skills
- **新功能：** 2026.3版支持session自动重置，每日凌晨自动重置会话，保持上下文清爽

### 最新玩法与技巧（2026.4更新）

#### 配置热重载机制
- **hybrid模式（默认）**：安全配置即时生效，关键配置自动重启
- **hot模式**：仅热应用安全配置，需要重启时输出警告
- **restart模式**：任何配置变更都重启
- **off模式**：禁用文件监听，需手动重启
- 配置：`gateway.reload: { mode: "hybrid", debounceMs: 300 }`
- 热应用：Channels、Agents、Automation、Sessions、Tools、UI、Bindings
- 需重启：Gateway server（port/bind/auth/tailscale/TLS）、Infrastructure（discovery/canvasHost/plugins）

#### Cron任务高级特性
- **SessionTarget**：`main`（主会话heartbeat）、`isolated`（独立会话）、`current`（创建时当前会话）、`session:custom-id`（持久化会话）
- **Delivery模式**：`announce`（channel交付）、`webhook`（HTTP POST）、`none`（仅内部）
- **模型/思考覆盖**：`model: "anthropic/claude-sonnet-4"`、`thinking: "high"`
- **工具白名单**：`toolsAllow: ["exec", "read"]` 限制job可用工具
- **轻量级引导**：`lightContext: true` 不注入workspace bootstrap文件
- **Topic交付（Telegram）**：`to: "-1001234567890:topic:123"` 发送到指定话题

#### 配置文件包含（$include）
- 单文件：`agents: { $include: "./agents.json5" }` 替换对象
- 数组文件：`broadcast: { $include: ["./a.json5", "./b.json5"] }` 深度合并
- 支持最多10层嵌套，相对路径基于包含文件

#### Secret Ref机制
```json
{
  "apiKey": {
    "source": "env|file|exec",
    "provider": "provider-name",
    "id": "key-or-path"
  }
}
```
- `env`：环境变量
- `file`：文件读取
- `exec`：命令执行获取

#### APNS Relay-backed Push（iOS官方构建）
- 配置：`gateway.push.apns.relay.baseUrl: "https://relay.example.com"`
- Gateway无需部署级token，使用App Attest + app receipt认证
- 仅限官方/TestFlight构建，本地构建仍用直接APNs

#### 其他技巧（2026.3保留）
1. **多账号飞书配置**：支持同一个飞书开放平台下多个应用在不同频道使用，通过 `channels.feishu.accounts` 配置多账号，指定defaultAccount
2. **记忆插件体系**：支持 mem0、memory-core、memory-lancedb 多种向量记忆后端，可在 `plugins` 配置启用
   - `memory-core`：OpenClaw官方推荐，本地LanceDB存储，内置意图隔离防记忆污染
   - `mem0`：云端同步方案，适合多设备访问
   - `memory-lancedb`：社区维护版，更多自定义选项
3. **PowerShell换行技巧**：Windows PowerShell中使用 `;` 分隔多条命令，不要使用 `&&`（语法不兼容）
4. **自我进化监控**：通过 `feishu-evolver-wrapper` + cron watchdog（每10分钟执行 `ensure`）保证进化进程稳定运行
5. **技能安装**：通过 `clawhub install <skill-name>` 从 ClawHub 安装社区技能
6. **自动会话重置**：2026.3版支持每日凌晨自动重置会话，保持上下文清爽，避免累积膨胀
7. **配置备份**：OpenClaw会自动备份 `openclaw.json` 带日期后缀，更新出错可快速回滚

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
