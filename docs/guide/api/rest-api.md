---
description: biliup REST API 与日志 WebSocket：路由、认证、手动上传示例（含必填 id/template_name）与日志频道（upload.log），基于 v1.2.2 核对。
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

## WebSocket 日志

`GET /v1/ws/logs` 建长连接后按频道推日志：

| 频道 | 说明 |
|---|---|
| `ds_update.log` | 直播检测 / 开播更新 |
| `download.log` | 下载 / 录制 |
| `upload.log` | 上传 / 后处理 |

::: warning
`/v1/ws/logs` 的鉴权边界：即使启用了 `--auth`，该 WebSocket 日志端点**仍位于登录守卫之外**，连接时不会要求会话认证，日志中可能包含文件名、路径等敏感信息。请勿在公网不经反向代理 / 访问控制直接暴露该端口；如需保护，请在反向代理层对 `/v1/ws/logs` 额外加鉴权。
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
