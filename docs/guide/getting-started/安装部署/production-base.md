# 生产部署基线

本页提供一套**可供复现、可审核**的长期运行部署基线，适用于 NAS / VPS / 服务器场景。内容基于 biliup **v1.3.0** 编写，命令已对照当前镜像入口（`ENTRYPOINT ["biliup"]`）核对。

::: warning 适用范围与前提
- 本文是**部署基线建议**，不是法律或安全承诺；涉及镜像 digest、SBOM、签名等供应链细节以官方 Release 与镜像仓库为准。
- 公网暴露前，请先阅读[安全与运维手册](/guide/getting-started/帮助/security-ops.html)。
- 升级前务必备份数据（见下文）。
:::

## 1. 固定版本（不要使用 latest）

::: warning 镜像标签
官方镜像 `ghcr.io/biliup/caution` 的发布流程会为 `v*` tag 生成 semver 标签（如 `1.3.0` / `1.3` / `1`），但**标签是否已推送以 registry 实际结果为准**。

生产环境建议用 **digest 固定**，不要依赖 `latest`：
:::

```bash
# 1. 拉取当前 latest，并记下它的 digest
docker pull ghcr.io/biliup/caution:latest

# 2. 取出该镜像的 digest（复制输出中 @sha256: 开头的部分）
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/biliup/caution:latest
# 输出形如：ghcr.io/biliup/caution@sha256:1a2b3c...

# 3. 在 Compose 中改用 digest 固定，避免 latest 静默变更
#    image: ghcr.io/biliup/caution@sha256:1a2b3c...
```

> 💡 CLI 版本号（`biliup --version`）与镜像标签不是一套编号。镜像内包含的 CLI 版本以 `docker run --rm ghcr.io/biliup/caution:latest --version` 为准。

## 2. 基础 Compose（持久化 + 健康检查）

```yaml
# docker-compose.yml —— biliup 生产基线
services:
  biliup:
    # 把 <digest> 换成第 1 步拿到的实际 digest；临时部署可先用 :latest
    image: ghcr.io/biliup/caution@sha256:<digest>
    container_name: biliup
    restart: unless-stopped
    # 镜像 ENTRYPOINT 已是 biliup，这里只追加子命令与参数
    # --bind 0.0.0.0 不可省：CLI 默认只监听 127.0.0.1，容器内不改写端口映射就转发不进来
    command: server --bind 0.0.0.0 --auth --port 19159
    ports:
      - "127.0.0.1:19159:19159"   # 仅监听本机，由反代对外暴露
    volumes:
      - ./data:/opt              # 数据库、凭据、日志与录像都在这一卷里
    environment:
      TZ: Asia/Shanghai
    # 资源限制，避免占用宿主机全部资源
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
    # 健康检查：探测 WebUI 端口
    healthcheck:
      test: ["CMD", "wget", "-q", "-O", "-", "http://127.0.0.1:19159/"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 20s
```

> 💡 `command` 写 `server --bind 0.0.0.0 --auth --port 19159`。**不要**写成 `biliup server ...`（会与镜像入口重复）或只写 `--auth`（缺少 `server` 子命令），也不要漏掉 `--bind 0.0.0.0`（端口映射会失效）。

## 3. 反向代理与 TLS（必做）

不要将 `19159` 直接暴露在公网。用反向代理统一终结 TLS 并加访问控制：

**Caddy 示例：**

```caddyfile
biliup.example.com {
    encode gzip
    reverse_proxy 127.0.0.1:19159
}
```

**Nginx 示例（片段）：**

```nginx
server {
    listen 443 ssl;
    server_name biliup.example.com;
    ssl_certificate     /path/fullchain.pem;
    ssl_certificate_key /path/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:19159;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 4. 数据目录与备份

biliup 的数据相对工作目录（容器内为 `/opt`）组织：

| 数据 | 容器内默认位置 | 是否敏感 | 是否必须备份 |
|---|---|---|---|
| SQLite 数据库 | `/opt/data/data.sqlite3` | 是（含账号/主播/模板） | 是 |
| B站账号凭据 | `/opt/data/<mid>.json`（扫码添加）；命令行登录为 `/opt/cookies.json` | 高敏感 | 是 |
| Fleet 数据（启用时） | `/opt/data/fleet.sqlite3`、`/opt/data/node.json` | 是 | 是 |
| 录像与临时文件 | `/opt`（工作目录） | 可能敏感 | 按业务策略 |

**备份脚本（先停服再拷贝整卷，保证一致性）：**

```bash
#!/bin/bash
set -e
BACKUP_DIR="./backups/biliup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
docker compose stop biliup
cp -a ./data "$BACKUP_DIR/data"
docker compose start biliup
echo "备份完成：$BACKUP_DIR"
```

> 只挂了一个 `./data:/opt` 卷，所以拷贝它就够了：数据库、凭据、日志和录像都在里面。

::: danger 不要使用按扩展名 + 时间无差别删除
旧文档中 `find ... -name "*.flv" -mtime +7 -delete` 会删除所有超过 7 天的 FLV，**不区分是否已上传完成**，可能误删未上传录像。清理前请先 `dry-run` 确认清单，并优先基于应用的上传状态判断。
:::

## 5. 升级与回滚

```bash
# 1) 升级前先按第 4 节备份，并记下当前运行的 digest 以便回滚
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/biliup/caution:latest > image-digest.bak

# 2) 拉取新镜像并取到新的 digest
docker pull ghcr.io/biliup/caution:latest
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/biliup/caution:latest

# 3) 把 compose 中的 image 改成新的 digest 后重启
docker compose up -d

# 4) 验证：健康检查通过、能登录、账号/模板/任务数据仍在
```

**回滚：** 把 `image` 改回第 1 步记录的旧 digest（旧镜像若已删除则重新 pull 该 digest），用同一 `data` 卷重启即可恢复数据。涉及不可逆数据迁移时，请先从备份恢复对应卷。

## 6. 验收清单（部署后）

- [ ] `docker compose ps` 显示 `healthy`
- [ ] 通过反向代理域名 `https://` 可访问，且直接 `http://<IP>:19159` 不可达
- [ ] 开启 `--auth`，首次访问设置 `biliup` 管理员密码
- [ ] 重启容器后账号、主播、模板、历史记录仍存在
- [ ] 已完成一次数据备份并验证可恢复
- [ ] 确认录像保存目录空间监控与清理策略（安全方式）

> 本基线建议在 CI 中加入一次冒烟测试：拉起 → 健康检查 → 登录 → 创建测试配置 → 重启 → 验证持久化。当前文档未内置该测试，欢迎贡献。
