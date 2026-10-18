# macOS 安装教程

::: info
- 测试环境为 macOS 12 (Monterey) 及以上，Apple Silicon（M 系列）与 Intel 均支持。
- **npm 与预编译二进制两种方式都不需要 Python 环境**。
:::

---

## 安装方式怎么选

| 方式 | 需要预装 | 说明 |
|---|---|---|
| **npm**（推荐） | Node.js 18+ | 自动匹配平台预编译二进制，装完即用 |
| 预编译二进制 | 无 | 手动下载解压 |
| uv / pip | Python + Rust 工具链 | PyPI 只发源码包，安装时需现场编译 |

> 三种方式装出来的都是同一个 Rust CLI，`biliup --help` 输出的参数完全一致。

---

## 方法一：使用 npm 安装（推荐）

官方通过 npm 分发**预编译二进制**，安装时会根据你的系统与 CPU 自动选择对应的子包（Intel / Apple Silicon），不需要 Python，也不需要本机编译。

### 1. 安装 Homebrew 与 ffmpeg

```bash
# 安装 Homebrew（如已安装可跳过）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 ffmpeg（改用 ffmpeg 下载器或配置后处理时才需要，见文末「外部依赖说明」）
brew install ffmpeg
```

> 💡 Apple Silicon 的 Homebrew 默认装在 `/opt/homebrew`，Intel Mac 装在 `/usr/local`。终端能直接调用 `ffmpeg` 即安装成功。

### 2. 安装 Node.js 18+

```bash
# 使用 Homebrew
brew install node

# 确认版本 >= 18
node --version
```

### 3. 安装 biliup

```bash
# 全局安装，之后直接用 biliup 命令
npm i -g @biliup/cli
```

不想全局安装，也可以每次直接运行：

```bash
npx @biliup/cli server --auth
```

### 4. 验证安装

```bash
biliup --version
```

返回版本号（如 `biliup 1.x.x`）即安装成功。

### 5. 启动 WebUI

```bash
# 前台启动 WebUI，开启密码认证
biliup server --auth

# 指定端口
biliup server --port 8080 --auth
```

启动后在浏览器访问 `http://localhost:19159`，管理员用户名为 `biliup`，首次访问时在注册页自行设置密码（开启 `--auth` 后密码不再由终端生成）。

### 6. 后台运行

macOS 推荐用 `tmux` 保持会话（需先 `brew install tmux`）：

```bash
tmux new -s biliup
biliup server --auth
# 按 Ctrl+B 然后按 D 分离会话，终端关闭后仍在运行
```

如需开机自启，可将 `biliup server --auth` 加入「系统设置 → 用户与群组 → 登录项」，或通过 `launchd` 编写 plist 服务。

### 7. 更新与卸载

```bash
# 更新到最新版
npm i -g @biliup/cli@latest

# 卸载
npm uninstall -g @biliup/cli
```

---

## 方法二：预编译二进制（无需 Node / Python）

### 1. 下载

前往 [Releases](https://github.com/biliup/biliup/releases/latest)，根据芯片架构下载对应文件：

| 芯片架构 | 文件后缀 |
|---|---|
| Apple Silicon（M1/M2/M3/M4） | `biliupR-v1.x.x-aarch64-macos.tar.xz` |
| Intel Mac | `biliupR-v1.x.x-x86_64-macos.tar.xz` |

```bash
# 示例：Apple Silicon（请把 1.2.11 换成最新版本号）
cd ~/Downloads
curl -L -O https://github.com/biliup/biliup/releases/download/v1.2.11/biliupR-v1.2.11-aarch64-macos.tar.xz
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

> ⚠️ macOS 首次运行未签名二进制可能报「无法打开」，请在「系统设置 → 隐私与安全性」中点击「仍要打开」，或执行 `xattr -d com.apple.quarantine /usr/local/bin/biliup` 移除隔离标志。

### 4. 更新

重新下载新版本压缩包，覆盖 `/usr/local/bin/biliup` 即可。

---

## 方法三：使用 uv / pip 安装

::: warning PyPI 只发布源码包
PyPI 上的 `biliup` **只有源码包（sdist），没有预编译 wheel**。因此 `uv tool install biliup` 和 `pip install biliup` 都会在**本机现场编译**，需要提前装好：

- Python 3.9+（推荐 3.11 及以上）
- **Rust 工具链**（`brew install rust` 或 [rustup.rs](https://rustup.rs/)），编译耗时较长

如果你只是想装好就能用，请优先选择 [方法一（npm）](#方法一-使用-npm-安装-推荐) 或 [方法二（预编译二进制）](#方法二-预编译二进制-无需-node-python)。
:::

### uv 方式

```bash
# 安装 uv
brew install uv
# 或：curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Rust 工具链（编译必需）
brew install rust

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
# 确保已有 Python 3.11+
python3 --version

# 安装 biliup
pip3 install biliup
```

更新与卸载：

```bash
pip3 install -U biliup               # 更新
pip3 uninstall biliup                # 卸载
```

---

## 外部依赖说明

biliup 本体已包含下载器，多数场景**开箱即用**，以下依赖按需安装：

| 依赖 | 什么时候需要 |
|---|---|
| — | 默认下载器 `mesio` 由 Rust 实现，**无需任何外部依赖** |
| `ffmpeg` | 改用 `ffmpeg` 下载器，或配置了压制 / remux 等后处理 |
| `yt-dlp` / `streamlink` | 录制 YouTube、niconico 等平台，或使用通用适配器处理非内置平台的地址 |

---

## 下一步

- 运行你的第一个录制任务：参见[工作原理与快速引导](/guide/workflow-demo/)
- 调整各平台参数：参见[全局设置](../配置/global-config.html)
- 登录 B 站账号：参见[登录方式](../配置/login.html)
