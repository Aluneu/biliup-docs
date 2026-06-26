# Rust CLI 开发

biliup 的核心逻辑（`biliup`、`biliup-cli`、`danmaku`）均使用 **Rust** 编写，提供高性能的直播下载、上传和弹幕录制能力。

---

## 技术栈

| 技术 | 用途 |
|---|---|
| Rust (stable) | 1.75+ |
| cargo | 包管理 + 构建工具 |
| tokio | 异步运行时 |
| reqwest | HTTP 客户端（B站 API 调用） |
| serde | 序列化 / 反序列化 |
| sqlx | SQLite 异步访问 |
| maturin | 编译为 Python 扩展（可选） |

---

## 环境搭建

### 1. 安装 Rust

```bash
# 官方推荐方式（Linux / macOS）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装后重新加载环境变量
source ~/.cargo/env
```

验证：

```bash
rustc --version   # 1.75+
cargo --version   # 1.75+
```

### 2. 安装系统依赖

**Ubuntu / Debian：**

```bash
sudo apt install -y \
  build-essential \
  pkg-config \
  libssl-dev \
  libsqlite3-dev
```

**macOS：**

```bash
brew install openssl sqlite
```

**Windows：**

安装 [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)（"Desktop development with C++" 工作负载）。

---

## 项目结构（Rust）

```
crates/
├── biliup/              # 核心库
│   ├── src/
│   │   ├── lib.rs      # 库入口
│   │   ├── downloader/ # 各平台下载器
│   │   ├── uploader/   # B站上传逻辑
│   │   └── config.rs   # 配置结构定义
│   └── Cargo.toml
├── biliup-cli/          # 命令行 + Web API
│   ├── src/
│   │   ├── main.rs    # CLI 入口
│   │   ├── server.rs   # Web 服务（axum）
│   │   └── api/       # REST API 路由
│   └── Cargo.toml
└── danmaku/            # 弹幕客户端（Rust 重构版）
    ├── src/
    │   └── lib.rs
    └── Cargo.toml
```

---

## 编译与运行

### 开发模式（快速编译）

```bash
# 编译并运行 CLI
cargo run --bin biliup -- --help

# 启动 Web 服务（开发常用）
cargo run --bin biliup -- server --auth
```

### 发布模式（优化编译）

```bash
cargo build --release --bin biliup
./target/release/biliup --version
```

### 只编译特定 crate

```bash
# 只编译核心库
cargo build -p biliup

# 只编译 CLI
cargo build -p biliup-cli
```

---

## Web API 开发

`biliup-cli` 使用 `axum` 框架提供 REST API，源码在 `crates/biliup-cli/src/api/`。

### 添加新接口

1. 在 `api/` 目录新建模块文件
2. 定义路由和处理函数
3. 在 `api/mod.rs` 中注册路由

示例（简化）：

```rust
// crates/biliup-cli/src/api/streamers.rs
use axum::{extract::Json, http::StatusCode};

pub async fn get_streamers() -> Json<Vec<Streamer>> {
    // 从数据库读取主播列表
    let streamers = vec![]; // TODO: 实际实现
    Json(streamers)
}
```

### 本地测试 API

```bash
# 启动服务
cargo run --bin biliup -- server

# 测试接口
curl http://localhost:19159/v1/streamers
```

---

## 弹幕功能开发

弹幕客户端在 `crates/danmaku/`，使用 Rust 重构（原 Python 版见历史版本）。

支持的弹幕协议：

| 平台 | 协议 |
|---|---|
| B站（直播） | WebSocket |
| 斗鱼 | TCP 自定义协议 |
| 虎牙 | WebSocket |
| Twitch | IRC / WebSocket |
| YouTube | 无需弹幕（使用 Chat API） |

添加新的弹幕源：

1. 在 `danmaku/src/platforms/` 实现对应 trait
2. 在 `danmaku/src/lib.rs` 中注册平台

---

## 与 Python 层桥接

Rust 代码通过 `pyo3` + `maturin` 暴露给 Python：

```rust
// crates/stream-gears/src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn start_download(url: String) -> PyResult<()> {
    // Rust 实现
    Ok(())
}

#[pymodule]
fn stream_gears(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_download))?;
    Ok(())
}
```

编译为 Python 扩展：

```bash
maturin develop
```

---

## 日志

Rust 后端使用 `tracing` 库输出日志，可通过环境变量控制级别：

```bash
# 输出调试日志
RUST_LOG=debug cargo run --bin biliup -- server

# 只输出 biliup 相关的日志
RUST_LOG=biliup=debug,info cargo run --bin biliup -- server
```

---

## 常见问题

### 编译慢

Rust 首次编译较慢（需编译所有依赖），后续增量编译会快很多。

加速技巧：

```bash
# 使用更快的 linker（Linux）
# 安装 mold，然后在 ~/.cargo/config.toml 中配置

# 并行编译（默认已启用）
cargo build -j $(nproc)
```

### Windows 上链接失败

原因：缺少 C++ 构建工具。

解决：安装 [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)。

### `cargo run` 时提示"地址已被占用"

原因：19159 端口已有 biliup 实例在运行。

解决：

```bash
# 找到并停止正在运行的进程
# Linux/macOS
lsof -i :19159
kill <PID>

# Windows
netstat -ano | findstr 19159
taskkill /PID <PID> /F
```

---

## 下一步

- [前端开发（Next.js）](/guide/开发指南/frontend)
- [Python 开发](/guide/开发指南/python)
- [系统架构](/guide/introduce/introduce/architecture)
- [REST API 文档](/guide/api/rest-api)
