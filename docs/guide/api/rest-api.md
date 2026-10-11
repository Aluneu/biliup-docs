---
description: biliup REST API 与日志 WebSocket：路由、认证与分级权限、B站账号与 WebUI 账号两组用户接口、Fleet 控制面路由、手动上传示例（含必填 id/template_name）与日志频道（upload.log），基于 v1.2.11 与 master 现行代码核对。
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
2. 之后用 `POST /v1/users/login` 登录，基于 Session（Cookie，名 `biliup.sid`，**7 天不活动过期**），登录后浏览器自动带会话；
3. 退出调 `GET /v1/logout`（也接受 POST）销毁会话。

开启 `--auth` 后，所有 `/v1/*` 业务路由经过一层**按路由表的权限校验（默认拒绝）**：

- 只读类（`GET` 列表 / 状态 / 媒体等）要求 *查看* 级权限——只读观察者即可访问；
- 变更类（增删改、暂停、导出等）按操作类型要求 *操作* 或 *配置* 级权限——操作员可日常操作，改全局配置 / 管理 WebUI 用户需超级管理员；
- 三种角色：`admin`（超级管理员）/ `operator`（操作员）/ `viewer`（只读观察者）；
- WebSocket / SSE / 直播流等长连接在握手后**每 30 秒复查一次**会话与权限，用户被禁用、改密或强制下线时连接会被切断；
- 登录相关接口（`/v1/users/login|register|logout|biliup`）与 `/v1/me*` 在权限层之外，只要求（或不要求）登录本身。

> ⚠️ WebUI 管理员账号的用户名**固定为 `biliup`**，注册 / 登录时该用户名不可修改，你只需设置密码。它与用于投稿的 B站账号（扫码 / Cookie 添加）是两套不同身份，接口上也分别对应 `/v1/web-users*` 与 `/v1/users*` 两组路由，请勿混淆。

> 没开 `--auth` 时接口没有任何保护（视同超管），登录与用户管理路由不会挂载，生产环境别直接把端口暴露出去。

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

### 标记

| 方法 | 路径 | 说明 |
|---|---|---|
| GET / POST | `/v1/sessions/{id}/markers` | 列出 / 新建标记（看直播时打点） |
| PATCH / DELETE | `/v1/sessions/{id}/markers/{mid}` | 更新 / 删除标记 |

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

### B站投稿账号

> 这一组管理的是**用于上传与投稿的 B站账号**（扫码 / Cookie 添加），不是 WebUI 登录账号。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/users` | 获取 B站账号列表 |
| POST | `/v1/users` | 添加 B站账号 |
| GET | `/v1/users/{id}` | 获取指定 B站账号信息 |
| DELETE | `/v1/users/{id}` | 删除 B站账号 |
| GET | `/v1/users/{id}/archives` | 获取指定 B站账号的稿件列表 |

### WebUI 登录用户与权限

> 这一组管理**登录 WebUI 后台的账号**（v1.2.8 起多用户 / 分级权限）。仅 `--auth` 开启时挂载，管理需要超管权限。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/web-users` | 获取 WebUI 用户列表 |
| POST | `/v1/web-users` | 添加 WebUI 用户 |
| GET | `/v1/web-users/roles` | 获取可分配的角色（`admin` / `operator` / `viewer`）|
| PUT | `/v1/web-users/{id}` | 修改用户（角色、禁用等）|
| DELETE | `/v1/web-users/{id}` | 删除用户 |
| POST | `/v1/web-users/{id}/logout-all` | 让该用户所有会话下线 |
| GET | `/v1/me` | 当前登录者身份与权限点（含 Fleet 能力标记，前端据此显隐菜单）|
| PUT | `/v1/me/password` | 修改自己的密码（会使其他会话失效）|

### 认证与会话

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/v1/users/login` | WebUI 用户登录 |
| POST | `/v1/users/register` | WebUI 用户注册（首个账号用户名固定 `biliup`）|
| GET | `/v1/users/biliup` | 检查默认管理账号是否已存在 |
| GET / POST | `/v1/logout` | 退出登录，销毁会话 |

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

### Fleet 主备接口

> Fleet 控制面（`/v1/fleet/*`）的路由只在 `biliup server --controller` 启动时挂载，普通服务端不注册。节点侧（`/v1/node/*`）只在被控制面托管的节点上存在，受节点凭据保护而非 WebUI 会话。

**控制面 `/v1/fleet/*`：**

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/v1/fleet/nodes` | 节点列表与状态 |
| DELETE | `/v1/fleet/nodes/{id}` | 移除（吊销）节点 |
| PUT | `/v1/fleet/nodes/{id}/labels` | 设置节点标签 |
| GET / PUT | `/v1/fleet/nodes/{id}/config` | 查看 / 下发节点配置覆写 |
| POST | `/v1/fleet/local-node` | 让控制面本机也作为录制节点 |
| GET / POST | `/v1/fleet/join-tokens` | 加入票据列表 / 新建票据（`bfleet` 开头）|
| DELETE | `/v1/fleet/join-tokens/{id}` | 删除票据 |
| GET / POST | `/v1/fleet/rooms` | 托管房间列表 / 新建 |
| PUT / DELETE | `/v1/fleet/rooms/{id}` | 更新 / 删除房间 |
| POST | `/v1/fleet/rooms/{id}/assign` | 手动指派房间到节点 |
| POST | `/v1/fleet/rooms/{id}/force` | 强制释放房间的节点占用 |
| POST | `/v1/fleet/rooms/{id}/pause` | 暂停 / 恢复房间调度 |
| GET / POST | `/v1/fleet/templates` | 房间模板列表 / 新建 |
| PUT / DELETE | `/v1/fleet/templates/{id}` | 更新 / 删除模板 |
| GET | `/v1/fleet/accounts` | 可下发的 B站账号列表 |
| GET / PUT | `/v1/fleet/configuration` | 集群全局配置读取 / 下发 |
| GET | `/v1/fleet/configuration/history` | 配置下发历史 |
| GET / DELETE | `/v1/fleet/alerts` | 告警列表 / 清空 |
| DELETE | `/v1/fleet/alerts/{id}` | 确认单条告警 |
| GET | `/v1/fleet/summary` | 控制台汇总 |
| GET / PUT / DELETE | `/v1/fleet/ha` | 主备配对状态 / 建立配对 / 解散 |
| GET | `/v1/fleet/ha/candidates` | 可配对候选 |
| POST | `/v1/fleet/ha/join` | 接受配对加入 |
| POST | `/v1/fleet/ha/role` | 切换主备角色 |
| POST | `/v1/fleet/ha/sessions/{key}/{action}` | 按会话手工仲裁（上传归属）|
| POST | `/v1/fleet/ha/handback/{kind}/{id}/{action}` | 接管后的回交动作 |

**节点侧 `/v1/node/*`：**

| 方法 | 路径 | 说明 |
|---|---|---|
| GET / PUT | `/v1/node/ha` | 查看 / 配置本机主备参数 |
| GET | `/v1/node/ha/candidates` | 本机可见的配对候选 |
| POST | `/v1/node/ha/join` | 从节点侧发起配对 |
| POST | `/v1/node/ha/role` | 本机角色切换 |
| POST | `/v1/node/ha/sessions/{key}/{action}` | 会话级手工动作 |
| DELETE | `/v1/node/revoked` | 确认被移除状态并清理 |
| POST | `/v1/node/revoked/resume` | 恢复被控制面暂停的受管主播 |

::: info 自动切片（auto-clip）接口未收录
源码中还有一组 `/v1/auto-clip/*` 与 `/v1/sessions/{id}/suggestions*` 路由（模型 API 驱动的自动切片，实验性质、尚未正式发布），本文暂不收录；接口形态以源码为准，正式发布后另行补文档。
:::

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
