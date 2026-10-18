# Python 开发

biliup 的 Python 部分在 v1.3.0 起收敛为**纯 API 绑定**：`stream-gears` 把 Rust 核心的上传、直链下载与登录能力暴露给 Python，**不再包含录制服务、WebUI、字体或命令行入口**。

> 如果你在找 `python -m biliup`：该入口已在 v1.3.0 移除。运行完整应用请用原生 CLI、桌面版或 Docker，见[安装部署](/guide/getting-started/安装部署/Linux.html)。

---

## 技术栈

| 技术 | 用途 |
|---|---|
| Python | 3.9+ |
| maturin | Rust/Python 桥接，编译 `stream-gears` 扩展 |
| stream-gears | Rust 核心的 Python 绑定（上传 / 直链下载 / 登录） |

---

## 环境搭建

### 1. 安装 Python

```bash
# 推荐使用 uv 管理 Python 版本
uv python install 3.12
uv venv --python 3.12
```

或系统包管理器：

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python@3.12
```

### 2. 安装 maturin

```bash
pip install maturin
maturin --version   # >= 1.0
```

---

## 编译 Rust 扩展（stream-gears）

```bash
# 仓库根目录
maturin develop -m crates/stream-gears/Cargo.toml
```

验证：

```bash
python -c "import stream_gears; print('OK')"
```

::: tip 构建 Python 包不需要构建前端
`stream-gears` 只链接 `biliup` 核心库，不依赖 `biliup-cli`、axum 或 `out/` 前端产物，因此不必先跑 `npm run build`。
:::

---

## 使用

### 登录

```python
import json
import stream_gears

# 方式一：用已保存的 cookie 文件登录
stream_gears.login_by_cookies("cookies.json")

# 方式二：扫码登录
qr = stream_gears.get_qrcode()        # 返回 JSON 字符串（含二维码 url 与 qrcode_key）
print(json.loads(qr)["url"])          # 自行渲染成二维码图片
stream_gears.login_by_qrcode(qr, file="cookies.json")   # 扫码确认后写入凭据
```

> `login_by_qrcode` 的第二个位置参数是 `proxy`，不是文件名；要落盘请用关键字参数 `file=`。

### 上传

```python
import stream_gears

stream_gears.upload(
    video_path=["video.mp4"],   # 列表，可传多个文件做多 P 上传
    cookie_file="cookies.json",
    title="测试投稿",
    tid=171,                    # 分区 id
    tag="测试,直播录制",
    desc="通过 stream_gears 上传",
    copyright=1,                # 1 自制 / 2 转载
    submit="b-cut-android",     # 可选：web / app / b-cut-android
)
```

其余参数（`source`、`cover`、`dynamic`、`dtime`、`line`、`extra_fields` 等）与 CLI 投稿参数一一对应，见[命令行参考](/guide/configs/config.html)。

### 下载直播流

```python
import stream_gears

segment = stream_gears.PySegment()
segment.time = 3600            # 每段 1 小时（秒）
segment.size = 2 * 1024 ** 3   # 或每段 2 GiB（字节）；都不设 = 不分段

stream_gears.download(
    url="https://...",
    header_map={"referer": "https://live.bilibili.com", "user-agent": "Mozilla/5.0"},
    file_name="recording%Y-%m-%dT%H_%M_%S",   # 文件名模板，不含扩展名
    segment=segment,
)
```

- `file_name` **不含扩展名**，容器由流决定（写了 `recording.flv` 会得到 `recording.flv.flv`），支持 strftime 占位符；
- `segment` 是**必填**参数，可传 `PySegment`、`{"time": …, "size": …}` 或带这两个属性的对象；
- 带回调的版本用 `download_with_callback`，每段文件写完后回调一次。

> 仓库里自带可直接运行的示例：`crates/stream-gears/examples/` 下的 `login.py`、`download.py`、`upload.py`。

### 接口一览

| 接口 | 说明 |
|---|---|
| `upload` | 上传视频到 B站（`video_path` 传列表） |
| `download` / `download_with_callback` | 下载直播流（带 / 不带分段回调） |
| `login_by_cookies` | 用 cookies.json 登录 |
| `login_by_web_cookies` | 用 Web Cookie 登录 |
| `get_qrcode` + `login_by_qrcode` | 二维码登录 |
| `send_sms` + `login_by_sms` | 短信登录 |
| `login_by_web_qrcode` | Web 二维码登录 |

> 所有接口出错时抛 `stream_gears.StreamGearsError`（`RuntimeError` 的子类），消息里带完整原因链。

---

## 项目结构

```
crates/stream-gears/
├── src/                 # Rust 侧实现
│   ├── lib.rs           # PyO3 模块导出
│   ├── login.rs         # 登录相关接口
│   └── uploader.rs      # 上传相关接口
├── stream_gears/        # Python 包（随 wheel 分发）
│   ├── __init__.py      # 导出 Credit / PySegment 等
│   ├── stream_gears.pyi # 类型提示
│   └── py.typed
├── examples/            # login.py / download.py / upload.py
├── tests/
├── Cargo.toml
└── pyproject.toml
```

---

## 打包与发布

```bash
# 本地构建（产物在 target/wheels/）
maturin build -m crates/stream-gears/Cargo.toml --release
```

> 官方**只往 PyPI 发布源码包（sdist）**，用户 `pip install biliup` 时在本机现场编译（需要 Rust 工具链）。想用预编译产物请走 [npm / 预编译二进制 / Docker](/guide/getting-started/安装部署/Linux.html)。

---

## 常见问题

### `import stream_gears` 失败

原因：扩展未编译或未安装到当前 Python 环境。

```bash
maturin develop -m crates/stream-gears/Cargo.toml
```

### Windows 上编译失败

需要安装 [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，勾选 "Desktop development with C++" 工作负载。

### macOS 上 maturin 找不到 Python

```bash
export PYTHON_SYS_EXECUTABLE=$(which python3)
maturin develop -m crates/stream-gears/Cargo.toml
```

---

## 下一步

- [前端开发（Next.js）](/guide/开发指南/frontend.html)
- [Rust CLI 开发](/guide/开发指南/rust-cli.html)
- [钩子系统（Hooks）](/guide/getting-started/配置/developer-options.html)
