# 🧠 MEMORY.md - 长期记忆库

这里是我的长期记忆，存储重要的决策、偏好、经验教训和关键信息。
只有在主会话（和你的直接对话）中才会加载，不会在群聊或共享场景中泄露。

---

## 🔧 系统配置
1. **Git配置**：
   - 用户名：jinqiang888
   - 邮箱：huangjinqinag999@gmail.com
   - SSH公钥：ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPUGY43ws89XAJmnSPKGhwtmn9ZSdc1KV1mPrN7j0Dou github@example.com

2. **飞书配置**：
   - 已开启流式输出（channels.feishu.streaming = true）
   - 已开启消息底部耗时显示（channels.feishu.footer.elapsed = true）
   - 已开启消息底部状态展示（channels.feishu.footer.status = true）

3. **OpenClaw版本**：2026.3.8 (3caab92)
4. **默认模型**：volcengine-plan/ark-code-latest

---

## 📝 用户信息
- 用户名：jinqiang888
- GitHub邮箱：huangjinqinag999@gmail.com

---

## 🎯 核心工作原则
1. **杜绝重复造轮子**：遇到重复的工作流，主动将其打包成可复用的技能，避免重复劳动
2. **优先复用现有能力**：处理任务前先检查已有技能和工具，能用现有能力解决的绝不重新开发
3. **代码可复用性优先**：编写代码和工作流时考虑通用性，方便后续复用

---

## 💡 经验教训
1. Windows系统下生成SSH密钥时，空密码参数需要用 `-N '""'` 而不是 `-N ""`
2. 飞书插件重复ID警告不影响正常功能使用，无需特殊处理
3. 修改配置后需要重启网关才能生效
