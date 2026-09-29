# Termux 安装教程（Android）

::: info
- Termux 是一个 Android 终端模拟器，可让手机直接运行 biliup 进行录制 / 上传。
- **务必从 [F-Droid](https://f-droid.org/packages/com.termux/) 安装 Termux**，Google Play 版本已停止更新，会导致依赖异常。
- 录制产物默认保存在 Termux 私有目录，建议先执行 `termux-setup-storage` 授权访问手机存储。
:::

---

## 1. 安装 Termux 与基础依赖

首次启动 Termux 后，先更新软件源并安装基础工具：

```bash
pkg update && pkg upgrade -y

# xz-utils 用于解压 .tar.xz，ffmpeg 按需（改用 ffmpeg 下载器或配置后处理时才需要）
pkg install xz-utils ffmpeg -y
```

---

## 2. 安装 biliup

### 方式 A：官方 Android 原生二进制（推荐）

官方为 Android (aarch64) 直接提供预编译二进制，**不需要 Python，也不需要本机编译**：

```bash
# 下载（请把 1.2.11 换成最新版本号）
cd ~
curl -L -O https://github.com/biliup/biliup/releases/download/v1.2.11/biliupR-v1.2.11-aarch64-android.tar.xz

# 解压
tar -xJf biliupR-*.tar.xz

# 安装到 Termux 的 PATH 目录
mv biliup $PREFIX/bin/
chmod +x $PREFIX/bin/biliup

# 验证
biliup --version
```

> `$PREFIX` 是 Termux 的安装前缀（通常为 `/data/data/com.termux/files/usr`），`$PREFIX/bin` 已在 `PATH` 中。
>
> 其他 ARM 架构的旧设备可尝试上面的 `aarch64` 包；若架构不匹配，请改用方式 B。

### 方式 B：pip / uv 安装（需要 Rust 工具链）

::: warning PyPI 只发布源码包
PyPI 上的 `biliup` **只有源码包（sdist），没有预编译 wheel**，在 Termux 里安装需要先装 Rust 工具链并现场编译，耗时长且容易失败。除非有特殊需求，**建议使用方式 A**。
:::

```bash
# 安装 Python 与 Rust（编译必需，体积较大）
pkg install python rust make -y

pip install biliup

# 或使用 uv
pkg install uv -y
uv tool install biliup
```

---

## 3. 启动 WebUI

```bash
biliup server --auth
```

启动后在手机浏览器访问 `http://localhost:19159`，管理员用户名为 `biliup`，首次访问时在注册页自行设置密码。

> ⚠️ Termux 会话在应用被系统回收后会中断。如需长期后台运行：
> - 开启 Termux 的「唤醒锁」：`termux-wake-lock`
> - 或使用 `nohup biliup server --auth &` 让其忽略挂断信号
> - 建议配合 [Termux:Boot](https://f-droid.org/packages/com.termux.boot/) 实现开机自启

---

## 4. 更新与卸载

方式 A（原生二进制）直接下载新版本覆盖即可：

```bash
cd ~
curl -L -O https://github.com/biliup/biliup/releases/download/v<新版本>/biliupR-v<新版本>-aarch64-android.tar.xz
tar -xJf biliupR-*.tar.xz
mv -f biliup $PREFIX/bin/
chmod +x $PREFIX/bin/biliup

# 卸载
rm $PREFIX/bin/biliup
```

方式 B：

```bash
pip install -U biliup                # pip 更新
uv tool install --reinstall biliup   # uv 更新
pip uninstall biliup                 # 卸载
```

---

## 5. 存储空间与权限

- 执行 `termux-setup-storage` 后，可在 `/sdcard/` 下读写文件，方便把录播移动到手机存储。
- 在 biliup 配置中把保存路径指向 `/sdcard/biliup/` 等目录即可。

---

## 进阶与排错

- 录制国外平台（YouTube / Twitch 等）需要在手机上配置代理或 VPN，biliup 不会自动读取系统代理；使用通用适配器时还需额外安装 `yt-dlp` 或 `streamlink`（`pkg install yt-dlp streamlink`）。
- Termux 系统里执行 `curl` 下载 GitHub 较慢时，可尝试 `pkg install aria2` 后用 `aria2c` 加速。
- 更多细节参见上游 [Wiki：Termux 中使用 biliup](https://github.com/biliup/biliup/wiki/Termux-%E4%B8%AD%E4%BD%BF%E7%94%A8-biliup)。
