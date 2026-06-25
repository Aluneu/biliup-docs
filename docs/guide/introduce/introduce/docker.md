# Docker 部署

> [!IMPORTANT]
> - 确保系统已安装 Docker（[官方安装文档](https://docs.docker.com/get-started/get-docker/)）
> - 默认端口为 19159，请开放对应端口（防火墙/安全组/面板）
> - 每个容器对应一个端口，不能多个容器共用同一端口

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
  --password password123
```

参数说明：

| 参数 | 说明 |
|------|------|
| `--name biliup` | 容器名称（可自定义） |
| `--restart unless-stopped` | 意外停止后自动重启 |
| `-p 0.0.0.0:19159:19159` | 端口映射（可改主机端口） |
| `-v /path/to/save_folder:/opt` | 录播文件存储路径挂载 |
| `--password password123` | WebUI 密码（用户名为 `biliup`） |

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

浏览器访问 `http://<你的服务器IP>:19159`，用户名为 `biliup`，密码为 `--password` 设置的值。

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
