::: info
biliup 能够支持数十个直播与视频平台、并稳定完成录制与弹幕采集，离不开社区中众多优秀开源项目的支撑。本页向这些项目的开发者与维护者致以诚挚的感谢。
:::

## 核心依赖

### 下载器

biliup 对大量直播 / 视频平台的流解析与下载能力，建立在以下成熟下载器项目之上：

| 项目 | 简介 | 在 biliup 中的作用 | 仓库地址 |
| --- | --- | --- | --- |
| **mesio / rust-srec** | Rust 实现的直播流下载与修复库 | v1.2.9 起的默认下载器，进程内完成 FLV / HLS 下载与时间戳修复 | [hua0512/rust-srec](https://github.com/hua0512/rust-srec) |
| **stream-gears** | biliup 自研的 Rust 下载与上传内核 | 提供 FLV / HLS 下载、断流重连与 GOP 收尾 | [biliup/stream-gears](https://github.com/biliup/stream-gears) |
| **streamlink** | 从流媒体服务提取并录制直播流的命令行工具 | 备选下载器，处理部分 HLS 平台 | [streamlink/streamlink](https://github.com/streamlink/streamlink) |
| **yt-dlp** | 广为人知的命令行视频下载工具 | 通用适配器（General）与 YouTube 等平台的下载后端 | [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) |

> 历史依赖：[ykdl](https://github.com/ykdl/ykdl) 与 [youtube-dl](https://github.com/ytdl-org/youtube-dl) 出现在 Python 时代的致谢里，v1.3.0 代码中已不再引用。

### 弹幕库

| 项目 | 简介 | 在 biliup 中的作用 | 仓库地址 |
| --- | --- | --- | --- |
| **THMonster/danmaku** | 多平台弹幕协议解析库 | 提供直播弹幕录制能力，输出标准 XML 弹幕文件 | [THMonster/danmaku](https://github.com/THMonster/danmaku) |
| **DanmakuFactory** | 弹幕 XML → ASS 转换工具 | v1.3.0 起 biliup 内置了原生 Rust 转换实现（排版逻辑派生自该项目），无需再单独安装 | [hihkm/DanmakuFactory](https://github.com/hihkm/DanmakuFactory) |

### 字体

录后合成与弹幕压制使用 **Noto Sans CJK SC** 与 **Noto Emoji**，均以 SIL Open Font License 分发，随 CLI 发布包 / 桌面安装包 / Docker 镜像提供。

## 特别感谢

- 感谢 biliup 项目的所有代码贡献者、文档维护者与社区成员；
- 感谢每一位参与测试、反馈问题、提交 Issue 与 Pull Request 的用户；
- 本中文文档站基于 biliup 项目整理与翻译，版权归各项目所有。

::: tip 许可证
上述项目均遵循各自的开源许可证。使用 biliup 时，请同时遵守相关依赖的许可条款。
:::
