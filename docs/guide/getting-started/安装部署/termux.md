# Termux 安装教程（Android）

::: info
- Termux 是一个 Android 终端模拟器，可让手机直接运行 biliup 进行录制 / 上传。
- **务必从 [F-Droid](https://f-droid.org/packages/com.termux/) 安装 Termux**，Google Play 版本已停止更新，会导致依赖异常。
- 录制产物默认保存在 Termux 私有目录，建议先执行 `termux-setup-storage` 授权访问手机存储。
:::


---

## 1. 安装 Termux 与基础依赖

首次启动 Termux 后，先更新软件源并安装 ffmpeg（录制与转码必需）与 Python：

```bash
pkg update && pkg upgrade -y
pkg install ffmpeg python -y
```

> 💡 `pkg` 是 Termux 的包管理器（基于 apt）。如需更现代的安装方式，也可安装 `uv`：`pkg install uv`，后续用 `uv tool install biliup`。

---

## 2. 安装 biliup

### 方式 A：pip 安装（简单直接）

```bash
pip install biliup

# 国内镜像加速（清华源）
pip install biliup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方式 B：uv 安装（推荐，版本管理更干净）

```bash
uv tool install biliup
```

验证安装：

```bash
biliup --version
```

---

## 3. 启动 WebUI

```bash
biliup server --auth
```

启动后在手机浏览器访问 `http://localhost:19159`，用户名为 `biliup`，密码为终端输出的密码。

> ⚠️ Termux 会话在应用被系统回收后会中断。如需长期后台运行：
> - 开启 Termux 的「唤醒锁」：`termux-wake-lock`
> - 或使用 `nohup biliup server --auth &` 让其忽略挂断信号
> - 建议配合 [Termux:Boot](https://f-droid.org/packages/com.termux.boot/) 实现开机自启

---

## 4. 更新与卸载

```bash
# pip 更新
pip install -U biliup

# uv 更新
uv tool install --reinstall biliup

# 卸载
pip uninstall biliup
```

---

## 5. 存储空间与权限

- 执行 `termux-setup-storage` 后，可在 `/sdcard/` 下读写文件，方便把录播移动到手机存储。
- 在 biliup 配置中把保存路径指向 `/sdcard/biliup/` 等目录即可。

---

## 进阶与排错

- 录制国外平台（YouTube / Twitch 等）需要在手机上配置代理或 VPN，biliup 不会自动读取系统代理。
- 更多细节参见上游 [Wiki：Termux 中使用 biliup](https://github.com/biliup/biliup/wiki/Termux-%E4%B8%AD%E4%BD%BF%E7%94%A8-biliup)。
