# FastapiAdmin 部署文档

本文档详细描述了 FastapiAdmin 项目的部署流程、环境要求、配置说明及常见问题排查方法。

## 项目简介

FastapiAdmin 是一个基于 FastAPI 和 Vue3 的管理系统，包含后端 API、前端界面、移动端应用和文档网站。项目采用 Docker 容器化部署，便于在不同环境中快速部署和运行。

## 项目结构

```sh
FastapiAdmin/
├── backend/      # 后端应用代码
├── frontend/     # 前端应用代码
├── devops/       # 部署配置文件
│   ├── backend/  # 后端部署目录
│   ├── mysql/    # MySQL 部署目录
│   ├── nginx/    # Nginx 部署目录
│   ├── redis/    # Redis 部署目录
│   └── README.md # 部署说明文档
├── deploy.sh     # 一键部署脚本
└── docker-compose.yaml # Docker 编排文件
```

## 系统要求

在部署项目之前，请确保服务器满足以下要求：

- **操作系统**：Linux (推荐 Ubuntu 20.04+) 或 macOS
- **Docker**：20.10.0 或更高版本
- **Docker Compose**：2.0.0 或更高版本
- **Git**：2.0.0 或更高版本
- **Node.js**：16.0.0 或更高版本
- **npm/pnpm**：8.0.0 或更高版本
- **内存**：至少 4GB RAM
- **磁盘空间**：至少 20GB 可用空间

## 部署前准备

### 1. 环境检查

首先，检查系统是否已安装必要的依赖：

```bash
# 检查 Docker 版本
docker --version
# 检查 Docker Compose 版本
docker compose version
# 检查 Git 版本
git --version
# 检查 Node.js 版本
node --version
# 检查 npm 版本
npm --version
# 检查 pnpm 版本
pnpm --version
```

如果缺少任何依赖，请先安装它们。

### 2. 克隆项目

如果尚未克隆项目代码，可以使用以下命令：

```bash
git clone https://gitee.com/fastapiadmin/fastapiadmin.git
cd fastapiadmin
```

## 一键部署

项目提供了一键部署脚本 `deploy.sh`，可以自动完成从代码拉取到服务启动的全过程。

### 1. 赋予脚本执行权限

```bash
chmod +x deploy.sh
```

### 2. 执行部署脚本

```bash
./deploy.sh
```

部署脚本会自动执行以下步骤：

- 检查系统依赖
- 停止现有容器（如果存在）
- 拉取最新代码
- 构建 Docker 镜像
- 启动容器
- 显示容器状态和日志

## 部署脚本命令详解

部署脚本支持以下命令行参数：

### 完整部署（默认）

```bash
./deploy.sh
```

执行完整的部署流程，包括检查依赖、停止容器、更新代码、构建镜像、启动容器和显示日志。

### 仅停止服务

```bash
./deploy.sh --stop
```

停止所有正在运行的项目容器。

### 启动服务

```bash
./deploy.sh --start
```

启动所有服务（等同于执行完整部署流程）。

### 查看日志

```bash
./deploy.sh --logs
# 或简写
./deploy.sh -l
```

显示所有容器的日志信息。

### 查看帮助信息

```bash
./deploy.sh --help
# 或简写
./deploy.sh -h
```

显示脚本使用说明。

## 部署流程详解

部署脚本的执行流程如下：

1. **权限和依赖检查**
   - 检查脚本执行权限
   - 检查系统依赖（git、docker、node、npm、pnpm）

2. **停止现有容器**
   - 如果项目目录存在，停止并删除现有容器
   - 如果项目目录不存在，从 Git 仓库克隆代码

3. **更新代码**
   - 拉取最新的代码更新
   - 检测前端、移动端和文档目录是否存在

4. **构建前端（当前已注释，如需启用请取消注释 deploy.sh 中的 build_frontend 调用）**
   - 安装前端依赖并构建前端工程
   - 安装移动端依赖并构建移动端工程
   - 安装文档依赖并构建文档

5. **构建镜像和启动容器**
   - 构建项目所需的 Docker 镜像
   - 启动所有服务容器
   - 清理 72 小时前的旧镜像

6. **显示容器状态和日志**
   - 显示所有容器的运行状态
   - 显示各服务的日志信息

## 服务访问

部署完成后，可以通过以下地址访问各服务：

- **前端管理系统**：[https://service.fastapiadmin.com/web](https://service.fastapiadmin.com/web)
- **移动端应用**：[https://service.fastapiadmin.com/app](https://service.fastapiadmin.com/app)
- **项目文档**：[https://service.fastapiadmin.com](https://service.fastapiadmin.com)
- **API 文档**：[https://service.fastapiadmin.com/api/v1/docs](https://service.fastapiadmin.com/api/v1/docs)

默认登录信息：

- **用户名**：admin
- **密码**：123456

> **注意**：实际部署时，请根据服务器配置修改域名或使用 IP 地址访问。

## 容器管理

### 查看容器状态

```bash
docker compose ps
```

### 查看实时日志

```bash
# 查看所有服务的实时日志
docker compose logs -f

# 查看单个服务的实时日志（例如后端服务）
docker compose logs -f backend
```

### 停止服务

```bash
docker compose down
```

### 重启服务

```bash
docker compose restart
```

### 进入容器

```bash
# 进入后端容器
docker compose exec backend bash

# 进入数据库容器
docker compose exec mysql bash
```

## 问题排查

### 常见问题

#### 1. 端口冲突

如果启动容器时出现端口冲突，请检查是否有其他服务占用了相同的端口，并在 docker-compose.yaml 中修改端口映射。

#### 2. 数据库连接失败

- 检查数据库容器是否正常运行
- 确认数据库配置是否正确（用户名、密码、数据库名）
- 查看后端服务日志获取详细错误信息

#### 3. 前端访问后端 API 失败

- 检查 Nginx 配置是否正确
- 确认 API 路径配置是否匹配
- 查看浏览器控制台的网络请求和错误信息

### 配置文件

以下是可能需要修改的关键配置文件：

1. **后端配置**：`backend/env/.env.prod.py`
2. **前端配置**：`frontend/vite.config.ts` 和 `frontend/.env.production`
3. **Docker 配置**：`docker-compose.yaml`
4. **Nginx 配置**：`devops/nginx/nginx.conf`

### 日志查看

遇到问题时，建议先查看相关服务的日志：

```bash
# 查看后端服务日志
docker compose logs backend

# 查看 Nginx 服务日志
docker compose logs nginx

# 查看 MySQL 服务日志
docker compose logs mysql

# 查看 Redis 服务日志
docker compose logs redis
```

## 安全建议

1. **修改默认密码**：部署后请立即修改默认的管理员密码
2. **配置 HTTPS**：在生产环境中请配置 SSL 证书，启用 HTTPS
3. **限制访问**：根据实际需求配置防火墙规则，限制对敏感服务的访问
4. **定期更新**：定期拉取最新代码并更新部署，以获取安全补丁和新功能

## 维护建议

1. **定期备份**：定期备份数据库和重要配置文件
2. **监控服务**：设置服务监控，及时发现并处理异常情况
3. **清理镜像**：定期清理不再使用的 Docker 镜像，释放磁盘空间

## 联系与支持

如有任何问题或需要技术支持，请联系项目维护者。
