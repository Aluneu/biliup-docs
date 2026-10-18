---
title: 上手
description: biliup 上手指南：安装方式、首次录制投稿路径、常用文档入口。
---

<div class="qs-hero">

<img class="qs-logo" src="/icon.png" alt="biliup" width="48" height="48" />

<h1>上手 biliup</h1>

<p class="qs-sub">直播录制、自动投稿、WebUI 管理。需要 Node.js 18+，两条命令就能起服务。</p>

<div class="qs-cmd">
<pre id="qs-hero-cmd"><code>npm i -g @biliup/cli
biliup server --auth</code></pre>
<button class="qs-copy" onclick="navigator.clipboard.writeText(document.getElementById('qs-hero-cmd').textContent.trim());this.textContent='已复制';setTimeout(()=>this.textContent='复制',1500)">复制</button>
</div>

<p class="qs-hint">也可以不装：<code>npx @biliup/cli server --auth</code>（npx 由 npm 自带，但不会生成 <code>biliup</code> 命令）</p>

<div class="qs-actions">
<a href="#qs-install" class="qs-btn qs-btn-primary">选择安装方式</a>
<a href="/guide/workflow-demo/" class="qs-btn">跑通首次投稿</a>
</div>

</div>

::: warning 开始前先看三条

- **默认只录不传，还可能删录像**：新建主播的上传器是 `Noop`，并且默认带 `rm` 后处理。先按[首次录制并投稿](/guide/workflow-demo/)建好投稿模板，再正式使用。
- **默认只监听本机**：远程访问要用 `biliup server --bind 0.0.0.0 --auth`（不加 `--auth` 会拒绝启动）；公网部署请加反代与 HTTPS，并定期备份数据目录。
- **WebUI 用户名固定为 `biliup`**：`--auth` 后首次访问时设置密码。忘记密码用 `biliup user reset-password <用户名>` 重置，不需要动数据库。

:::

## 安装方式 {#qs-install}

| 平台 | 安装方式 | 说明 |
|---|---|---|
| [Linux](../安装部署/Linux.html) | npm / 预编译二进制 / Docker | 服务器与 NAS 的常规选择 |
| [Windows](../安装部署/windows.html) | npm / 解压即用 / 桌面客户端 | 桌面客户端自带 FFmpeg |
| [macOS](../安装部署/macos.html) | npm / 预编译二进制 | 支持 Apple Silicon |
| [Docker](../安装部署/docker.html) | 官方镜像 | 一行 `docker run` 起服务 |

其他环境：[Termux](../安装部署/termux.html) · [Docker 进阶部署](../安装部署/docker-advanced.html) · [FFmpeg 安装](../安装部署/ffmpeg安装.html)

::: tip 国内网络慢？给 npm 换个镜像源
```bash
npm config set registry https://registry.npmmirror.com
```

只想这一次走镜像，就在安装命令后加 `--registry=https://registry.npmmirror.com`；想换回官方源用 `npm config set registry https://registry.npmjs.org`。`npx` 用的也是同一个源。
:::

## 继续阅读

<div class="qs-links">

<div>
<b>使用</b>
<a href="/guide/configs/config.html">命令行参考</a>
<a href="/guide/webui/usage.html">WebUI 使用指南</a>
<a href="../配置/global-config.html">全局设置</a>
<a href="../配置/live-config.html">各平台设置</a>
</div>

<div>
<b>进阶</b>
<a href="/guide/tutorials/recording-and-masking.html">遮挡与本地合并</a>
<a href="/guide/tutorials/post-recording-render.html">录后合成</a>
<a href="/guide/api/rest-api.html">REST API</a>
<a href="../更多/architecture.html">系统架构</a>
</div>

<div>
<b>帮助</b>
<a href="../帮助/faq.html">常见问题</a>
<a href="../帮助/help.html">帮助与反馈</a>
<a href="../安装部署/production-base.html">生产部署基线</a>
<a href="../帮助/security-ops.html">安全与运维</a>
</div>

</div>

<details class="qs-collapse">
<summary>使用声明</summary>
<ol>
<li><b>仅供个人学习与研究使用</b>，使用本工具所产生的一切后果由使用者自行承担；</li>
<li>严禁录制、上传任何侵犯他人版权或违反平台规定的内容；</li>
<li>本项目不保证稳定性，不提供任何形式的技术支持与担保；</li>
<li>请在使用前仔细阅读并遵守 B 站及相关平台的服务条款与当地法律法规；</li>
<li>仓库 <code>LICENSE</code> 为 MIT，但上游 README 的免责声明中另写有「禁止商业用途」，两者尚未澄清，商用前请以维护者官方说明为准。</li>
</ol>
</details>

<p class="qs-footnote">本文档对应 biliup <b>v1.3.0</b>（开源免费），更新可能不及时，请以 <a href="https://github.com/biliup/biliup">biliup 主仓库</a>实际代码为准 · 桌面客户端在<a href="https://github.com/biliup/biliup-app-new">独立仓库</a>维护</p>
