> [!IMPORTANT]
> * 直播间 / 频道链接格式：`https://www.youtube.com/@频道名/videos`（频道名替换为目标频道）。
> * 支持 **直播** 与 **VOD（点播/回放）** 录制，可指定回放下载日期。
> * 访问受限内容（会员 / 地区限制）需要配置 **登录信息（Cookie）**。

> [!TIP]
> * 推荐使用 `streamlink` 或 `yt-dlp` 下载器以获得更好兼容性，需先完成 [FFmpeg 安装](../安装部署/ffmpeg安装.html)。
> * 支持通过 **Yaml 源文件**添加 YouTube 直播源与 VOD，详见[开发者选项](../配置/developerOptions.html)。

----

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
* [全局设置](../配置/GlobalConfig.html)
* [各平台设置](../配置/liveconfig.html)
* [开发者选项](../配置/developerOptions.html)
