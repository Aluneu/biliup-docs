# 开发者选项

> [!WARNING]
> 以下选项面向进阶用户和开发者，普通用户无需修改。

---

## 钩子系统（Hooks）

biliup 提供四个阶段的钩子，支持自定义脚本和外部通知：

| 钩子阶段 | 触发时机 | 用途示例 |
|----------|----------|----------|
| **录制前** | 检测到开播，准备开始录制 | 发送开播通知 |
| **分段后** | 录制文件达到分段条件 | 弹幕压制、格式转换 |
| **上传前** | 文件准备上传 | 文件预处理 |
| **上传后** | 上传完成 | 发送通知、删除本地文件、Webhook |

### 钩子配置方式

在 WebUI「空间配置」→「开发者选项」中配置：

- **脚本路径**：指向可执行的 Python 脚本
- **Webhook URL**：上传完成后向该 URL 发送 POST 请求

### Webhook 格式

上传完成后发送的 POST 请求包含以下信息：

```json
{
  "title": "视频标题",
  "bvid": "BVxxxxxxxxxx",
  "aid": 123456789,
  "file": "/path/to/video.flv"
}
```

---

## 分段处理器（segment_processor）

录制文件达到分段条件后，可对文件进行后处理。

### 内置处理器

| 处理器 | 说明 |
|--------|------|
| `remux:mp4` | 将 FLV 重新封装为 MP4（无需重新编码，速度快） |

### 自定义处理器

可编写自定义 Python 脚本，搭配 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory) 等工具实现弹幕压制。

---

## 高级配置

### 配置文件位置

- WebUI 默认使用 `data/data.sqlite3` 存储配置
- 支持通过 `--config` 参数指定 YAML 配置文件
- 新版启动时自动将旧版 YAML 配置转换到数据库

### 日志级别

```bash
# 详细日志（用于排查问题）
biliup server -v
```

### 自定义 WebUI 目录

```bash
biliup server --static-dir /path/to/custom-ui
```
（此功能暂未完全开放）
