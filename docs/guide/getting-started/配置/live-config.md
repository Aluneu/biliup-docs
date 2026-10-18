# 各平台设置

此页面索引各直播平台的独立配置说明。各平台详细配置请点击对应链接查看。

::: tip
大部分平台使用默认下载器 `mesio` 即可，无需额外配置。以下仅列出需要特殊配置的平台。
:::


---

## 平台配置索引

| 平台 | 需要配置的项 | 详情链接 |
|---|---|---|
| 哔哩哔哩 | Cookie、直播流协议、API 反代 | [哔哩哔哩配置](/guide/getting-started/平台配置/哔哩哔哩.html) |
| 虎牙 | CDN 线路优选 | [虎牙配置](/guide/getting-started/平台配置/虎牙.html) |
| 斗鱼 | CDN 线路优选 | [斗鱼配置](/guide/getting-started/平台配置/斗鱼.html) |
| 抖音 | Cookie（避免风控）、弹幕、双屏 | [抖音配置](/guide/getting-started/平台配置/抖音.html) |
| 快手 | 需中国大陆 IPv4 家宽 IP | [快手配置](/guide/getting-started/平台配置/快手.html) |
| Twitch | 登录信息（获取更高画质） | [Twitch 配置](/guide/getting-started/平台配置/twitch.html) |
| YouTube | cookies 文件（访问受限内容）、弹幕 | [YouTube 配置](/guide/getting-started/平台配置/youtube.html) |
| TwitCasting | 弹幕、密码房 | [TwitCasting 配置](/guide/getting-started/平台配置/TwitCasting.html) |
| Bigo | 无需特殊配置 | [Bigo 配置](/guide/getting-started/平台配置/Bigo.html) |
| AcFun | - | [AcFun 配置](/guide/getting-started/平台配置/acfun.html) |
| AfreecaTV | - | [AfreecaTV 配置](/guide/getting-started/平台配置/afreecaTV.html) |
| NicoNico | - | [NicoNico 配置](/guide/getting-started/平台配置/nico.html) |
| YY 语音 | - | [YY 语音配置](/guide/getting-started/平台配置/YY语音.html) |
| 克拉克拉 | - | [克拉克拉配置](/guide/getting-started/平台配置/克拉克拉.html) |
| 映客 | - | [映客配置](/guide/getting-started/平台配置/映客.html) |
| 猫耳 FM | - | [猫耳FM 配置](/guide/getting-started/平台配置/猫耳FM.html) |
| 网易 CC | - | [网易CC 配置](/guide/getting-started/平台配置/网易CC.html) |
| Picarto | 无内置插件，走 streamlink / yt-dlp | [Picarto 配置](/guide/getting-started/平台配置/Picarto.html) |
| TTingLive | 无内置插件，走 streamlink / yt-dlp | [TTingLive 配置](/guide/getting-started/平台配置/TTingLive.html) |

> 各平台详细配置参数见对应链接页面或下方补充说明。

---

## 抖音配置

| 配置项 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `douyin_quality` | Select | 画质：`origin`(原画)/`uhd`/`hd`/`sd`/`ld`/`md` | — |
| `douyin_protocol` | Select | 直播流协议：`flv`/`hls` | `flv` |
| `douyin_danmaku` | Switch | 录制弹幕 | 关闭 |
| `douyin_double_screen` | Switch | 双屏直播录制 | 关闭 |
| `douyin_true_origin` | Switch | 抖音真原画（HEVC） | 关闭 |
| `user.douyin_cookie` | Input | Cookie（避免风控、解锁首页直播录制） | — |

---

## TwitCasting 配置

| 配置项 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `twitcasting_quality` | Select | 画质：`high`/`medium`/`low` | — |
| `twitcasting_danmaku` | Switch | 录制弹幕 | 关闭 |
| `twitcasting_password` | Input | 密码房访问密码 | — |
| `user.twitcasting_cookie` | Input | Cookie | — |

链接示例：`https://twitcasting.tv/username`

---

## Bigo 配置

Bigo 平台无需特殊配置，使用默认下载器 `mesio` 即可。

链接示例：`https://www.bigo.tv/123456`

---

## 通用配置说明

### Cookie 文件配置

部分平台需要登录态 Cookie 才能录制（如哔哩哔哩、YouTube、Twitch 等）。

Cookie 文件放置路径：
- Windows：`%APPDATA%\biliup\cookies.json`
- Linux / macOS：`~/.config/biliup/cookies.json`

格式支持 Netscape Cookie 文件或 JSON 数组，详见[登录方式详解 - Cookie 文件登录](/guide/getting-started/配置/login.html#方式五-网页-cookie-文件登录)。

### 下载器选择

各平台对下载器的兼容性不同：

| 下载器 | 适用平台 | 说明 |
|---|---|---|
| `mesio`（默认） | 大部分平台 | Rust 实现，进程内下载与修复，无外部依赖 |
| `stream-gears` | 大部分平台 | 上一版本的默认下载器（v1.2.9 起默认改为 `mesio`）；v1.3.0 起支持 HLS（TS / fMP4），收尾不再丢最后一个 GOP |
| `streamlink` | B站（HLS）、YouTube、Twitch | 需安装 FFmpeg |
| `ffmpeg` | 全部平台 | 通用但资源占用较高 |
| `sync-downloader` | 支持边录边传的平台 | 需稳定上行带宽 |
| `ytarchive` | YouTube Live | 专为 YouTube 直播设计 |

完整清单与说明见[全局设置 - 下载器](./global-config.html#下载器)。

### 境外服务器录制 B站

如在非中国大陆服务器上录制 B站直播，需要配置 API 反代：

1. 准备一台国内服务器，搭建反代（Nginx / Caddy / 宝塔）
2. 反代目标：`https://api.live.bilibili.com`
3. 反代成功后打开反代地址应显示 B站 404 页面
4. 将反代地址填入「空间配置 → 各平台设置 → 哔哩哔哩 → 直播主 API」

---

## B站补充配置项

以下配置项在平台配置页面中可用，补充说明：

| 配置项 | 说明 |
|---|---|
| `bilibili_danmaku_detail` | 录制详细弹幕（含昵称/UID/醒目留言/上舰/礼物） |
| `bilibili_danmaku_raw` | 录制 B站原始弹幕数据 |
| `bili_force_source` | 强制真原画 |
| `bili_anonymous_origin` | 免登录原画 |
| `bili_hls_transcode_timeout` | hls_fmp4 转码等待时间（秒，默认 60） |
| `bili_replace_cn01` | cn01 节点替换 |

---

## 虎牙补充配置项

| 配置项 | 说明 |
|---|---|
| `huya_max_ratio` | 码率上限 |
| `huya_cdn_fallback` | CDN 回退 |
| `huya_protocol` | 协议选择 |
| `huya_imgplus` | 二次编码（**默认开启**；2K/4K 超分与 HDR 依赖它，谨慎关闭） |
| `huya_codec` | 编码选择（264/265） |
| `huya_mobile_api` | 移动端 API |

---

## 斗鱼补充配置项

| 配置项 | 说明 |
|---|---|
| `douyu_cookie` | 斗鱼网页版登录 Cookie（请求头字符串或浏览器 JSON 导出）。原画等高码率需要登录 |
| `douyu_ltp0` | 长期续期凭据 `LTP0`（仅本机保存，不下发 Fleet）|
| `douyu_refresh_device_id` | 续期用的 Web 设备号 `dy_did` |
| `douyu_auto_refresh` | 是否自动续期，有 `LTP0` 时默认开启 |
| `douyu_cdn` | 斗鱼 CDN 节点 |
| `douyu_force_hs` | 强制 hs 流使用构造链接 |
| `douyu_rate` | 请求的最高画质档位：`0` 原画 / `8` 蓝光 8M / `4` 蓝光 4M / `3` 超清 / `2` 高清 |
| `douyu_codec` | 视频编码：`AVC`（默认）或 `HEVC`（需 `mesio` 或支持的新版 FFmpeg）|
| `douyu_device_id` | 对应 Cookie 中 `acf_did` 的值 |
| `douyu_disable_interactive_game` | 跳过互动游戏（不录制互动游戏画面） |

> 登录、续期与画质排查见[斗鱼平台配置](/guide/getting-started/平台配置/斗鱼.html)。

---

## 网易 CC / 克拉克拉补充配置项

| 配置项 | 说明 |
|---|---|
| `cc_protocol` | 网易 CC 直播协议：`hls` 或 `flv` |
| `kila_protocol` | 克拉克拉直播协议：`hls` 或 `flv` |

---

## Twitch 补充配置项

| 配置项 | 说明 |
|---|---|
| `twitch_danmaku` | 弹幕录制 |
| `twitch_disable_ads` | 禁用广告（**默认开启**） |

---

## YouTube 补充配置项

| 配置项 | 说明 |
|---|---|
| `youtube_prefer_vcodec` | 首选视频编码（`av01`/`vp9`/`avc`） |
| `youtube_prefer_acodec` | 首选音频编码（`opus`/`mp4a`） |
| `youtube_max_resolution` | 最大分辨率 |
| `youtube_max_videosize` | 最大视频大小 |
| `youtube_after_date` | 开始日期，只处理该日期之后的内容 |
| `youtube_before_date` | 结束日期，只处理该日期之前的内容 |
| `youtube_enable_download_live` | 启用直播下载（**默认开启**） |
| `youtube_enable_download_playback` | 启用回放下载（**默认开启**） |
| `youtube_danmaku` | 弹幕录制（旧字段 `ytb_danmaku` 仍兼容，作用相同） |

---

## 常见问题

### 某个平台无法录制

1. 确认已添加正确的直播间链接
2. 检查该平台是否需要 Cookie
3. 确认下载器：默认 `mesio` 支持大部分平台的 FLV / HLS（含 HEVC 与 B站 `hls_fmp4`）；仍在用 `stream-gears` 的话先换回 `mesio`，特定需求再考虑 `streamlink` / `ffmpeg`
4. 查看日志（`/logviewer`）确认具体错误

### 录制文件花屏

通常是下载器不支持该平台的流格式，尝试切换到默认 `mesio`，或 `streamlink` / `ffmpeg`。

### 弹幕录制失败

弹幕录制自 v1.2.0 起由 Rust 弹幕客户端在进程内完成，**不依赖 FFmpeg**，在主播编辑页面开启「弹幕录制」即可。若弹幕缺失，优先检查平台是否需要 Cookie（如 B站、抖音）以及对应平台的弹幕开关字段（如 `bilibili_danmaku`）。

---

## 相关链接

- [全局设置](/guide/getting-started/配置/global-config.html)
- [登录方式详解](/guide/getting-started/配置/login.html)
- [FFmpeg 安装](/guide/getting-started/安装部署/ffmpeg安装.html)
- [WebUI 使用指南](/guide/webui/usage.html)
