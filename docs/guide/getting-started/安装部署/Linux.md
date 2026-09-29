# Linux 安装教程

::: info
- 测试系统为 Debian 10/11/12、Ubuntu 20.04/22.04/24.04。
- **npm 与预编译二进制两种方式都不需要 Python 环境**。
- CentOS 等未经测试的系统可能产生未知错误，建议使用已验证系统。
:::

---

## 安装方式怎么选

| 方式 | 需要预装 | 说明 |
|---|---|---|
| **npm**（推荐） | Node.js 18+ | 自动匹配平台预编译二进制，装完即用 |
| 预编译二进制 | 无 | 手动下载解压，适合无 Node 的服务器 |
| uv / pip | Python + Rust 工具链 | PyPI 只发源码包，安装时需现场编译 |
| Docker | Docker | 见 [Docker 部署](./docker.html)，环境隔离最彻底 |

> 三种方式装出来的都是同一个 Rust CLI，`biliup --help` 输出的参数完全一致。

---

## 方法一：使用 npm 安装（推荐）

官方通过 npm 分发**预编译二进制**，安装时会根据你的系统与 CPU 自动选择对应的子包，不需要 Python，也不需要本机编译。

### 1. 安装 Node.js 18+

```bash
# 更新软件源
sudo apt update

# 安装 Node.js 与 npm
sudo apt install nodejs npm -y

# 确认版本 >= 18
node --version
```

> 发行版自带源里的 Node 版本偏旧时，可用 [NodeSource](https://github.com/nodesource/distributions) 或 [nvm](https://github.com/nvm-sh/nvm) 安装较新版本。

### 2. 安装 biliup

```bash
# 全局安装，之后直接用 biliup 命令
npm i -g @biliup/cli
```

不想全局安装，也可以每次直接运行（首次会缓存）：

```bash
npx @biliup/cli server --auth
```

### 3. 验证安装

```bash
biliup --version
```

返回版本号（如 `biliup 1.x.x`）即安装成功。

### 4. 启动 WebUI

```bash
# 前台启动 WebUI，开启密码认证
biliup server --auth

# 指定端口
biliup server --port 8080 --auth
```

启动后在浏览器访问 `http://127.0.0.1:19159`，管理员用户名为 `biliup`，首次访问时在注册页自行设置密码（开启 `--auth` 后密码不再由终端生成）。

要从其他设备访问，需要 `biliup server --bind 0.0.0.0 --auth`（详见[命令行参考](/guide/configs/config.html)）。

### 5. 后台运行

```bash
# 使用 tmux
tmux new -s biliup
biliup server --auth
# Ctrl+B 然后按 D 分离

# 或使用 screen
screen -S biliup
biliup server --auth
# Ctrl+A 然后按 D 分离

# 或最简单的方式
nohup biliup server --auth &
```

### 6. 更新与卸载

```bash
# 更新到最新版
npm i -g @biliup/cli@latest

# 卸载
npm uninstall -g @biliup/cli
```

### npm 支持哪些平台

| 平台 | 架构 |
|---|---|
| Linux | x64（glibc / musl）、arm64（glibc）、armv6+（glibc, gnueabi） |
| macOS | x64、arm64（Apple Silicon） |
| Windows | x64 |

未列出的平台请改用下方预编译二进制或 Docker。

---

## 方法二：使用预编译二进制（无需 Node / Python）

适用于不希望安装 Node.js 的服务器场景。下载的就是 npm 子包里同版本的原始二进制。

### 1. 下载

前往 [Releases](https://github.com/biliup/biliup/releases/latest)，根据 CPU 架构下载对应文件：

| CPU 架构 | 文件后缀 |
|---|---|
| x86_64（大多数 VPS） | `biliupR-v1.x.x-x86_64-linux.tar.xz` |
| x86_64（musl libc，如 Alpine） | `biliupR-v1.x.x-x86_64-linux-musl.tar.xz` |
| aarch64（ARM64 服务器） | `biliupR-v1.x.x-aarch64-linux.tar.xz` |
| armv7（树莓派 3/4） | `biliupR-v1.x.x-arm-linux.tar.xz` |

```bash
# 示例：x86_64 架构
cd /tmp
wget https://github.com/biliup/biliup/releases/download/v1.2.11/biliupR-v1.2.11-x86_64-linux.tar.xz
```

### 2. 解压并安装

```bash
# 解压
tar -xJf biliupR-*.tar.xz

# 移动到 PATH 目录
sudo mv biliup /usr/local/bin/

# 验证
biliup --version
```

### 3. 启动

```bash
biliup server --auth
```

### 4. 更新

重新下载新版本压缩包，覆盖 `/usr/local/bin/biliup` 即可。

---

## 方法三：使用 uv / pip 安装

::: warning PyPI 只发布源码包
PyPI 上的 `biliup` **只有源码包（sdist），没有预编译 wheel**。因此 `uv tool install biliup` 和 `pip install biliup` 都会在**本机现场编译**，需要提前装好：

- Python 3.9+（推荐 3.11 及以上）
- **Rust 工具链**（[rustup.rs](https://rustup.rs/)），编译耗时较长

如果你只是想装好就能用，请优先选择 [方法一（npm）](#方法一-使用-npm-安装-推荐) 或 [方法二（预编译二进制）](#方法二-使用预编译二进制-无需-node-python)。
:::

### uv 方式

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# 安装 Rust 工具链（编译必需）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 biliup
uv tool install biliup
```

更新与卸载：

```bash
uv tool install --reinstall biliup   # 更新
uv tool uninstall biliup             # 卸载
```

### pip 方式

```bash
sudo apt update && sudo apt install python3-pip -y
pip3 install biliup

# 国内镜像加速（清华源）
pip3 install biliup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

更新与卸载：

```bash
pip3 install -U biliup               # 更新
pip3 uninstall biliup                # 卸载
```

---

## 方法四：Termux（Android）

Android 设备可通过 [Termux](https://termux.dev/) 运行 biliup，完整步骤已单独成文：

> 📱 [Termux 安装教程（Android）](./termux.html)

---

## 一键脚本安装

以下脚本由 [biliup 社区](https://biliup.me) 提供，适用于快速部署：

```bash
# 确保已安装 wget 和 curl
sudo apt install wget curl -y

# 下载并执行安装脚本
wget -O install.sh https://image.biliup.me/install.sh && chmod +x install.sh && bash install.sh
```

---

## 外部依赖说明

biliup 本体已包含下载器，多数场景**开箱即用**，以下依赖按需安装：

| 依赖 | 什么时候需要 |
|---|---|
| — | 默认下载器 `stream-gears` 由 Rust 实现，**无需任何外部依赖** |
| `ffmpeg` | 改用 `ffmpeg` 下载器，或配置了压制 / remux 等后处理 |
| `yt-dlp` / `streamlink` | 录制 YouTube、niconico 等平台，或使用通用适配器处理非内置平台的地址 |

```bash
sudo apt install ffmpeg -y
pip3 install -U yt-dlp
```
