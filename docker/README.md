# FastapiAdmin 部署说明

## 项目结构

```
docker/
├── backend/                # 后端服务配置
│   └── Dockerfile          # 后端 Dockerfile（多阶段构建）
├── nginx/                  # Nginx 配置
│   ├── nginx.conf          # Nginx 配置文件
│   ├── ssl/                # SSL 证书目录（已被 gitignore 保护，需自行放置）
│   │   └── server.key      # SSL 私钥文件
│   │   └── server.pem      # SSL 证书文件
│   ├── web/                # 前端静态文件（Web）
│   ├── app/                # 前端静态文件（小程序 H5）[已禁用：不开源]
│   └── docs/               # 前端静态文件（官网文档）[已禁用：不开源]
├── mysql/                  # MySQL 数据目录
│   └── data/               # MySQL 数据持久化目录
├── redis/                  # Redis 数据目录
│   └── data/               # Redis 数据持久化目录
├── docker-compose.yaml     # Docker Compose 编排文件
├── .env                    # 环境变量配置文件（已加入 .gitignore，不提交）
├── .env.example            # 环境变量示例文件（使用占位值）
├── env.sh                  # 环境变量加载脚本（供其他命令使用）
└── README.md               # 本部署说明文档
```

## 部署准备

### 系统依赖

- Git
- Docker (>= 20.10)
- Docker Compose (v2，Docker 内置的 `docker compose` 命令)
- Node.js (前端构建需要，可选)
- pnpm (前端构建需要，可选)

### 环境配置

1. **配置环境变量**

   复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：

   ```bash
   cp .env.example .env
   chmod 600 .env  # 限制权限，防止其他用户读取密码
   ```

   主要配置项：

   - `MYSQL_ROOT_PASSWORD`: MySQL 根密码
   - `MYSQL_DATABASE`: 数据库名
   - `MYSQL_USER`: 数据库用户
   - `MYSQL_PASSWORD`: 数据库密码
   - `REDIS_PASSWORD`: Redis 密码
   - `BACKEND_PORT`: 后端服务端口
   - `HTTP_PORT`: HTTP 端口
   - `HTTPS_PORT`: HTTPS 端口

2. **SSL 证书配置** (可选，但生产环境必须)

   将 SSL 证书文件放在 `nginx/ssl/` 目录下：

   ```bash
   # 自签名证书（测试用）：
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout docker/nginx/ssl/server.key \
     -out docker/nginx/ssl/server.pem \
     -subj "/CN=service.fastapiadmin.com"

   # 生产环境请使用正规 CA 签发的证书
   ```

## 部署流程

### 1. 使用部署脚本（推荐）

在项目根目录执行：

```bash
./deploy.sh
```

部署脚本会自动执行以下步骤：

1. 检查脚本权限
2. 加载环境变量
3. 检查系统依赖并创建必要目录
4. 停止现有容器
5. 更新代码
6. 构建前端（可选，默认跳过）
7. 构建 Docker 镜像
8. 启动容器
9. 验证部署
10. 显示日志
11. 清理旧资源（悬空镜像 + 构建缓存）

### 2. 命令选项

| 命令 | 说明 |
|------|------|
| `./deploy.sh` | 完整部署流程 |
| `./deploy.sh start` | 启动所有容器 |
| `./deploy.sh stop` | 停止所有容器 |
| `./deploy.sh restart` | 重启所有容器 |
| `./deploy.sh logs` | 查看所有容器日志 |
| `./deploy.sh verify` | 验证部署状态 |
| `./deploy.sh clean` | 清理旧镜像 |
| `./deploy.sh --build-frontend` | 完整部署并构建前端 |
| `./deploy.sh --skip-frontend` | 完整部署并跳过前端构建（默认） |

### 3. 手动操作（不通过脚本）

```bash
cd docker

# 启动所有服务
docker compose --env-file .env up -d

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f [service_name]

# 停止服务
docker compose down

# 仅重建某个服务
docker compose up -d --no-deps --build [service_name]
```

## 容器资源限制

为提高部署稳定性，各服务都设置了资源限制：

| 服务 | CPU 限制 | 内存限制 | 内存预留 |
|------|----------|----------|----------|
| MySQL | 无限制 | 1 GB | 256 MB |
| Redis | 无限制 | 512 MB | 128 MB |
| Backend | 1 核 | 1 GB | 256 MB |
| Nginx | 0.5 核 | 256 MB | 64 MB |

如需调整，修改 `docker-compose.yaml` 中对应服务的 `deploy.resources` 字段。

## 访问信息

部署完成后，可以通过以下地址访问：

- **官网**: https://域名(或 ip)/docs [已禁用：不开源]
- **前端**: https://域名(或 ip)/web
- **小程序**: https://域名(或 ip)/app [已禁用：不开源]
- **API 文档**: https://域名(或 ip)/api/v1/docs
- **登录信息**: 账号 admin，密码 123456

> **注意**: `docs` 和 `app` 已禁用开源部署，如需使用请取消相关配置注释。

## 日志管理

### 查看容器日志

```bash
# 查看所有容器日志
./deploy.sh logs

# 查看实时日志
cd docker
docker compose logs -f [服务名]

# 服务名：backend, nginx, mysql, redis
```

### 日志轮转

各容器的日志会被 Docker 自动轮转，限制为每个容器最多保留 3 个日志文件，每个最大 10MB。
如有需要，可在 `docker-compose.yaml` 中调整 `logging` 配置。

## 常见问题

### 1. 环境变量文件不存在

如果 `.env` 文件不存在，部署脚本会自动从 `.env.example` 创建。你也可以手动复制：

```bash
cp docker/.env.example docker/.env
```

### 2. 前端构建失败

如果服务器资源不足，建议在本地构建前端，然后将 `dist` 目录上传到 `docker/nginx/` 对应目录。

### 3. 容器启动失败

检查容器日志，查看具体错误信息：

```bash
cd docker
docker compose logs [服务名]
```

### 4. 数据库连接失败

确保 `.env` 文件中的数据库配置正确，并且 MySQL 容器正常运行：

```bash
docker compose ps mysql
docker compose logs mysql
```

### 5. 端口冲突

如果端口被占用，修改 `.env` 文件中的端口配置，然后重新部署。

### 6. MySQL 数据目录权限问题

如果 MySQL 启动报权限错误，检查 `mysql/data` 目录权限：

```bash
sudo chown -R 999:999 docker/mysql/data
sudo chmod -R 755 docker/mysql/data
```

## 安全建议

1. **修改默认密码**：部署后请修改 `docker/.env` 中的密码
2. **保护 `.env` 文件**：本部署已将 `docker/.env` 加入 `.gitignore`，请勿手动提交
3. **使用正规 SSL 证书**：生产中不要使用自签名证书
4. **限制端口访问**：通过防火墙只开放 80/443 端口
5. **及时更新**：定期执行部署脚本获取最新版本

## 版本更新

当项目有新版本时，执行部署脚本即可自动更新：

```bash
./deploy.sh
```

脚本会自动：
1. 拉取最新代码
2. 构建新镜像
3. 重启容器
