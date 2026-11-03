---
layout: home

title: biliup
titleTemplate: 高性能直播录制与视频投稿工具

hero:
  name: biliup
  text: 高性能直播录制与视频投稿工具
  tagline: CLI + WebUI 交互，支持 19 个直播平台自动录制与 B站投稿
  actions:
    - theme: brand
      text: 开始安装
      link: /guide/getting-started/上手/
    - theme: alt
      text: GitHub
      link: https://github.com/biliup/biliup
  image:
    src: /home.webp
    alt: biliup Logo

features:
  - icon: 🎬
    title: 直播录制
    details: 自动检测开播并录制，内置 19 个直播平台解析。斗鱼、虎牙、B站、抖音、Twitch、YouTube 全覆盖，未匹配的地址交给通用适配器处理。
  - icon: ⚡
    title: 高性能架构
    details: 核心基于 Rust 构建，异步 IO 多线程，CPU 和内存占用低。具体并发数取决于直播码率与硬件，请以实际压测为准。
  - icon: 🚀
    title: 边录边传
    details: 流式视频上传，录制过程中实时上传。默认上传器为 `Noop`（仅录制），需在投稿模板中选择 `biliup-rs` 才会自动投稿。
  - icon: 🖧
    title: 多机 Fleet
    details: 控制面统一分派房间，节点凭票据加入，配置下发、标签与告警都在控制面。默认就已开启，单机使用不受影响。
  - icon: ✂️
    title: 回看与切片
    details: 按场次回看录像，关键帧快速剪不转码，精确剪重编码为 MP4；切片按模板直接投稿，还能让大模型先挑高光候选。
  - icon: 🔐
    title: 多用户权限
    details: 超级管理员 / 操作员 / 只读观察者三级权限，钩子与 ffmpeg 参数只有超级管理员能改。
  - icon: 📦
    title: 自托管须知
    details: 自托管工具，需自行提供设备、存储、网络与平台账号。社区项目无 SLA，请遵守各平台服务条款。
  - icon: 🎨
    title: WebUI 交互
    details: 内置 Web 管理界面，浏览器中配置录制参数、管理主播、查看状态，无需手动编辑配置文件。
  - icon: 📤
    title: B站投稿
    details: 支持多p上传、线路切换、大文件上传（最高 32G）、多账号管理，自动选择最优线路。
  - icon: 🐳
    title: 灵活部署
    details: npm 一行安装、预编译二进制解压即用，官方 Docker 镜像一键部署，另有 Windows 桌面客户端。
  - icon: 🔓
    title: 开源免费
    details: 基于 MIT 协议完全开源，无付费墙、无云端绑定。代码与问题追踪均在 GitHub，欢迎贡献。
---
