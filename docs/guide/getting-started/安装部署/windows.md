---
description: Windows 上运行 biliup：桌面应用、预编译 CLI 与 uv 安装方式，Rust CLI 需 server 子命令启动 WebUI，基于 v1.2.2 核对。
---

# Windows 安装教程

::: info
- 测试系统为 Windows 10+，Win7 或 Windows Server 旧版可能产生意料之外的错误。
- 不推荐使用主力机进行操作，你永远不知道 Windows 为什么会杀掉你的进程。
:::


---

## 方法一：运行预编译 CLI（Rust 构建，无需 Python）

biliup 在 Releases 的 Assets 中提供预编译的 Rust CLI 压缩包，**无需安装 Python**。

::: warning
Rust CLI 是一个命令行程序，**必须带子命令运行**。直接双击 `biliup.exe` 不会自动启动 WebUI（窗口会一闪而过）。请通过终端执行 `biliup.exe server` 启动服务，详见下方「3. 使用参数启动」。若想要「双击即运行」的体验，请改用[方法四：biliup-app 桌面应用](/guide/getting-started/更多/desktop-app.html) 或[方法三：uv 安装](/guide/getting-started/安装部署/windows.html#方法三使用-uv-安装)。
:::

### 1. 下载

访问 [biliup Releases 页面](https://github.com/biliup/biliup/releases)，在最新版本的 Assets 中下载对应架构的压缩包：

- **x64（大多数 PC）**：`biliupR-v1.x.x-x86_64-windows.zip`
- **ARM64（Surface Pro X 等）**：`biliupR-v1.x.x-aarch64-windows.zip`

解压后得到 `biliup.exe`（Rust 命令行可执行文件）。

### 2. 放置

将解压出的 `biliup.exe` 放在一个**独立文件夹**内（如 `D:\biliup\`）。

::: info
`biliup.exe` 所在的目录就是录播文件、配置文件的默认存储目录。
:::

### 3. 使用参数启动

在 `biliup.exe` 所在目录打开终端（PowerShell / CMD），执行：

```powershell
# 启动 WebUI（--auth 开启登录认证；首次访问时管理员用户名固定为 biliup，请设置密码）
D:\biliup\biliup.exe server --auth
```

启动后浏览器访问 `http://localhost:19159`。

::: info
Windows 11 运行 `biliup.exe` 后可能弹出防火墙窗口，请点击「允许」放行对应端口（默认 19159）。
:::

---

## 方法二：使用 winget 安装（Windows 11）

Windows 11 用户可通过系统自带的 `winget` 包管理器一键安装命令行版本：

```powershell
winget install biliup
```

安装后验证：

```powershell
biliup --version
```

> 💡 `winget` 安装的是命令行版本（Rust CLI），启动同样需要 `server` 子命令：`biliup server --auth`。如需图形界面请使用[方法四（biliup-app 桌面应用）](/guide/getting-started/更多/desktop-app.html)。

---

## 方法三：使用 uv 安装

先安装 Python（推荐 3.11+），然后：

```powershell
# 安装 uv（PowerShell）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装 biliup
uv tool install biliup

# 启动（uv 安装的入口会自动补 server 子命令，直接 biliup 即可；显式写法为 biliup server --auth）
biliup server --auth
```

---

## 方法四：biliup-app（Tauri 桌面应用，推荐小白用户）

biliup-app 将 WebUI 打包为原生桌面客户端，打开即运行，无需命令行操作。

1. 前往 [Releases](https://github.com/biliup/biliup/releases/latest)
2. 下载 `bbup-app_x.y.z_x64-setup.exe`（或 `.msi`）
3. 运行安装程序，按提示完成安装
4. 从开始菜单或桌面快捷方式启动

> 详细使用说明请参阅 [biliup-app 文档](/guide/getting-started/更多/desktop-app.html)。

---

## 方法五：预编译二进制（高级用户）

适用于不希望安装 `uv` 或 `winget` 的场景（本质上与方法一相同的 Rust CLI）。

1. 前往 [Releases](https://github.com/biliup/biliup/releases/latest)
2. 根据 CPU 架构下载对应文件：
   - **x64（大多数 PC）**：`biliupR-v1.x.x-x86_64-windows.zip`
   - **ARM64（Surface Pro X 等）**：`biliupR-v1.x.x-aarch64-windows.zip`
3. 解压到任意目录（如 `D:\biliup\`）
4. 通过终端启动（**不要直接双击**，Rust CLI 需子命令）：

```powershell
D:\biliup\biliup.exe server --auth
```

---

## 代理配置（录制国外平台）

Windows 终端默认不走系统代理。如需录制 YouTube、Twitch 等国外平台：

- **推荐方式**：在代理软件中开启 **TUN 模式** 或 **全局 VPN 模式**。
- **备用方式**：参考 [Windows 终端代理配置教程](https://blog.csdn.net/zhu6201976/article/details/132763545)。
