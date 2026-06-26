# REST API 文档

biliup 启动 Web 服务后，会在指定端口暴露一组 REST 风格的 HTTP API，供 WebUI 前端调用，同时也支持外部程序通过 HTTP 请求进行集成。

> 本文档基于 biliup v1.x 版本后端路由，路径均以实际源码为准。

---

## 基础信息

| 项目 | 说明 |
|---|---|
| 默认端口 | `19159` |
| 默认基地址 | `http://localhost:19159` |
| 响应格式 | JSON |
| 请求体格式 | JSON（`Content-Type: application/json`）|
| 认证方式 | HTTP Basic Auth（`--auth user:pass` 启动参数，不设置则无认证）|

### 认证说明

如启动时指定了 `--auth`，所有 API 请求需在 Header 中携带：

```http
Authorization: Basic <base64(user:password)>
```

未设置 `--auth` 时，API 无认证保护，**请勿在生产环境中不设认证直接暴露端口**。

---

## 接口总览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/streamers` | 获取主播列表 |
| POST | `/v1/streamers` | 添加主播 |
| PUT | `/v1/streamers` | 更新主播 |
| DELETE | `/v1/streamers/{id}` | 删除主播 |
| PUT | `/v1/streamers/{id}/pause` | 暂停/恢复主播录制 |
| GET | `/v1/configuration` | 获取全局配置 |
| PUT | `/v1/configuration` | 更新全局配置 |
| GET | `/v1/streamer-info` | 获取主播信息（录制状态等）|
| GET | `/v1/streamer-info/files/{id}` | 获取主播的文件列表 |
| GET | `/v1/upload/streamers` | 获取上传模板列表 |
| POST | `/v1/upload/streamers` | 添加上传模板 |
| GET | `/v1/upload/streamers/{id}` | 获取单个上传模板 |
| DELETE | `/v1/upload/streamers/{id}` | 删除上传模板 |
| GET | `/v1/users` | 获取已登录账号列表 |
| POST | `/v1/users` | 添加账号 |
| DELETE | `/v1/users/{id}` | 删除账号 |
| GET | `/v1/get_qrcode` | 获取 B 站扫码登录二维码 |
| POST | `/v1/login_by_qrcode` | 二维码扫码登录 |
| GET | `/v1/videos` | 获取视频文件列表 |
| GET | `/v1/status` | 获取系统运行状态 |
| POST | `/v1/uploads` | 手动触发上传任务 |
| GET | `/bili/archive/pre` | B 站投稿预处理（代理）|
| GET | `/bili/space/myinfo` | 获取 B 站账号信息（代理）|
| GET | `/bili/proxy` | B 站 API 通用代理 |

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
  "name": "某直播间",
  "url": "https://live.bilibili.com/12345678",
  "upload_id": null
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `name` | string | 是 | 主播显示名称 |
| `url` | string | 是 | 直播间地址 |
| `upload_id` | number \| null | 否 | 关联的上传模板 ID |

---

### PUT `/v1/streamers`

更新主播配置。请求体与添加主播相同，需包含 `id` 字段。

```json
{
  "id": 1,
  "name": "新名称",
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

### GET `/v1/upload/streamers/{id}`

获取指定 ID 的上传模板详情。

---

### DELETE `/v1/upload/streamers/{id}`

删除指定 ID 的上传模板。

---

## 用户（账号）管理

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

## 认证（扫码登录）

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

### 带认证的请求

```bash
curl -u admin:password http://localhost:19159/v1/streamers
```

### 添加主播

```bash
curl -X POST http://localhost:19159/v1/streamers \
  -H "Content-Type: application/json" \
  -d '{"name": "某直播间", "url": "https://live.bilibili.com/12345678"}'
```

### 暂停主播录制

```bash
curl -X PUT http://localhost:19159/v1/streamers/1/pause
```

### 删除主播

```bash
curl -X DELETE http://localhost:19159/v1/streamers/1
```
