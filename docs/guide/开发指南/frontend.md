# 前端开发（Next.js）

biliup 的 WebUI 是仓库根目录下的一个 **Next.js 16（App Router）+ React 19 + TypeScript** 工程，构建时**静态导出**到 `out/`，再由 Rust 后端用 `rust-embed` 内嵌托管。

> ⚠️ 常见误区：`app/` 是 Next.js 的 App Router 目录，**不是**前端工程根目录。`package.json`、`next.config.js` 都在仓库根目录。

---

## 技术栈

| 技术 | 版本 | 用途 |
|---|---|---|
| Next.js | 16（App Router） | React 框架，`output: 'export'` 静态导出 |
| React | 19 | UI 组件 |
| TypeScript | 5+ | 类型安全 |
| [Semi Design](https://semi.design/) | 2.x | 字节跳动开源 UI 组件库 |
| Sass | 1.x | 样式（`*.module.scss`） |
| esbuild | 0.25 | 构建期打包辅助脚本 |

播放器与图表相关：`artplayer` / `mpegts.js` / `hls.js` / `jassub`（弹幕字幕渲染）、`uplot`（曲线）、`swr`（数据请求）。

---

## 环境搭建

### 1. 安装 Node.js

Next.js 16 要求 **Node.js 20.9+**：

```bash
# 使用 nvm
nvm install 22
nvm use 22

node --version   # v20.9+
npm --version
```

### 2. 安装依赖（在仓库根目录）

```bash
git clone https://github.com/biliup/biliup.git
cd biliup
npm i
```

> 国内网络慢可换镜像：`npm config set registry https://registry.npmmirror.com`

---

## 启动开发服务器

```bash
npm run dev
```

- 开发地址：`http://localhost:3000`（被占用时 Next.js 会自动换端口）
- 开发环境的 API 地址来自 `.env.development`：

  ```
  NEXT_PUBLIC_API_SERVER=http://localhost:19159
  ```

  所以另开一个终端把后端跑起来即可联调：

  ```bash
  cargo run --bin biliup -- server --auth
  ```

- 想连**远程后端**，改 `.env.development` 里的 `NEXT_PUBLIC_API_SERVER` 为远端地址后重启 `npm run dev`。

> 生产环境（`.env.production`）里 `NEXT_PUBLIC_API_SERVER` 为空，前端走同源请求，由 Rust 后端直接托管。

---

## 项目结构

```
biliup/
├── app/                    # Next.js App Router 源码
│   ├── (app)/              # 登录后的主界面
│   │   ├── page.tsx        # 控制台
│   │   ├── streamers/      # 直播管理
│   │   ├── workbench/      # 剪辑台
│   │   ├── upload-manager/ # 投稿管理
│   │   ├── renders/        # 压制任务（v1.3.0 新增）
│   │   ├── upload-queue/   # 上传队列（v1.3.0 新增）
│   │   ├── nodes/          # Fleet 节点
│   │   └── users/          # 用户管理
│   ├── (auth)/login/       # 登录 / 首次注册
│   ├── lib/                # API 客户端与工具函数
│   ├── ui/                 # 复用组件（含 ui/plugins/ 平台表单）
│   └── layout.tsx          # 根布局与导航
├── public/                 # 静态资源
├── scripts/                # 构建辅助脚本
├── next.config.js          # output: 'export'
└── package.json            # 前端工程在这里
```

---

## 构建生产版本

```bash
npm run build     # 仓库根目录，产物在 out/
```

Rust 后端通过 `rust-embed` 把 `out/` 编进二进制，所以：

> ⚠️ 在 `cargo build` / `cargo test` 之前**必须先执行一次 `npm run build`**，否则编译会因找不到 `out/` 失败。

---

## 常见问题

### 端口 3000 被占用

Next.js 会自动换端口，也可手动指定：

```bash
npm run dev -- -p 3002
```

### 依赖安装失败

```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm i
```

### 修改后页面不更新

1. 确认文件改在 `app/` 目录内（不是仓库根目录的其它同名目录）；
2. 看终端有没有编译报错；
3. 环境变量改动需要重启 `npm run dev`。

---

## 下一步

- [Python 开发](/guide/开发指南/python.html)
- [Rust CLI 开发](/guide/开发指南/rust-cli.html)
- [系统架构](/guide/getting-started/更多/architecture.html)
