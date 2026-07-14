# 支持的直播平台

## 直播平台列表

| 直播平台 | 支持类型 | 链接示例 | 备注 |
|----------|----------|----------|------|
| 哔哩哔哩 | 直播 | `https://live.bilibili.com/123456` | HLS分区需streamlink/可录制弹幕 |
| 斗鱼 | 直播 | `https://www.douyu.com/123456` | 可录制弹幕 |
| 虎牙 | 直播 | `https://www.huya.com/123456` | 可录制弹幕 |
| 抖音 | 直播 | `https://live.douyin.com/123456` | 可录制弹幕/主页/风控需Cookie |
| 快手 | 直播 | `https://live.kuaishou.com/u/biliup123` | 需大陆家宽/风控严格 |
| 网易CC | 直播 | `https://cc.163.com/123456` | — |
| YY语音 | 直播 | `https://www.yy.com/123456` | — |
| 映客 | 直播 | `https://www.inke.cn/liveroom/index.html?uid=123456` | — |
| 猫耳FM | 直播 | `https://fm.missevan.com/live/123456` | 纯音频流 |
| acfun | 直播 | `https://live.acfun.cn/live/123456` | — |
| 克拉克拉 | 直播 | `https://live.kilakila.cn/PcLive/index/detail?id=123456` | HLS/FLV |
| BIGO | 直播 | `https://www.bigo.tv/123456` | — |
| Picarto | 直播 | — | — |
| afreecaTV | 直播 | `https://play.afreecatv.com/biliup123/123456` | 部分需登录 |
| flextv | 直播 | `https://www.flextv.co.kr/channels/123456/live` | — |
| nico | 直播 | `https://live.nicovideo.jp/watch/lv123456` | 可配置登录信息 |
| TwitCasting | 直播 | `https://twitcasting.tv/username` | 可录制弹幕/支持密码房 |
| TTingLive | 直播 | — | — |
| Twitch | 直播 / VOD | `https://www.twitch.tv/biliup123` | 可配置登录/支持弹幕/推荐录回放 |
| YouTube | 直播 / VOD | `https://www.youtube.com/@biliup123/videos` | 可配置登录/支持回放下载日期/可录制弹幕 |

---

## 弹幕录制支持

以下平台支持弹幕录制，在主播编辑页面开启「弹幕录制」即可：

| 平台 | 弹幕配置字段 | 协议 |
|---|---|---|
| 哔哩哔哩 | `bilibili_danmaku` | WebSocket（二进制+压缩） |
| 斗鱼 | `douyu_danmaku` | TCP（STT 协议） |
| 虎牙 | `huya_danmaku` | WebSocket（TARS 协议） |
| 抖音 | `douyin_danmaku` | WebSocket（Protobuf 协议） |
| Twitch | `twitch_danmaku` | WebSocket（IRC 协议） |
| TwitCasting | `twitcasting_danmaku` | WebSocket（JSON 协议） |
| YouTube | `youtube_danmaku` | HTTP 轮询 |

> [!TIP]
> 弹幕录制输出为 B站兼容的 XML 格式，可配合 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory) 进行弹幕压制。

---

## Yaml 源文件

以下平台可通过 Yaml 文件的方式添加直播源：

| 平台 | 支持类型 |
|------|----------|
| Twitch | 直播 / VOD |
| NicoNico | 直播 / 时间表 |
| Pixiv Sketch | 直播 |
| Mirrativ | 直播 |
| Mildom | 直播 |
| 抖音 | 直播（备用方案） |
| Showroom | 直播 |
| TwitCasting | 直播 |
| Whowatch | 直播 |

---

## 其他兼容平台

理论上 `streamlink` 与 `yt-dlp` 支持的平台均可下载，但不保证稳定性：

- [streamlink 支持列表](https://streamlink.github.io/plugins.html)
- [yt-dlp 支持列表](https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/extractor)

> [!TIP]
> 对于不在内置列表中的平台，可使用 `General`（通用）下载器，支持任意 streamlink/yt-dlp 兼容的 URL。
