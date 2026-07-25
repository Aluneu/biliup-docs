::: info
* 直播间链接格式：`https://twitcasting.tv/用户名`（用户名为频道名）。
* 支持**弹幕录制**与**密码房**录制。
* 可配置登录信息以获取更稳定的直播流。
:::


::: tip
* 支持通过 **Yaml 源文件**添加 TwitCasting 直播源，详见[开发者选项](../配置/developerOptions.html)。
:::


----

## 画质（twitcasting_quality）

* 选择录制画质：`high` / `medium` / `low`。

## 弹幕录制（twitcasting_danmaku）

* 开启后录制 TwitCasting 弹幕（WebSocket JSON 协议），弹幕输出为 B站兼容的 XML 格式。默认关闭。

## 密码房（twitcasting_password）

* 填写密码房访问密码，用于录制设置了密码的直播间。

## 登录信息（user.twitcasting_cookie）

* 填写 TwitCasting Cookie，用于登录态录制。可在[登录方式详解](../配置/login.html)中了解网页 Cookie 文件登录。

----

## 相关链接

* [登录方式详解](../配置/login.html)
* [全局设置](../配置/GlobalConfig.html)
* [各平台设置](../配置/liveconfig.html)
* [开发者选项](../配置/developerOptions.html)
