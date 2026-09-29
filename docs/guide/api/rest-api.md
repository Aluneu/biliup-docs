---
description: biliup REST API 与日志 WebSocket：路由、认证、手动上传示例（含必填 id/template_name）与日志频道（upload.log），基于 v1.2.11 核对。
---

# REST API 文档

biliup 启动 Web 服务后会在 `19159` 端口暴露一组 REST 风格的 HTTP API，既给 WebUI 前端用，也支持外部程序直接拿 HTTP 调。

> 接口路径与字段以 [biliup 源码](https://github.com/biliup/biliup/tree/master/crates/biliup-cli/src/server/api) 为准。

## 基础信息

| 项目 | 说明 |
|---|---|
| 默认端口 | `19159` |
| 默认基地址 | `http://localhost:19159` |
| 响应格式 | JSON |
| 请求体格式 | JSON（`Content-Type: application/json`）|
| 认证方式 | Session/Cookie 认证（`--auth` 启动参数开启）|

### 认证说明

启动时加 `--auth` 开启认证：

```bash
biliup server --auth
```

`--auth` 是布尔开关，不接 `user:pass`。流程：

1. 首次启动没用户时，WebUI 出注册页，用 `POST /v1/users/register` 建管理员；
2. 之后用 `POST /v1/users/login` 登录，基于 Session（Cookie），登录后浏览器自动带 Session ID；
3. 退出调 `GET /v1/logout` 销毁会话。

> ⚠️ WebUI 管理员账号的用户名**固定为 `biliup`**，注册 / 登录时该用户名不可修改，你只需设置密码。它与用于投稿的 B站账号（扫码 / Cookie 添加，对应 `/v1/users/biliup` 之外的 B站账号体系）是两套不同身份，请勿混淆。

> 没开 `--auth` 时接口没有任何保护，生产环境别直接把端口暴露出去。

## 接口总览

### 主播管理

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/streamers` | 获取主播列表 |
| POST | `/v1/streamers` | 添加主播 |
| PUT | `/v1/streamers` | 更新主播 |
| DELETE | `/v1/streamers/{id}` | 删除主播 |
| PUT | `/v1/streamers/{id}/pause` | 暂停/恢复主播录制 |

### 直播预览与实时数据

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/streamers/{id}/cover` | 正在录制直播间的封面。服务端带 `Referer` 转发，避开图片 CDN 防盗链 |
| GET | `/v1/streamers/{id}/avatar` | 主播头像（同上处理） |
| GET | `/v1/streamers/{id}/live` | 直播预览流：复用正在录制的那一路（chunked FLV / MPEG-TS） |
| DELETE / POST | `/v1/streamers/{id}/live` | 释放预览。POST 供 `navigator.sendBeacon` 在播放器销毁时调用 |
| GET | `/v1/streamers/{id}/live-url` | 浏览器直连模式：当前录制中那条流的 CDN 直链 |
| GET | `/v1/streamers/{id}/danmaku` | 预览播放器的实时弹幕（SSE） |
| GET | `/v1/danmaku` | 多路复用的弹幕（SSE），监视器一次订阅多个房间 |
| GET | `/v1/live-rates` | 录制中各房间的写盘速率（HTTP 版，供回退 / curl 使用） |
| GET | `/v1/ws/live-rates` | 同上，WebSocket 每秒推一帧，用于画实时码率曲线 |

> 上述预览相关端点与普通接口一样**在登录校验之内**。`/v1/ws/live-rates` 是每秒推送的高频端点，不要为了它去调快 `/v1/streamers` 的轮询。

### 录制会话 / 切片工作台

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/sessions` | 列出录制会话（场次） |
| GET | `/v1/sessions/{id}` | 获取单个会话 |
| PATCH | `/v1/sessions/{id}` | 更新会话，用于「保留这场」（改 `retain_until`） |
| GET | `/v1/sessions/{id}/keyframes` | 可落刀位置（关键帧） |
| GET | `/v1/sessions/{id}/media` | DVR 回看流，拖动进度 |
| GET | `/v1/sessions/{id}/thumb` | 会话缩略图 |
| GET | `/v1/sessions/{id}/danmaku-density` | 弹幕密度曲线（10 秒一桶，含基线与高峰） |

### 标记与候选

| 方法 | 路径 | 说明 |
|---|---|---|
| GET / POST | `/v1/sessions/{id}/markers` | 列出 / 新建标记（看直播时打点） |
| PATCH / DELETE | `/v1/sessions/{id}/markers/{mid}` | 更新 / 删除标记 |
| GET | `/v1/sessions/{id}/suggestions` | 自动切片候选列表 |
| POST | `/v1/sessions/{id}/suggestions/{sid}/accept` | 接受候选（生成切片草稿） |
| POST | `/v1/sessions/{id}/suggestions/{sid}/dismiss` | 丢弃候选 |

### 切片与导出

| 方法 | 路径 | 说明 |
|---|---|---|
| GET / POST | `/v1/sessions/{id}/clips` | 列出 / 新建切片 |
| PATCH / DELETE | `/v1/sessions/{id}/clips/{cid}` | 更新 / 删除切片 |
| GET | `/v1/clips/{cid}` | 获取切片详情 |
| GET / PUT / DELETE | `/v1/clips/{cid}/cover` | 读取 / 上传 / 删除切片封面（JPEG，有大小上限） |
| POST | `/v1/clips/{cid}/export` | 导出切片 |
| GET | `/v1/clips/{cid}/download` | 下载切片文件 |
| POST | `/v1/clips/{cid}/publish` | 发布：导出 → 上传 → 投稿。一律按转载提交，来源默认直播间地址 |

### 发布队列

| 方法 | 路径 | 说明 |
|---|---|---|
| GET / POST | `/v1/publish-jobs` | 列出发布任务 / 批量发布 |
| POST | `/v1/publish-jobs/preview` | 发布预览 |
| POST | `/v1/publish-jobs/resume` | 恢复发布队列 |
| POST | `/v1/publish-jobs/{jid}/retry` | 重试某条发布任务 |
| DELETE | `/v1/publish-jobs/{jid}` | 移除某条发布任务 |

### 自动切片（实验）

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/v1/auto-clip/test` | 模型接口连通性测试 |
| GET | `/v1/auto-clip/status` | 自动切片状态 |
| GET | `/v1/auto-clip/jobs` | 多场各自的最近任务（剪辑台一页一次请求） |
| GET / POST / DELETE | `/v1/sessions/{id}/auto-clip` | GET 看任务与用量预估；POST 先预估、确认后入队；DELETE 取消 |

### 全局配置

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/configuration` | 获取全局配置 |
| PUT | `/v1/configuration` | 更新全局配置 |

### 主播信息

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/streamer-info` | 获取主播信息（录制状态等）|
| GET | `/v1/streamer-info/files/{id}` | 获取主播的文件列表 |

### 上传模板管理

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/upload/streamers` | 获取上传模板列表 |
| POST | `/v1/upload/streamers` | 添加上传模板 |
| GET | `/v1/upload/streamers/{id}` | 获取单个上传模板 |
| DELETE | `/v1/upload/streamers/{id}` | 删除上传模板 |

### 系统与工具

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/system-stats` | 控制台首页系统状态（CPU / 内存 / 录制目录磁盘 / 网速）。带 `?since=` 时只取增量 |
| GET | `/v1/tools` | FFmpeg 是否可用、版本与许可 |

### 用户与认证

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/users` | 获取用户列表 |
| POST | `/v1/users` | 添加用户 |
| GET | `/v1/users/{id}` | 获取指定用户信息 |
| DELETE | `/v1/users/{id}` | 删除用户 |
| GET | `/v1/users/{id}/archives` | 获取指定用户的稿件列表 |
| POST | `/v1/users/login` | WebUI 用户登录 |
| POST | `/v1/users/register` | WebUI 用户注册 |
| GET | `/v1/users/biliup` | 检查默认用户是否已存在 |
| GET | `/v1/logout` | 退出登录 |

### B站扫码登录

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/get_qrcode` | 获取 B 站扫码登录二维码 |
| POST | `/v1/login_by_qrcode` | 二维码扫码登录 |

### 视频与状态

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/videos` | 获取视频文件列表 |
| GET | `/v1/status` | 获取系统运行状态 |
| POST | `/v1/uploads` | 手动触发上传任务 |
| GET | `/v1/ws/logs` | WebSocket 实时日志推送 |

### B 站 API 代理

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/bili/archive/pre` | B 站投稿预处理（代理）|

> 当前版本仅注册上面这一条 `/bili/*` 路由。早期文档中出现的 `/bili/space/myinfo`、`/bili/proxy` 在源码中并不存在，调用会返回 404。

### 静态资源

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/static/{path}` | WebUI 前端静态文件服务 |

## WebSocket 日志

`GET /v1/ws/logs` 建长连接后按频道推日志：

| 频道 | 说明 |
|---|---|
| `ds_update.log` | 直播检测 / 开播更新 |
| `download.log` | 下载 / 录制 |
| `upload.log` | 上传 / 后处理 |

::: tip `/v1/ws/logs` 的鉴权边界
该端点与普通 REST 路由一起受登录守卫保护：开启 `--auth` 后，未携带有效会话的连接会被拒绝；未开启 `--auth` 时则完全开放（服务端源码中有对应的行为测试）。

日志内容包含文件名、路径等敏感信息，公网暴露仍建议走反向代理并终结 TLS。
:::

```javascript
const ws = new WebSocket('ws://localhost:19159/v1/ws/logs');
ws.onmessage = (event) => console.log(event.data);
```

## 扫码登录

配合 `--auth` 用，三步：

1. `GET /v1/get_qrcode` 拿 `qrcode_key` 和二维码 `url`，生成二维码给 B 站 App 扫；
2. 扫完轮询 `POST /v1/login_by_qrcode`（带 `qrcode_key`）确认状态；
3. 成功后 biliup 存下这个 B 站账号，之后在「用户与认证」那组接口里管。

## 使用示例

几个能直接抄的调用：

### 拉主播列表

```bash
curl http://localhost:19159/v1/streamers
```

### 加主播（最小请求体）

```bash
curl -X POST http://localhost:19159/v1/streamers \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://live.bilibili.com/12345678",
    "remark": "某直播间"
  }'
```

### 暂停录制

```bash
curl -X PUT http://localhost:19159/v1/streamers/1/pause
```

### 删主播

```bash
curl -X DELETE http://localhost:19159/v1/streamers/1
```

### 手动上传

> `POST /v1/uploads` 的 `params` 在服务端会被反序列化为上传模板模型，**必须包含 `id` 与 `template_name`**，否则请求在进入上传逻辑前就会失败。

```bash
curl -X POST http://localhost:19159/v1/uploads \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["/opt/录播/video.flv"],
    "params": {
      "id": 1,
      "template_name": "默认投稿",
      "title": "手动上传",
      "tid": 171,
      "tags": ["直播录制"],
      "copyright": 1
    }
  }'
```

> 示例中的 `id` 与 `template_name` 需替换为你实际已创建的投稿模板的值（可通过 `GET /v1/upload/streamers` 获取）。如果开启了 `--auth`，上述 `curl` 还需携带会话 Cookie（先 `POST /v1/users/login` 登录并保存 Cookie 后再请求）。

### 监听日志（Python）

```python
import websockets
import asyncio

async def listen_logs():
    async with websockets.connect("ws://localhost:19159/v1/ws/logs") as ws:
        async for message in ws:
            print(message)

asyncio.run(listen_logs())
```
