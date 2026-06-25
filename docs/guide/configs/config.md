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
  server     启动Web服务，默认端口19159
  list       列出所有已上传的视频
  comments   批量下载视频评论
  reply      批量下载视频评论回复
  help       Print this message or the help of the given subcommand(s)

Options:
  -p, --proxy <PROXY>              配置代理
  -u, --user-cookie <USER_COOKIE>  登录信息文件 [default: cookies.json]
      --rust-log <RUST_LOG>        [default: tower_http=debug,info]
  -h, --help                       Print help
  -V, --version                    Print version
```

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
| `--auth` | 开启登录密码认证 | 关闭 |
| `--no-http` | 禁用 WebUI（仅后台运行） | 关闭 |
| `--no-access-log` | 禁用 Web 访问日志 | 关闭 |
| `--config` | 指定配置文件路径 | `./config.yaml` |
| `-v, --verbose` | 输出详细日志 | 关闭 |
| `-h, --help` | 打印帮助 | — |

示例：
```bash
# 基础启动
biliup server

# 带密码认证
biliup server --auth

# 指定端口
biliup server --port 8080 --auth

# 纯后台运行（无 WebUI）
biliup server --no-http
```

---

## login — 登录B站

```bash
biliup login [OPTIONS]

Options:
  -p, --proxy <PROXY>         代理地址
  -u, --user-cookie <FILE>    登录信息保存路径 [default: cookies.json]
```

扫码登录后可保存 cookie 信息，用于后续投稿操作。

---

## upload — 上传视频

```bash
biliup upload [OPTIONS] <VIDEO_PATH>

Options:
  -c, --config <FILE>     配置文件路径
  -t, --title <TITLE>     自定义标题
  --tag <TAG>             自定义标签（可多次指定）
  -d, --desc <DESC>       自定义简介
  --line <LINE>           上传线路（bda2 / ws / qn）
  --threads <N>           并发线程数
```

---

## renew — 刷新登录信息

```bash
biliup renew [OPTIONS]
```
手动验证并刷新 B站登录状态。

---

## append — 追加视频到已有稿件

```bash
biliup append [OPTIONS] <VIDEO_PATH>

Options:
  --aid <AID>   目标稿件 ID
```

---

## show — 查看视频详情

```bash
biliup show <VIDEO_PATH>
```
打印本地视频文件的编码、分辨率、码率等元数据。

---

## download — 下载视频/直播

```bash
biliup download <URL>
```
下载指定 URL 的直播流或视频。

---

## list — 列出已上传视频

```bash
biliup list
```
列出当前账号已上传的所有视频稿件。

---

## comments — 下载视频评论

```bash
biliup comments <AID>
```
批量下载指定稿件的评论数据。

---

## reply — 下载评论回复

```bash
biliup reply <AID>
```
批量下载指定稿件评论的回复数据。
