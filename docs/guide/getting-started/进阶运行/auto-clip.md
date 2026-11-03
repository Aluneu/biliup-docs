---
description: 自动切片：用语音转写 + 大模型从录像里挑高光候选，人工接受后才建切片。[auto_clip] 配置项、用量上限与接口一览。
---

# 自动切片

下播后让模型先看一遍录像，挑出可能的高光片段作为**候选**；候选只进回看页，**人工接受后才建切片**，不会自动导出或投稿。

> 实验功能。没有配置 `[auto_clip]` 或 `enabled = false` 时，**不会调用任何 API**。

---

## 它做了什么

1. FFmpeg 抽音轨，跳过静音段；
2. 送语音转写（ASR），得到带时间戳的文字；
3. 叠加弹幕密度（模型支持看图时再加关键帧缩图）；
4. 交给 chat 模型挑出候选片段（默认 15–180 秒，最多 20 个）；
5. 候选写进回看页，等你接受或丢弃——接受只是建一个**切片草稿**。

整个过程跑在 biliup 进程内，录像不出本机（只有音频 / 文本 / 缩图发给你配置的模型接口）。

---

## 配置

WebUI：「**空间配置 › 自动切片（实验）**」，对应配置文件的 `[auto_clip]`。

只支持 **OpenAI 兼容接口**（`/chat/completions`、`/audio/transcriptions`）。

| 字段 | 说明 | 默认 |
|---|---|---|
| `enabled` | 总开关 | `false` |
| `base_url` | chat 接口地址，一般以 `/v1` 结尾 | — |
| `api_key` | chat 的 key；也可用环境变量 `BILIUP_AUTO_CLIP_API_KEY`（**环境变量优先**） | — |
| `chat_model` | 挑候选用的模型 | — |
| `asr_base_url` | 转写服务地址；留空沿用 `base_url` | 同 chat |
| `asr_api_key` | 转写 key；留空沿用 chat 的 key | 同 chat |
| `asr_model` | 转写模型（如 `whisper-1`） | — |
| `asr_language` | 传给转写的语言；留空由服务识别 | 自动 |
| `asr_prompt` | 转写热词（主播名、游戏名、梗），提升专有名词识别 | — |
| `thumbnails` | 关键帧缩图：`auto`（模型能看图才开）/ `on` / `off` | `auto` |
| `max_asr_minutes` | 每场送转写的分钟数上限 | `300` |
| `max_chat_tokens` | 每场 chat 的 token 上限（输入 + 输出） | `300000` |
| `chat_timeout_secs` | 单次 chat 请求超时 | `180` |
| `asr_timeout_secs` | 单次转写请求超时 | `300` |
| `min_clip_secs` / `max_clip_secs` | 候选时长范围（秒） | `15` / `180` |
| `max_candidates` | 每场最多保留几个候选（上限 200） | `20` |

```toml
[auto_clip]
enabled = true
base_url = "https://api.example.com/v1"
chat_model = "your-chat-model"
asr_model = "whisper-1"
asr_language = "zh"
asr_prompt = "主播名, 游戏名"
max_asr_minutes = 180
max_candidates = 12
```

::: warning 先「测试连接」再开开关
WebUI 的自动切片面板有「测试连接」，会分别打一次 chat 与转写接口。key 保存后接口只回显掩码（`sk-…abcd`）；**改了接口地址后必须重新填完整 key**——已保存的 key 不会被发往新地址，这是防止掩码变成外发通道。
:::

---

## 触发方式

| 方式 | 位置 | 说明 |
|---|---|---|
| 下播后自动生成 | 主播编辑 →「下播后自动生成候选」（全局字段 `auto_clip_after_live`） | 默认**关闭**，仅超级管理员可改 |
| 手动生成 | 剪辑台「直播场次」→「生成候选」 | 先给出用量预估（转写分钟数 / token），确认后入队 |
| 取消 | 同上，任务进行中 | 取消当前场次的任务 |

费用以服务商账单为准，预估只是本地按上限算的粗估。

---

## 上限与过期

- 每场最多转写 `max_asr_minutes`（默认 300 分钟）、chat 消耗 `max_chat_tokens`（默认 30 万），到顶就停，不会偷偷超支；
- 候选 **72 小时**未处理自动过期；
- 重新生成会先给一次用量预估，超过上限的部分不会送去转写。

---

## 接受之后

- 「接受」建一个**切片草稿**（时间区间 + 标题），之后和手动切片一样可以导出、按模板投稿；
- 「丢弃」只是标记，不会删除录像；
- 候选里的标题只是建议，导出前可以改。

---

## 相关接口

自动切片这组接口目前定位为实验性，形态可能调整：

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/v1/auto-clip/test` | 测试 chat / 转写连通性 |
| GET | `/v1/auto-clip/status` | 是否启用、key 来源（env / config） |
| GET | `/v1/auto-clip/jobs` | 多场各自最近的任务 |
| GET / POST / DELETE | `/v1/sessions/{id}/auto-clip` | 查看任务与用量预估 / 预估后入队 / 取消 |
| GET | `/v1/sessions/{id}/suggestions` | 候选列表 |
| POST | `/v1/sessions/{id}/suggestions/{sid}/accept` | 接受（建切片草稿） |
| POST | `/v1/sessions/{id}/suggestions/{sid}/dismiss` | 丢弃 |
| GET | `/v1/sessions/{id}/danmaku-density` | 弹幕密度曲线（10 秒一桶） |

---

## 注意事项

- 抽音频与取帧会真的调用 `ffmpeg`，需要本机安装；
- 转写很吃时间，一场 4 小时的直播即使只跑 300 分钟音频也要等一阵；
- 隐私：音频、转写文本与关键帧缩图会发到你配置的接口，选服务商前想清楚；
- 与「画面遮挡」互不影响：候选基于录像做时间点判断，实际导出沿用当前的遮挡 / 合成设置。

---

## 相关

- [剪辑台与回放](/guide/webui/usage.html#剪辑台-workbench)
- [全局设置](/guide/getting-started/配置/global-config.html)
- [REST API](/guide/api/rest-api.html)
