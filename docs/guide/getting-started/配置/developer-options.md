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

每个钩子阶段接受一个步骤数组，每个步骤支持以下格式：

| 格式 | JSON 示例 | 说明 |
|---|---|---|
| `run` | `{"run": "sh ./process.sh"}` | 执行 Shell 命令（Windows: `cmd /C`，Unix: `sh -c`） |
| `mv` | `{"mv": "backup/"}` | 移动文件到指定目录 |
| `remux` | `{"remux": "mp4"}` | 转封装为 MP4（使用 ffmpeg，不重编码） |
| `render` | `{"render": {"danmaku": {"enabled": true}, "regions": [...]}}` | 内置遮挡 / 弹幕压制（与工作台导出同一个引擎） |
| `rm` | `"rm"` | 删除文件 |

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

### 各阶段输入数据

| 阶段 | 输入方式 | 数据格式 |
|---|---|---|
| `preprocessor` | JSON via stdin | `{"name":"主播名","url":"直播间URL","start_time":时间戳}` |
| `segment_processor` | 文件路径 via stdin | 视频分段的文件路径 |
| `downloaded_processor` | JSON via stdin | `{"name":"主播名","url":"URL","room_title":"标题","start_time":时间戳,"end_time":时间戳,"file_list":[文件列表]}` |
| `postprocessor` | 文件路径 via stdin | 已上传视频的文件路径 |

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

### 外部通知（Webhook）

当前 Rust 版本**没有内置的 Webhook 功能**（Python 时代的 `Webhook` / `task_queue` 配置未迁移）。要做上传完成通知，在 `postprocessor`（或 `downloaded_processor`）里用 `run` + `curl` 自行实现，钩子数据按上表从 stdin 读入。示例：

```yaml
postprocessor:
  - run: "curl -s -X POST -H 'Content-Type: application/json' -d '{\"file\":\"'$(cat)\"}' https://example.com/notify"
```

---

## 分段处理器（segment_processor）

录制文件达到分段条件后，可对文件进行后处理。

### 内置处理器

| 处理器 | 说明 |
|--------|------|
| `remux:mp4` | 将 FLV/TS 重新封装为 MP4（无需重新编码，速度快） |

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
