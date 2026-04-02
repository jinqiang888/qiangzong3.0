# 每日学习汇总 - 2026年4月3日

## 📋 任务概述
执行时间：2026-04-03 02:00 (UTC: 2026-04-02 18:00)
执行人：强总（自动学习cron）
目标：搜索OpenClaw最新玩法技巧、访问EvoMap获取进化资产、整理汇报内容

---

## 🆕 OpenClaw 2026.4.1 最新更新（2026-04-01发布）

### 核心新功能

#### 1. 任务管理升级
- **`/tasks`命令**：聊天原生后台任务面板，可查看当前会话的最近任务详情
- 当没有关联任务时，显示agent本地回退计数

#### 2. Web搜索增强
- **SearXNG插件**：新增bundled SearXNG provider插件，支持可配置的host
- 使用：`web_search`工具可通过SearXNG进行搜索

#### 3. Amazon Bedrock Guardrails支持
- bunded provider新增Bedrock Guardrails支持
- 提供企业级安全护栏功能

#### 4. macOS Voice Wake（语音唤醒）
- 新增Voice Wake选项，可触发Talk Mode
- 配置位置：macOS语音设置

#### 5. 飞书评论协作
- **飞书Drive评论事件流**：专用评论事件处理
- 支持评论线程上下文解析
- 支持线程内回复
- 新增`feishu_drive comment actions`用于文档协作工作流

#### 6. WebChat配置优化
- **聊天历史截断可配置**：`gateway.webchat.chatHistoryMaxChars`
- 支持per-request maxChars
- 保持静默回复过滤和现有payload限制

#### 7. Agent默认参数
- **`agents.defaults.params`**：全局默认provider参数
- 统一管理所有agent的默认参数

#### 8. Agent故障转移优化
- 同一provider的prompt-side和assistant-side auth-profile重试限流
- 跨provider model fallback前的auth冷却
- 新增`auth.cooldowns.rateLimitedProfileRotations`配置

#### 9. Cron工具白名单
- **`openclaw cron --tools`**：per-job工具白名单
- 限制特定cron任务可用的工具，提升安全性

#### 10. Channel会话路由改进
- provider-specific会话对话语法移至plugin-owned session-key surfaces
- 保留Telegram topic路由和飞书scope继承
- 覆盖bootstrap、model override、restart、tool-policy路径

#### 11. WhatsApp反应增强
- **`reactionLevel`指导**：agent reactions的反应级别指导
- 更自然的对话交互

#### 12. Telegram错误处理
- **`errorPolicy`和`errorCooldownMs`**：可配置的错误策略和冷却时间
- 按account、chat、topic抑制重复投递错误
- 不静默不同的失败

#### 13. Z.AI模型扩展
- 新增`glm-5.1`和`glm-5v-turbo`模型

#### 14. Agent压缩一致性
- **`agents.defaults.compaction.model`**：手动`/compact`和其他context-engine compaction路径一致解析
- engine-owned compaction使用配置的override model

---

## 🔧 重要修复

### 安全性修复
1. **聊天错误回复**：停止向外部聊天频道泄露原始provider/runtime失败，返回友好的重试消息
2. **Bedrock工具结果**：添加特定`/new`提示，解决toolResult/toolUse会话不匹配

### Gateway优化
3. **配置重载**：忽略启动时的配置写入（持久化哈希），避免重启循环
4. **任务Gateway**：防止任务注册维护sweep因SQLite压力阻塞Gateway事件循环
5. **HTTP请求**：跳过失败的HTTP请求阶段，避免一个失败facade导致所有HTTP端点返回500

### 任务管理
6. **任务状态**：在`/status`和`session_status`中隐藏陈旧的已完成任务
7. **任务清理**：清理前重新检查当前任务记录

### Exec审批
8. **审批默认值**：内联或配置工具策略未设置时，尊重exec-approvals.json安全默认值
9. **Allow-always持久化**：allow-always持久化为耐用的用户批准信任，不再像allow-once一样行为
10. **Shell包装器**：对不能持久化可执行allowlist条目的shell包装器路径重用精确命令信任
11. **Windows执行计划**：Windows无法构建allowlist执行计划时，要求显式批准

### 会话和模型
12. **模型切换**：`/model`变更在繁忙运行后排队，不中断活动轮次
13. **后续任务重定向**：重定向排队后续，以便后续工作在当前轮次结束后立即接收新模型

### Node管理
14. **Node命令**：停止将活动node命令固定到已批准的node配对记录
15. **Node配对**：保持node配对为信任/token流程，per-node system.run策略保留在node的exec审批配置中

### Channel特定修复
16. **Discord媒体**：Discord附件和sticker下载通过共享空闲超时和worker中止路径
17. **Telegram重试**：非幂等发送保持严格安全发送路径，重试包装预连接失败
18. **Telegram审批**：topic感知exec审批后续通过Telegram-owned threading和审批目标解析路由
19. **WhatsApp时间戳**：向模型上下文传递入站消息时间戳

---

## 🎯 2026.4.x 系列更新亮点（2026-03-31发布）

### Breaking Changes
1. **Node exec**：移除CLI和agent nodes工具中重复的`nodes.run` shell包装器
2. **Plugin SDK**：弃用旧版provider compat子路径和bundled provider设置
3. **安全安装**：内置危险代码关键发现和安装时扫描失败现在默认失败关闭
4. **Gateway认证**：trusted-proxy拒绝混合共享token配置
5. **Node命令**：node命令在node配对批准前保持禁用
6. **Node事件**：node发起的运行保持在减少的信任表面

### 重大功能更新
1. **Background Tasks统一控制面**
   - 统一ACP、subagent、cron和后台CLI执行到SQLite账本
   - 添加审计/维护/状态可见性
   - 改进自动清理和丢失运行恢复
   - 阐明heartbeat/main-session自动化和分离计划运行之间的分离

2. **QQ Bot Channel**
   - 新增bundled channel插件
   - 多账号设置、SecretRef感知凭据、slash命令、提醒、媒体发送/接收

3. **LINE出站媒体**
   - 新增LINE图片、视频、音频出站发送
   - 视频的显式预览/跟踪处理

4. **Matrix增强**
   - **历史上下文**：`channels.matrix.historyLimit`可选房间历史上下文
   - **代理**：`channels.matrix.proxy`显式代理配置
   - **流式传输**：部分Matrix回复更新同一消息
   - **线程**：per-DM threadReplies覆盖

5. **MCP远程支持**
   - 远程HTTP/SSE服务器支持`mcp.servers` URL配置
   - 包括auth headers和更安全的配置编辑

6. **Pi/Codex原生web搜索**
   - 嵌入Pi运行的原生Codex web搜索支持
   - 包括config/docs/wizard覆盖

7. **Slack exec审批**
   - 原生Slack审批路由和审批者授权
   - exec审批提示可留在Slack中

8. **WhatsApp reactions**
   - agents可以emoji反应入站WhatsApp消息

---

## 🚀 配置优化建议（基于2026.4更新）

### 1. 启用配置热重载（推荐）
```json5
{
  gateway: {
    reload: {
      mode: "hybrid",
      debounceMs: 300
    }
  }
}
```

### 2. 配置WebChat历史截断
```json5
{
  gateway: {
    webchat: {
      chatHistoryMaxChars: 50000
    }
  }
}
```

### 3. Agent默认参数（统一管理）
```json5
{
  agents: {
    defaults: {
      params: {
        temperature: 0.7,
        maxTokens: 4096
      },
      compaction: {
        model: "anthropic/claude-sonnet-4"
      }
    }
  }
}
```

### 4. Cron任务工具使用限制（安全最佳实践）
```bash
openclaw cron --tools
```
在cron配置中添加：
```json5
{
  toolsAllow: ["exec", "read", "web_search"]
}
```

### 5. Auth冷却配置
```json5
{
  auth: {
    cooldowns: {
      rateLimitedProfileRotations: 3
    }
  }
}
```

### 6. Telegram错误策略
```json5
{
  channels: {
    telegram: {
      errorPolicy: "suppress",
      errorCooldownMs: 300000
    }
  }
}
```

---

## 📊 建议的升级行动计划

### 立即执行（本周）
1. ✅ 检查当前OpenClaw版本
2. ✅ 运行`openclaw update`升级到2026.4.1
3. ✅ 备份`openclaw.json`配置文件
4. ✅ 审查breaking changes对当前配置的影响

### 短期优化（1-2周）
1. 配置WebChat历史截断
2. 设置Agent默认参数
3. 为敏感cron任务添加工具白名单
4. 配置Telegram错误策略

### 中期规划（1个月）
1. 测试新的`/tasks`命令集成到工作流
2. 启用飞书评论DRIVE功能
3. 如果使用Amazon Bedrock，配置Guardrails
4. 如果使用macOS，测试Voice Wake

### 长期规划（3个月+）
1. 评估是否需要QQ Bot或LINE channel
2. 测试MCP远程服务器集成
3. 评估Background Tasks统一控制面的使用

---

## ⚠️ 潜在风险提示

1. **安全安装变更**：plugin install现在默认失败关闭，如果有自动安装流程需要添加`--dangerously-force-unsafe-install`
2. **Node命令配对**：需要显式批准node配对才能使用node命令
3. **Node事件信任表面**：node触发的流程现在在减少的信任表面上运行，可能需要调整自动化流程
4. **Exec审批变更**：allow-always行为改变，现在持久化为耐用的信任

---

## 📝 待深入研究的问题

1. EvoMap访问需要配置，暂时无法获取进化资产
2. 需要评估新功能对当前工作流的具体影响
3. 需要测试Breaking Changes对现有自动化流程的影响
4. 需要了解SearXNG的具体配置和使用方法

---

## 🎓 关键学习点

1. **配置管理**：2026.4引入更细粒度的配置热重载机制
2. **任务管理**：Background Tasks成为一等公民，统一管理所有后台工作
3. **安全增强**：Exec审批、Node命令、Plugin安装都有重要安全增强
4. **Channel扩展**：QQ Bot、LINE、Matrix等新channel支持更广泛的应用场景
5. **Agent优化**：故障转移、压缩、默认参数等方面有重要改进

---

**汇报完成时间**：2026-04-03 02:10
**下次汇报计划**：2026-04-04 08:00
**负责人**：强总
