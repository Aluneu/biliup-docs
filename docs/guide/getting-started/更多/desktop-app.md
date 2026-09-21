# biliup-app（桌面客户端）

biliup-app 是 biliup 的桌面客户端，基于 Tauri 打包，支持 Windows / macOS / Linux，用来在图形界面里完成 **B 站投稿与稿件管理**。

::: info 它和 `biliup server` 不是同一个东西
命令行版的 `biliup server` 负责**直播录制 + 自动投稿**，核心是一套常驻服务与本页文档描述的 WebUI。

biliup-app 是**投稿与稿件管理客户端**（[独立仓库](https://github.com/biliup/biliup-app-new)维护，原 `biliup/biliup-app` 已归档），面向"已有视频文件、要上传和管理稿件"的场景，不负责直播录制。两者可以并存，但用途不同，请勿当作 WebUI 的桌面版来用。
:::

---

## 概述

| 项目 | 说明 |
|---|---|
| 技术栈 | Tauri + Vue 3 + Element Plus |
| 定位 | B 站视频投稿与稿件管理客户端 |
| 支持平台 | Windows 10+、macOS 10.15+、Linux（现代发行版） |
| 安装包 | Windows：`.exe` / `.msi`；macOS：`.dmg`；Linux：`.deb` / `.AppImage` |
| 源码仓库 | [biliup/biliup-app-new](https://github.com/biliup/biliup-app-new) |
| 许可 | MIT 或 Apache-2.0，二选一 |

> 💡 适合不习惯命令行、主要需求是"把本地视频传上去并管理稿件"的用户。需要自动录播请用 CLI + WebUI。

---

## 功能

| 分类 | 能力 |
|---|---|
| 视频管理 | 拖拽上传、批量选择处理、监控文件夹变化自动上传 |
| 模板系统 | 为不同类型视频创建可复用模板、一键重置到上次保存状态、按 BV 号复制现有稿件的配置 |
| 稿件编辑 | 联合投稿（按 UID 或昵称搜索好友）、简介 @ 好友、稿件状态显示、同一模板下多稿件按序投稿 |
| 多账号 | 同时登录并管理多个 B 站账号 |

**快捷键**：`Ctrl/Cmd + S` 保存模板 · `Ctrl/Cmd + R` 重置模板 · `Ctrl/Cmd + F5` 刷新

---

## 安装（预编译包）

安装包随主仓库一起发布，前往 [biliup Releases](https://github.com/biliup/biliup/releases/latest) 下载。

### Windows

1. 下载 `bbup-app_<版本>_x64-setup.exe`（或 `bbup-app_<版本>_x64_en-US.msi`）
2. 运行安装程序，按提示完成安装
3. 从开始菜单或桌面快捷方式启动

### macOS

1. 下载对应架构的 `.dmg`
2. 打开 `.dmg`，将应用拖入"应用程序"文件夹
3. 首次启动需在"系统设置 → 隐私与安全"中允许运行

### Linux

1. 下载对应架构的 `.deb` 或 `.AppImage`
2. 安装：
   ```bash
   # Debian/Ubuntu
   sudo dpkg -i bbup-app_<版本>_amd64.deb

   # 或运行 AppImage
   chmod +x bbup-app_<版本>.AppImage
   ./bbup-app_<版本>.AppImage
   ```

::: tip 注意包名
发布包名前缀是 **`bbup-app`**，不是 `biliup-app`。桌面端版本号与 CLI 版本号相互独立（例如 CLI 为 v1.2.6 时，桌面端可能是 0.1.x），下载时以 Releases 页面实际列出的为准。
:::

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
# 1. 克隆独立仓库
git clone https://github.com/biliup/biliup-app-new.git
cd biliup-app-new

# 2. 安装依赖
npm i

# 3. 开发模式（热更新）
npm run tauri dev

# 4. 构建生产版本
npm run tauri build
# 产物在 src-tauri/target/release/bundle/ 目录
```

---

## 常见问题

### 上传时进度长时间不动

删除该任务，手动切换一条上传线路后重新上传。

### Windows 上被标记为"未知发布者"

原因：应用未做代码签名（需购买证书）。

解决：在 Windows SmartScreen 提示时点击"更多信息"→"仍要运行"。

### macOS 上提示"无法验证开发者"

原因：未对应用进行公证（notarization）。

解决：在"系统设置 → 隐私与安全"中滚动到底部，点击"仍要打开"。

### 启动后白屏

原因：前端资源未正确加载。

解决：重新安装应用，或从源码构建时先确认前端已构建（`npm run build`）。

---

## 相关链接

- [biliup-app Releases](https://github.com/biliup/biliup-app-new/releases)
- [biliup CLI 下载](https://github.com/biliup/biliup/releases/latest)
- [Tauri 官方文档](https://v2.tauri.app/)
- [WebUI 使用指南](/guide/webui/usage.html)
- [CLI 命令行参考](/guide/configs/config.html)
