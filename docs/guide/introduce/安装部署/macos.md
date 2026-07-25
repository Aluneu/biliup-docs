# macOS 安装教程

::: info
- 测试环境为 macOS 12 (Monterey) 及以上，Apple Silicon（M 系列）与 Intel 均支持。
- 推荐 Python 版本 3.11 及以上。
- macOS 与 Linux 共用同一套 `uv` 安装流程，区别仅在 ffmpeg 的安装方式（Homebrew）。
:::


---

## 方法一：使用 uv 安装（推荐）

`uv` 是 Python 生态的现代化包管理工具，也是 biliup 官方推荐的安装方式。

### 1. 安装 Homebrew 与 ffmpeg

biliup 录制/处理视频依赖 `ffmpeg`，macOS 需通过 Homebrew 安装：

```bash
# 安装 Homebrew（如已安装可跳过）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 ffmpeg（录制与转码必需）
brew install ffmpeg
```

> 💡 Apple Silicon 的 Homebrew 默认装在 `/opt/homebrew`，Intel Mac 装在 `/usr/local`。终端能直接调用 `ffmpeg` 即安装成功。

### 2. 安装 uv

```bash
# 官方安装脚本（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 如使用 Homebrew
brew install uv
```

安装后重新打开终端，或执行 `source ~/.bashrc` / `source ~/.zshrc` 使 `uv` 生效。

### 3. 安装 biliup

```bash
uv tool install biliup
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

启动后在浏览器访问 `http://localhost:19159`，用户名为 `biliup`，密码为 `--auth` 启动时终端输出的密码。

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
# 更新
uv tool install --reinstall biliup

# 卸载
uv tool uninstall biliup
```

---

## 方法二：使用 pip 安装（备选）

```bash
# 确保已有 Python 3.11+
python3 --version

# 安装 biliup
pip3 install biliup

# 国内镜像加速（清华源）
pip3 install biliup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

验证与启动同方法一。

更新与卸载：

```bash
pip3 install -U biliup                       # 更新
pip3 install -U biliup -i https://pypi.tuna.tsinghua.edu.cn/simple  # 镜像更新
pip3 uninstall biliup                        # 卸载
```

---

## 方法三：预编译二进制（无需 Python 环境）

适用于不希望安装 Python / uv 的纯净环境。

### 1. 下载

前往 [Releases](https://github.com/biliup/biliup/releases/latest)，根据芯片架构下载对应文件：

| 芯片架构 | 文件后缀 |
|---|---|
| Apple Silicon（M1/M2/M3/M4） | `biliupR-v1.x.x-aarch64-macos.tar.xz` |
| Intel Mac | `biliupR-v1.x.x-x86_64-macos.tar.xz` |

```bash
# 示例：Apple Silicon
cd ~/Downloads
curl -L -O https://github.com/biliup/biliup/releases/download/v1.2.1/biliupR-v1.2.1-aarch64-macos.tar.xz
```

### 2. 解压并安装

```bash
# 解压
tar -xJf biliupR-*.tar.xz

# 移动到 PATH 目录（需要 ffmpeg，请先 brew install ffmpeg）
sudo mv biliup /usr/local/bin/

# 验证
biliup --version
```

### 3. 启动

```bash
biliup server --auth
```

> ⚠️ macOS 首次运行未签名二进制可能报「无法打开」，请在「系统设置 → 隐私与安全性」中点击「仍要打开」，或执行 `xattr -d com.apple.quarantine /usr/local/bin/biliup` 移除隔离标志。

---

## 下一步

- 运行你的第一个录制任务：参见 [快速入门](/guide/introduce/上手/get-start.html)
- 调整各平台参数：参见 [全局设置](../配置/GlobalConfig.html)
- 登录 B 站账号：参见 [登录方式](../配置/login.html)
