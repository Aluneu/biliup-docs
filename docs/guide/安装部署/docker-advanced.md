# Docker 进阶部署指南

本文档面向需要在生产环境部署 biliup 的用户，覆盖 `docker-compose` 完整配置、数据持久化、反向代理、HTTPS 等进阶场景。

---

## 基础回顾

如果你还未完成基础部署，请先查看[Docker 安装指引](/guide/introduce/introduce/docker.html)。

最简启动命令：

```bash
docker run -d \
  --name biliup \
  -p 19159:19159 \
  -v $(pwd)/data:/app/data \
  biliup/biliup:latest
```

---

## docker-compose 完整配置

使用 `docker-compose.yml` 管理容器是推荐方式，便于维护、升级和备份。

### 最小可用配置

```yaml
# docker-compose.yml
version: "3.8"

services:
  biliup:
    image: biliup/biliup:latest
    container_name: biliup
    restart: unless-stopped
    ports:
      - "19159:19159"
    volumes:
      - ./data:/app/data
    command: >
      biliup server
      --auth admin:your_password_here
      --port 19159
```

启动：`docker compose up -d`

### 生产环境推荐配置

```yaml
# docker-compose.yml
version: "3.8"

services:
  biliup:
    image: biliup/biliup:latest
    container_name: biliup
    restart: unless-stopped
    # 资源限制（防止 OOM）
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 512M
    ports:
      - "127.0.0.1:19159:19159"  # 仅绑定本地，由反向代理转发
    volumes:
      # 数据持久化（数据库、配置、录制文件）
      - ./data:/app/data
      # 如需自定义 WebUI，挂载自定义前端目录
      # - ./custom-ui:/app/custom-ui
    environment:
      # 时区设置（录制文件名时间戳用）
      - TZ=Asia/Shanghai
    command: >
      biliup server
      --auth admin:your_strong_password
      --port 19159
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - biliup-net

  # 可选：Nginx 反向代理（见下方反向代理章节）
  # nginx:
  #   image: nginx:alpine
  #   ...

networks:
  biliup-net:
    driver: bridge
```

---

## 数据持久化详解

### 目录结构

`./data` 目录挂载到容器内的 `/app/data`，包含：

```
data/
├── data.sqlite3        # WebUI 配置数据库（账号、模板、主播配置）
├── log/                # 运行日志
├── recordings/         # 录制文件存放目录（默认）
└── cookies/           # 存放 B站等平台的 Cookie 文件
```

### 重要提醒

> ⚠️ **必须挂载 `/app/data` 卷**，否则容器重启后所有配置（账号登录状态、主播列表、投稿模板）会全部丢失。

### 自定义录制文件存放路径

默认录制文件保存在容器内的 `/app/data/recordings`，映射到宿主机：

```yaml
volumes:
  # 将录制文件存放到宿主机的指定路径
  - /mnt/large-disk/biliup-data:/app/data
```

或在「空间配置 → 全局设置」中修改录制文件保存路径（需挂载对应路径）。

---

## 环境变量参考

| 环境变量 | 说明 | 默认值 |
|---|---|---|
| `TZ` | 时区（影响文件名时间戳） | `UTC` |
| `BILIUP_AUTH` | 认证凭据（格式：`user:pass`） | - |
| `BILIUP_PORT` | 服务端口 | `19159` |
| `BILIUP_CONFIG` | 自定义配置文件路径 | - |

> 💡 推荐使用启动参数而非环境变量配置认证信息，避免环境变量泄露风险。

---

## 反向代理 + HTTPS

生产环境建议通过反向代理（Nginx / Caddy）访问 WebUI，而非直接暴露端口。

### Nginx 配置示例

```nginx
# /etc/nginx/sites-available/biliup
server {
    listen 80;
    server_name biliup.yourdomain.com;

    # 先配置 HTTP 以便 Certbot 验证，之后再开启 HTTPS
    location / {
        proxy_pass http://127.0.0.1:19159;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持（日志查看器需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 开启 HTTPS（Certbot）

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 自动配置 HTTPS
sudo certbot --nginx -d biliup.yourdomain.com

# 设置自动续期
sudo systemctl enable certbot.timer
```

### Caddy 配置示例（推荐，自动 HTTPS）

```caddyfile
# Caddyfile
biliup.yourdomain.com {
    reverse_proxy 127.0.0.1:19159
}
```

Caddy 会自动申请和续期 Let's Encrypt 证书，无需额外配置。

---

## 安全加固

### 1. 设置强密码

```bash
# 生成随机强密码
openssl rand -base64 16
# 在 --auth 参数中使用
```

### 2. 不要将端口直接暴露到公网

在 `docker-compose.yml` 中将端口绑定改为 `127.0.0.1:19159:19159`，仅允许本地访问，再通过反向代理转发。

### 3. 定期备份数据

```bash
# 备份脚本示例（可加入 crontab）
#!/bin/bash
BACKUP_DIR=/opt/backups/biliup
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/biliup-data-$(date +%Y%m%d).tar.gz /opt/biliup/data
# 保留最近 7 天的备份
find $BACKUP_DIR -name "biliup-data-*.tar.gz" -mtime +7 -delete
```

### 4. 限制容器资源

见上方「生产环境推荐配置」中的 `deploy.resources` 配置，防止录制任务占用过多资源影响宿主机。

---

## 升级 biliup 容器

### 方法一：使用 docker-compose（推荐）

```bash
# 拉取最新镜像
docker compose pull

# 重新创建容器（配置和数据卷不变）
docker compose up -d --force-recreate
```

### 方法二：手动操作

```bash
# 拉取最新镜像
docker pull biliup/biliup:latest

# 停止并删除旧容器（数据卷不受影响）
docker stop biliup
docker rm biliup

# 使用相同参数重新创建容器
docker run -d \
  --name biliup \
  -p 19159:19159 \
  -v $(pwd)/data:/app/data \
  biliup/biliup:latest \
  biliup server --auth admin:password --port 19159
```

> ⚠️ 升级前建议备份 `./data` 目录，尤其是跨大版本升级时（如 0.4.x → 1.x）。

---

## 常见问题

### Docker 容器数据丢失

确认 `docker-compose.yml` 中已正确配置 `volumes` 挂载。检查：

```bash
# 查看容器挂载情况
docker inspect biliup | grep -A 10 "Mounts"
```

### 录制文件占用过多磁盘空间

biliup 不会自动清理已上传的视频文件。建议：

1. 在「空间配置 → 全局设置」中启用「上传后删除本地文件」（如已上传完成）
2. 或设置定期清理脚本：

```bash
# 删除 7 天前已上传完成的录制文件（谨慎使用）
find /path/to/recordings -name "*.flv" -mtime +7 -delete
```

### 端口冲突

如果 `19159` 端口已被占用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "19160:19159"  # 宿主机 19160 → 容器 19159
```

同时记得在 `--port` 参数中保持一致（容器内部端口），或只改宿主机映射端口。

### 宿主机时区不正确导致文件名时间异常

在 `docker-compose.yml` 中添加时区环境变量：

```yaml
environment:
  - TZ=Asia/Shanghai
```

---

## 下一步

- 了解[WebUI 完整使用指南](/guide/webui/webui-guide.html)
- 了解[全局配置参数](/guide/introduce/Config/GlobalConfig.html)
- 遇到问题时查看[常见问题 Q&A](/guide/introduce/introduce/faq.html)
