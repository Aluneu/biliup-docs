# biliup 文档站结构说明（开发者指南）

> 本文档说明文档站（VitePress）的目录结构、侧边栏生成机制、路由规则与日常维护流程，便于开发者新增 / 修改文档。

---

## 1. 概述

| 项 | 值 |
|---|---|
| 技术栈 | [VitePress](https://vitepress.dev/) |
| 源码根目录 | `docs/` |
| 部署地址 | `https://aluneu.github.io/biliup-docs/` |
| base 路径 | `/biliup-docs/`（所有内部链接、资源都基于此） |
| 本地构建 | `npm run docs:build`（`vitepress build docs`） |
| 本地开发（热更新） | `npm run docs:dev` |
| 部署方式 | 推送到 `main` 分支后由 GitHub Actions 自动构建并发布 |

> ⚠️ `dist/` 是构建产物，通常被 gitignore，无需手动提交。

---

## 2. 目录结构

```
biliup-docs/
├── docs/                         # 所有文档源码
│   ├── index.md                  # 站点根页（通常重定向/引导到首页）
│   ├── sponsor/                  # 赞助页
│   ├── public/                   # 静态资源（图片、favicon 等）
│   └── guide/                    # 主要内容目录（侧边栏由它生成）
│       ├── introduce/            # 首页 + 快速开始 + 配置 + 架构
│       │   └── introduce/
│       │       └── introduce.md  # ★ 站点首页（自定义结构 + CSS）
│       ├── 安装部署/             # Linux / Windows / Docker 安装
│       ├── 基础配置/             # 首次运行等
│       ├── 进阶运行/             # 进阶命令
│       ├── 开发指南/             # 开发者向文档
│       ├── live/                 # 各直播平台独立页（斗鱼/虎牙/抖音…）
│       ├── configs/              # CLI / 配置参考
│       ├── webui/                # WebUI 使用
│       ├── api/                  # REST API
│       ├── skill/                # skill 子命令
│       ├── changelog/            # 更新日志
│       ├── docs/                 # ffmpeg 等环境依赖说明
│       ├── help.md               # 帮助与反馈
│       ├── login.md              # 登录方式
│       ├── faq.md                # 常见问题
│       ├── mapping.json          # ★ 侧边栏显示名映射
│       ├── set_sidebar.mts       # ★ 侧边栏自动生成脚本
│       └── GenerateMapping.ps1   # 辅助生成 mapping.json
├── docs/.vitepress/              # VitePress 配置
│   ├── config.mts                # 站点配置（nav / 插件 / markdown）
│   └── theme/
│       ├── custom.css            # ★ 全站自定义样式（首页装饰类都在这里）
│       ├── index.ts
│       └── style/ / styles/      # 主题细节
└── package.json                  # scripts: docs:dev / docs:build / docs:preview
```

---

## 3. 侧边栏自动生成机制

侧边栏**不是手写**的，而是由 `docs/guide/set_sidebar.mts` 扫描 `docs/guide/` 目录树自动生成。

- 每个 `.md` 在侧边栏的**显示名**取自 `mapping.json` 的键 `"文件名.md"`。
- 若 `mapping.json` 中**缺少该文件条目**，会回退显示成文件名本身（**带 `.md` 后缀**，例如 `抖音.md`）——这是最常见的“侧边栏显示怪名”根因。
- 目录层级 = 侧边栏分组层级。

### 新增一个页面的标准动作

1. 在 `docs/guide/` 下合适子目录新建 `xxx.md`。
2. 在 `mapping.json` 追加一条：`"xxx.md": "显示名"`。
3. 构建验证（`npm run docs:build`），确认侧边栏显示的是“显示名”而非“xxx.md”。

> 提示：`GenerateMapping.ps1` 可辅助批量生成 mapping，但最终以手写 key 为准。

---

## 4. 路由与内部链接规则（最重要）

VitePress 的线上 URL **镜像源码目录结构**，与文件位置一一对应：

| 源文件 | 线上地址 |
|---|---|
| `docs/guide/introduce/Config/GlobalConfig.md` | `/biliup-docs/guide/introduce/Config/GlobalConfig.html` |
| `docs/guide/introduce/introduce/introduce.md` | `/biliup-docs/guide/introduce/introduce/introduce.html` |

**写内部链接时必须遵守：**

1. **用 `.html` 后缀**（不是 `.md`）。
2. **相对路径深度要正确**——从当前页位置推算 `../` 层数。
   - 例：从 `introduce/introduce/introduce.md` 链接到同级的 `Config/GlobalConfig.md`：
     `./Config/GlobalConfig.html`（同级，1 个 `./`）
   - 例：从 `introduce/introduce/` 链接到上一级 `configs/config.md`：
     `../../configs/config.html`（上两级，2 个 `../`）
3. **跨目录引用务必数清 `../`**，多写或少写一级都会 404。

> 排错口诀：线上 404 时，先看源文件真实路径，再核对链接里 `../` 的层数，最后确认目标文件真实存在。

---

## 5. 首页（introduce.md）结构

首页是**唯一使用自定义 HTML + CSS 装饰**的页面，位置：
`docs/guide/introduce/introduce/introduce.md`

当前由 4 个区块组成（顺序即页面顺序）：

| 区块 | 标题 | 说明 |
|---|---|---|
| 上手流程 | `## 🚀 上手流程` | 4 步按钮（安装→快速入门→配置→交流群），可点击 |
| 工作原理 | `## ⚙️ 工作原理` | 3 节点轻量流程图（监测开播→录制→上传投稿），不可点 |
| 选择安装方式 | `## 📦 选择安装方式` | 3 张卡片（Linux/Windows/Docker） |
| 深入了解 | `## 📚 深入了解` | 分组卡片：核心功能(4) + 支持与帮助(2) |

### 对应的自定义 CSS 类（均在 `docs/.vitepress/theme/custom.css`）

| 用途 | 类名 |
|---|---|
| 上手流程横幅容器 | `.gs-path` |
| 单步按钮 | `.gs-step` |
| 步骤间箭头 | `.gs-arrow` |
| 序号徽标（渐变圆） | `.gs-num` |
| 工作原理流程容器 | `.arch-flow` |
| 原理节点 | `.arch-node` |
| 原理节点图标 | `.arch-icon` |
| 卡片网格容器 | `.link-grid` / `.link-grid-3` / `.link-grid-2` |
| 单张卡片 | `.link-item` |
| 卡片图标 | `.link-icon` |

> 设计约定：首页是**入口/指路页**，不是营销落地页，也不是导航墙。新增内容请复用上述类，保持全页一套视觉语言；不要堆砌重复侧边栏已有信息的卡片。

---

## 6. 样式定制

- **唯一手写样式入口**：`docs/.vitepress/theme/custom.css`。
- 配色遵循 VitePress 设计变量（如 `--vp-c-brand`、`--vp-c-text-1/2`、`--vp-c-bg`、`--vp-c-gutter`），明暗主题自动适配，**不要硬编码颜色**。
- 品牌色：靛蓝 `#6366f1` → 粉 `#fb7299`（biliup 粉）渐变，仅用于强调元素。

---

## 7. 本地预览

```bash
# 开发模式（热更新，推荐改文档时用）
npm run docs:dev

# 或：构建后静态预览产物
npm run docs:build
# 然后用任意静态服务器打开 docs/.vitepress/dist/（注意 base=/biliup-docs/）
```

---

## 8. 新增 / 修改文档标准流程（Checklist）

- [ ] 在 `docs/guide/` 对应子目录新建或编辑 `.md`
- [ ] **新页面**：在 `docs/guide/mapping.json` 加 `"文件名.md": "显示名"`
- [ ] 内部链接用 `.html` 后缀，并数清 `../` 相对层数
- [ ] 如需在首页加入口：复用 `custom.css` 中已有类，不要新造样式
- [ ] 跑 `npm run docs:build` 确认 0 错误、无死链
- [ ] 推送到 `main` 触发 GitHub Actions 自动部署

---

## 9. 常见坑速查

| 现象 | 原因 | 解决 |
|---|---|---|
| 侧边栏显示 `xxx.md` | `mapping.json` 缺该文件条目 | 补 `"xxx.md": "显示名"` |
| 点击卡片/链接 404 | 链接 `../` 层数错或少了 `.html` | 按第 4 节核对路径 |
| 改了文案构建后页面没变 | VitePress 是 SPA，正文在 JS chunk 里 | 清 `dist/` 重新构建，或硬刷浏览器 |
| 首页样式没生效 | 改了 `custom.css` 但没重新 build | 重新 `npm run docs:build` |
| 卡片高度不齐 | 描述文字过长 | 描述控制在 1–2 行（已加 `line-clamp`） |
