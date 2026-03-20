# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

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

### 最新玩法与技巧（2026.3更新）
1. **多账号飞书配置**：支持同一个飞书开放平台下多个应用在不同频道使用，通过 `channels.feishu.accounts` 配置多账号，指定defaultAccount
2. **记忆插件体系**：支持 mem0、memory-core、memory-lancedb 多种向量记忆后端，可在 `plugins` 配置启用
3. **PowerShell换行技巧**：Windows PowerShell中使用 `;` 分隔多条命令，不要使用 `&&`（语法不兼容）
4. **自我进化监控**：通过 `feishu-evolver-wrapper` + cron watchdog（每10分钟执行 `ensure`）保证进化进程稳定运行
5. **技能安装**：通过 `clawhub install <skill-name>` 从 ClawHub 安装社区技能

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
