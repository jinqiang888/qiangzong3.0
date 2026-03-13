# 🧠 MEMORY.md - 长期记忆

> 最后更新：2026-03-13
> 这是精炼后的长期记忆，原始日志见 `memory/YYYY-MM-DD.md`

---

## ⚠️ 安全红线
- **服务器绝对不能暴露在外网！**
- Gateway 绑定 loopback (127.0.0.1)
- 防火墙不开端口
- 任何涉及网络暴露的操作必须先征求用户同意

## 🔧 系统配置
- AutoClaw Gateway 端口：18788
- OpenClaw 版本：2026.3.12
- 模型：zai/zai_pony-alpha-2
- Embedding：OpenAI text-embedding-3-small
- 飞书已连接（流式输出已开启）
- Tavily 搜索已配置
- 自动备份：每天 3:00 AM → GitHub jinqiang888/qiangzong2.0

## 📋 用户信息
- 用户名：jinqiang888
- 称呼：暂未填写
- 时区：Asia/Shanghai
- GitHub：jinqiang888 (huangjinqinag999@gmail.com)
- 飞书 open_id：ou_665c60d83c6b1a2d49b9ced94edb4aa7

## 🎯 重要决策
- 备份仓库使用 qiangzong2.0（另一个实例用 qiangzong3.0，已合并）
- 记忆系统采用三层架构（会话/文件/语义搜索）

## 📝 偏好与习惯
- 命令用代码块格式，方便一键复制
- 优先复用现有能力，不重复造轮子

## 💡 经验教训
- 换端口时要注意配置文件（openclaw.json）和服务脚本（gateway.cmd）两处都要改
- AutoClaw 的端口是桌面应用管理的，不能通过命令行直接改
- Windows 下 SSH 密钥空密码用 `-N '""'` 而非 `-N ""`
- 飞书插件重复 ID 警告不影响功能
- 修改配置后需重启网关才生效
- **绝对禁止模拟执行**：所有操作必须真实落地，禁止只回复不干活

## 📌 待办
- [ ] 确认用户的真实姓名和称呼
- [ ] 确定我的名字、人设和签名 emoji
- [ ] 配置阿里云百炼模型（待用户提供 API Secret 和区域）
