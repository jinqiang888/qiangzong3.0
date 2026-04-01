# 学习笔记 - 2026-04-02

## OpenClaw配置热重载机制（重要新发现）
**日期：** 2026-04-02
**来源：** OpenClaw官方文档

### 核心发现
OpenClaw支持四种配置热重载模式：
- **hybrid（默认）**：安全配置即时生效，关键配置自动重启
- **hot**：仅热应用安全配置，需重启时输出警告
- **restart**：任何配置变更都重启
- **off**：禁用文件监听，需手动重启

### 热应用配置（无需重启）
- Channels所有配置
- Agents & models
- Automation（hooks, cron, heartbeat）
- Sessions & messages
- Tools & media
- UI & misc
- Bindings

### 需重启配置
- Gateway server：port, bind, auth, tailscale, TLS, HTTP
- Infrastructure：discovery, canvasHost, plugins

### 实用配置
```json
{
  "gateway": {
    "reload": {
      "mode": "hybrid",
      "debounceMs": 300
    }
  }
}
```

---

## Cron任务高级特性
**日期：** 2026-04-02
**来源：** OpenClaw官方文档

### SessionTarget新机制
- `main`：在主会话的下次heartbeat运行（系统事件）
- `isolated`：独立会话 `cron:<jobId>`，默认announce输出
- `current`：绑定到创建时的当前会话
- `session:custom-id`：持久化命名会话，保留上下文

### Delivery交付模式
- `announce`：直接通过channel adapter交付
- `webhook`：POST到指定URL
- `none`：仅内部运行，不交付

### 模型和思考级别覆盖
```json
{
  "payload": {
    "model": "anthropic/claude-sonnet-4-20250514",
    "thinking": "high"
  }
}
```

### 工具白名单（安全性）
```json
{
  "toolsAllow": ["exec", "read", "write"]
}
```

### 轻量级引导上下文
```json
{
  "lightContext": true
}
```
不注入workspace bootstrap文件，适合高频低复杂度任务

---

## 配置文件包含（$include）
**日期：** 2026-04-02
**来源：** OpenClaw官方文档

### 单文件包含
```json
{
  "agents": {
    "$include": "./agents.json5"
  }
}
```
替换对象

### 数组文件包含
```json
{
  "broadcast": {
    "$include": ["./a.json5", "./b.json5"]
  }
}
```
深度合并（后覆盖前），支持最多10层嵌套

---

## Secret Ref机制
**日期：** 2026-04-02
**来源：** OpenClaw官方文档

### 三种secret来源
```json
{
  "apiKey": {
    "source": "env|file|exec",
    "provider": "provider-name",
    "id": "key-or-path"
  }
}
```
- `env`：从环境变量读取
- `file`：从文件读取
- `exec`：通过命令执行获取

---

## APNS Relay-backed Push
**日期：** 2026-04-02
**来源：** OpenClaw官方文档

### iOS官方构建的push通知机制
```json
{
  "gateway": {
    "push": {
      "apns": {
        "relay": {
          "baseUrl": "https://relay.example.com",
          "timeoutMs": 10000
        }
      }
    }
  }
}
```

### 核心特性
- Gateway不需要部署级relay token
- 使用App Attest + app receipt进行认证
- 仅限官方/TestFlight构建使用
- 本地/手动构建仍用直接APNs

---

## 应用场景
1. **配置热重载**：开发环境用hot模式，生产环境用hybrid模式
2. **Cron工具白名单**：安全敏感任务限制可用工具
3. **$include**：拆分大型配置文件，模块化管理
4. **Secret Ref**：敏感信息不直接写在配置文件中
5. **APNS Relay**：大规模iOS部署的push通知方案

---

## 下一步行动
- [x] 更新TOOLS.md记录新知识
- [x] 创建学习笔记
- [ ] 探索EvoMap获取进化资产
- [ ] 实践配置热重载机制
- [ ] 测试Cron高级特性
