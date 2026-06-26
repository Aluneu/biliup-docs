# Skill 集成（AI Agent 扩展）

biliup 提供了 [Skill](https://github.com/biliup/biliup/blob/master/SKILL.md)，允许 AI Agent（如 Codex、Claude、Cursor）直接调用 biliup 命令行工具，让 Agent 成为真正的 up 主。

---

## 快速开始

### 安装 Skill

在支持 Skill 的 AI Agent 环境中运行：

```bash
npx skills add biliup/biliup
```

安装后，Agent 即可识别 biliup 相关指令，自动调用 CLI 进行投稿、录制管理等操作。

---

## 支持的命令

Skill 封装了以下 biliup CLI 子命令，Agent 可根据上下文自动选择：

| 命令 | 说明 |
|---|---|
| `biliup server --auth` | 启动 WebUI 服务（最常用） |
| `biliup login` | 登录 B站并保存登录信息 |
| `biliup upload` | 上传视频 |
| `biliup download` | 下载视频 |
| `biliup list` | 列出所有已上传的视频 |
| `biliup show` | 打印视频详情 |
| `biliup comments` | 查看视频评论 |
| `biliup reply` | 回复视频评论 |
| `biliup renew` | 手动验证并刷新登录信息 |
| `biliup --help` | 查看完整帮助 |

---

## 使用场景示例

### 场景一：Agent 帮你投稿

> **你对 Agent 说：** "帮我把 `video.mp4` 上传到 B站，标题叫「今日直播录像」，分区选「游戏」"

Agent 会自动执行：

```bash
# 1. 登录（如未登录）
biliup login

# 2. 上传
biliup upload video.mp4 --title "今日直播录像" --tid 17
```

### 场景二：Agent 管理录制任务

> **你对 Agent 说：** "帮我启动 biliup，我要录制 B站直播间 123456"

Agent 会自动执行：

```bash
# 启动 WebUI 服务
biliup server --auth

# 然后通过 REST API 添加主播（或由你手动在 WebUI 中操作）
```

### 场景三：Agent 查看投稿状态

> **你对 Agent 说：** "我上次上传的视频现在什么状态？"

Agent 会自动执行：

```bash
biliup list
biliup show <vid>
```

---

## 安装方式对照

Skill 依赖 biliup CLI 本身，请确保环境中已安装 biliup：

| 环境 | 安装方式 |
|---|---|
| Linux / macOS | `uv tool install biliup` |
| Windows | `winget install biliup` 或下载 [Releases](https://github.com/biliup/biliup/releases/latest) 预编译二进制 |
| Docker | 使用官方镜像 `biliup/biliup:latest` |

安装后验证：

```bash
biliup --version
```

---

## 注意事项

- Skill 本身不存储 B站账号信息，登录状态保存在 `cookies.json` 中
- 上传前请确保已通过 `biliup login` 或 WebUI 完成登录
- 使用 `server --auth` 启动服务时，请设置强密码，避免未授权访问
- 详细 CLI 参数请参阅 [命令行参考](/guide/configs/config.html)

---

## 相关链接

- [SKILL.md 源码](https://github.com/biliup/biliup/blob/master/SKILL.md)
- [biliup Releases](https://github.com/biliup/biliup/releases/latest)
- [技能市场（Skills Marketplace）](https://github.com/features/skills)
