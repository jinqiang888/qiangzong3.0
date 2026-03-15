# 飞书机器人无响应排查指南
## 当前现象：给强策划发消息没有反应
---

## 🔍 第一步：检查飞书开放平台配置（90%的问题出在这里）
### 1. 检查机器人是否启用
- 飞书开放平台 → 应用 → 应用能力 → 机器人
- 确认「机器人功能」是**启用**状态
- 确认机器人名称和头像已设置

### 2. 检查权限是否已申请并通过
- 进入「权限管理」
- 确认以下权限已**申请并审核通过**（状态显示「已获得」）：
  ✅ `im:message` - 发送消息
  ✅ `im:message.p2p_msg` - 接收单聊消息
  ✅ `im:message.p2p_msg:readonly` - 读取单聊消息
  ✅ `contact:user.id:readonly` - 获取用户信息
- 如果权限是「待审核」状态，需要找企业管理员通过审核

### 3. 检查事件订阅配置
- 进入「事件订阅」
- 确认「请求网址」已正确填写，并且显示「验证成功」
- 确认已订阅以下事件：
  ✅ `接收消息v2.0`（im.message.message_receive_v1）
  ✅ `消息已读`（可选）
- **重要**：事件订阅的请求网址必须是**公网可访问**的，本地地址（localhost/127.0.0.1）飞书访问不到

### 4. 检查应用是否已发布
- 进入「版本管理与发布」
- 确认有已发布的版本，状态是「已上线」
- 确认可见范围包含你自己（测试可以先选「全部成员」）

---

## 🔧 第二步：检查本地OpenClaw配置
### 1. 检查网关是否正常运行
在PowerShell中执行：
```bash
openclaw gateway status
```
应该显示「running」状态，如果是停止状态，执行：
```bash
openclaw gateway start
```

### 2. 检查飞书配置是否正确
执行：
```bash
openclaw config get channels.feishu
```
确认输出的：
- `appId` 是 `cli_a93c6c21e5f89cb0`
- `appSecret` 是 `smtZc5KePxJufG0F3NkX8gd7TcLHkWXg`
- `enabled` 是 `true`
- `allowFrom` 包含你的open_id：`ou_01080b390e23107f3ff33904dba77a02`

### 3. 查看网关日志，看是否收到飞书消息
执行：
```bash
openclaw logs --tail 50
```
给机器人发消息后，看日志中是否有新的请求进入，如果没有，说明飞书的事件没推过来。

---

## 🚀 快速测试方法（先解决公网问题）
如果没有公网IP，可以先使用内网穿透工具：
1. 下载ngrok：https://ngrok.com/download
2. 执行：`ngrok http 18788`
3. 把得到的公网地址（比如 `https://xxx.ngrok.io`）填到飞书事件订阅的请求网址里，后面加 `/feishu/webhook`，完整地址是：`https://xxx.ngrok.io/feishu/webhook`
4. 验证地址，保存
5. 再发消息测试

---

## ✅ 临时解决方案
如果你现在就要测试功能，可以直接在当前对话中发指令测试，比如：
> 给我3个创始人IP的爆款选题

我会直接返回结果，等机器人配置好后就能自动回复了。
