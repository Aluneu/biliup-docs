---
title: 上手
description: biliup 上手指南：安装方式、首次录制投稿路径、常用文档入口。
---

<div class="qs-hero">

<img class="qs-logo" src="/icon.png" alt="biliup" width="72" height="72" />

<span class="qs-badge">v1.2.6 · 开源免费</span>

<h1>上手 biliup</h1>

<p class="qs-sub">直播录制、自动投稿、WebUI 管理 —— 一个命令行工具，几分钟跑通第一条视频。</p>

<div class="qs-cmd">
<code id="qs-hero-cmd">docker run -d --name biliup --restart unless-stopped -p 19159:19159 -v "$PWD/data":/opt ghcr.io/biliup/caution:latest server --bind 0.0.0.0 --auth</code>
<button class="qs-copy" onclick="navigator.clipboard.writeText(document.getElementById('qs-hero-cmd').textContent.trim());this.textContent='已复制';setTimeout(()=>this.textContent='复制',1500)">复制</button>
</div>

<div class="qs-actions">
<a href="#qs-install" class="qs-btn qs-btn-primary">选择安装方式</a>
<a href="/guide/workflow-demo/" class="qs-btn">跑通首次投稿</a>
</div>

</div>

<details class="qs-collapse">
<summary>⚠️ 首次使用必读（3 条高频踩坑）</summary>
<ol>
<li><b>默认只录不传，且可能删除录像</b>：新建主播默认上传器为 <code>Noop</code>（只录制不上传），且默认带 <code>rm</code> 后处理。直接用默认配置，录完的文件可能被删除，请先跟着<a href="/guide/workflow-demo/">首次录制并投稿</a>建好投稿模板再正式使用。</li>
<li><b>默认只监听本机</b>：<code>biliup server</code> 的 <code>--bind</code> 默认是 <code>127.0.0.1</code>，其他设备访问不了。需要远程访问请用 <code>biliup server --bind 0.0.0.0 --auth</code>（不加 <code>--auth</code> 会拒绝启动）。</li>
<li><b>WebUI 管理员用户名固定为 <code>biliup</code></b>：开启 <code>--auth</code> 后首次访问设置密码，不是在终端生成，也别和 B站投稿账号混淆。忘记密码需重置数据库（会丢失全部配置）。</li>
<li><b>别把 19159 直接暴露公网，并定期备份</b>：至少开启 <code>--auth</code>，有域名建议反代 + HTTPS；B站 Cookie 约 1-3 个月过期（过期后 WebUI 重新扫码即可），配置与 Cookie 都在数据目录，请定期备份。</li>
</ol>
</details>

## 安装方式 {#qs-install}

<div class="qs-grid">

<a href="../安装部署/Linux.html" class="qs-card">
  <span class="qs-icon">🐧</span>
  <b>Linux</b>
  <small>uv 一键安装，可注册 systemd 服务</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../安装部署/windows.html" class="qs-card">
  <span class="qs-icon">🪟</span>
  <b>Windows</b>
  <small>下载 exe 直接运行</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../安装部署/docker.html" class="qs-card">
  <span class="qs-icon">🐳</span>
  <b>Docker</b>
  <small>官方镜像，一键起服务</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../安装部署/macos.html" class="qs-card">
  <span class="qs-icon">🍎</span>
  <b>macOS</b>
  <small>uv 安装，支持 Apple Silicon</small>
  <span class="qs-arrow">→</span>
</a>

</div>

其他环境： [Termux](../安装部署/termux.html) · [Docker 进阶部署](../安装部署/docker-advanced.html) · [FFmpeg 安装](../安装部署/ffmpeg安装.html)

::: tip 下一步：跑通第一次录制与投稿
装好之后，直接跟着[工作原理与快速引导](/guide/workflow-demo/)走一遍「启动 → 登录 → 建投稿模板 → 绑定主播 → 完成录制投稿」。这是唯一一条需要按顺序做完的路径，做完之后 biliup 就能无人值守运行了。

只想手动下一次命令行，不看 WebUI：[命令行参考](/guide/configs/config.html)
:::

## 日常使用

<div class="qs-grid">

<a href="/guide/configs/config.html" class="qs-card">
  <span class="qs-icon">⌨️</span>
  <b>命令行参考</b>
  <small>子命令与参数说明、常用示例</small>
  <span class="qs-arrow">→</span>
</a>

<a href="/guide/webui/usage.html" class="qs-card">
  <span class="qs-icon">🖱️</span>
  <b>WebUI 使用指南</b>
  <small>空间配置、主播管理、投稿模板</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../配置/global-config.html" class="qs-card">
  <span class="qs-icon">⚙️</span>
  <b>全局设置</b>
  <small>下载器、分段、上传与后处理策略</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../配置/live-config.html" class="qs-card">
  <span class="qs-icon">📡</span>
  <b>各平台设置</b>
  <small>斗鱼 / 虎牙 / B站 等平台专属参数</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../平台配置/哔哩哔哩.html" class="qs-card">
  <span class="qs-icon">🎬</span>
  <b>按平台查看</b>
  <small>各平台单独的链接格式与注意事项</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../配置/login.html" class="qs-card">
  <span class="qs-icon">🔐</span>
  <b>登录与凭据</b>
  <small>B站投稿账号与录制平台 Cookie</small>
  <span class="qs-arrow">→</span>
</a>

</div>

## 深入了解

<div class="qs-grid">

<a href="./supported-platforms.html" class="qs-card">
  <span class="qs-icon">📺</span>
  <b>平台总览</b>
  <small>19 个内置平台一览与弹幕支持矩阵</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../更多/architecture.html" class="qs-card">
  <span class="qs-icon">🏗️</span>
  <b>系统架构</b>
  <small>Rust 引擎 + WebUI 的分层结构</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../更多/desktop-app.html" class="qs-card">
  <span class="qs-icon">🖥️</span>
  <b>桌面客户端</b>
  <small>biliup-app：投稿与稿件管理</small>
  <span class="qs-arrow">→</span>
</a>

<a href="/guide/api/rest-api.html" class="qs-card">
  <span class="qs-icon">🔌</span>
  <b>REST API</b>
  <small>接口清单与调用示例</small>
  <span class="qs-arrow">→</span>
</a>

</div>

## 运维与帮助

<div class="qs-grid">

<a href="../帮助/faq.html" class="qs-card">
  <span class="qs-icon">❓</span>
  <b>常见问题</b>
  <small>安装、录制、上传分类解答</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../帮助/help.html" class="qs-card">
  <span class="qs-icon">🆘</span>
  <b>帮助与反馈</b>
  <small>提问技巧、反馈渠道、日志排查</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../安装部署/production-base.html" class="qs-card">
  <span class="qs-icon">🏢</span>
  <b>生产部署基线</b>
  <small>固定版本、健康检查、备份回滚</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../帮助/security-ops.html" class="qs-card">
  <span class="qs-icon">🔒</span>
  <b>安全与运维</b>
  <small>认证边界、网络暴露、备份恢复</small>
  <span class="qs-arrow">→</span>
</a>

</div>

<details class="qs-collapse">
<summary>⚠️ 使用声明</summary>
<ol>
<li><b>仅供个人学习与研究使用</b>，使用本工具所产生的一切后果由使用者自行承担；</li>
<li>严禁录制、上传任何侵犯他人版权或违反平台规定的内容；</li>
<li>本项目不保证稳定性，不提供任何形式的技术支持与担保；</li>
<li>请在使用前仔细阅读并遵守 B 站及相关平台的服务条款与当地法律法规；</li>
<li>仓库 <code>LICENSE</code> 为 MIT，但上游 README 的免责声明中另写有「禁止商业用途」，两者尚未澄清，商用前请以维护者官方说明为准。</li>
</ol>
</details>

<p class="qs-footnote">本文档对应 biliup <b>v1.2.6</b>，更新可能不及时，请以 <a href="https://github.com/biliup/biliup">biliup 主仓库</a>实际代码为准 · 桌面客户端（biliup-app）在<a href="https://github.com/biliup/biliup-app-new">独立仓库</a>维护</p>
