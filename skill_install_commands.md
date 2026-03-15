# 强策划 - 技能安装命令
## 执行路径：C:\Users\Administrator\.openclaw\workspace
---

## 🚀 核心技能安装（必须装）

### 1. Tavily搜索（全网搜索，替代Brave）
```bash
openclaw skill install tavily-search
```
配置：安装后输入你的Tavily API密钥即可使用，每天免费1000次请求

### 2. 小红书技能（爬取爆款笔记、热点分析）
```bash
openclaw skill install xiaohongshu
```
功能：搜索小红书爆款内容、获取帖子详情、评论、热点话题分析

### 3. 智能浏览器代理（爬抖音/视频号内容、网页自动化）
```bash
openclaw skill install autoglm-browser-agent
```
功能：自动打开网页、爬取视频文案、模拟操作，支持所有主流平台

### 4. 飞书文档技能（客户资料管理、方案自动生成）
```bash
openclaw skill install feishu-doc
```
功能：自动读写飞书文档、整理客户资料、生成策划方案

---

## ⚡ 效率技能安装（推荐装）

### 5. SEO文案写作（爆款标题、文案优化）
```bash
openclaw skill install seo-content-writer
```
功能：生成SEO优化的文案、标题、脚本，提高内容曝光

### 6. 文案写作（转化型文案、话术优化）
```bash
openclaw skill install copywriting
```
功能：写高转化的短视频文案、销售话术、钩子设计

### 7. OCR文字识别（提取视频/图片中的文案）
```bash
openclaw skill install paddleocr-text-recognition
```
功能：从爆款视频截图、图片中提取文案，快速拆解竞品内容

---

## 📌 安装说明
1. 所有命令直接在PowerShell中执行即可
2. 安装过程中需要输入API密钥的，按照提示输入
3. 安装完成后运行 `openclaw skill list` 查看是否安装成功
4. 安装完需要重启网关生效：`openclaw gateway restart`

---

## ✅ 验证安装
安装完成后测试：
> 帮我搜一下小红书上创始人IP的最新爆款内容

如果能返回结果，说明安装成功。
