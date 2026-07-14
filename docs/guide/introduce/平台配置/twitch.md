> [!IMPORTANT]
> * 直播间链接格式：`https://www.twitch.tv/用户名`（用户名为频道名）。
> * 支持 **直播** 与 **VOD（点播/回放）** 录制。
> * 可配置**登录信息**以获取更高画质与更稳定的直播流。

> [!TIP]
> * 支持通过 **Yaml 源文件**添加 Twitch 直播源与 VOD，详见[开发者选项](../配置/developerOptions.html)。
> * 推荐使用 `streamlink` 下载器以获得更好兼容性，需先完成 [FFmpeg 安装](../安装部署/ffmpeg安装.html)。

----

## 登录信息

* 配置 Twitch 登录信息后，可解锁更高画质并提升录制稳定性。请在[登录方式详解](../配置/login.html)中配置对应账号，并在主播编辑页关联。

----

## 弹幕录制（twitch_danmaku）

* Twitch 弹幕通过 WebSocket（IRC 协议）获取，开启「弹幕录制」后即可录制对应直播间的弹幕。
* 弹幕输出为 B站兼容的 XML 格式，可配合 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory) 进行弹幕压制。

----

## 回放录制

* Twitch 支持录制已结束的 VOD（回放），在添加直播源时填入回放链接即可，**推荐**用于补录错过的直播。

----

## 相关链接

* [登录方式详解](../配置/login.html)
* [全局设置](../配置/GlobalConfig.html)
* [各平台设置](../配置/liveconfig.html)
* [开发者选项](../配置/developerOptions.html)
