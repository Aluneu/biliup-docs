# biliup-app（Tauri 桌面应用）

biliup-app 是 biliup 的 **Tauri 桌面应用版本**，将 WebUI 打包为原生桌面客户端，支持 Windows / macOS / Linux，无需浏览器即可管理录制任务。

---

## 概述

| 项目 | 说明 |
|---|---|
| 技术栈 | Tauri v2 + Next.js（同 WebUI） |
| 支持平台 | Windows（x64）、macOS（x64 / aarch64）、Linux（x64 / aarch64） |
| 安装包格式 | Windows：`.exe` / `.msi`；macOS：`.dmg`；Linux：`.deb` / `.AppImage` |
| 与 WebUI 的区别 | 内置服务端，打开即运行，无需手动启动 `biliup server` |
| 源码位置 | `tauri-app/` 目录（主项目） |

> 💡 适合不想配置命令行、希望开箱即用的桌面用户。

---

## 安装（预编译包）

### Windows

1. 前往 [Releases](https://github.com/biliup/biliup/releases/latest)
2. 下载 `biliup-app_x.y.z_x64-setup.exe`（或 `.msi`）
3. 运行安装程序，按提示完成安装
4. 从开始菜单或桌面快捷方式启动

### macOS

1. 下载 `biliup-app_x.y.z_x64.dmg`（或 aarch64 版）
2. 打开 `.dmg`，将 biliup-app 拖入"应用程序"文件夹
3. 首次启动需在"系统设置 → 隐私与安全"中允许运行

### Linux

1. 下载对应架构的 `.deb` 或 `.AppImage`
2. 安装：
   ```bash
   # Debian/Ubuntu
   sudo dpkg -i biliup-app_x.y.z_amd64.deb

   # 或运行 AppImage
   chmod +x biliup-app_x.y.z.AppImage
   ./biliup-app_x.y.z.AppImage
   ```

---

## 使用方式

### 首次启动

1. 启动 biliup-app，会自动打开主窗口
2. 如设置了 `--auth`，在登录页输入用户名和密码
3. 登录后进入主界面（同 WebUI）

### 系统托盘

biliup-app 最小化到系统托盘（Windows 右下角 / macOS 右上角菜单栏），右键可：

- **打开主窗口** — 显示/隐藏主界面
- **启动/停止服务** — 控制录制服务
- **退出** — 完全退出（会停止所有录制任务）

---

## 与 `biliup server` 的区别

| 对比项 | biliup server（命令行） | biliup-app（桌面应用） |
|---|---|---|
| 启动方式 | 终端执行 `biliup server` | 打开桌面应用 |
| 后台运行 | 需手动配置系统服务 | 自动以 Tauri 后台进程运行 |
| 自动启动 | 需手动配置 | 可设置"开机自启" |
| 更新方式 | `uv tool upgrade biliup` 或重新下载二进制 | 应用内提示更新，手动下载新版本 |
| 适合场景 | 服务器、VPS、进阶用户 | 个人电脑、小白用户 |

---

## 开发（从源码构建）

### 环境要求

| 依赖 | 版本 |
|---|---|
| Node.js | 18+ |
| Rust | stable（最新） |
| Tauri CLI | v2 |
| 平台 SDK | Windows：Visual Studio；macOS：Xcode；Linux：webkit2gtk-devel |

### 构建步骤

```bash
# 1. 克隆仓库
git clone https://github.com/biliup/biliup.git
cd biliup

# 2. 安装前端依赖
cd tauri-app
npm i

# 3. 开发模式（热更新）
npm run tauri dev

# 4. 构建生产版本
npm run tauri build
# 产物在 src-tauri/target/release/bundle/ 目录
```

---

## 配置文件位置

biliup-app 的配置文件和数据库与命令行版本**共用**，位置在各平台的用户目录：

| 平台 | 路径 |
|---|---|
| Windows | `%APPDATA%\biliup\` |
| macOS | `~/Library/Application Support/com.biliup.app/` |
| Linux | `~/.config/biliup/` |

> 💡 这意味着你可以在 biliup-app 中添加主播，然后在命令行版本中继续管理，数据是互通的。

---

## 常见问题

### Windows 上被标记为"未知发布者"

原因：biliup-app 未进行代码签名（需购买证书）。

解决：在 Windows SmartScreen 提示时点击"更多信息"→"仍要运行"。

### macOS 上提示"无法验证开发者"

原因：未对应用进行公证（notarization）。

解决：
1. 在"系统设置 → 隐私与安全"中滚动到底部，点击"仍要打开"
2. 或使用 Homebrew 版本（如提供）

### 启动后白屏

原因：前端资源未正确加载。

解决：重新安装应用，或检查 `tauri-app/` 下的前端是否已构建（`npm run build`）。

---

## 相关链接

- [biliup-app Releases](https://github.com/biliup/biliup/releases/latest)
- [Tauri 官方文档](https://v2.tauri.app/)
- [WebUI 使用指南](/guide/webui/usage)
