---
title: biliup 工作原理与快速引导
---

# biliup 工作原理与快速引导

biliup 把直播和本地视频推送到 B 站等平台，同时提供一个 WebUI 管理界面。下面先说明一次完整的处理流程，再带你跑通第一个录制任务。

## 一次处理经历哪些环节

<WorkflowDiagram />

> 链路随来源切换：直播走「直播链路」，本地文件走「本地链路」；输出目标通常是 B站投稿，也可配置为只录制不上传。

## 录制你的第一个主播

下面以 Docker 部署为例，串起从安装到看到录制文件的完整路径。其他安装方式见[安装部署](/guide/getting-started/安装部署/docker.html)。

1. **启动服务并开启认证**
   运行 `biliup server --auth`。`--auth` 是开关，不接收密码；首次访问 WebUI 时注册管理员账号并设置密码。
   参考：[Docker 安装指引](/guide/getting-started/安装部署/docker.html)

2. **登录 B站账号**
   在 WebUI 中扫码或填入 Cookie 完成登录，登录状态保存在本地。
   参考：[B站账号登录](/guide/getting-started/配置/login.html)

3. **添加主播**
   在 WebUI「录播管理」中填入直播间链接，保存后即开始监控。
   参考：[WebUI 使用指南](/guide/webui/usage.html)

4. **等待录制与上传**
   开播后 biliup 自动录制，是否上传、转码或仅本地保存由全局设置决定。
   参考：[全局配置](/guide/getting-started/配置/global-config.html)

5. **查看结果**
   在 WebUI「录播管理」查看进度与历史，文件默认存于 `recordings/`。

## 下一步

- 了解每个配置项：[全局配置](/guide/getting-started/配置/global-config.html)
- 按平台微调参数：[平台配置](/guide/getting-started/平台配置/哔哩哔哩.html)
- 使用命令行而非界面：[命令行参考](/guide/configs/config.html)
- 遇到问题：[常见问题 Q&A](/guide/getting-started/帮助/faq.html)
