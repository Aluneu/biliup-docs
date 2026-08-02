---
title: 上手
---

<div class="qs-hero">

<img class="qs-logo" src="/icon.png" alt="biliup" width="72" height="72" />

<span class="qs-badge">v1.2.2 · 开源免费</span>

<h1>上手 biliup</h1>

<p class="qs-sub">直播录制、自动投稿、WebUI 管理 —— 一个命令行工具，几分钟跑通第一条视频。</p>

<div class="qs-cmd">
<code id="qs-hero-cmd">docker run -d --name biliup --restart unless-stopped -p 19159:19159 -v "$PWD/data":/opt ghcr.io/biliup/caution:latest server --auth</code>
<button class="qs-copy" onclick="navigator.clipboard.writeText(document.getElementById('qs-hero-cmd').textContent.trim());this.textContent='已复制';setTimeout(()=>this.textContent='复制',1500)">复制</button>
</div>

<div class="qs-actions">
<a href="#qs-install" class="qs-btn qs-btn-primary">安装指南</a>
</div>

<div class="qs-metrics">
<div class="qs-metric"><b>20+</b><span>直播平台</span></div>
<div class="qs-metric"><b>7×24</b><span>无人值守</span></div>
<div class="qs-metric"><b>Rust</b><span>核心引擎</span></div>
<div class="qs-metric"><b>MIT</b><span>开源许可</span></div>
</div>

</div>

<details class="qs-collapse">
<summary>⚠️ 首次使用必读（3 条高频踩坑）</summary>
<ol>
<li><b>默认只录不传，且可能删除录像</b>：新建主播默认上传器为 <code>Noop</code>（只录制不上传），且默认带 <code>rm</code> 后处理。直接用默认配置，录完的文件可能被删除，请先跟着<a href="/guide/workflow-demo/">首次录制并投稿</a>建好投稿模板再正式使用。</li>
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

## 从零到第一条视频

<div class="qs-grid qs-steps-grid">

<a href="#qs-install" class="qs-card qs-step-card">
  <span class="qs-step-num">1</span>
  <b>安装 biliup</b>
  <small>选一种方式装好，开启 <code>--auth</code> 进入 WebUI</small>
</a>

<a href="/guide/workflow-demo/#第一次成功-从录制到投稿" class="qs-card qs-step-card">
  <span class="qs-step-num">2</span>
  <b>跑通一次录制</b>
  <small>跟着端到端流程，从添加主播到第一条投稿</small>
</a>

<a href="../配置/global-config.html" class="qs-card qs-step-card">
  <span class="qs-step-num">3</span>
  <b>按需配置</b>
  <small>平台参数、上传策略与后处理，逐项调优</small>
</a>

<a href="https://biliup.me" class="qs-card qs-step-card" target="_blank" rel="noopener">
  <span class="qs-step-num">4</span>
  <b>加入社区</b>
  <small>项目主页、文档与下载入口，遇到问题来这里</small>
  <span class="qs-arrow">↗</span>
</a>

</div>

## 常用入口

<div class="qs-grid">

<a href="../安装部署/docker.html" class="qs-card">
  <span class="qs-icon">🐳</span>
  <b>Docker 一键部署</b>
  <small>官方镜像，一条命令拉起服务</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../../webui/usage.html" class="qs-card">
  <span class="qs-icon">🖱️</span>
  <b>WebUI 使用指南</b>
  <small>空间配置、任务平台、直播历史</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../配置/global-config.html" class="qs-card">
  <span class="qs-icon">⚙️</span>
  <b>全局配置</b>
  <small>平台参数、上传策略与后处理</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../配置/login.html" class="qs-card">
  <span class="qs-icon">🔐</span>
  <b>B站登录方式</b>
  <small>扫码 / 短信 / 密码 / Cookie</small>
  <span class="qs-arrow">→</span>
</a>

</div>

## 了解更多

<div class="qs-grid">

<a href="./supported-platforms.html" class="qs-card">
  <span class="qs-icon">📡</span>
  <b>支持平台</b>
  <small>20+ 直播平台支持列表</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../更多/architecture.html" class="qs-card">
  <span class="qs-icon">🏗️</span>
  <b>系统架构</b>
  <small>Rust 引擎 + WebUI + 桌面端</small>
  <span class="qs-arrow">→</span>
</a>

<a href="../更多/desktop-app.html" class="qs-card">
  <span class="qs-icon">🖥️</span>
  <b>桌面应用 biliup-app</b>
  <small>Tauri 独立图形客户端</small>
  <span class="qs-arrow">→</span>
</a>

</div>

## 帮助与运维

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
<summary>⚠️ 免责声明</summary>
<ol>
<li><b>仅供个人学习与研究使用</b>，使用本工具所产生的一切后果由使用者自行承担；</li>
<li>❌ 禁止用于任何商业用途；严禁录制、上传任何侵犯他人版权或违反平台规定的内容；</li>
<li>❌ 本项目不保证稳定性，不提供任何形式的技术支持与担保；</li>
<li>请在使用前仔细阅读并遵守 B 站及相关平台的服务条款与当地法律法规。</li>
</ol>
</details>

<p class="qs-footnote">本文档更新可能不及时，请以 <a href="https://github.com/biliup/biliup">biliup 主仓库</a> 实际代码为准 · 主项目已合并 Rust 引擎，WebUI / 桌面端（biliup-app）作为<a href="https://github.com/biliup/biliup-app-new">独立仓库</a>维护</p>
