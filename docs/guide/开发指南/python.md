# Python 开发

biliup 的 Python 包提供投稿库（`bili_webup`）和 CLI 最小入口（`biliup.__main__`），同时 `stream-gears` 作为 Rust 核心的 Python 绑定，是 Python 层与 Rust 层之间的桥梁。

---

## 技术栈

| 技术 | 用途 |
|---|---|
| Python | 3.9+ |
| maturin | Rust/Python 桥接，编译 `stream-gears` 扩展 |
| bili_webup | B站投稿库（可被外部项目 import） |
| bili_webup_sync | 同步版投稿库 |
| stream-gears | Rust 核心的 Python 绑定（由 maturin 编译） |

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
```

验证：

```bash
maturin --version  # >= 1.0
```

### 3. 安装 Python 依赖

```bash
cd biliup/          # Python 包在 biliup/ 目录
pip install -e ".[dev]"
```

---

## 编译 Rust 扩展（stream-gears）

Python 包依赖 `stream-gears`（Rust 编译的 Python 扩展模块），需要先编译：

```bash
cd biliup           # 仓库根目录

# 开发模式：编译并安装到当前 Python 环境
maturin develop

# 如需每次修改 Rust 代码后自动重新编译
maturin develop --cargo-extra-args="-Z unstable-options"
```

验证安装：

```bash
python -c "import stream_gears; print('OK')"
```

---

## 运行 biliup（Python 入口）

```bash
# 方式一：作为模块运行
python -m biliup

# 方式二：直接调用 CLI（如已安装 biliup CLI）
biliup --help
```

---

## 项目结构（Python）

```
biliup/                    # Python 包根目录
├── biliup/
│   ├── __init__.py
│   ├── __main__.py      # python -m biliup 入口
│   ├── bili_webup.py    # B站投稿库
│   ├── bili_webup_sync.py # 同步版投稿库
│   └── ...
├── crates/
│   └── stream-gears/    # Rust 扩展（由 maturin 编译为 .pyd/.so）
├── pyproject.toml       # Python 包配置
└── setup.py             # 兼容旧版 pip 安装
```

---

## 开发技巧

### 修改投稿逻辑

编辑 `biliup/bili_webup.py`，然后直接运行测试（无需重新编译）：

```bash
python -m biliup upload test.mp4
```

### 修改下载逻辑（Rust 部分）

如下载器核心在 Rust 的 `crates/biliup/` 中，修改后需重新编译：

```bash
maturin develop
```

### 使用虚拟环境

推荐始终在虚拟环境中开发：

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

---

## 打包与发布

### 构建 wheel 包

```bash
maturin build --release
# 产物在 target/wheels/ 目录
```

### 发布到 PyPI

```bash
maturin publish
```

---

## 常见问题

### `import stream_gears` 失败

原因：`stream-gears` 未编译或未安装到当前 Python 环境。

解决：

```bash
maturin develop
```

### Windows 上编译失败

原因：Windows 需要安装 [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)。

解决：安装 "Desktop development with C++" 工作负载。

### macOS 上 maturin 找不到 Python

原因：Python 路径未正确设置。

解决：

```bash
export PYTHON_SYS_EXECUTABLE=$(which python3)
maturin develop
```

---

## 下一步

- [前端开发（Next.js）](/guide/开发指南/frontend)
- [Rust CLI 开发](/guide/开发指南/rust-cli)
- [钩子系统（Hooks）](/guide/introduce/Config/developerOptions)
