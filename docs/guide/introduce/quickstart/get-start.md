# 快速入门

> [!TIP]
> 此页面帮助你在安装完成后快速完成首次运行。

---

## 项目结构

biliup 会在运行目录下自动创建以下结构：

```
📁 项目根目录
├── 📁 data/                # 核心数据存储目录
│   ├── 📜 data.sqlite3      # 配置数据库
│   └── 📜 xxx.json          # 账号敏感信息（请勿外泄）
├── 📁 cover/               # 直播间封面缓存（use_live_cover）
├── 📜 download.log          # 下载日志
├── 📜 ds_update.log         # 运行日志（报错排查）
├── 📜 upload.log            # 上传日志（失败排查）
└── 📜 xxx.flv.part          # 正在录制的文件
```

---

## 启动 WebUI

根据安装方式选择对应的启动命令：

### Linux / macOS

```bash
# 进入要保存录播文件的目录
cd /home

# 启动 WebUI（开启密码认证）
biliup server --auth

# 启动后会显示访问地址
#  * Running on http://127.0.0.1:19159
#  * Running on http://172.19.0.1:19159
```

### Windows (.exe)

```powershell
# 进入 .exe 所在目录
cd D:\biliup

# 启动 WebUI
.\biliup.exe server --auth
```

### Docker

```bash
docker run -d \
  --name biliup \
  --restart unless-stopped \
  -p 0.0.0.0:19159:19159 \
  -v /path/to/save_folder:/opt \
  ghcr.io/biliup/caution:latest \
  --password password123
```

---

## 访问 WebUI

在浏览器中访问 `http://<服务器IP>:19159`（本地访问 `http://localhost:19159`）。

如果有密码，用户名为 `biliup`，密码为启动时设定的值。

---

## 首次配置

### 1. 登录B站

进入「投稿管理」→ 点击左上角图标 → 选择「新增」→ 「扫码登录」，用哔哩哔哩 APP 扫码登录。

登录后刷新页面，确认能看到账号信息即可。

### 2. 添加直播源

进入「录播管理」→「直播管理」→ 添加房间链接：

- B站：`https://live.bilibili.com/1024`
- 斗鱼：`https://www.douyu.com/123456`
- 虎牙：`https://www.huya.com/123456`
- 更多平台见 [支持平台列表](../introduce/supportedLivePlatforms)

### 3. 配置上传（可选）

进入「空间配置」→ 在模板中将「上传插件」从 `Noop` 改为 `biliup-rs`，保存即可启用自动上传。

---

## 哔哩哔哩录制特别说明

B站的 APEX 等分区使用 HLS 流，需要以下额外配置：

1. 「空间配置」→「全局设置」→ 下载器改为 `streamlink`
2. 「空间配置」→「各平台设置」→「哔哩哔哩」：
   - 选择你的 B站 Cookie 文件
   - 将直播流协议改为 `hls_fmp4`
3. 保存后重启 biliup

### 境外服务器录制B站

需要自备国内机器（如腾讯云/阿里云轻量），反代 `https://api.live.bilibili.com` 域名，将反代地址填入「各平台设置」→「哔哩哔哩」→「直播主要API」即可。
