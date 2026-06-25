# Linux 安装教程

> [!IMPORTANT]
> - 推荐 Python 版本 3.11 及以上。
> - 测试系统为 Debian 10/11/12、Ubuntu 20.04/22.04/24.04。
> - CentOS 等未经测试的系统可能产生未知错误，建议使用已验证系统。

---

## 方法一：使用 uv 安装（推荐）

`uv` 是 Python 生态的现代化包管理工具，比 pip 更快速、更可靠，也是 biliup 官方推荐的安装方式。

### 1. 安装 uv

```bash
# 更新软件源并安装 curl
sudo apt update && sudo apt install curl -y

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 重新加载 shell 配置
source ~/.bashrc
```

### 2. 安装 biliup

```bash
uv tool install biliup
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

启动后在浏览器访问 `http://<你的服务器IP>:19159`，用户名为 `biliup`，密码为 `--auth` 启动时终端输出的密码。

如需后台运行：
```bash
# 使用 tmux
tmux new -s biliup
biliup server --auth
# Ctrl+B 然后按 D 分离

# 或使用 screen
screen -S biliup
biliup server --auth
# Ctrl+A 然后按 D 分离
```

### 5. 更新与卸载

```bash
# 更新
uv tool install --reinstall biliup

# 卸载
uv tool uninstall biliup
```

---

## 方法二：使用 pip 安装（备选）

```bash
# 安装必要组件
sudo apt update
sudo apt install python3-pip -y

# 标准安装
pip3 install biliup

# 国内镜像加速（清华源）
pip3 install biliup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

验证安装：
```bash
biliup --version
```

更新与卸载：
```bash
# 更新
pip3 install -U biliup

# 国内镜像更新
pip3 install -U biliup -i https://pypi.tuna.tsinghua.edu.cn/simple

# 卸载
pip3 uninstall biliup
```

---

## 一键脚本安装

以下脚本由 [biliup 社区](https://biliup.me) 提供，适用于快速部署：

```bash
# 确保已安装 wget 和 curl
sudo apt install wget curl -y

# 下载并执行安装脚本
wget -O install.sh https://image.biliup.me/install.sh && chmod +x install.sh && bash install.sh
```
