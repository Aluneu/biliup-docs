::: info
* 直播间 / 频道链接格式：`https://www.youtube.com/@频道名/videos`（频道名替换为目标频道）。
* 支持 **直播** 与 **VOD（点播/回放）** 录制，可指定回放下载日期。
* 访问受限内容（会员 / 地区限制）需要配置 **登录信息（Cookie）**。
:::


::: tip
* 推荐使用 `streamlink` 或 `yt-dlp` 下载器以获得更好兼容性，需先完成 [FFmpeg 安装](../安装部署/ffmpeg安装.html)。
* 支持通过 **Yaml 源文件**添加 YouTube 直播源与 VOD，详见[开发者选项](../配置/developer-options.html)。
:::


----

## 支持的链接形式

YouTube 插件本身负责**解析**，实际下载仍交给配置的下载器。链接分两类：

| 链接 | 解析方式 | 说明 |
|---|---|---|
| `https://www.youtube.com/feeds/videos.xml?channel_id=UCxxx` | 原生 XML | 频道 RSS，全内容 |
| `...?playlist_id=UULFxxx` | 原生 XML | 只要长视频（RSS 视图） |
| `...?playlist_id=UUSHxxx` | 原生 XML | 只要 Shorts |
| `...?playlist_id=UULVxxx` | 原生 XML | 只要直播回放 |
| `https://www.youtube.com/@频道名`、`/channel/UCxxx` | `yt-dlp --flat-playlist` | 频道页，只做轻量枚举 |
| `https://www.youtube.com/playlist?list=PLxxx` | `yt-dlp --flat-playlist` | 播放列表 |
| `https://www.youtube.com/results?search_query=关键词` | `yt-dlp --flat-playlist` | 搜索结果 |
| `https://www.youtube.com/watch?v=xxx`、`https://youtu.be/xxx` | `yt-dlp` / 直链 | 单个视频或直播 |

::: warning 需要本机有 yt-dlp
除 RSS 订阅（原生解析）以外，YouTube 的枚举与直链提取都调用 `yt-dlp`，**PATH 里没有 `yt-dlp` 时会直接失败**。RSS 链接省掉这一次调用，适合订阅固定频道、批量搬运。
:::

> 频道 / 播放列表 / 搜索结果会一次枚举出多个条目，每个条目按自己的视频 ID 录制。想限制数量请用 `youtube_after_date` / `youtube_before_date` 收窄时间范围。

## 登录信息（Cookie）

* 配置 YouTube 登录信息（Cookie 文件）后可解锁受限内容、提升稳定性。请在[登录方式详解](../配置/login.html)中了解网页 Cookie 文件登录，并在主播编辑页关联。

## 回放下载日期

* YouTube 支持按日期筛选并下载历史回放，在添加直播源时按需指定即可。

----

## 编码偏好

### 首选视频编码（youtube_prefer_vcodec）

* 选择优先录制的视频编码：`av01` / `vp9` / `avc`。默认自动。

### 首选音频编码（youtube_prefer_acodec）

* 选择优先录制的音频编码：`opus` / `mp4a`。默认自动。

## 弹幕录制（youtube_danmaku）

* 开启后录制 YouTube 弹幕（HTTP 轮询获取），弹幕输出为 B站兼容的 XML 格式。默认关闭。

----

## 相关链接

* [登录方式详解](../配置/login.html)
* [全局设置](../配置/global-config.html)
* [各平台设置](../配置/live-config.html)
* [开发者选项](../配置/developer-options.html)
