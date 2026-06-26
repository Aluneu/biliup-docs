# 更新日志

本页面记录 biliup 各版本的变更内容。

> ⚠️ 从 v1.0.0 开始，biliup 合并了原 `biliup`、`biliup-rs`、`biliup-app` 三个项目，采用 Rust + Python + Next.js 统一架构。

---

## 标签含义

| 标签 | 含义 |
|---|---|
| 💡 | 新添加的功能 |
| 🔧 | 已修复的问题 |
| ⚠️ | 需要手动操作的更新（配置变更、不兼容修改等）|

---

## v1.2.1

> 发布时间：2026-06-05

- 🔧 具体变更请查看 [v1.2.0 → v1.2.1 完整对比](https://github.com/biliup/biliup/compare/v1.2.0...v1.2.1)

> 该版本 Release Notes 仅包含对比链接，详细变更请访问上方链接查看。

---

## v1.2.0

> 发布时间：2024-05-31

- 💡 适配新版本斗鱼直播源 [@xxxxuanran]
- 💡 `upload_by_config` 支持通过 Web 提交视频配置 [@gwy15]
- 🔧 修复虎牙 `WEB_ROOM_DATA_REGEX` 正则错误匹配 HTML 转义的问题 [@xxxxuanran]
- 🔧 修复上传失败后重建 segment 通道，避免后续视频段被静默丢弃 [@Micuks]
- 💡 使用 Rust 重构弹幕客户端实现 [@xxxxuanran]
- 💡 启用 `segment_processor` 阶段，新增 `remux:mp4` 内置钩子 [@Micuks]
- 💡 新增评论和回复命令支持 (`comments` / `reply`) [@fchange]
- 💡 更新 `CHANGELOG.md` 及其他项目文档 [@XenoAmess]

**新贡献者：** @gwy15, @Micuks, @fchange, @XenoAmess

---

## v1.1.29

> 发布时间：2024-03-01

- 🔧 使用 `getCdnTokenInfoEx` API 重构虎牙 anticode 生成逻辑 [@xxxxuanran]
- 🔧 修复使用 `os.path.basename` 提取文件名的问题 [@lovegaoshi]
- 💡 命令行支持通过 Web 接口投稿 [@zhangaoyun]
- 💡 新增合集（Season）管理功能 [@112292454]
- 💡 新增配置文件参数支持 [@Sora3QwQ]

**新贡献者：** @lovegaoshi, @zhangaoyun, @112292454

---

## v1.1.28

> 发布时间：2023-12-14

- 🔧 从 HLS 流中提取斗鱼 `stream_id` [@xxxxuanran]
- 🔧 优化断点续传、标题自动截断及限流重试逻辑 [@DzmingLi]

---

## v1.1.27

> 发布时间：2023-11-30

- 🔧 具体变更请查看 [v1.1.26 → v1.1.27 完整对比](https://github.com/biliup/biliup/compare/v1.1.26...v1.1.27)

---

## v1.1.26

> 发布时间：2023-11-29

- 💡 为 `biliup-cli` 添加 Nix flake 支持，优化路径处理逻辑 [@DzmingLi]
- 🔧 修复 `shellexpand::tilde` 类型错误，优化 Nix 构建流程 [@DzmingLi]
- 🔧 修复斗鱼直播源，强制使用构造的 URL 用于 hls-h5 [@Sora3QwQ]

**新贡献者：** @DzmingLi, @Sora3QwQ

---

## v1.1.25

> 发布时间：2023-11-26

- 🔧 具体变更请查看 [v1.1.24 → v1.1.25 完整对比](https://github.com/biliup/biliup/compare/v1.1.24...v1.1.25)

---

## v1.1.24

> 发布时间：2023-11-19

- 🔧 具体变更请查看 [v1.1.23 → v1.1.24 完整对比](https://github.com/biliup/biliup/compare/v1.1.23...v1.1.24)

---

## v1.1.23

> 发布时间：2023-11-18

- 🔧 具体变更请查看 [v1.1.22 → v1.1.23 完整对比](https://github.com/biliup/biliup/compare/v1.1.22...v1.1.23)

---

## v1.1.22

> 发布时间：2023-11-17

- 🔧 具体变更请查看 [v1.1.21 → v1.1.22 完整对比](https://github.com/biliup/biliup/compare/v1.1.21...v1.1.22)

---

## v1.1.21

> 发布时间：2023-11-03

- 🔧 具体变更请查看 [v1.1.20 → v1.1.21 完整对比](https://github.com/biliup/biliup/compare/v1.1.20...v1.1.21)

---

## v1.1.20

> 发布时间：2023-10-30

- 🔧 具体变更请查看 [v1.1.19 → v1.1.20 完整对比](https://github.com/biliup/biliup/compare/v1.1.19...v1.1.20)

---

## v1.1.0 ~ v1.1.19

> 各版本详细变更请参考 [GitHub Releases](https://github.com/biliup/biliup/releases?page=1)

---

## v1.0.0

> 发布时间：2023 年（合并版本）

🎉 **重大版本更新** — biliup 合并原 `biliup`（Python CLI）、`biliup-rs`（Rust 上传引擎）、`biliup-app`（WebUI）三个项目，统一为单一仓库。

- 💡 核心下载引擎部分迁移至 Rust（`biliup-rs` 合并）
- 💡 内置基于 Next.js 的 WebUI 管理界面（原 `biliup-app` 合并）
- 💡 新增 `server` 子命令，一站式启动录制服务 + Web 管理界面
- 💡 数据库取代配置文件（自动从旧版 YAML 配置迁移）
- ⚠️ 升级前请备份旧版 `config.yaml` / `config.toml`

---

## v0.4.34

> 更新时间：2024-01-27

- 💡 新增随机 UA 功能以及统一使用来解决部分平台请求 API / 弹幕录制风控问题 [@Kataick]
- 🔧 优化 WebUI 处理时间的函数 [@Kataick]
- 🔧 解决文件上传乱序的问题 [@storyxc]
- 🔧 解决从旧版 Config 中读取 postprocessor 指令并写入数据库的格式错误，导致 postprocessor 无法执行的问题 [@boxie123]

---

## v0.4.32 / v0.4.33

> ⚠️⚠️⚠️⚠️⚠️⚠️ 超大版本更新，在升级到此版本之前请认真阅读说明。

> 更新时间：2023 年末

- 🔧 自动修正 `stream_gears` 设置不支持的 format [@Kataick]
- 🔧 修复分段下载时 `streamlink` 不会退出的问题 [@dreammu]
- 💡 AfreecaTV 添加账号密码登录，直播间标题 [@CoolZxp]
- 🔧 修复快手直播录制，因风控严格暂时移除快手 CDN 及流类型选择 [@CoolZxp]
- 🔧 优化 BiliLive 部分运行逻辑（添加登录验证，原画链接复用，使用移动端房间信息，获取正确 emoji 标题）[@xxxxuanran]
- 💡 **数据库存档**（替代原本的 config 文件，在此版本之后，老版本的 config 将会在第一次启动被读取并写入新的数据库中，之后将不再使用 config 文件）[@boxie123]
- 🔧 修复在 py3.7 版本运行问题 [@CoolZxp]
- 💡 添加 Bigo 支持 [@CoolZxp]
- 🔧 兼容 `stream-gears` 在无 Cookie 时的下载 [@xxxxuanran]
- 🔧 标题为空时下载报错 [@boxie123]
- 🔧 修复弹幕重新连接时覆盖原有弹幕问题 [@CoolZxp]
- 🔧 修复斗鱼下播后可能会录制回放问题 [@CoolZxp]
- 🔧 修复使用 `biliup-rs` 上传后内存不会清空的问题 [@CoolZxp]
- 🔧 猫耳 FM 提供格式默认值 [@xxxxuanran]
- 💡 **新增 WEBUI 支持**，可在 WEBUI 进行所有的设置与管理 [@boxie123]

---

## v0.4.31

> 更新时间：2023-09-12

- 🔧 修复抖音弹幕问题 [@CoolZxp]

---

## v0.4.30

> ⚠️⚠️ 有重大问题，请勿使用该版本。

> 更新时间：2023-09-12

- 🔧 YouTube 配置说明修改 [@CoolZxp]
- 🔧 避免 Windows 可能的弹幕录制任务关闭失败 [@CoolZxp]
- 🔧 为部分检测添加超时时间避免检测时间过长 [@CoolZxp]
- 🔧 调整弹幕录制日志 [@CoolZxp]
- 🔧 斗鱼录制及弹幕对 URL 支持同步 [@CoolZxp]
- 🔧 修复斗鱼弹幕缺失 [@CoolZxp]
- 🔧 修复 Bilibili 弹幕缺失 [@CoolZxp]
- 🔧 抖音录制及弹幕对 URL 支持同步 [@CoolZxp]
- 🔧 抖音弹幕也会使用配置内的 Cookie [@CoolZxp]
- 🔧 适配新版抖音录制及弹幕 [@CoolZxp]
- 🔧 优化 Bilibili 提示报错 [@Kataick]
- 🔧 补全 yaml 配置文件抖音画质符号 [@Kataick]
- 💡 YouTube 添加缓存 [@CoolZxp]
- 💡 YouTube 跳过检测 after_date 日期后的视频及直播 [@CoolZxp]
- ⚠️ 修改 `preprocessor`（下载直播）、`downloaded_processor`（上传直播）时返回的开播及下播时间为时间戳 [@Kataick]

---

## v0.4.29

> 更新时间：2023-08-04

- 🔧 YouTube 配置说明修改 [@CoolZxp]
- 🔧 将上传录像时可以开始新的录制调整为默认功能 [@CoolZxp]
- 🔧 下载上传逻辑调整 [@CoolZxp]
- 🔧 上传后正确的删除弹幕 [@CoolZxp]
- 🔧 `downloaded_processor` 的时间被正确格式化以及明确时间默认值 [@Kataick]
- 🔧 `downloaded_processor` 的参数被正确格式化 [@Kataick]
- 🔧 `bili_web` 强制选择 UpOS 模式下的线路 [@1toldyou]
- 🔧 正确的检测进程空闲状态 [@CoolZxp]
- 🔧 正确的重启进程 [@CoolZxp]
- 💡 YouTube 添加单独下载直播和回放选项 [@CoolZxp]
- 💡 YouTube 添加 `streams` / `playlists` / `shorts` 类型链接支持 [@CoolZxp]
- 💡 YouTube 添加筛选无效时提示 [@CoolZxp]
- 💡 封面下载支持 webp [@CoolZxp]
- 💡 启动时删除临时缓存文件 [@CoolZxp]

---

## v0.4.28

> 更新时间：2023-07-30

- 🔧 在读取 YouTube 缓存失败时增加提示 [@CoolZxp]
- 🔧 调整 Twitch 日志输出 [@CoolZxp]
- 🔧 调整 Twitch / YouTube 封面下载逻辑 [@CoolZxp]
- 🔧 修复 YouTube 视频录制异常中断时多余文件不删除 [@CoolZxp]
- 🔧 兼容低版本 Python [@CoolZxp]
- 🔧 斗鱼请求优化 [@CoolZxp]
- 🔧 斗鱼适配移动端 URL [@CoolZxp]
- 🔧 斗鱼避免下播时可能的异常 [@CoolZxp]
- 🔧 避免上传时由于操作文件权限不足导致后处理失败 [@CoolZxp]
- 🔧 补充 `downloaded_processor` toml 配置 [@Kataick]
- 🔧 删除多余日志输出 [@Kataick]
- 🔧 让检测后能更快的开始下载 [@CoolZxp]
- 🔧 修复快手录制问题 [@CoolZxp]
- 💡 上传后封面自动删除 [@CoolZxp]
- 💡 `downloaded_processor` 增加返回参数（下播时间和视频列表）[@Kataick]
- 💡 `stream-gears` 升级至 0.1.19

---

## v0.4.27

> 更新时间：2023-07-29

- 🔧 修复虎牙拉流 403 分段问题 [@CoolZxp]
- 🔧 统一 `download.py` 的输出格式 [@Kataick]
- 🔧 修复抖音弹幕分段与录制 stop 的问题 [@CoolZxp]
- 🔧 调整直播流获取失败及下播延迟检测功能 [@CoolZxp]
- 🔧 优化下载流程与下载日志逻辑以及下播检测延迟阈值 [@CoolZxp]
- 🔧 虎牙画质修复 [@CoolZxp]
- 🔧 调整封面下载逻辑 [@CoolZxp]
- 🔧 调整批量检测功能 [@CoolZxp]
- 🔧 优化 YouTube 与 Twitch 下载策略 [@CoolZxp]
- 💡 添加斗鱼、虎牙、哔哩哔哩、抖音自选画质 [@CoolZxp]

---

## v0.4.26

> 更新时间：2023-07-27

- 🔧 修复虎牙直播流下载的问题 [@xxxxuanran]

---

## v0.4.25

> 更新时间：2023-07-27

- 💡 新增 NOW 直播 [@Kataick]
- 💡 新增映客直播 [@Kataick]
- 💡 增加 `downloaded_processor` 功能，支持结束录制时执行指定 Shell 指令 [@Kataick]

---

## v0.4.24

> 更新时间：2023 年中

- 🔧 修复哔哩哔哩 flv 流 403 的问题 [@xxxxuanran]

---

## v0.4.23

> 更新时间：2023-07-17

- 🔧 `preprocessor` 增加开播时返回主播名字和开播地址 [@Kataick]
- 🔧 修复当获取流失败后会触发获取流频繁的问题 [@Kataick]
- 🔧 优化设置大 `delay` 会出现漏录的问题 [@Kataick]
- 🔧 优化在 config 中读取值的代码写法 [@Kataick]
- 🔧 增加对 `yt-dlp` 的 `lazy_playlist` 功能支持 [@Kataick]
- 🔧 修复 `format` 为 `mp4` 时无法时间分段的问题 [@Kataick]
- 🔧 修复 `bilibili` 导致进程卡死问题 (`get_play_info`) [@Kataick]
- 🔧 修复 `afreecaTV` 导致进程卡死问题 [@Kataick]
- 🔧 修复快手导致进程卡死问题 [@Kataick]
- 🔧 去除 `quickjs` 依赖；相对应的修改了 Readme 和 Douyu [@xxxxuanran]
- 🔧 `Bililive` 兼容 APEX 分区 [@xxxxuanran]
- 🔧 `Kuaishou` 新增协议切换和 CDN 优选 [@xxxxuanran]
- 🔧 修正快手 HLS 流原画 [@xxxxuanran]
- 🔧 修复 `biliup-rs` 的参数绑定 [@hguandl]
- 💡 增加由于地区限制导致无法下载指定区域直播间的提示 [@xxxxuanran]
- 💡 增加对 `biliup-rs` 的支持（杜比音效、Hi-Res、转载、充电）[@Kataick]
- 💡 `bili_web` 上传插件新增简介 @ 功能 [@zzc10086]
- 💡 增加抖音弹幕录制支持 [@KNaiFen]

---

## v0.4.22

> 更新时间：2023-06-29

- 🔧 优化虎牙错误提示和抖音代码与错误提示 [@Kataick]
- 🔧 优化获取直播流失败时增加等待重试 [@Kataick]
- 🔧 修复 ffmpeg 时长分段时弹幕文件不会跟着分段的问题；修复防止重复请求流的功能工作异常的问题 [@KNaiFen]
- 🔧 修正 CHANGELOG 更新日志、修正 README.MD [@KNaiFen]
- 🔧 弹幕报错记录增加文件名部分，方便排查 BUG [@KNaiFen]
- 🔧 yaml、toml 配置文件注释修正，格式修正 [@KNaiFen]
- 💡「BETA」增加未上传完录像时同一主播重新开播是否立刻开始录制功能 [@Kataick]
- 💡「BETA」增加 cn01 的 fmp4 流获取真原画流功能 [@haha114514]

---

## v0.4.21

> 更新时间：2023-06-11

- 🔧 抖音增加获取错误时的提示并优化纯数字房间号的代码 [@Kataick]
- 🔧 修复虎牙与抖音关闭连接导致进程终止问题 [@Kataick]
- 🔧 同步 yaml 配置文件的更新到 toml 中 [@Kataick]
- 🔧 NICO 标题获取从 BS4 改为正则，开播后仍然重复请求的 BUG 的修复 [@KNaiFen]
- 🔧 添加 `quickjs` 依赖 [@haha114514]
- 💡 新增 NICO 录播 [@KNaiFen]
- 💡 增加 NICO 用户配置文件模板 [@KNaiFen]
- 💡 增加 Twitch 的去广告开关（解决广告分段问题）[@KNaiFen]
- 💡 增加 Twitch 弹幕录播、修复斗鱼、虎牙的弹幕录制 BUG 并增加报错提示，修改了 XML 文件的删除部分，修改了部分代码的协程的调用，优化断流时频繁重复请求 [@KNaiFen]

---

## v0.4.20

> 更新时间：2023-05-25

- 🔧 修复抖音可能导致进程卡死问题 [@KkakaMann]
- 🔧 改正部分下载器的日志等级，避免刷屏 [@xxxxuanran]
- 🔧 尝试修复斗鱼下载失败的问题，同时禁用主线路 [@xxxxuanran]
- 🔧 修正快手日志提示，尝试规避风控 [@xxxxuanran]
- 🔧 修正 Windows 下自动过滤删除文件由于占用权限问题，导致整体卡住的问题 [@haha114514]

---

## v0.4.19

> 更新时间：2023-05-11

- 🔧 修复新版本 `urllib3.connectionpool` 下 `xrange` 报错的问题 [@zclkkk]
- 🔧 修复新版本 `urllib3` 2 下 `method_whitelist` 报错的问题 [@Weidows]

---

## v0.4.18

> 更新时间：2023-04-21

- 🔧 修复录制 B站直播，自动上传标题里面的 title 为下播前的最后一个标题的 bug（正确的应该是开播之后的第一个标题）[@haha114514]
- 🔧 `streamlink` 下载稳定与内存占用优化 [@haha114514]
- 🔧 修复多余弹幕文件自动过滤失效的问题 [@haha114514]
- 🔧 增加 B站 `fmp4` 流的等待时间，因为有些主播开播到推流时间较慢 [@zclkkk]
- 💡 B站直播优选 CDN 支持同时添加多个节点 [@haha114514]
- 💡 新增 B站自定义 `fmp4` 流获取不到时，重新获取一遍 flv 直播流的 API [@haha114514]
- 💡 新增对快手平台的支持 [@xxxxuanran]

---

## v0.4.17

> 更新时间：2023-03-24

- 🔧 修复不填 B站自定义 API 就无法开始录制的问题 [@xxxxuanran]

---

## v0.4.16

> ⚠️⚠️ 有重大问题，请勿使用该版本。

> 更新时间：2023-03-23

- 🔧 修复 B站自定义 API 不生效的问题 [@xxxxuanran]
- 🔧 修复部分 config 示例的错误 [@haha114514]

---

## v0.4.15

> 更新时间：2023-03-21

- 🔧 修复上一版本关于 b站下载部分的优化相关的问题 [@xxxxuanran]
- 🔧 优化 YouTube 下载相关参数 [@haha114514]

---

## v0.4.14

> 更新时间：2023-03-19

- 🔧 回滚 @xxxxuanran 关于 b站下载部分的优化 [@haha114514]

---

## v0.4.13

> ⚠️⚠️ 有重大问题，请勿使用该版本。

> 更新时间：2023-03-19

- 🔧 优化部分下载逻辑，并将封面下载功能移动到 `download.py` 中，方便以后适配更多平台的直播间封面下载 [@xxxxuanran]
- 🔧 修复配置文件错误 [@xxxxuanran]
- 🔧 优化 `streamlink` 下载参数 [@haha114514]
- 💡 新增跳过斗鱼 scdn，并增加了斗鱼与虎牙最新的 CDN 的支持 [@xxxxuanran]
- 💡 新增指定 YouTube 视频下载时间范围区间的功能 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。

---

## v0.4.12

> 更新时间：2023-03-17

- 🔧 修复优选 CDN 与直播流不生效的问题 [@haha114514]
- 🔧 优化 `streamlink` 下载参数 [@haha114514]
- 🔧 完善依赖列表，将最低的 `yt-dlp` 版本要求升级到 2023.3.3，解决 2022 年版本已无法解析 YouTube 视频的问题；并且将 `streamlink` 最低要求版本升级到 5.3.0，提升 HLS 流录制稳定性 [@haha114514]

---

## v0.4.11

> 更新时间：2023-03-07

- 🔧 修复上一版本的封面上传问题 [@haha114514]

---

## v0.4.10

> ⚠️⚠️ 有重大问题，请勿使用该版本。

> 更新时间：2023-03-07

- 🔧 修复上一版本的封面上传问题 [@haha114514]
- 🔧 优化上传过滤文件规则 [@haha114514]
- 💡 修改判断逻辑，支持 `cn-gotcha01` flv 流的自选域名 [@haha114514]
- 💡 增加 YouTube 转载视频自动获取视频封面并用作投稿封面的功能 [@haha114514]

---

## v0.4.9

> ⚠️⚠️ 有重大问题，请勿使用该版本。

> 更新时间：2023-03-06

- 🔧 `biliup-rs` 上传器自动过滤 xml 文件，避免上传 xml 弹幕文件导致整个投稿转码失败的问题 [@haha114514]
- 🔧 修复自动获取封面不生效的问题 [@haha114514]

---

## v0.4.8

> 更新时间：2023-03-04

- 🔧 在最后处理文件的时候，自动删除多余的 xml 弹幕文件，只保留有同样文件名视频的弹幕 xml 文件 [@haha114514]
- 🔧 优化 ffmpeg 录制 HLS 流的参数 [@haha114514]
- 💡 新增 `streamlink+ffmpeg` 混合下载器选项 [@haha114514]
- 💡 新增 B站直播 `hls_fmp4` 流的获取（目前只有 `streamlink+ffmpeg` 混合模式才能稳定下载）[@haha114514]
- ⚠️ 上两条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。

---

## v0.4.7

> 更新时间：2023-02-28

- 🔧 修复 0.4.5 的 BUG 并添加缺失的依赖 [@haha114514]

---

## v0.4.5

> ⚠️⚠️ 此版本存在重大 BUG，导致很多情况下无法录制 B站直播，请勿使用。

> 更新时间：2023-02-28

- 💡 新增斗鱼、虎牙、B站的弹幕录制功能，默认关闭，需要在 config 文件中开启，只支持 FFMPEG（目前）[@KNaiFen]
- 🔧 修复了 BILIBILI 录制中 OV05 节点的 BUG [@haha114514]
- ⚠️ 由于为 Config 新增了弹幕录制的设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。
- 🔧 优化代码 [@ForgQi]

---

## v0.4.4

> ⚠️⚠️ 本次修改了 config 内部分参数的名称，请需要使用的用户参考最新的 config 示例修改。

> 更新时间：2023-02-20

- 💡 统一了 Config 中关键词替换的关键词 [@haha114514]
- ⚠️⚠️ 请注意修改 `file_name` 与 `title` 和 `Description` 中关键词替换的部分。目前全部统一为 `streamer`，`title` 和 `url` 了。
- 💡 新增 `cn-gotcha01` 和 `ov-gotcha05` 自选 ip/节点的设置 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。
- 🔧 修复上一版本由于新增的哔哩哔哩直播自定义下载 CDN 导致报错的问题 [@haha114514]
- 🔧 修复过多请求开播 API 导致 IP 被限制访问的问题 [@ForgQi]

---

## v0.4.3

> 更新时间：2023-02-15

- 💡 为 YouTube 视频下载增加指定音视频编码的设置 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。
- 🔧 修复上一版本由于新增的哔哩哔哩直播自定义下载 CDN 导致报错的问题 [@haha114514]

---

## v0.4.2

> ⚠️⚠️ 此版本存在重大 BUG，导致很多情况下无法录制 B站直播，请勿使用。

> 更新时间：2023-02-15

- 💡 为 YouTube 视频下载增加指定封装格式，最大纵向分辨率，最大单视频大小的设置 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。
- 🔧 修复上一版本由于新增的哔哩哔哩登录 Cookie 导致报错的问题 [@haha114514]
- 🔧 修复 Twitch 的 Clips 无法下载的问题 [@haha114514]
- 🔧 为上一版本的 B站 Fallback 机制启用开关 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。

---

## v0.4.1

> 更新时间：2023-02-13

- 💡 增加 Preprocessor 功能，支持开始录制时执行指定 Shell 指令 [@haha114514]
- 💡 为上传标题与简介增加 `streamers` 变量 [@haha114514]
- ⚠️ 上两条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。
- 🔧 修复访问 acfun 过于频繁导致 ip 被拉黑之后报错卡住的问题 [@haha114514]
- 🔧 修复嵌入示例中延后发布时间的错误 [@stevenlele]
- 🔧 修复 `twitch_cookie` 配置不生效问题 [@v2wy]
- 🔧 尝试为 B站直播录制启用 Fallback 机制，当指定 CDN 反复无法下载之后，自动尝试另外的 CDN [@xxxxuanran]
- 🔧 增加 Cookie 登录 B站功能，可用于下载付费直播与大航海专属直播 [@xxxxuanran]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。

---

## v0.4.0

> 更新时间：2023-02-10

- ⚠️ 修改 cookie 在配置文件中的位置 [@haha114514]
- 🔧 修复斗鱼直播间被关闭一直报错的问题 [@v2wy]
- 🔧 修改 `probe_version` 参数，增加两个常用的网页上传地址 [@FairyWorld]

---

## v0.3.12

> 更新时间：2023-02-05

- 🔧 为 readme 文档添加关于主要支持录制的直播平台的介绍以及删掉关于上传 CDN 描述中已经失效的节点 [@haha114514]
- 🔧 修复 ffmpeg 录制参数缺失 `.part` 后缀，导致录制出来的文件都没有 `.part` 后缀的问题 [@haha114514]
- 🔧 修复了 ffmpeg 录制情况下，按大小分段录制时，分段之后上一段的 `.part` 后缀不会被去掉的问题 [@haha114514]
- 🔧 完善 config 示例，增加 `postprocessor` 可参考用法的描述 [@haha114514]
- ⚠️ 上一条由于为 Config 新增了一些设置，如需使用相关功能请参考最新的 config 示例添加缺失的部分。

---

## v0.3.11

> 更新时间：2023-02-02

- 🔧 修复 `config.yaml` 示例中 `filename_prefix` 配置格式 [@FairyWorld]
- 🔧 添加 `config.toml` 示例中缺失的关于 `downloader` 的设置 [@haha114514]
- 🔧 修改 `postprocessor`，避免出现指令有问题导致反复从头开始执行任务的问题 [@haha114514]
- 🔧 去掉自动替换文件名中空格为 `_` 字符的功能，避免和录播完毕自动改名冲突 [@haha114514]
- 🔧 修复由于上一版的修改导致 `stream-gears` 录制文件名重复出现分段覆盖的问题 [@haha114514]

---

## v0.3.10

> ⚠️⚠️ 此版本存在 `stream-gears` 录制文件名重复导致覆盖上一段分段的问题，请勿使用。

> 更新时间：2023-02-01

- 💡 添加全局与单个主播自定义录播文件命名设置 [@haha114514]
- ⚠️ 新增与主播自定义录播文件命名设置的两个参数，如需使用此功能，请老版本用户参考 config 的示例添加。
- 💡 启用了文件名过滤特殊字符的功能，避免文件名中出现特殊字符，导致 ffmpeg 无法录制的问题 [@haha114514]

---

## v0.3.9

> 更新时间：2023-01-31

- 💡 添加一个虎牙的 CDN 线路 [@ForgQi]
- 🔧 虎牙无法正确获取房间标题的问题 [@luckycat0426]
- 💡 哔哩哔哩直播流协议可选 `stream`（Flv）、`hls` [@xxxxuanran]
- 💡 哔哩哔哩直播优选 CDN [@xxxxuanran]
- 💡 哔哩哔哩直播强制原画（仅限 HLS 流的 `cn-gotcha01` CDN）[@xxxxuanran]
- 💡 自定义哔哩哔哩直播 API [@xxxxuanran]
- 💡 Twitch 自定义用户 Cookie，作用是可以不让广告嵌入到视频流中 [@KNaiFen]

---
