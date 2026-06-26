# 开发指南

本指南涵盖 biliup 三大层的开发环境搭建与编译运行方式。

---

## 快速导航

biliup 采用混合架构，你可以只搭建需要开发的那一层：

| 开发目标 | 需要搭建的环境 | 参考章节 |
|---|---|---|
| 修改 WebUI 前端页面 | Node.js ≥ 18 | [前端开发](/guide/开发指南/frontend) |
| 修改 Python 脚本/钩子 | Python 3.9+ | [Python 开发](/guide/开发指南/python) |
| 修改核心下载/上传逻辑 | Rust + maturin | [Python 开发](/guide/开发指南/python) |
| 修改 CLI / Web API | Rust (cargo) | [Rust CLI 开发](/guide/开发指南/rust-cli) |
| 修改弹幕功能 | Rust (cargo) | [Rust CLI 开发](/guide/开发指南/rust-cli) |
| 完整本地开发（全栈） | Node.js + Python + Rust | 全部章节 |

---

## 系统依赖

### 必需

| 依赖 | 最低版本 | 安装方式（Linux） |
|---|---|---|
| Node.js | 18 | `nvm install 20` 或 [nodejs.org](https://nodejs.org/) |
| Python | 3.9 | `apt install python3 python3-pip` 或 [python.org](https://python.org/) |
| Rust | 1.75 (stable) | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` |
| maturin | 1.0 | `pip install maturin` |
| npm | 9 | 随 Node.js 自带 |

### 可选（部分功能需要）

| 依赖 | 说明 |
|---|---|
| ffmpeg | 弹幕录制、HLS 流下载、视频转封装 |
| streamlink | 备选下载器 |
| yt-dlp | YouTube 视频/直播下载 |
| Nix | Nix flake 构建（可选） |

---

## 克隆仓库

```bash
git clone https://github.com/biliup/biliup.git
cd biliup
```

---

## 下一步

根据你的开发目标，选择对应章节：

- [前端开发（Next.js）](/guide/开发指南/frontend)
- [Python 开发](/guide/开发指南/python)
- [Rust CLI 开发](/guide/开发指南/rust-cli)
