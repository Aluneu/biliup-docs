---
description: Windows 上安装 biliup：npm 预编译二进制、手动下载 CLI、桌面客户端，Rust CLI 需 server 子命令启动 WebUI，基于 v1.3.0 核对。
---

# Windows 安装教程

::: info
- 测试系统为 Windows 10+，Win7 或 Windows Server 旧版可能产生意料之外的错误。
- 不推荐使用主力机进行操作，你永远不知道 Windows 为什么会杀掉你的进程。
:::

---

## 安装方式怎么选

| 方式 | 需要预装 | 说明 |
|---|---|---|
| **npm**（推荐） | Node.js 18+ | 自动匹配平台预编译二进制，装完即用 |
| 手动下载 CLI | 无 | 下载解压即用，适合不想装 Node 的用户 |
| 桌面客户端 | 无 | `biliup`，图形界面，适合主要做投稿的用户 |
| uv | Python + Rust 工具链 | PyPI 只发源码包，安装时需现场编译 |

> 前三种方式装出来的命令行工具是同一个 Rust CLI，`biliup --help` 输出的参数完全一致。

::: warning Rust CLI 必须带子命令运行
命令行版本**不会**双击启动。直接双击 `biliup.exe` 窗口会一闪而过，必须通过终端执行 `biliup server --auth`。

想要「双击即运行」的体验，请使用[桌面客户端](#方法三-桌面客户端-biliup)。
:::

---

## 方法一：使用 npm 安装（推荐）

官方通过 npm 分发**预编译二进制**，安装时会根据你的系统与 CPU 自动选择对应的子包，不需要 Python，也不需要本机编译。

### 1. 安装 Node.js 18+

```powershell
# 使用 winget（Windows 11 自带）
winget install OpenJS.NodeJS.LTS

# 或从官网下载安装包：https://nodejs.org/

# 确认版本 >= 18（可能需要重开终端）
node --version
```

### 2. 安装 biliup

```powershell
# 全局安装，之后直接用 biliup 命令
npm i -g @biliup/cli
```

不想全局安装，也可以每次直接运行：

```powershell
npx @biliup/cli server --auth
```

### 3. 启动 WebUI

```powershell
# --auth 开启登录认证；首次访问时管理员用户名固定为 biliup，请设置密码
biliup server --auth
```

启动后浏览器访问 `http://localhost:19159`。

::: info
Windows 首次运行可能弹出防火墙窗口，请点击「允许」放行对应端口（默认 19159）。
:::

### 4. 更新与卸载

```powershell
npm i -g @biliup/cli@latest     # 更新
npm uninstall -g @biliup/cli    # 卸载
```

---

## 方法二：手动下载预编译 CLI（无需 Node / Python）

### 1. 下载

访问 [biliup Releases 页面](https://github.com/biliup/biliup/releases)，在最新版本的 Assets 中下载对应架构的压缩包：

- **x64（大多数 PC）**：`biliupR-v1.x.x-x86_64-windows.zip`
- **ARM64（Surface Pro X 等）**：`biliupR-v1.x.x-aarch64-windows.zip`

解压后得到 `biliup.exe`。

### 2. 放置

将 `biliup.exe` 放在一个**独立文件夹**内（如 `D:\biliup\`）。

::: info
`biliup.exe` 所在的目录就是录播文件、配置文件的默认存储目录。
:::

### 3. 启动

在 `biliup.exe` 所在目录打开终端（PowerShell / CMD），执行：

```powershell
D:\biliup\biliup.exe server --auth
```

### 4. 更新

重新下载新版本压缩包，覆盖原来的 `biliup.exe` 即可。

---

## 方法三：桌面客户端（biliup）

如果你主要需求是**把本地视频投稿到 B 站并管理稿件**，而不是自动录播，可以直接用图形客户端，无需命令行。

1. 前往 [Releases](https://github.com/biliup/biliup/releases/latest)
2. 下载 `biliup_<版本>_x64-setup.exe`（或 `biliup_<版本>_x64_en-US.msi`）
3. 运行安装程序，按提示完成安装
4. 从开始菜单或桌面快捷方式启动

> 详细说明请参阅[桌面客户端文档](/guide/getting-started/更多/desktop-app.html)。
>
> ⚠️ 桌面客户端是**投稿与稿件管理工具**，不负责直播录制。需要自动录播请用上面的命令行版本。

---

## 方法四：使用 uv 安装

::: warning PyPI 只发布源码包
PyPI 上的 `biliup` **只有源码包（sdist），没有预编译 wheel**。因此 `uv tool install biliup` 会在**本机现场编译**，需要提前装好 Python 3.11+ 与 **Rust 工具链**（[rustup.rs](https://rustup.rs/)），编译耗时较长。

如果你只是想装好就能用，请优先选择 [方法一（npm）](#方法一-使用-npm-安装-推荐)。
:::

```powershell
# 安装 uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装 Rust 工具链（编译必需）
# 从 https://rustup.rs/ 下载 rustup-init.exe 运行

# 安装 biliup
uv tool install biliup

# 启动
biliup server --auth
```

更新与卸载：

```powershell
uv tool install --reinstall biliup   # 更新
uv tool uninstall biliup             # 卸载
```

---

## 其他方式：winget

部分 Windows 11 环境可尝试：

```powershell
winget install biliup
```

> ⚠️ winget 源中是否收录该包**以实际搜索结果为准**：先执行 `winget search biliup` 确认。如果搜不到或安装报错，请改用 [方法一（npm）](#方法一-使用-npm-安装-推荐)。

---

## 代理配置（录制国外平台）

Windows 终端默认不走系统代理。如需录制 YouTube、Twitch 等国外平台：

- **推荐方式**：在代理软件中开启 **TUN 模式** 或 **全局 VPN 模式**。
- **备用方式**：参考 [Windows 终端代理配置教程](https://blog.csdn.net/zhu6201976/article/details/132763545)。
