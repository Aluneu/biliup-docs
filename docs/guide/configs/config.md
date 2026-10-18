# CLI 命令行参考

获取命令帮助：`biliup --help`

```
Upload video to bilibili.

Usage: biliup [OPTIONS] <COMMAND>

Commands:
  login      登录B站并保存登录信息
  renew      手动验证并刷新登录信息
  upload     上传视频
  append     是否要对某稿件追加视频
  show       打印视频详情
  comments   查看视频评论
  reply      回复视频评论，默认只打印将要回复的内容
  dump-flv   输出flv元数据
  download   下载视频
  server     启动web服务，默认端口19159
  season     管理自己的合集：列合集、查小节、加入 / 移出稿件、排序
  user       管理 Web 界面的登录用户
  node       把这台机器加入 Fleet 控制面或退出
  list       列出所有已上传的视频
  help       Print this message or the help of the given subcommand(s)

Options:
  -p, --proxy <PROXY>              配置代理
  -u, --user-cookie <USER_COOKIE>  登录信息文件 [default: cookies.json]
      --rust-log <RUST_LOG>        日志过滤规则，如 debug；不指定时读取环境变量 RUST_LOG，都没有则为 tower_http=debug,info
  -h, --help                       Print help
  -V, --version                    Print version
```

::: info
`-p`、`-u`、`--rust-log` 是**全局选项**，必须放在子命令之前使用。例如：`biliup -p http://proxy:8080 login`
:::


---

## server - 启动录制服务

这是最常用的命令，用于启动 WebUI 和录制/上传服务。

```shell
biliup server [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-b, --bind` | 绑定地址。`127.0.0.1` 仅本机可访问，`0.0.0.0` 允许局域网 / 公网访问 | `127.0.0.1` |
| `-p, --port` | 端口号 | `19159` |
| `--auth` | 开启 WebUI 登录认证（布尔开关，不接收参数） | 关闭 |
| `--secure-session-cookie` | 为会话 Cookie 附加 `Secure` 属性。**仅当通过 HTTPS 反向代理访问时开启**，直接 HTTP 远程访问时开启会导致浏览器丢弃登录态 | 关闭 |
| `-c, --config` | 使用 biliup 1.0.7 风格配置文件启动录制 | — |
| `--controller` | 以 Fleet 控制面运行：接受其他 biliup 节点加入并显示它们的状态（数据在 `data/fleet.sqlite3`） | 关闭 |
| `--relay-listen` | 控制面内嵌 relay 的 TCP 监听地址，节点必须能连到它；填 `off` 表示不起内嵌 relay（此时必须用 `--relay-url` 指定外部 relay）。**仅在 `--controller` 时生效** | `0.0.0.0:19160` |
| `--relay-url` | 写进加入票据的 relay 地址，可重复指定；不填时自动列出本机网卡地址。用于域名、端口转发、反向代理或外部 relay。**仅在 `--controller` 时生效** | 自动检测 |
| `-h, --help` | 打印帮助 | — |

示例：
```bash
# 基础启动（仅本机可访问 http://127.0.0.1:19159）
biliup server

# 开启认证（首次启动需在 WebUI 注册账号）
biliup server --auth

# 指定端口
biliup server --port 8080 --auth

# 允许其他设备访问（必须同时加 --auth，否则拒绝启动）
biliup server --bind 0.0.0.0 --auth

# HTTPS 反向代理后
biliup server --bind 0.0.0.0 --auth --secure-session-cookie

# 使用旧版 YAML 配置文件启动
biliup server --config /path/to/config.yaml
```

::: warning 默认只监听本机
自 v1.2.3（[#1660](https://github.com/biliup/biliup/pull/1660)）起，`--bind` 的默认值由 `0.0.0.0` 改为 `127.0.0.1`。直接 `biliup server` 启动后，**局域网或公网设备无法访问**，这是有意为之的安全默认。

如果需要从其他设备访问，必须显式指定 `--bind 0.0.0.0` 并同时开启 `--auth`：

```bash
biliup server --bind 0.0.0.0 --auth
```

若绑定了非本机地址却**没有** `--auth`，服务会直接拒绝启动并提示 `refusing to expose the unauthenticated Web API`。

> 🐳 **Docker 用户注意**：镜像默认 `CMD` 已带 `--bind 0.0.0.0 --auth`，不写参数时正常。但一旦你显式写了 `command:` 或镜像名后的参数（覆盖默认 `CMD`），**必须自己补上 `--bind 0.0.0.0`**，否则容器内只监听回环地址，端口映射转不进去，WebUI 打不开。详见 [Docker 部署](/guide/getting-started/安装部署/docker.html)。
:::

::: tip
`--auth` 是布尔开关，不接收 `user:pass` 参数。开启后首次访问 WebUI 会进入注册页面，需创建管理账号（用户名固定为 `biliup`）。详见 [WebUI 认证](/guide/api/rest-api.html#认证说明)。
:::


---

## login - 登录B站

```bash
biliup login
```

执行后通过交互式菜单选择登录方式（扫码 / 短信 / 账号密码），登录成功后自动保存 Cookie。

> `-p` 和 `-u` 是全局选项，需放在子命令之前：`biliup -p http://proxy:8080 login`

---

## renew - 刷新登录信息

```bash
biliup renew
```

手动验证并刷新 B站登录状态，延长 Cookie 有效期。

---

## upload - 上传视频

```bash
biliup upload [OPTIONS] [VIDEO_PATH]...
```

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `<VIDEO_PATH>` | `Vec<PathBuf>` | 视频文件路径（可指定多个） | 必填（指定 `--config` 时可省略）|
| `-c, --config` | `PathBuf` | 配置文件路径（指定后可从配置中读取投稿参数，省略视频路径） | — |
| `--submit` | `app`/`web`/`bcutandroid` | 提交接口 | `app` |
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
| `--tid-v2` | `u32` | 新版分区 ID（不设置时不提交该字段） | — |
| `--interactive` | `u8` | 互动视频：`0`=关闭 `1`=开启 | `0` |
| `--mission-id` | `u32` | 活动 ID | — |
| `--dolby` | `u8` | 杜比音效：`0`=关闭 `1`=开启 | `0` |
| `--hires` | `u8` | Hi-Res 无损音质：`0`=关闭 `1`=开启 | `0` |
| `--no-reprint` | `u8` | 转载权限：`0`=允许转载 `1`=禁止转载 | `0` |
| `--charging-pay` | `u8` | 开启充电：`0`=关闭 `1`=开启 | `0` |
| `--is-only-self` | `u8` | 仅自己可见 | — |
| `--up-selection-reply` | 开关 | 开启精选评论（仅 `--submit app` 可用） | 关闭 |
| `--up-close-reply` | 开关 | 关闭评论（仅 `--submit app` 可用） | 关闭 |
| `--up-close-danmu` | 开关 | 关闭弹幕（仅 `--submit app` 可用） | 关闭 |
| `--extra-fields` | JSON 字符串 | 自定义提交参数，按 JSON 追加到提交请求 | — |

**`--line` 可选值：**

| 值 | 说明 |
|---|---|
| `bldsa` / `cnbldsa` | BLDSA 线路（常规 / 国内） |
| `andsa` / `atdsa` | ANDSA 线路（海外） |
| `bda2` / `cnbd` / `anbd` / `atbd` | 百度线路（常规 / 国内 / 海外） |
| `tx` / `cntx` / `antx` / `attx` | 腾讯云线路（常规 / 国内 / 海外） |
| `txa` | 腾讯云备用线路 |
| `alia` | 阿里云线路 |
| `estx` / `akbd` | 其他线路 |

> `--line` 只接受上表中的具体线路名，不接受 `AUTO`；`AUTO`（自动选择）是全局配置 `lines` 的取值，详见[全局设置](/guide/getting-started/配置/global-config.html)。若某条线路上传失败，换一条重试即可。

::: info CLI 与服务端的提交接口默认值不同
CLI `upload` / `append` 不带 `--submit` 时默认用 **app** 接口投稿；服务端录制完成后的自动投稿则由全局配置 `submit_api` 决定，2026-10 起默认 **web**（[#1801](https://github.com/biliup/biliup/pull/1801)）。两者互不影响。
:::

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

## append - 追加视频到已有稿件

```bash
biliup append [OPTIONS] --vid <VID> <VIDEO_PATH>...
```

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `--vid` / `-v` | `Vid` | 目标稿件 AV 或 BV 号（**必填**） | — |
| `<VIDEO_PATH>` | `Vec<PathBuf>` | 视频文件路径（可指定多个） | 必填 |
| `--submit` | `app`/`web`/`bcutandroid` | 提交接口 | `app` |
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

## show - 查看视频详情

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

## download - 下载视频/直播

```bash
biliup download [OPTIONS] <URL>
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<URL>` | 直播间或视频 URL | 必填 |
| `-o, --output` | 输出文件名模板（支持 `{title}` 变量和 strftime 格式） | `{title}` |
| `--split-size` | 按大小分割视频（支持 K/M/G 后缀，**按 1000 进制**，如 `4G` = 4,000,000,000 字节）。必须是正的有限值；`0`、负数、`NaN` 与溢出的值会直接报错 | — |
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

## list - 列出已上传视频

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

## comments - 查看视频评论

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

## reply - 回复视频评论

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

## dump-flv - 输出 FLV 元数据

```bash
biliup dump-flv <FILE_NAME>
```

输出指定 FLV 文件的元数据信息（用于调试录制问题）。

示例：
```bash
biliup dump-flv recording_20260101.flv
```

---

## season - 管理合集

管理自己 B 站账号下的合集（Season）：列出合集、查看小节、加入 / 移出稿件、调整顺序。

```bash
biliup season [--json] <SUBCOMMAND>
```

| 子命令 | 说明 |
|---|---|
| `list` | 列出自己的合集及其小节，合集顺序与 B 站创作中心里的自定义顺序一致 |
| `sections <SEASON_ID>` | 查看合集的各个小节和其中的稿件（输出里的 episode id 用于 `remove` / `sort`） |
| `add --vid <VID>... <SECTION_ID>` | 把稿件加入小节，cid 与标题自动获取；`--vid` 可重复指定以一次加入多个 |
| `remove <EPISODE_ID>` | 从合集移出一个稿件（注意是 **episode id，不是 aid**，见 `sections` 的输出） |
| `sort <SECTION_ID> [EPISODE_IDS...]` | 重排小节里的稿件：列出的 episode id 按给定顺序排在最前，其余保持原有顺序 |

全局标志 `--json` 以 JSON 输出，便于脚本处理。

`sort` 的附加参数：

| 参数 | 说明 |
|---|---|
| `--reverse` | 把现有顺序整体倒过来（与列出 episode id 的用法互斥） |
| `--season-id <ID>` | 合集 ID；仅在 B 站返回的小节信息里没有该字段时才需要指定 |

示例：
```bash
# 列出自己的合集
biliup season list

# 查看 12345 号合集的各个小节
biliup season sections 12345

# 把两个稿件加入 678 号小节
biliup season add --vid BV1xx411x7xx --vid av12345678 678

# 从合集移出一个稿件
biliup season remove 999

# 调整 678 号小节里的顺序
biliup season sort 678 999 1000
```

---

## user - 管理 Web 登录用户

管理登录 biliup 管理界面的用户。**必须在 biliup 服务的工作目录下执行**（命令直接读写 `data/data.sqlite3`）。

```bash
biliup user <SUBCOMMAND>
```

| 子命令 | 说明 |
|---|---|
| `list` | 列出所有 Web 用户 |
| `reset-password <USERNAME>` | 重置某个用户的密码并让其所有会话失效；新密码从终端提示输入，或从标准输入读一行 |

::: warning 这是 WebUI 账号，不是 B 站投稿账号
`user` 管理的是登录 biliup 管理界面用的账号（v1.2.8 起支持多用户与分级权限）。B 站投稿账号通过扫码或 Cookie 添加，与这套账号体系无关，别弄混。
:::

示例：
```bash
cd /opt/data                    # 切到 biliup 服务的工作目录
biliup user list
biliup user reset-password operator
```

---

## node - Fleet 节点管理

把本机加入 Fleet 控制面或退出。**必须在 biliup 服务的工作目录下执行**（命令读写 `data/node.json`）。

| 子命令 | 说明 |
|---|---|
| `join <TICKET> [--allow-hooks]` | 用控制面「添加节点」给出的票据加入；成功后需要重启 `biliup server` 才生效 |
| `leave` | 通知控制面移除本节点，并删除本地凭据 |
| `status` | 查看本机的节点凭据（不连控制面） |

::: danger --allow-hooks 是安全敏感开关
`join --allow-hooks` 允许控制面下发的房间使用钩子（各 `*processor`），**等于允许控制面在这台机器上执行命令**。只在你完全信任该控制面时才开启。
:::

示例：
```bash
biliup node join bfleet_xxxxxxxx
biliup node status
biliup node leave
```
