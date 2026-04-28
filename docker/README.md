# FastapiAdmin 部署说明

## 项目结构

```
docker/
├── backend/           # 后端服务配置
│   └── Dockerfile     # 后端Dockerfile
├── nginx/             # Nginx配置
│   ├── nginx.conf     # Nginx配置文件
│   ├── ssl/           # SSL证书目录
│   ├── web/           # 前端静态文件
│   ├── app/           # 小程序静态文件
│   └── docs/          # 文档静态文件
├── mysql/             # MySQL数据目录
│   └── data/          # MySQL数据持久化目录
├── redis/             # Redis数据目录
│   └── data/          # Redis数据持久化目录
├── docker-compose.yaml    # Docker Compose配置文件
├── .env                # 环境变量配置文件
├── .env.example        # 环境变量示例文件
└── README.md           # 部署说明文档
```

## 部署准备

### 系统依赖

- Git
- Docker
- Docker Compose
- Node.js (前端构建需要)
- pnpm (前端构建需要)

### 环境配置

1. **配置环境变量**

   复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：

   ```bash
   cp .env.example .env
   ```

   主要配置项：

   - `MYSQL_ROOT_PASSWORD`: MySQL根密码
   - `MYSQL_DATABASE`: 数据库名
   - `MYSQL_USER`: 数据库用户
   - `MYSQL_PASSWORD`: 数据库密码
   - `REDIS_PASSWORD`: Redis密码
   - `BACKEND_PORT`: 后端服务端口
   - `HTTP_PORT`: HTTP端口
   - `HTTPS_PORT`: HTTPS端口

2. **SSL证书配置** (可选)

   如果需要HTTPS，将SSL证书文件放在 `nginx/ssl/` 目录下：
   - `server.key`: 私钥文件
   - `server.pem`: 证书文件

## 部署流程

### 1. 执行部署脚本

在项目根目录执行部署脚本：

```bash
./deploy.sh
```

部署脚本会自动执行以下步骤：

1. 加载环境变量
2. 检查系统依赖
3. 停止现有容器
4. 更新代码
5. 构建前端（可选）
6. 构建镜像
7. 启动容器
8. 显示日志

### 2. 命令选项

部署脚本支持以下命令选项：

- `./deploy.sh start` - 启动所有容器
- `./deploy.sh stop` - 停止所有容器
- `./deploy.sh restart` - 重启所有容器
- `./deploy.sh logs` - 查看所有容器日志
- `./deploy.sh help` - 显示帮助信息

## 访问信息

部署完成后，可以通过以下地址访问：

- **官网**: https://域名(或ip:端口)
- **前端**: https://域名(或ip:端口)/web
- **小程序**: https://域名(或ip:端口)/app
- **登录信息**: 账号 admin，密码 123456

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

### 清理旧镜像

部署脚本会自动清理72小时前的旧镜像，以节省磁盘空间。

## 常见问题

### 1. 环境变量文件不存在

如果 `.env` 文件不存在，部署脚本会自动从 `.env.example` 创建。

### 2. 前端构建失败

如果服务器资源不足，建议在本地构建前端，然后将 `dist` 目录上传到 `docker/nginx/` 对应目录。

### 3. 容器启动失败

检查容器日志，查看具体错误信息：

```bash
cd docker
docker compose logs [服务名]
```

### 4. 数据库连接失败

确保 `.env` 文件中的数据库配置正确，并且MySQL容器正常运行。

### 5. 端口冲突

如果端口被占用，修改 `.env` 文件中的端口配置。

## 安全建议

1. **修改默认密码**：部署后请修改默认的数据库密码和Redis密码
2. **更新SSL证书**：使用有效的SSL证书，定期更新
3. **限制访问**：配置防火墙，限制不必要的端口访问
4. **定期备份**：定期备份数据库和重要数据

## 版本更新

当项目有新版本时，执行部署脚本即可自动更新：

```bash
./deploy.sh
```

脚本会自动拉取最新代码，构建新镜像，重启容器。
