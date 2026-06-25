# Windows 安装教程

> [!IMPORTANT]
> - 测试系统为 Windows 10+，Win7 或 Windows Server 旧版可能产生意料之外的错误。
> - 理论上支持 macOS，但文档暂未覆盖。

---

## 方法一：运行 .exe 文件（推荐，无需环境）

biliup 提供了预编译的 `.exe` 文件，无需安装 Python 即可直接运行。

### 1. 下载

访问 [biliup Releases 页面](https://github.com/biliup/biliup/releases)，在最新版本的 Assets 中下载 `biliup.exe`。

### 2. 运行

将下载的 `.exe` 文件放在一个**独立文件夹**内（如 `D:\biliup\`），双击运行即可。

> [!IMPORTANT]
> `.exe` 所在的目录就是录播文件、配置文件的默认存储目录。

Windows 11 运行 `.exe` 后可能弹出防火墙窗口，请点击「允许」放行。

### 3. 使用参数启动

即使是 `.exe` 文件，也可以通过命令行传递参数：

```powershell
# 使用绝对路径，设置 WebUI 密码
D:\biliup\biliup.exe server --auth
```

启动后浏览器访问 `http://localhost:19159`。

---

## 方法二：使用 uv 安装

先安装 Python（推荐 3.11+），然后：

```powershell
# 安装 uv（PowerShell）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装 biliup
uv tool install biliup

# 启动
biliup server --auth
```

---

## 代理配置（录制国外平台）

Windows 终端默认不走系统代理。如需录制 YouTube、Twitch 等国外平台：

- **推荐方式**：在代理软件中开启 **TUN 模式** 或 **全局 VPN 模式**。
- **备用方式**：参考 [Windows 终端代理配置教程](https://blog.csdn.net/zhu6201976/article/details/132763545)。
