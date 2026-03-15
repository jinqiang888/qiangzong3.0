# 飞书机器人（强策划）配置指南

## 🚀 已完成的配置
✅ 应用凭证已更新：
- AppID: `cli_a93c6c21e5f89cb0`
- AppSecret: `smtZc5KePxJufG0F3NkX8gd7TcLHkWXg`
✅ OpenClaw网关配置已更新并重启
✅ 机器人名称已定为：**强策划**

---

## 🔧 接下来需要在飞书开放平台完成的配置
### 1. 开启机器人能力
- 进入飞书开放平台 → 你的应用 → 应用能力 → 机器人
- 点击「启用机器人」
- 填写机器人信息：
  - 名称：强策划
  - 描述：创始人IP/短视频获客专属AI策划师
  - 头像：上传你设计的头像
- 保存

### 2. 配置权限（必须开启）
进入「权限管理」，添加以下权限：
- `im:message` - 发送消息
- `im:message.group_at_msg` - 获取群组中@机器人的消息
- `im:message.group_at_msg:readonly` - 接收群组中@机器人的消息
- `im:message.p2p_msg` - 获取用户发给机器人的单聊消息
- `im:message.p2p_msg:readonly` - 接收用户发给机器人的单聊消息
- `im:chat:readonly` - 获取群组信息
- `contact:user.id:readonly` - 获取用户基本信息

全部权限添加后，点击「批量申请」，等待企业管理员审核通过。

### 3. 配置事件订阅
进入「事件订阅」：
- 加密策略：选择「明文模式」（先测试，后续可以改成加密）
- 请求网址：填 `wss://gateway.openclaw.ai/feishu/webhook` 或者你自己的公网地址 + `/feishu/webhook`
- 订阅事件：添加以下事件：
  - `接收消息v2.0`（im.message.message_receive_v1）
  - `消息已读`（im.message.message_read_v1）
- 点击「保存」，验证地址是否能连通

### 4. 配置版本与发布
- 进入「版本管理与发布」→ 创建新版本
- 填写版本号、更新说明
- 选择可见范围（可以先选「全部成员」或指定测试用户）
- 提交审核，发布上线

---

## ✅ 验证配置是否成功
发布后，在飞书中搜索「强策划」，发消息测试：
> 给我几个创始人IP的爆款选题

如果能正常回复，说明配置成功。

---

## 📌 可选配置
如果需要接收图片、文件等消息，还需要添加：
- `im:message.resource:readonly` - 下载消息中的文件/图片资源
- `drive:file:readonly` - 读取云文档资源
