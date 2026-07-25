# CLI 命令行参考

获取命令帮助：`biliup --help`

```
Upload video to bilibili.

Usage: biliup [OPTIONS] <COMMAND>

Commands:
  login      登录B站并保存登录信息
  renew      手动验证并刷新登录信息
  upload     上传视频
  append     对某稿件追加视频
  show       打印视频详情
  dump-flv   输出flv元数据
  download   下载视频
  server     启动web服务，默认端口19159
  list       列出所有已上传的视频
  comments   批量下载视频评论
  reply      回复视频评论
  help       Print this message or the help of the given subcommand(s)

Options:
  -p, --proxy <PROXY>              配置代理
  -u, --user-cookie <USER_COOKIE>  登录信息文件 [default: cookies.json]
      --rust-log <RUST_LOG>        日志级别（RUST_LOG 格式）[default: tower_http=debug,info]
  -h, --help                       Print help
  -V, --version                    Print version
```

::: info
`-p`、`-u`、`--rust-log` 是**全局选项**，必须放在子命令之前使用。例如：`biliup -p http://proxy:8080 login`
:::


---

## server — 启动录制服务

这是最常用的命令，用于启动 WebUI 和录制/上传服务。

```shell
biliup server [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-b, --bind` | 绑定地址 | `0.0.0.0` |
| `-p, --port` | 端口号 | `19159` |
| `--auth` | 开启 WebUI 登录认证（布尔开关，不接收参数） | 关闭 |
| `-c, --config` | 使用 biliup 1.0.7 风格配置文件启动录制 | — |
| `-h, --help` | 打印帮助 | — |

示例：
```bash
# 基础启动
biliup server

# 开启认证（首次启动需在 WebUI 注册账号）
biliup server --auth

# 指定端口
biliup server --port 8080 --auth

# 使用旧版 YAML 配置文件启动
biliup server --config /path/to/config.yaml
```

::: tip
`--auth` 是布尔开关，不接收 `user:pass` 参数。开启后首次访问 WebUI 会进入注册页面，需创建管理账号。详见 [WebUI 认证](/guide/api/rest-api.html#认证说明)。
:::


---

## login — 登录B站

```bash
biliup login
```

执行后通过交互式菜单选择登录方式（扫码 / 短信 / 账号密码），登录成功后自动保存 Cookie。

> `-p` 和 `-u` 是全局选项，需放在子命令之前：`biliup -p http://proxy:8080 login`

---

## renew — 刷新登录信息

```bash
biliup renew
```

手动验证并刷新 B站登录状态，延长 Cookie 有效期。

---

## upload — 上传视频

```bash
biliup upload [OPTIONS] [VIDEO_PATH]...
```

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `<VIDEO_PATH>` | `Vec<PathBuf>` | 视频文件路径（可指定多个） | 必填（指定 `--config` 时可省略）|
| `-c, --config` | `PathBuf` | 配置文件路径（指定后可从配置中读取投稿参数，省略视频路径） | — |
| `--submit` | `app`/`web`/`bcutandroid` | 提交接口 | 自动选择 |
| `-l, --line` | `UploadLine` | 上传线路（见下方可选值） | 自动选择 |
| `--limit` | `usize` | 单视频文件最大并发上传数 | `3` |
| `--copyright` | `u8` | 版权：`1`=自制 `2`=转载 | `1` |
| `--source` | `String` | 转载来源（`copyright=2` 时需填写） | — |
| `--tid` | `u16` | 投稿分区 ID（如 `171`=电子竞技） | `171` |
| `--cover` | `String` | 视频封面 URL | — |
| `--title` | `String` | 视频标题 | — |
| `--desc` | `String` | 视频简介 | — |
| `--dynamic` | `String` | 空间动态内容 | — |
| `--tag` | `String` | 视频标签（逗号分隔） | — |
| `--dtime` | `u32` | 延时发布时间戳（距提交需 >4h） | — |
| `--interactive` | `u8` | 互动视频：`0`=关闭 `1`=开启 | `0` |
| `--missionid` | `u32` | 活动 ID | — |
| `--dolby` | `u8` | 杜比音效：`0`=关闭 `1`=开启 | — |

**`--line` 可选值：**

| 值 | 说明 |
|---|---|
| `bldsa` / `cnbldsa` | BLDSA 线路（国内/海外） |
| `andsa` / `atdsa` | ANDSA 线路（海外） |
| `bda2` / `cnbd` / `anbd` / `atbd` | 百度线路（国内/海外） |
| `tx` / `cntx` / `antx` / `attx` | 腾讯云线路（国内/海外） |
| `bda` / `txa` / `alia` | 百度 / 腾讯 / 阿里云线路 |

示例：
```bash
# 基础上传
biliup upload video.mp4

# 指定标题和标签
biliup upload --title "直播录像" --tag "直播,游戏" video.mp4

# 转载视频上传
biliup upload --copyright 2 --source "https://example.com" video.mp4

# 使用配置文件上传（可省略视频路径）
biliup upload -c config.yaml
```

---

## append — 追加视频到已有稿件

```bash
biliup append [OPTIONS] --vid <VID> <VIDEO_PATH>...
```

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `--vid` | `String` | 目标稿件 AV 或 BV 号（**必填**） | — |
| `<VIDEO_PATH>` | `Vec<PathBuf>` | 视频文件路径（可指定多个） | 必填 |
| `--submit` | `app`/`web`/`bcutandroid` | 提交接口 | 自动选择 |
| `-l, --line` | `UploadLine` | 上传线路（同 upload） | 自动选择 |
| `--limit` | `usize` | 单视频文件最大并发上传数 | `3` |
| Studio 字段 | — | 同 upload 命令的 `--title`/`--tag`/`--desc` 等 | — |

示例：
```bash
# 追加视频到 BV 稿件
biliup append --vid BV1xx411x7xx new_video.mp4

# 追加多个视频
biliup append --vid BV1xx411x7xx part1.mp4 part2.mp4
```

---

## show — 查看视频详情

```bash
biliup show <VID>
```

打印指定稿件的在线详情（标题、播放量、状态等）。`VID` 为 AV 或 BV 号。

示例：
```bash
biliup show BV1xx411x7xx
biliup show av12345678
```

---

## download — 下载视频/直播

```bash
biliup download [OPTIONS] <URL>
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<URL>` | 直播间或视频 URL | 必填 |
| `-o, --output` | 输出文件名模板（支持 `{title}` 变量和 strftime 格式） | `{title}` |
| `--split-size` | 按大小分割视频（支持 K/M/G 后缀，如 `4G`） | — |
| `--split-time` | 按时间分割视频（如 `1h30m`） | — |

示例：
```bash
# 下载直播
biliup download https://live.bilibili.com/123456

# 指定输出文件名
biliup download -o "{title}_%Y%m%d" https://live.bilibili.com/123456

# 按大小分割
biliup download --split-size 4G https://live.bilibili.com/123456
```

---

## list — 列出已上传视频

```bash
biliup list [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--is-pubing` | 只包含进行中的视频 | 关闭 |
| `--pubed` | 只包含已通过的视频 | 关闭 |
| `--not-pubed` | 只包含未通过的视频 | 关闭 |
| `-f, --from-page` | 从第几页开始获取 | `1` |
| `-m, --max-pages` | 最大获取页数 | 全部 |

示例：
```bash
# 列出所有视频
biliup list

# 只看已通过的视频，前 5 页
biliup list --pubed --max-pages 5
```

---

## comments — 下载视频评论

```bash
biliup comments [OPTIONS] <VID>
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<VID>` | 稿件 AV 或 BV 号 | 必填 |
| `--sort` | 排序方式：`0`=按时间 `2`=按热度 | `0` |
| `--pn` | 页码 | `1` |
| `--ps` | 每页条数 | `20` |

示例：
```bash
# 下载视频评论
biliup comments BV1xx411x7xx

# 按热度排序，获取前 50 条
biliup comments --sort 2 --ps 50 BV1xx411x7xx
```

---

## reply — 回复视频评论

```bash
biliup reply [OPTIONS] <VID> <RPID> <MESSAGE>
```

回复指定视频的评论。默认仅打印将要回复的内容，加 `--execute` 才实际发送。

| 参数 | 说明 |
|------|------|
| `<VID>` | 稿件 AV 或 BV 号 |
| `<RPID>` | 评论 ID（rpid） |
| `<MESSAGE>` | 回复内容 |
| `--execute` | 实际发送回复（不加则仅预览） |

示例：
```bash
# 预览回复内容
biliup reply BV1xx411x7xx 123456789 "感谢评论"

# 实际发送回复
biliup reply --execute BV1xx411x7xx 123456789 "感谢评论"
```

---

## dump-flv — 输出 FLV 元数据

```bash
biliup dump-flv <FILE_NAME>
```

输出指定 FLV 文件的元数据信息（用于调试录制问题）。

示例：
```bash
biliup dump-flv recording_20260101.flv
```
