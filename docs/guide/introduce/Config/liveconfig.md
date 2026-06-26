# 各平台设置

此页面索引各直播平台的独立配置说明。各平台详细配置请点击对应链接查看。

> [!TIP]
> 大部分平台使用默认 `stream-gears` 下载器即可，无需额外配置。以下仅列出需要特殊配置的平台。

---

## 平台配置索引

| 平台 | 需要配置的项 | 详情链接 |
|---|---|---|
| 哔哩哔哩 | Cookie、直播流协议、API 反代 | [哔哩哔哩配置](/guide/introduce/live/哔哩哔哩.html) |
| 虎牙 | CDN 线路优选 | [虎牙配置](/guide/introduce/live/虎牙.html) |
| 斗鱼 | CDN 线路优选 | [斗鱼配置](/guide/introduce/live/斗鱼.html) |
| 抖音 | Cookie（避免风控） | 待补充 |
| 快手 | 需中国大陆 IPv4 家宽 IP | [快手配置](/guide/introduce/live/快手.html) |
| Twitch | 登录信息（获取更高画质） | [Twitch 配置](/guide/introduce/live/twitch.html) |
| YouTube | cookies 文件（访问受限内容） | [YouTube 配置](/guide/introduce/live/youtube.html) |
| AcFun | - | [AcFun 配置](/guide/introduce/live/acfun.html) |
| AfreecaTV | - | [AfreecaTV 配置](/guide/introduce/live/afreecatv.html) |
| FlexTV | - | [FlexTV 配置](/guide/introduce/live/flextv.html) |
| NicoNico | - | [NicoNico 配置](/guide/introduce/live/nico.html) |
| YY 语音 | - | [YY 语音配置](/guide/introduce/live/YY语音.html) |
| 克拉克拉 | - | [克拉克拉配置](/guide/introduce/live/克拉克拉.html) |
| 映客 | - | [映客配置](/guide/introduce/live/映客.html) |
| 猫耳 FM | - | [猫耳FM 配置](/guide/introduce/live/猫耳FM.html) |
| 网易 CC | - | [网易CC 配置](/guide/introduce/live/网易CC.html) |

> 各平台详细配置参数见对应链接页面。

---

## 通用配置说明

### Cookie 文件配置

部分平台需要登录态 Cookie 才能录制（如哔哩哔哩、YouTube、Twitch 等）。

Cookie 文件放置路径：
- Windows：`%APPDATA%\biliup\cookies.json`
- Linux / macOS：`~/.config/biliup/cookies.json`

格式支持 Netscape Cookie 文件或 JSON 数组，详见[登录方式详解 - Cookie 文件登录](/guide/introduce/introduce/login.html#方式五网页-cookie-文件登录)。

### 下载器选择

各平台对下载器的兼容性不同：

| 下载器 | 适用平台 | 说明 |
|---|---|---|
| `stream-gears`（默认） | 大部分平台 | 不支持 HLS 流 |
| `streamlink` | B站（HLS）、YouTube、Twitch | 需安装 FFmpeg |
| `ffmpeg` | 全部平台 | 通用但资源占用较高 |
| `sync-downloader` | 支持边录边传的平台 | 需稳定上行带宽 |

### 境外服务器录制 B站

如在非中国大陆服务器上录制 B站直播，需要配置 API 反代：

1. 准备一台国内服务器，搭建反代（Nginx / Caddy / 宝塔）
2. 反代目标：`https://api.live.bilibili.com`
3. 反代成功后打开反代地址应显示 B站 404 页面
4. 将反代地址填入「空间配置 → 各平台设置 → 哔哩哔哩 → 直播主 API」

---

## 常见问题

### 某个平台无法录制

1. 确认已添加正确的直播间链接
2. 检查该平台是否需要 Cookie
3. 尝试切换下载器（如 `stream-gears` 失败，换 `streamlink`）
4. 查看日志（`/logviewer`）确认具体错误

### 录制文件花屏

通常是下载器不支持该平台的流格式，尝试切换到 `streamlink` 或 `ffmpeg`。

### 弹幕录制失败

弹幕录制依赖 FFmpeg，请先完成 [FFmpeg 安装](/guide/docs/ffmpeg安装.html)，再在主播编辑页面开启「弹幕录制」。

---

## 相关链接

- [全局设置](/guide/introduce/Config/GlobalConfig.html)
- [登录方式详解](/guide/introduce/introduce/login.html)
- [FFmpeg 安装](/guide/docs/ffmpeg安装.html)
- [WebUI 使用指南](/guide/webui/usage.html)
