::: info
biliup 能够支持数十个直播与视频平台、并稳定完成录制与弹幕采集，离不开社区中众多优秀开源项目的支撑。本页向这些项目的开发者与维护者致以诚挚的感谢。
:::

## 核心依赖

### 下载器

biliup 对大量直播 / 视频平台的流解析与下载能力，建立在以下成熟下载器项目之上：

| 项目 | 简介 | 在 biliup 中的作用 | 仓库地址 |
| --- | --- | --- | --- |
| **ykdl** | 支持国内外多个视频与直播平台的下载库 | 提供大量国内平台（B 站、斗鱼、虎牙等）的流地址解析 | [ykdl/ykdl](https://github.com/ykdl/ykdl) |
| **youtube-dl** | 广为人知的命令行视频下载工具 | 提供广泛的视频平台下载与解析能力 | [ytdl-org/youtube-dl](https://github.com/ytdl-org/youtube-dl) |
| **streamlink** | 从流媒体服务提取并录制直播流的命令行工具 | 提供直播流提取与录制能力，是 biliup 录制的重要基础 | [streamlink/streamlink](https://github.com/streamlink/streamlink) |

### 弹幕库

| 项目 | 简介 | 在 biliup 中的作用 | 仓库地址 |
| --- | --- | --- | --- |
| **THMonster/danmaku** | 多平台弹幕协议解析库 | 提供直播弹幕录制能力，输出标准 XML 弹幕文件 | [THMonster/danmaku](https://github.com/THMonster/danmaku) |

## 特别感谢

- 感谢 biliup 项目的所有代码贡献者、文档维护者与社区成员；
- 感谢每一位参与测试、反馈问题、提交 Issue 与 Pull Request 的用户；
- 本中文文档站基于 biliup 项目整理与翻译，版权归各项目所有。

::: tip 许可证
上述项目均遵循各自的开源许可证。使用 biliup 时，请同时遵守相关依赖的许可条款。
:::
