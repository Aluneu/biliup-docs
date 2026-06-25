# BiliuP

高性能直播录制与视频投稿工具。基于 **Rust + Python** 引擎，提供命令行与 WebUI 双重交互方式，支持 20+ 直播平台自动录制，边录边传至 B站。

> [!NOTE]
> 从 v1.0 起，biliup、biliup-rs、biliup-app 已合并为统一主项目。不再需要分别安装多个工具。
> [GitHub 仓库](https://github.com/biliup/biliup)

---

## 项目简介

**BiliuP** 是一个为直播录制和视频平台投稿设计的自动化工具，由开源社区维护。它的核心思路很简单：自动检测开播 → 录制 → 上传 → 投稿，全程无需人工干预。

<div class="vp-card-grid">

<a href="./Linux.html" class="vp-card">
  <span class="card-icon">🐧</span>
  <span class="card-title">Linux 安装</span>
  <span class="card-desc">推荐使用 uv 一键安装，支持 systemd 服务</span>
</a>

<a href="./windows.html" class="vp-card">
  <span class="card-icon">🪟</span>
  <span class="card-title">Windows 安装</span>
  <span class="card-desc">下载 exe 一键运行，开箱即用</span>
</a>

<a href="./docker.html" class="vp-card">
  <span class="card-icon">🐳</span>
  <span class="card-title">Docker 部署</span>
  <span class="card-desc">官方镜像，一行命令拉起</span>
</a>

<a href="./faq.html" class="vp-card">
  <span class="card-icon">❓</span>
  <span class="card-title">常见问题</span>
  <span class="card-desc">安装、录制、上传、WebUI 分类解答</span>
</a>

</div>

---

## 开始之前

> [!WARNING]
> 不建议在已配置好重要开发环境或生产环境的企业服务器上直接运行本项目，建议使用 Docker 或虚拟机隔离。

> [!TIP]
> 本项目功能丰富，有一定学习曲线。我们已通过详尽的文档和 WebUI 引导来降低使用门槛。

> [!TIP]
> B站上传速度主要取决于上行带宽。国内用户使用境外服务器上传通常速度更优（请遵守相关法律法规）。

> [!WARNING]
> 上传日志中如出现 `Retry attempt`，请调整上传并发数，建议从 1 开始逐渐增加。

---

## 快速开始

安装完成后，阅读 [快速入门指南](../quickstart/get-start.html) 开始第一次运行。

<div class="vp-card-grid">

<a href="../quickstart/get-start.html" class="vp-card">
  <span class="card-icon">⚡</span>
  <span class="card-title">快速入门</span>
  <span class="card-desc">从零开始，运行你的第一个录制任务</span>
</a>

<a href="./supportedLivePlatforms.html" class="vp-card">
  <span class="card-icon">📘</span>
  <span class="card-title">支持平台</span>
  <span class="card-desc">查看完整直播平台支持列表</span>
</a>

<a href="../../configs/config.html" class="vp-card">
  <span class="card-icon">⌨️</span>
  <span class="card-title">CLI 命令行</span>
  <span class="card-desc">login / upload / server / download 等命令参考</span>
</a>

<a href="../../Config/GlobalConfig.html" class="vp-card">
  <span class="card-icon">⚙️</span>
  <span class="card-title">配置指南</span>
  <span class="card-desc">全局设置、各平台配置、开发者选项</span>
</a>

</div>

---

## 帮助与反馈

遇到问题？请先查阅 [帮助与反馈](/guide/help.html) 页面，了解如何有效提问。主要反馈渠道：[GitHub Issues](https://github.com/biliup/biliup/issues) · QQ 群 · Telegram 群。

<div class="vp-card-grid">

<a href="../../help.html" class="vp-card">
  <span class="card-icon">🆘</span>
  <span class="card-title">帮助与反馈</span>
  <span class="card-desc">提问技巧、反馈渠道、日志排查指南</span>
</a>

<a href="https://biliup.me" class="vp-card" target="_blank">
  <span class="card-icon">🌐</span>
  <span class="card-title">biliup 社区</span>
  <span class="card-desc">社区论坛、使用心得、脚本分享</span>
</a>

</div>
