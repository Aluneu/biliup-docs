# REST API 文档

biliup 启动 Web 服务后，会在指定端口暴露一组 REST 风格的 HTTP API，供 WebUI 前端调用，同时也支持外部程序通过 HTTP 请求进行集成。

> 本文档基于 biliup v1.2.1 版本后端路由，路径均以实际源码为准。

---

## 基础信息

| 项目 | 说明 |
|---|---|
| 默认端口 | `19159` |
| 默认基地址 | `http://localhost:19159` |
| 响应格式 | JSON |
| 请求体格式 | JSON（`Content-Type: application/json`）|
| 认证方式 | Session/Cookie 认证（`--auth` 启动参数开启） |

### 认证说明

启动时指定 `--auth` 参数开启认证模式：

```bash
biliup server --auth
```

`--auth` 是布尔开关，不接收 `user:pass` 参数。认证流程如下：

1. **首次启动**：如果没有用户存在，WebUI 会显示注册页面，通过 `POST /v1/users/register` 创建管理账号
2. **后续访问**：通过 `POST /v1/users/login` 登录，认证基于 Session（Cookie），登录后浏览器自动携带 Session ID
3. **退出登录**：调用 `GET /v1/logout` 销毁当前会话

> [!WARNING]
> 未设置 `--auth` 时，API 无认证保护，**请勿在生产环境中不设认证直接暴露端口**。

---

## 接口总览

### 主播管理

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/streamers` | 获取主播列表 |
| POST | `/v1/streamers` | 添加主播 |
| PUT | `/v1/streamers` | 更新主播 |
| DELETE | `/v1/streamers/{id}` | 删除主播 |
| PUT | `/v1/streamers/{id}/pause` | 暂停/恢复主播录制 |

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
| PUT | `/v1/upload/streamers` | 更新上传模板 |
| GET | `/v1/upload/streamers/{id}` | 获取单个上传模板 |
| DELETE | `/v1/upload/streamers/{id}` | 删除上传模板 |

### 用户与认证

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/users` | 获取用户列表 |
| POST | `/v1/users` | 添加用户 |
| DELETE | `/v1/users/{id}` | 删除用户 |
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
| GET | `/bili/space/myinfo` | 获取 B 站账号信息（代理）|
| GET | `/bili/proxy` | B 站 API 通用代理 |

### 静态资源

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/static/{path}` | WebUI 前端静态文件服务 |

---

## 主播管理

### GET `/v1/streamers`

获取已添加的主播列表。

**响应示例**

```json
[
  {
    "id": 1,
    "name": "某直播间",
    "url": "https://live.bilibili.com/12345678",
    "enabled": true
  }
]
```

---

### POST `/v1/streamers`

添加新主播。

**请求体**

```json
{
  "url": "https://live.bilibili.com/12345678",
  "remark": "主播备注名",
  "filename_prefix": "自定义前缀",
  "time_range": "00:00-23:59",
  "upload_streamers_id": 1,
  "format": "mp4",
  "override": {},
  "preprocessor": [{"run": "echo $0"}],
  "segment_processor": [{"remux": "mp4"}],
  "downloaded_processor": [{"run": "sh ./notify.sh"}],
  "postprocessor": ["rm", {"mv": "backup/"}, {"run": "sh ./cleanup.sh"}],
  "opt_args": ["--extra-arg"],
  "excluded_keywords": ["关键词1"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | 是 | 直播间地址 |
| `remark` | string | 是 | 主播备注名 |
| `upload_streamers_id` | number \| null | 否 | 关联的上传模板 ID |
| `filename_prefix` | string \| null | 否 | 覆盖全局文件名模板 |
| `time_range` | string \| null | 否 | 录制时间范围（如 `00:00-23:59`） |
| `format` | string \| null | 否 | 录制格式（如 `mp4`） |
| `override` | object \| null | 否 | 覆盖全局配置的键值对 |
| `preprocessor` | array | 否 | 录制前钩子 |
| `segment_processor` | array | 否 | 分段后钩子 |
| `downloaded_processor` | array | 否 | 下载完成钩子 |
| `postprocessor` | array | 否 | 上传后钩子 |
| `opt_args` | array | 否 | 额外 ffmpeg 参数 |
| `excluded_keywords` | array | 否 | 标题排除关键词 |

---

### PUT `/v1/streamers`

更新主播配置。请求体与添加主播相同，需包含 `id` 字段。

```json
{
  "id": 1,
  "remark": "新名称",
  "url": "https://live.bilibili.com/12345678"
}
```

---

### DELETE `/v1/streamers/{id}`

删除指定主播。`id` 为主播的数字 ID。

**路径参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `id` | number | 主播 ID |

---

### PUT `/v1/streamers/{id}/pause`

暂停或恢复指定主播的录制任务。

**路径参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `id` | number | 主播 ID |

---

## 主播信息

### GET `/v1/streamer-info`

获取所有主播的实时信息，包含录制状态、当前文件等。

**响应示例**

```json
[
  {
    "id": 1,
    "name": "某直播间",
    "status": "recording",
    "filename": "某直播间_20260101_120000.flv"
  }
]
```

---

### GET `/v1/streamer-info/files/{id}`

获取指定主播已录制的文件列表。

**路径参数**

| 参数 | 类型 | 说明 |
|---|---|---|
| `id` | number | 主播 ID |

---

## 上传模板管理

### GET `/v1/upload/streamers`

获取所有上传模板列表。上传模板包含 B 站投稿所需的分区、标题模板、标签、简介等配置。

**响应示例**

```json
[
  {
    "id": 1,
    "name": "默认模板",
    "tid": 21,
    "title": "{name} {date}",
    "tags": ["直播录像", "biliup"],
    "desc": ""
  }
]
```

---

### POST `/v1/upload/streamers`

添加新的上传模板。

**请求体**（示例）

```json
{
  "name": "我的模板",
  "tid": 21,
  "title": "{name} {date}",
  "tags": ["直播录像"],
  "desc": "自动录制上传"
}
```

常用字段说明：

| 字段 | 说明 |
|---|---|
| `name` | 模板名称（仅用于管理界面显示）|
| `tid` | B 站分区 ID（如 21 = 日常，17 = 游戏）|
| `title` | 投稿标题模板，支持变量 `{name}`（主播名）、`{date}`（日期）等 |
| `tags` | 标签列表 |
| `desc` | 投稿简介 |
| `cover` | 封面图路径（可选）|
| `dynamic` | 动态文案（可选）|

---

### PUT `/v1/upload/streamers`

更新现有上传模板。请求体与 POST 相同，需包含 `id` 字段。

---

### GET `/v1/upload/streamers/{id}`

获取指定 ID 的上传模板详情。

---

### DELETE `/v1/upload/streamers/{id}`

删除指定 ID 的上传模板。

---

## 用户与认证

### GET `/v1/users`

获取已登录的 B 站账号列表。

**响应示例**

```json
[
  {
    "id": 1,
    "name": "用户昵称",
    "uid": 12345678
  }
]
```

---

### POST `/v1/users`

添加新的 B 站账号。通常配合扫码登录流程使用。

---

### DELETE `/v1/users/{id}`

删除指定账号。`id` 为账号在 biliup 内部的 ID（非 B 站 UID）。

---

### POST `/v1/users/login`

WebUI 管理界面登录。

**请求体**

```json
{
  "username": "biliup",
  "password": "your_password",
  "remember": true
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `username` | string | 用户名 |
| `password` | string | 密码 |
| `remember` | boolean | 是否记住登录状态 |

---

### POST `/v1/users/register`

首次使用时注册 WebUI 管理账号。仅在 `--auth` 模式且无用户存在时可用。

**请求体**

```json
{
  "username": "biliup",
  "password": "your_password"
}
```

---

### GET `/v1/users/biliup`

检查默认用户是否已创建。返回用户存在状态，前端据此决定是否显示注册页面。

---

### GET `/v1/logout`

退出当前登录会话，销毁 Session。

---

## B站扫码登录

### GET `/v1/get_qrcode`

获取 B 站扫码登录所需的二维码信息。

**响应示例**

```json
{
  "qrcode_key": "xxxxxxxx",
  "url": "https://passport.bilibili.com/h5-app/passport/login/scan?navhide=1&qrcode_key=xxxxxxxx"
}
```

使用方式：
1. 调用此接口获取 `url` 并生成二维码图片
2. 用 B 站 App 扫码
3. 调用 `/v1/login_by_qrcode` 确认登录状态

---

### POST `/v1/login_by_qrcode`

轮询扫码登录结果，确认登录是否成功。

**请求体**

```json
{
  "qrcode_key": "xxxxxxxx"
}
```

---

## 视频与状态

### GET `/v1/videos`

获取 biliup 管理的视频文件列表（已录制未上传的文件等）。

---

### GET `/v1/status`

获取 biliup 系统当前运行状态，包括各主播录制状态、上传队列等。

**响应示例**

```json
{
  "version": "1.2.1",
  "recording": 2,
  "uploading": 1
}
```

---

### POST `/v1/uploads`

手动触发一个上传任务，将指定视频文件上传至 B 站。

**请求体**

```json
{
  "files": ["/opt/录播/主播名_20260101_120000.flv"],
  "params": {
    "template_name": "手动上传",
    "title": "{title} - {date}",
    "tid": 171,
    "tags": ["直播录制"],
    "copyright": 1,
    "uploader": "biliup-rs",
    "user_cookie": "cookies.json"
  }
}
```

| 字段 | 说明 |
|---|---|
| `files` | 视频文件路径列表 |
| `params` | 上传配置（结构与上传模板相同） |

---

### GET `/v1/ws/logs` （WebSocket）

WebSocket 连接，实时推送运行日志。

**连接方式**

```javascript
const ws = new WebSocket('ws://localhost:19159/v1/ws/logs');
ws.onmessage = (event) => console.log(event.data);
```

**日志频道**

| 频道 | 说明 |
|---|---|
| `ds_update.log` | 直播检测/更新日志 |
| `download.log` | 下载/录制日志 |
| `postprocessor` | 上传/后处理日志 |

---

## 全局配置

### GET `/v1/configuration`

获取 biliup 当前的全局配置。

---

### PUT `/v1/configuration`

更新全局配置。请求体为配置的完整 JSON 对象（建议先 GET 获取再修改后 PUT 回去）。

---

## B 站 API 代理

以下接口将请求代理至 B 站官方 API，供 WebUI 前端使用，**通常不需要直接调用**。

### GET `/bili/archive/pre`

获取 B 站投稿分区等预置数据。

### GET `/bili/space/myinfo`

获取当前登录 B 站账号的个人信息。

### GET `/bili/proxy`

通用代理，转发任意 B 站 API 请求。

---

## 静态资源

### GET `/static/{path}`

提供 WebUI 前端静态文件服务（HTML/JS/CSS 等）。直接访问 `http://localhost:19159` 即可打开 WebUI。

---

## 使用示例

### 通过 curl 获取主播列表

```bash
curl http://localhost:19159/v1/streamers
```

### 添加主播（完整请求体）

```bash
curl -X POST http://localhost:19159/v1/streamers \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://live.bilibili.com/12345678",
    "remark": "某直播间"
  }'
```

### 暂停主播录制

```bash
curl -X PUT http://localhost:19159/v1/streamers/1/pause
```

### 删除主播

```bash
curl -X DELETE http://localhost:19159/v1/streamers/1
```

### 手动触发上传

```bash
curl -X POST http://localhost:19159/v1/uploads \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["/opt/录播/video.flv"],
    "params": {
      "title": "手动上传",
      "tid": 171,
      "tags": ["直播录制"],
      "copyright": 1
    }
  }'
```

### WebSocket 监听日志（Python 示例）

```python
import websockets
import asyncio

async def listen_logs():
    async with websockets.connect("ws://localhost:19159/v1/ws/logs") as ws:
        async for message in ws:
            print(message)

asyncio.run(listen_logs())
```
