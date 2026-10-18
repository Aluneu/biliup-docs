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

想要「双击即运行」的体验，请使用[桌面客户端](#方法三-桌面版-biliup-图形客户端)。
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
# 国内网络慢可加：--registry=https://registry.npmmirror.com
npm i -g @biliup/cli
```

不想全局安装，也可以每次直接运行：

```powershell
npx @biliup/cli server --auth
```

::: tip npm 包不含渲染字体
弹幕渲染、画面遮挡与录后合成需要 `render-tools/`（Noto 字体），npm 包只含二进制。只录制 + 投稿不受影响；需要这些功能时，把 Release 压缩包里的 `render-tools/` 放到二进制旁，或配置 `render_fonts_dir`（见[全局设置](/guide/getting-started/配置/global-config.html#字体目录-render-fonts-dir)）。
:::

### 3. 启动 WebUI

```powershell
# --auth 开启登录认证；首次访问时自行设置管理员用户名（默认预填 biliup，可改）与密码
biliup server --auth
```

启动后浏览器访问 `http://localhost:19159`。

::: info
默认只监听 `127.0.0.1`，本机访问不会触发防火墙弹窗。只有用 `--bind 0.0.0.0` 让其他设备访问时，Windows 才会询问是否放行——此时必须同时加 `--auth`，否则服务会拒绝启动。
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

> Windows 目前只提供 x64 二进制，没有 aarch64 版本；ARM 设备请走 WSL 或 Docker。

解压后得到 `biliup.exe` 与 `render-tools/`，两者放在同一目录。

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

## 方法三：桌面版（biliup 图形客户端）

不想碰命令行的话，可以直接装**桌面版**：它在窗口里跑完整的 biliup 服务（录制 + WebUI + 自动投稿），安装包还内置 FFmpeg。

1. 前往 [Releases](https://github.com/biliup/biliup/releases/latest)
2. 下载 `biliup_<版本>_x64-setup.exe`（或 `biliup_<版本>_x64_en-US.msi`）
3. 运行安装程序，按提示完成安装
4. 从开始菜单或桌面快捷方式启动；首次启动若装在系统盘，会让你选数据与录像目录

> 详细说明（含数据目录、未签名提示）见[桌面端文档](/guide/getting-started/更多/desktop-app.html)。
>
> ⚠️ 另有一个独立的 **biliup-app**，它只做投稿与稿件管理、不负责录制，别装错。

---

## 方法四：Python API（uv / pip，可选）

::: warning 这是给 Python 脚本用的，不是装 CLI
PyPI 上的 `biliup` 是 **stream-gears 的 Python 绑定**（模块名 `stream_gears`），只提供上传、直链下载与登录接口，**没有 `biliup` 命令，也没有录制服务**（v1.3.0 起 `python -m biliup` 已移除）。

它只有源码包（sdist），安装时要在本机现场编译，需要 Python 3.9+ 与 **Rust 工具链**（[rustup.rs](https://rustup.rs/)），耗时较长。

只想装好就能用，请选 [方法一（npm）](#方法一-使用-npm-安装-推荐) 或 [方法三（桌面版）](#方法三-桌面版-biliup-图形客户端)。
:::

```powershell
# 安装 uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装 Rust 工具链：从 https://rustup.rs/ 下载 rustup-init.exe 运行

# 在虚拟环境里装绑定库
uv venv
.venv\Scripts\activate
uv pip install biliup

# 验证
python -c "import stream_gears; print('ok')"
```

更新与卸载：

```powershell
uv pip install -U biliup    # 更新
uv pip uninstall biliup     # 卸载
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
