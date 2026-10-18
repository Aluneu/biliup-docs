# 桌面端：biliup 桌面版与 biliup-app

biliup 有两个**用途完全不同**的桌面程序，都基于 [Tauri](https://tauri.app/)，别混用：

| | **biliup 桌面版** | **biliup-app** |
|---|---|---|
| 用途 | 图形界面运行完整 biliup 服务：录制 + WebUI + 自动投稿 | 只做 B站投稿与稿件管理 |
| 平台 | Windows x64 | Windows / macOS / Linux |
| 版本 | 跟随主项目（如 `1.3.0`） | 独立版本号（`app-v*`） |
| 发布 | 主项目 [Releases](https://github.com/biliup/biliup/releases/latest) | [biliup-app-new Releases](https://github.com/biliup/biliup-app-new/releases) |
| 源码 | 主仓库 `tauri-app/` | [biliup/biliup-app-new](https://github.com/biliup/biliup-app-new) |

---

## 一、biliup 桌面版（推荐给不想用命令行的录制用户）

把完整的 biliup 服务装进桌面窗口，不需要另装 Python / FFmpeg，也不需要手敲 `biliup server`。

| 项目 | 说明 |
|---|---|
| 技术栈 | Tauri v2（Rust）+ 内嵌 WebUI |
| 运行方式 | 进程内启动 biliup 服务，窗口里直接打开 WebUI；默认 `127.0.0.1:19159`，端口被占用时自动换一个 |
| 内置依赖 | FFmpeg（`ffmpeg/` 目录）与渲染字体（`render-tools/`），遮挡 / 录后合成开箱可用 |
| 数据目录 | 程序不在系统盘时=安装目录；在系统盘时首次启动会让你选，记录在 `desktop.json` |

### 安装

1. 打开 [biliup Releases](https://github.com/biliup/biliup/releases/latest)；
2. 下载 `biliup_<版本>_x64-setup.exe`（或 `biliup_<版本>_x64_en-US.msi`）；
3. 双击安装。默认装在当前用户目录，**不需要管理员权限**；
4. 首次启动若程序装在系统盘，会询问数据和录像放在哪里——选完写入配置，之后不再询问。

::: warning 安装包暂未签名
浏览器提示「不常下载 / 可能有害」时，在下载列表点「…」→「保留」；首次运行遇到蓝色 SmartScreen 提示，点「更多信息」→「仍要运行」。
:::

> 安装包里的 FFmpeg 是 BtbN 的 win64 GPL 静态构建，按 GPLv3 分发，许可文本在 `ffmpeg/LICENSE.txt`。

---

## 二、biliup-app（投稿与稿件管理客户端）

适合"已经有视频文件、只想上传和管理稿件"的场景，**不负责直播录制**。需要自动录播请用上面的桌面版或 CLI + WebUI。

### 功能

| 分类 | 能力 |
|---|---|
| 视频管理 | 拖拽上传、批量选择处理、监控文件夹变化自动上传 |
| 模板系统 | 为不同类型视频创建可复用模板、一键重置到上次保存状态、按 BV 号复制现有稿件的配置 |
| 稿件编辑 | 联合投稿（按 UID 或昵称搜索好友）、简介 @ 好友、稿件状态显示、同一模板下多稿件按序投稿 |
| 多账号 | 同时登录并管理多个 B 站账号 |

**快捷键**：`Ctrl/Cmd + S` 保存模板 · `Ctrl/Cmd + R` 重置模板 · `Ctrl/Cmd + F5` 刷新

### 安装（预编译包）

包名与主项目的桌面版不同，注意区分：

| 渠道 | 平台 | 包名 |
|---|---|---|
| [biliup-app-new Releases](https://github.com/biliup/biliup-app-new/releases) | Windows / macOS / Linux | `biliup-app_<版本>_<平台>` |

#### Windows

1. 前往 [biliup-app-new Releases](https://github.com/biliup/biliup-app-new/releases)
2. 下载 `biliup-app_<版本>_x64-setup.exe`（中文界面选 `_x64_zh-CN.msi`）
3. 运行安装程序完成安装

#### macOS

1. 前往 [biliup-app-new Releases](https://github.com/biliup/biliup-app-new/releases)
2. 下载 `biliup-app_<版本>_x64.dmg`（Apple Silicon 选对应 `aarch64` 包）
3. 打开 `.dmg`，将应用拖入「应用程序」文件夹
4. 首次启动需在「系统设置 → 隐私与安全」中允许运行

#### Linux

1. 前往 [biliup-app-new Releases](https://github.com/biliup/biliup-app-new/releases)
2. 按发行版下载：

   ```bash
   # Debian / Ubuntu
   sudo dpkg -i biliup-app_<版本>_amd64.deb

   # Fedora / openSUSE（RPM）
   sudo rpm -i biliup-app-<版本>-1.x86_64.rpm

   # 或直接运行 AppImage
   chmod +x biliup-app_<版本>_amd64.AppImage
   ./biliup-app_<版本>_amd64.AppImage
   ```

---

## 三、从源码构建

### biliup 桌面版（主仓库）

需要先在仓库根目录构建 WebUI，再构建 Tauri 外壳：

```bash
npm install && npm run build      # 仓库根目录，产出 out/
cd tauri-app && npm ci && npm run tauri build
```

> 安装包版本写在 `tauri-app/src-tauri/tauri.conf.json`，发布前需与根目录 `Cargo.toml` 的 `[workspace.package] version` 保持一致。

### biliup-app（独立仓库）

| 依赖 | 版本 |
|---|---|
| Node.js | 18+ |
| Rust | stable（最新） |
| Tauri CLI | v2 |
| 平台 SDK | Windows：Visual Studio；macOS：Xcode；Linux：webkit2gtk-devel |

```bash
git clone https://github.com/biliup/biliup-app-new.git
cd biliup-app-new
npm i
npm run tauri dev      # 开发模式
npm run tauri build    # 产物在 src-tauri/target/release/bundle/
```

---

## 常见问题

### 上传时进度长时间不动

删除该任务，手动切换一条上传线路后重新上传。

### Windows 上被标记为「未知发布者」

原因：安装包未做代码签名（需购买证书）。

解决：在 SmartScreen 提示时点击「更多信息」→「仍要运行」。

### macOS 上提示「无法验证开发者」

原因：未对应用进行公证（notarization）。

解决：在「系统设置 → 隐私与安全」中滚动到底部，点击「仍要打开」。

### 桌面版启动后白屏

biliup 桌面版的外壳只负责显示内嵌 WebUI。先看安装目录下的 `ds_update.log` / `data/` 是否正常；如果是从源码构建，确认仓库根目录已执行 `npm run build` 生成 `out/`。

---

## 相关链接

- [biliup Releases（CLI + biliup 桌面版）](https://github.com/biliup/biliup/releases/latest)
- [biliup-app Releases](https://github.com/biliup/biliup-app-new/releases)
- [Tauri 官方文档](https://v2.tauri.app/)
- [WebUI 使用指南](/guide/webui/usage.html)
- [CLI 命令行参考](/guide/configs/config.html)
