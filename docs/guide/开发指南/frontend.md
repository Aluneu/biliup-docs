# 前端开发（Next.js）

biliup 的 WebUI 基于 **Next.js 13+（App Router）+ React + TypeScript + Semi UI** 构建。

---

## 技术栈

| 技术 | 版本 | 用途 |
|---|---|---|
| Next.js | 13+ | React 框架，提供 SSR/SSG |
| React | 18+ | UI 组件 |
| TypeScript | 5+ | 类型安全 |
| Semi UI | latest | 字节跳动开源 UI 组件库 |
| lucide-react | latest | 图标库 |
| Tailwind CSS | 3+ | 样式（部分页面） |

---

## 环境搭建

### 1. 安装 Node.js

推荐使用 `nvm` 管理 Node.js 版本：

```bash
# 安装 nvm（如未安装）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 安装 Node.js 20（推荐）
nvm install 20
nvm use 20
```

验证：

```bash
node --version  # v18+
npm --version   # v9+
```

### 2. 安装依赖

```bash
cd app          # 前端源码在 app/ 目录
npm i
```

> ⚠️ 如果在大陆网络环境下 `npm i` 速度慢，可使用国内镜像：
> ```bash
> npm config set registry https://registry.npmmirror.com
> npm i
> ```

---

## 启动开发服务器

```bash
npm run dev
```

启动后访问：`http://localhost:3000`

> 💡 开发服务器的默认端口是 `3000`，但 Rust 后端托管生产前端时使用 `19159`。如果端口被占用，Next.js 会自动切换到 `3001`。

---

## 项目结构（前端）

```
app/
├── src/
│   ├── app/           # Next.js App Router 页面
│   │   ├── dashboard/ # 仪表盘
│   │   ├── streamers/  # 录播管理
│   │   ├── upload-manager/ # 投稿管理
│   │   ├── job/        # 任务管理
│   │   ├── history/    # 历史记录
│   │   ├── status/     # 运行状态
│   │   └── logviewer/  # 日志查看
│   ├── components/   # 复用组件
│   ├── lib/          # 工具函数、API 客户端
│   └── styles/       # 全局样式
├── public/           # 静态资源
├── next.config.js    # Next.js 配置
└── package.json
```

---

## 与后端联调

前端通过 HTTP 请求调用 Rust 后端 API（默认 `http://localhost:19159`）。

开发时有两个选择：

### 方式一：前端代理（推荐）

`next.config.js` 中已配置代理，开发服务器会将 `/v1/*` 请求转发到后端。

确保 Rust 后端在 `19159` 端口运行：

```bash
# 另开终端
cargo run --bin biliup -- server --auth
```

### 方式二：直接连接远程后端

修改前端环境变量：

```bash
# .env.development
NEXT_PUBLIC_API_BASE=http://your-remote-server:19159
```

---

## 构建生产版本

```bash
npm run build
```

构建产物在 `app/out/` 或 `app/.next/` 目录，由 Rust 后端托管。

Rust 后端会在启动时读取前端构建产物并提供静态文件服务。

---

## 常见问题

### 端口 3000 被占用

Next.js 会自动切换到 `3001`，或手动指定端口：

```bash
npm run dev -- -p 3002
```

### 依赖安装失败

尝试清除缓存后重装：

```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm i
```

### 修改后页面不更新

Next.js 支持热更新，如不生效请检查：
1. 文件是否保存在 `src/` 目录内
2. 终端是否有编译错误输出

---

## 下一步

- [Python 开发](/guide/开发指南/python)
- [Rust CLI 开发](/guide/开发指南/rust-cli)
- [系统架构](/guide/introduce/introduce/architecture)
