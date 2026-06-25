# REST API 文档

biliup 启动 Web 服务后，会在指定端口暴露一组 REST 风格的 HTTP API，供 WebUI 前端调用，同时也支持外部程序通过 HTTP 请求进行集成。

> ⚠️ API 文档基于 biliup v1.x 版本。部分接口在旧版中路径可能不同。

---

## 基础信息

| 项目 | 说明 |
|---|---|
| 默认基地址 | `http://localhost:19159` |
| API 路径前缀 | `/api/` |
| 认证方式 | HTTP Basic Auth（`--auth user:pass` 启动参数）|
| 响应格式 | JSON |
| 请求体格式 | JSON (`Content-Type: application/json`) |

### 认证

如启动时指定了 `--auth`，所有 API 请求需在 Header 中携带 Basic Auth：

```
Authorization: Basic <base64(user:password)>
```

未设置 `--auth` 时，API 无认证保护，**请勿在生产环境不设认证**。

---

## 接口总览

| 模块 | 路径前缀 | 说明 |
|---|---|---|
| 系统状态 | `/api/status` | 获取运行状态、版本信息 |
| 主播管理 | `/api/streamers` | 增删改查直播间录制配置 |
| 录制控制 | `/api/record` | 手动触发/停止录制 |
| 上传管理 | `/api/upload` | 查询上传任务、触发上传 |
| 投稿模板 | `/api/templates` | 管理投稿模板配置 |
| 账号管理 | `/api/accounts` | 管理 B站登录账号 |
| 任务查询 | `/api/jobs` | 查询当前运行中的任务 |
| 历史记录 | `/api/history` | 查询录制/上传历史 |
| 日志 | `/api/logs` | 获取运行日志 |
| 配置 | `/api/config` | 读写全局/平台配置 |
| Webhook | `/api/webhook` | 配置上传完成通知 |

---

## 系统状态

### GET /api/status

获取 biliup 运行状态。

**响应示例：**

```json
{
  "version": "v1.2.1",
  "uptime": 86400,
  "cpu_usage": 12.5,
  "memory_usage_mb": 256,
  "disk_free_gb": 50.2,
  "active_recordings": 3,
  "active_uploads": 1,
  "pool_size": 5,
  "bili_accounts": [
    { "uid": 123456, "name": "用户名", "expires": "2025-06-01T00:00:00Z" }
  ]
}
```

---

## 主播管理

### GET /api/streamers

列出所有已添加的主播。

**查询参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `platform` | string | 按平台过滤（`bilibili` / `douyu` / `huya` 等）|
| `status` | string | `recording` / `idle` / `error` |
| `page` | int | 分页页码（默认 1）|
| `page_size` | int | 每页数量（默认 20）|

**响应示例：**

```json
{
  "total": 15,
  "page": 1,
  "data": [
    {
      "id": 1,
      "name": "主播名",
      "platform": "bilibili",
      "room_url": "https://live.bilibili.com/123456",
      "status": "recording",
      "title": "直播标题",
      "file_size_mb": 1024.5,
      "start_time": "2025-03-25T12:00:00Z",
      "template_id": 2,
      "enabled": true
    }
  ]
}
```

### POST /api/streamers

添加新主播。

**请求体：**

```json
{
  "room_url": "https://live.bilibili.com/123456",
  "template_id": 1,
  "enabled": true
}
```

**响应：** `201 Created`

```json
{ "id": 16, "message": "主播已添加，正在检测开播状态..." }
```

### PUT /api/streamers/{id}

更新指定主播的配置。

**请求体：（部分字段可选）**

```json
{
  "enabled": false,
  "template_id": 3,
  "filename_prefix": "{streamer}_{date}",
  "segment_size": 4294967296,
  "danmaku": true
}
```

### DELETE /api/streamers/{id}

删除指定主播（不会删除已录制的文件）。

**响应：** `204 No Content`

---

## 录制控制

### POST /api/record/start/{streamer_id}

手动触发指定主播的录制（无论是否开播）。

### POST /api/record/stop/{streamer_id}

停止指定主播的录制。

### GET /api/record/status

获取所有当前录制任务的状态。

---

## 上传管理

### GET /api/upload/queue

获取等待上传和正在上传的任务列表。

### POST /api/upload/start/{history_id}

手动触发指定历史记录的 Upload。

**请求体：**

```json
{
  "template_id": 1,
  "account_id": 1
}
```

### POST /api/upload/retry/{upload_id}

重试失败的上传任务。

### GET /api/upload/progress/{upload_id}

获取指定上传任务的进度。

**响应示例：**

```json
{
  "upload_id": 42,
  "status": "uploading",
  "progress": 68.5,
  "speed_mbps": 12.3,
  "remaining_seconds": 120
}
```

---

## 投稿模板

### GET /api/templates

列出所有投稿模板。

**响应示例：**

```json
{
  "total": 3,
  "data": [
    {
      "id": 1,
      "name": "默认投稿",
      "account_id": 1,
      "tid": 17,
      "tid_name": "游戏 → 电子竞技",
      "title_template": "{title}",
      "desc_template": "录制自 {streamer} 的直播间",
      "tag_template": "直播录制,{streamer}",
      "cover_mode": "auto",
      "delay_hours": 0,
      "dolby": false
    }
  ]
}
```

### POST /api/templates

创建新投稿模板。

### PUT /api/templates/{id}

更新指定模板。

### DELETE /api/templates/{id}

删除指定模板（正在使用的主播会变为未指定模板状态）。

---

## 账号管理

### GET /api/accounts

列出所有已登录的 B站账号。

### POST /api/accounts/login

触发扫码登录流程，返回二维码 URL。

**响应示例：**

```json
{
  "qr_url": "https://passport.bilibili.com/x/passport-login/web/qrcode...",
  "qrcode_key": "xxx",
  "pol_interval": 3
}
```

### POST /api/accounts/poll

轮询扫码登录状态。

**请求体：**

```json
{ "qrcode_key": "xxx" }
```

**响应：**

```json
{ "status": "waiting" }       // 等待扫码
{ "status": "scanned" }      // 已扫码，等待确认
{ "status": "success", "uid": 123456, "name": "用户名" }  // 登录成功
```

### POST /api/accounts/refresh/{id}

刷新指定账号的登录状态（续期 Cookie）。

### DELETE /api/accounts/{id}

删除指定账号（不会注销 B站账号，只是移除本地 Cookie）。

---

## 历史记录

### GET /api/history

查询录制/上传历史记录。

**查询参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `streamer_id` | int | 按主播过滤 |
| `status` | string | `recorded` / `uploading` / `uploaded` / `submitted` |
| `start_date` | string | 起始日期 `YYYY-MM-DD` |
| `end_date` | string | 结束日期 `YYYY-MM-DD` |
| `keyword` | string | 按标题搜索 |
| `page` | int | 分页页码 |
| `page_size` | int | 每页数量 |

### DELETE /api/history/{id}

删除指定历史记录（可选是否同时删除本地文件）。

**查询参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `delete_file` | bool | 是否同时删除本地录制文件（默认 `false`）|

---

## 任务查询

### GET /api/jobs

获取当前运行中的任务列表。

**查询参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `type` | string | `record` / `upload` / `process` / `submit` |

**响应示例：**

```json
{
  "total": 2,
  "data": [
    {
      "id": "job_abc123",
      "type": "record",
      "streamer_name": "主播名",
      "status": "running",
      "progress": null,
      "created_at": "2025-03-25T12:00:00Z"
    },
    {
      "id": "job_def456",
      "type": "upload",
      "streamer_name": "主播名",
      "status": "uploading",
      "progress": 72.3,
      "speed_mbps": 8.5,
      "created_at": "2025-03-25T13:00:00Z"
    }
  ]
}
```

### DELETE /api/jobs/{job_id}

取消指定任务。

---

## 日志

### GET /api/logs

获取运行日志（支持级别过滤和分页）。

**查询参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `level` | string | `ERROR` / `WARN` / `INFO` / `DEBUG`（默认返回该级别及以上）|
| `lines` | int | 返回行数（默认 500）|
| `search` | string | 关键词过滤 |
| `follow` | bool | 是否保持连接流式返回（SSE）|

> 💡 日志查看器页面使用 `follow=true` 的 SSE 模式实现实时日志推送。

---

## 配置

### GET /api/config

获取当前全局配置（不含敏感信息如 Cookie 内容）。

### PUT /api/config

更新全局配置。

**请求体：**（与 WebUI「空间配置 → 全局设置」中的参数对应）

```json
{
  "downloader": "stream-gears",
  "segment_size": 4294967296,
  "segment_time": "01:00:00",
  "filename_prefix": "{streamer}%Y-%m-%dT%H_%M_%S",
  "pool1_size": 5,
  "filtering_threshold": 20,
  "delay": 0,
  "event_loop_interval": 10
}
```

### GET /api/config/platform/{platform}

获取指定平台的配置。

### PUT /api/config/platform/{platform}

更新指定平台的配置。

---

## 集成示例

### 使用 curl 添加主播

```bash
# 添加 B站直播间
curl -u admin:password \
  -X POST http://localhost:19159/api/streamers \
  -H "Content-Type: application/json" \
  -d '{"room_url": "https://live.bilibili.com/123456", "enabled": true}'
```

### 使用 Python 查询录制状态

```python
import requests

API_BASE = "http://localhost:19159/api"
auth = ("admin", "password")

resp = requests.get(f"{API_BASE}/streamers", auth=auth)
for s in resp.json()["data"]:
    if s["status"] == "recording":
        print(f"正在录制：{s['name']} - {s['title']}")
```

### Webhook 通知（上传完成后）

在「空间配置 → 开发者选项」中配置 Webhook URL 后，上传完成时会收到如下 POST 请求：

```json
POST https://your-webhook-url.com/biliup-notify
Content-Type: application/json

{
  "event": "upload_complete",
  "streamer": "主播名",
  "title": "直播标题",
  "file_size_mb": 2048.0,
  "upload_time": "2025-03-25T14:00:00Z",
  "bvid": "BV1xx411c7mD",
  "account": "用户名"
}
```

---

## 注意事项

1. **接口稳定性**：biliup 的 HTTP API 目前未承诺版本间兼容，升级时请注意确认接口是否有变化。
2. **并发控制**：同时发起大量请求可能导致服务压力过大，建议控制调用频率。
3. **文件上传接口**：如需通过 API 直接上传视频文件，需使用 `multipart/form-data` 格式，详见各版本的实际接口定义。
4. **更多接口**：本列表覆盖了主要使用场景，完整接口定义以实际抓包或源码为准。

---

## 下一步

- 了解[WebUI 完整使用指南](/guide/webui/webui-guide.html)
- 了解[命令行参考](/guide/configs/config.html)
- 了解[开发者选项（Hooks / 自定义后处理）](/guide/introduce/Config/developerOptions.html)
