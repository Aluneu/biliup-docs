---
description: 在 Docker 中部署 biliup WebUI：正确的启动命令（server --auth）、端口映射、持久化卷与认证开启，基于 v1.2.2 核对。
---

# Docker 部署

::: info
- 确保系统已安装 Docker（[官方安装文档](https://docs.docker.com/get-started/get-docker/)）
- 默认端口为 19159，请开放对应端口（防火墙/安全组/面板）
- 每个容器对应一个端口，不能多个容器共用同一端口
:::


---

## 拉取镜像

```bash
docker pull ghcr.io/biliup/caution:latest
```

---

## 创建容器

```bash
docker run -d \
  --name biliup \
  --restart unless-stopped \
  -p 0.0.0.0:19159:19159 \
  -v /path/to/save_folder:/opt \
  ghcr.io/biliup/caution:latest \
  server --auth
```

::: warning
镜像已将 `biliup` 设为入口命令（ENTRYPOINT），因此镜像名之后**只需追加子命令与参数**，不要重复写 `biliup`。正确形式是 `... caution:latest server --auth`；写成 `... caution:latest --auth`（缺少 `server`）或 `command: biliup server --auth`（重复入口）都会导致启动失败。
:::

参数说明：

| 参数 | 说明 |
|------|------|
| `--name biliup` | 容器名称（可自定义） |
| `--restart unless-stopped` | 意外停止后自动重启 |
| `-p 0.0.0.0:19159:19159` | 端口映射（可改主机端口） |
| `-v /path/to/save_folder:/opt` | 录播文件存储路径挂载 |
| `server` | 启动 WebUI 服务的子命令（镜像已含 `biliup` 入口，此处只需子命令） |
| `--auth` | 开启 WebUI 登录认证（首次访问时用户名为固定 `biliup`，请设置管理员密码） |

---

## 验证启动

```bash
docker ps -a
```

输出示例：
```
CONTAINER ID   IMAGE                          STATUS        PORTS                      NAMES
xxxxxxxxxxxx   ghcr.io/biliup/caution:latest  Up 4 seconds  0.0.0.0:19159->19159/tcp   biliup
```

---

## 访问 WebUI

浏览器访问 `http://<你的服务器IP>:19159`，首次访问会进入登录页。管理员用户名固定为 `biliup`，请设置密码；之后使用同一用户名（`biliup`）与密码登录。

::: warning
WebUI 管理员账号（固定用户名 `biliup`）与用于投稿的 B站账号（通过扫码 / Cookie 添加）是**两套不同的身份**，请勿混淆。忘记管理员密码时只能重置数据库中的用户，详见[WebUI 使用指南 - 忘记密码](/guide/webui/usage.html#忘记-webui-密码)。
:::

---

## 容器管理

```bash
# 停止
docker stop biliup

# 重启
docker restart biliup

# 删除
docker rm -f biliup

# 查看日志
docker logs biliup

# 进入容器
docker exec -it biliup /bin/sh
```

---

## 更新镜像

```bash
docker pull ghcr.io/biliup/caution:latest
docker stop biliup
docker rm biliup
# 重新执行 docker run 命令（数据在挂载目录中不变）
```
