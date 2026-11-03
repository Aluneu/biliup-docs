# 开发者选项

::: warning
以下选项面向进阶用户和开发者，普通用户无需修改。
:::


---

## 钩子系统（Hooks）

biliup 提供四个阶段的钩子，支持自定义脚本和外部通知：

| 钩子阶段 | 配置字段 | 触发时机 | 用途示例 |
|----------|----------|----------|----------|
| **录制前** | `preprocessor` | 检测到开播，准备开始录制 | 发送开播通知 |
| **分段后** | `segment_processor` | 录制文件达到分段条件 | 弹幕压制、格式转换 |
| **下载完成** | `downloaded_processor` | 直播录制全部完成 | 文件预处理、通知 |
| **上传后** | `postprocessor` | 上传完成 | 发送通知、删除本地文件 |

### 钩子步骤类型

每个钩子阶段接受一个步骤数组。**不同阶段能用的步骤不一样**（WebUI 的处理流程编辑器只提供可用项）：

| 格式 | JSON 示例 | 说明 | 可用阶段 |
|---|---|---|---|
| `run` | `{"run": "sh ./process.sh"}` | 执行 Shell 命令（Windows: `cmd /C`，Unix: `sh -c`）；加 `"json": true` 时 stdin 改传 JSON 对象 | 四个阶段都可用 |
| `webhook` | `{"webhook": "https://example.com/hook"}` | 上传结果回调，必须在任何文件后处理之前返回 `success`，详见下方 | 仅 `postprocessor` |
| `remux` | `{"remux": "mp4"}` | 把 `.ts` / `.m2ts` 转封装为 MP4（ffmpeg，不重编码）；其它格式跳过 | 仅 `segment_processor` |
| `render` | `{"render": {"danmaku": {"enabled": true}, "regions": [...]}}` | 内置遮挡 / 弹幕压制（与工作台导出同一个引擎） | 仅 `segment_processor` |
| `mv` | `{"mv": "backup/"}` | 移动文件到指定目录 | 仅 `postprocessor` |
| `rm` | `"rm"` | 删除文件（受[保留策略](/guide/getting-started/配置/global-config.html#存储与清理)约束） | 仅 `postprocessor`（`segment_processor` 里也能执行，但编辑器不提供） |

### 处理流程编辑器

v1.3.0 起 WebUI 提供**图形化的处理流程编辑器**（直播间 → 处理流程）：四个阶段一次编排，步骤可拖动排序，画布上能看到「下载结束」分支；保存时仍写回原有的四个钩子数组，不引入第二套存储。

`render` 步骤与「录后合成」共用同一编码管线，可同时完成遮挡与弹幕压制：

```yaml
segment_processor:
  - render:
      danmaku:
        enabled: true
        font: "Noto Sans CJK SC"
        font_size: 38
      regions:
        - effect_type: mosaic   # mosaic | blur | smooth_blur | solid | image
          x: 0.05
          y: 0.05
          width: 0.25
          height: 0.2
          strength: 16
          intervals: []         # 留空 = 全程生效；否则填 [{from_ms, to_ms}]
```

> 区域坐标与宽高都是 **0–1 的比例**（相对画面），不是像素。一般不需要手写这段 JSON——在遮挡编辑器里画好保存即可。

### 权限：钩子与 ffmpeg 参数只有超级管理员能改

钩子里的 `run` 走 `sh -c`、主播的 `override` 能覆盖任意全局配置、主播的「ffmpeg 参数」（`opt_args`）能让 ffmpeg 往任意路径写文件——合起来等于这台机器上的 shell。因此：

- 只有 **超级管理员**（`streamer.hooks` 权限）能查看和修改这些字段；操作员 / 只读观察者保存主播时，这些字段保持原值，不会被清空也不会被改；
- v1.3.4 起 `opt_args` 与钩子同级受管（此前它不生效，也就没有人管）；
- Fleet 控制面下发的房间里若带钩子或 ffmpeg 参数，只会派给**加入时带 `--allow-hooks`**（或启用「本机」时勾选「允许钩子」）的节点。

### 处理过的原片与中间文件

`remux`、`render` 这类会「产出新文件」的步骤会把成品与它的来源（原片、中间文件）登记下来。之后：

- `postprocessor` 的 `rm` 或[延期清理](/guide/getting-started/配置/global-config.html#存储与清理)删除成品时，**连带删掉没有人再引用的来源文件**，不会把原片长期堆在盘里；
- 同一份来源被多个成品引用时不删，等最后一个引用释放；
- 记录存在数据库里，**服务重启后依然有效**；`mv` 之后来源关系跟着搬到新路径。

> 遮挡功能出于安全考虑，待遮挡的原片本来就不进入投稿或切片导出；这条清理规则保证它们在成品被删除后也不会残留。


### 各阶段输入数据

| 阶段 | stdin | 数据格式 |
|---|---|---|
| `preprocessor` | 空 | 不传数据，仅触发（只支持 `run`） |
| `segment_processor` | 文件路径 | 本段视频路径；有弹幕时**第二行**是弹幕 XML 路径 |
| `downloaded_processor` | 空 | 不传数据，仅触发（只支持 `run`） |
| `postprocessor` | 文件路径 | 已上传视频的路径；多个路径按换行分隔 |

> 脚本从标准输入按行读取路径即可，例如 `while IFS= read -r line; do ...; done`。

写了 `"json": true` 的 `run` 步骤收到的则是一个 JSON 对象，字段与 Python 版一致：

```json
{
  "name": "主播备注",
  "url": "https://live.bilibili.com/1234",
  "room_title": "直播标题",
  "start_time": "2026-10-22 20:00:00",
  "end_time": "2026-10-22 23:10:00",
  "file_list": ["/data/record/xxx.flv"]
}
```

`downloaded_processor` 的 `run` 还可以在 stdout 上打印一行 `BILIUP_OUTPUT=<JSON 数组>`，显式告诉 biliup 处理后要接手的具体文件；不打印则沿用录制产出的路径。一行脚本只能输出一条，内容必须是 UTF-8 JSON，超过 1 MiB 会报错而不是被截断。

### 钩子配置方式

在 WebUI「空间配置」→「开发者选项」中配置，或在主播的独立配置中指定。

配置示例（YAML 格式）：

```yaml
preprocessor:
  - run: "echo $0"
segment_processor:
  - remux: "mp4"
downloaded_processor:
  - run: "sh ./notify.sh"
postprocessor:
  - rm
  - mv: "backup/"
  - run: "sh ./cleanup.sh"
```

### 上传结果回调（Webhook）

v1.3.2 起 Rust 版本重新内置了上传结果回调，写成一个钩子步骤即可，不需要自己拼 `curl`：

```yaml
postprocessor:
  - webhook: "https://example.com/biliup/hook"
  - rm
```

触发时机与语义：

- **上传结束后、任何文件后处理之前**执行一次。即使它排在 `rm` / `mv` 后面，也会先回调，避免通知还没发出去文件已经被删。
- 请求体是 JSON：`{"stream_info": {...}, "caught_error": ""}`，`stream_info` 里除了主播与直播信息，还带投稿模板的字段（`tid`、`title`、`tags`…）以及格式化后的 `format_title` / `format_desc`；`name` 是主播的**备注名**（与 Python 版一致）。
- 必须返回 **2xx + 纯文本 `success`**（响应体不超过 128 字节）才继续；返回别的状态码、别的正文或超时（连接 10 秒 / 整体 30 秒）都算失败，**录像保留在本地**并中止后续后处理，日志会写明失败原因。
- 上传失败时也会回调一次，此时 `caught_error` 带错误原因，方便外部系统记录；回调本身失败不会覆盖原始的上传错误。
- 只接受 `http` / `https` 地址，**不跟随重定向**；不支持在其它阶段使用（`preprocessor` / `segment_processor` / `downloaded_processor` 里写 webhook 会报错）。
- 一轮上传只回调一次，多段录像不会重复通知。

> 未开启 `--auth` 时 Webhook 没有额外保护——回调地址由你提供，但请不要把带凭据的地址写进公开模板。WebUI 的「处理流程」编辑器里可以直接添加 webhook 步骤并校验地址格式。

---

## 分段处理器（segment_processor）

录制文件达到分段条件后，可对文件进行后处理。

### 内置处理器

| 处理器 | 说明 |
|--------|------|
| `remux:mp4` | 将 `.ts` / `.m2ts` 重新封装为 MP4（不重编码，速度快）；其它格式会跳过 |
| `render` | 内置遮挡与弹幕压制（与「录后合成」同一引擎），见上节 |

#### remux:mp4 技术细节

`remux:mp4` 将 `.ts`/`.m2ts` 文件转封装为 `.mp4`（不重编码），使用以下 ffmpeg 命令：

```bash
ffmpeg -hide_banner -loglevel warning -y \
  -fflags +genpts+igndts \
  -i input.ts \
  -c copy \
  -bsf:a aac_adtstoasc \
  -movflags +faststart \
  -avoid_negative_ts make_zero \
  output.mp4
```

> 这解决了 B站对 `.ts` 直传的时间戳跳变问题。

### 自定义处理器

可以编写自定义 Shell / Python 脚本做任意处理（如调用外部工具转码、上传到网盘）。

弹幕压制**不再需要**外部 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory)：XML → ASS 转换已内置为原生 Rust 实现，用 `render` 步骤或「录后合成」即可，详见[录后合成](/guide/tutorials/post-recording-render.html)。

---

## 高级配置

### 配置文件位置

- WebUI 默认使用 `data/data.sqlite3` 存储配置
- 支持通过 `--config` 参数使用 biliup 1.0.7 风格的 YAML 配置文件启动录制
- 新版启动时自动将旧版 YAML 配置转换到数据库

::: info
`--config` 加载的是**旧版 YAML 配置**（v1.0.7 风格），而非当前版本的数据库配置。主要用于兼容旧版部署。
:::


### 日志级别

当前 Rust 版本通过全局配置的 `loggers_level` 设置日志过滤，**取值为 RUST_LOG（`EnvFilter`）风格**，在 WebUI 保存后立即生效：

| 配置项 | 说明 | 示例值 |
|---|---|---|
| `loggers_level` | 服务运行期日志过滤（不设置时读环境变量 `RUST_LOG`，都没有则 `tower_http=debug,info`） | `debug`、`tower_http=debug,info` |

> Python 时代的 `LOGGING` 配置块（`LOGGING.root.level` 等）在当前版本**不再被读取**，写进配置文件会被忽略。

命令行启动的日志过滤可用全局选项 `--rust-log`（与 `loggers_level` 同一套格式）：

```bash
# 详细日志（用于排查问题）
biliup --rust-log debug server

# 仅特定模块的详细日志
biliup --rust-log "tower_http=debug,biliup=trace,info" server
```

### 数据库结构

biliup 使用 SQLite 存储配置和运行数据，主要表结构：

| 表名 | 说明 |
|---|---|
| `livestreamers` | 直播主播配置 |
| `uploadstreamers` | 上传模板 |
| `streamerinfo` | 录制记录 |
| `filelist` | 录制文件列表 |
| `configuration` | 全局配置和 Cookie 存储 |
