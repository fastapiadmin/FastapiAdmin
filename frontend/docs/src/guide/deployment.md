---
outline: "deep"
title: 部署指南
---
# 部署指南

## 🚀部署概述

FastapiAdmin 项目支持多种部署方式，包括：

- **Docker Compose 部署**：推荐的部署方式，快速、便捷、可移植
- **手动部署**：适用于特殊场景或需要高度定制的情况
- **云服务部署**：可以部署到阿里云、腾讯云等云服务提供商

本指南将详细介绍 FastapiAdmin 主工程和 FastApp 移动端的部署步骤。

## 🐳Docker Compose 部署

### 1. 环境准备

- **服务器**：推荐使用 Ubuntu 20.04+、CentOS 7+ 等 Linux 系统
- **Docker**：版本 >= 20.0
- **Docker Compose**：版本 >= 1.29.0
- **网络**：确保服务器可以访问互联网，并且开放所需端口

### 2. 安装 Docker 和 Docker Compose

#### Ubuntu/Debian

```sh
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装 Docker
sudo apt install docker.io -y

# 安装 Docker Compose
sudo apt install docker-compose -y

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 添加当前用户到 docker 组（可选）
sudo usermod -aG docker $USER
newgrp docker
```

#### CentOS/RHEL

```sh
# 更新系统
sudo yum update -y

# 安装 Docker
sudo yum install docker -y

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 添加当前用户到 docker 组（可选）
sudo usermod -aG docker $USER
newgrp docker
```

### 3. 部署步骤

#### 1. 获取代码

```sh
# 克隆代码到服务器
cd /opt
git clone https://github.com/fastapiadmin/FastapiAdmin.git
cd FastapiAdmin
```

#### 2. 配置环境变量

```sh
# 配置后端环境变量
cd backend
cp env/.env.prod.example env/.env.prod
# 编辑 env/.env.prod 文件，配置数据库、Redis 等信息

# 配置前端环境变量
cd ../frontend
cp .env.production.example .env.production
# 编辑 .env.production 文件，配置 API 地址等信息

cd ..
```

#### 3. 配置 Docker Compose

Docker Compose 配置文件位于 `docker-compose.yaml`，包含了所有服务的配置：

```yaml
# docker-compose.yaml 示例
version: '3'
services:
  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: ../devops/backend/Dockerfile
    container_name: fastapiadmin-backend
    ports:
      - "8001:8001"
    volumes:
      - ./backend:/app
      - ./backend/logs:/app/logs
    environment:
      - ENV=prod
    depends_on:
      - mysql
      - redis
    networks:
      - fastapiadmin-network
    restart: always

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: fastapiadmin-frontend
    ports:
      - "5173:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
    networks:
      - fastapiadmin-network
    restart: always

  # MySQL 数据库
  mysql:
    image: mysql:8.0
    container_name: fastapiadmin-mysql
    ports:
      - "3306:3306"
    volumes:
      - ./devops/mysql/data:/var/lib/mysql
      - ./devops/mysql/conf:/etc/mysql/conf.d
    environment:
      - MYSQL_ROOT_PASSWORD=your_root_password
      - MYSQL_DATABASE=fastapiadmin
      - MYSQL_USER=fastapiadmin
      - MYSQL_PASSWORD=your_password
    networks:
      - fastapiadmin-network
    restart: always

  # Redis 缓存
  redis:
    image: redis:7.0
    container_name: fastapiadmin-redis
    ports:
      - "6379:6379"
    volumes:
      - ./devops/redis/data:/data
      - ./devops/redis/conf/redis.conf:/etc/redis/redis.conf
    networks:
      - fastapiadmin-network
    restart: always

  # Nginx 反向代理
  nginx:
    image: nginx:1.21
    container_name: fastapiadmin-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./devops/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./devops/nginx/ssl:/etc/nginx/ssl
    networks:
      - fastapiadmin-network
    restart: always

networks:
  fastapiadmin-network:
    driver: bridge
```

#### 4. 配置 Nginx

Nginx 配置文件位于 `devops/nginx/nginx.conf`，用于反向代理和 SSL 配置：

```nginx
# devops/nginx/nginx.conf 示例
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # 前端服务
    upstream frontend {
        server frontend:80;
    }

    # 后端服务
    upstream backend {
        server backend:8001;
    }

    # 主站点
    server {
        listen       80;
        server_name  service.fastapiadmin.com;

        # 重定向到 HTTPS
        return 301 https://$host$request_uri;
    }

    # HTTPS 站点
    server {
        listen       443 ssl http2;
        server_name  service.fastapiadmin.com;

        # SSL 配置
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  10m;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # 前端路由
        location /web {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 后端 API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 静态文件
        location /static {
            alias /usr/share/nginx/html/static;
            expires 30d;
        }

        # 健康检查
        location /health {
            return 200 "OK";
        }
    }
}
```

#### 5. 启动服务

```sh
# 执行部署脚本
chmod +x start.sh
./start.sh

# 或手动启动
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 部署后配置

#### 1. 初始化数据库

```sh
# 进入后端容器
docker exec -it fastapiadmin-backend bash

# 初始化数据库
python main.py init

# 退出容器
exit
```

#### 2. 配置域名

1. 在域名注册商处添加 A 记录，指向服务器 IP 地址
2. 等待 DNS 解析生效

#### 3. 配置 SSL 证书

推荐使用 Let's Encrypt 免费 SSL 证书：

```sh
# 安装 Certbot
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d service.fastapiadmin.com

# 自动续期
echo "0 0 1 * * certbot renew --quiet" | sudo crontab -
```

## 📦手动部署

### 1. 后端部署

#### 1. 环境准备

- Python 3.10+
- MySQL 8.0+
- Redis 7.0+

#### 2. 安装依赖

```sh
# 进入后端目录
cd FastapiAdmin/backend

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置环境变量

```sh
cp env/.env.prod.example env/.env.prod
# 编辑 env/.env.prod 文件，配置数据库、Redis 等信息
```

#### 4. 初始化数据库

```sh
# 生成迁移文件
python main.py revision "初始化迁移" --env=prod

# 应用迁移
python main.py upgrade --env=prod

# 初始化系统数据
python main.py init
```

#### 5. 启动后端服务

```sh
# 使用 Gunicorn 启动（推荐）
pip install gunicorn uvloop

# 启动服务
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001 --daemon

# 或使用 systemd 管理服务
# 创建 systemd 服务文件
```

### 2. 前端部署

#### 1. 环境准备

- Node.js 20.0+
- Nginx

#### 2. 构建前端

```sh
# 进入前端目录
cd FastapiAdmin/frontend

# 安装依赖
pnpm install

# 构建前端
pnpm run build
```

#### 3. 配置 Nginx

```nginx
# /etc/nginx/conf.d/fastapiadmin.conf
server {
    listen 80;
    server_name service.fastapiadmin.com;

    # 前端静态文件
    location /web {
        root /path/to/FastapiAdmin/frontend;
        index index.html;
        try_files $uri $uri/ /web/index.html;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. 重启 Nginx

```sh
sudo nginx -t
sudo systemctl restart nginx
```

## ☁️云服务部署

### 1. 阿里云部署

#### 1. 创建 ECS 实例

1. 登录阿里云控制台
2. 创建 ECS 实例，选择 Ubuntu 20.04 或 CentOS 7+
3. 配置安全组，开放 80、443、8001 等端口

#### 2. 部署步骤

参考前面的 Docker Compose 部署或手动部署步骤。

### 2. 腾讯云部署

#### 1. 创建 CVM 实例

1. 登录腾讯云控制台
2. 创建 CVM 实例，选择 Ubuntu 20.04 或 CentOS 7+
3. 配置安全组，开放 80、443、8001 等端口

#### 2. 部署步骤

参考前面的 Docker Compose 部署或手动部署步骤。

## 🔧常见部署问题及解决方案

### 1. Docker 相关问题

**问题**：Docker 构建失败
**解决方案**：检查 Dockerfile 是否正确，依赖是否可用，网络连接是否正常。

**问题**：容器启动失败
**解决方案**：查看容器日志 `docker logs <容器名>`，检查配置是否正确，端口是否被占用。

**问题**：Docker -compose 命令不执行
**解决方案**：检查 Docker Compose 版本是否正确，配置文件格式是否正确。

### 2. 数据库相关问题

**问题**：数据库连接失败
**解决方案**：检查数据库服务是否正常运行，用户名密码是否正确，防火墙是否开放 3306 端口。

**问题**：数据库初始化失败
**解决方案**：检查数据库权限是否足够，SQL 语句是否正确，查看错误日志。

### 3. Nginx 相关问题

**问题**：Nginx 启动失败
**解决方案**：检查 Nginx 配置文件是否正确 `nginx -t`，端口是否被占用。

**问题**：前端页面无法访问
**解决方案**：检查 Nginx 配置是否正确，前端文件是否存在，权限是否正确。

**问题**：API 请求失败
**解决方案**：检查后端服务是否正常运行，Nginx 反向代理配置是否正确，防火墙是否开放 8001 端口。

### 4. 网络相关问题

**问题**：服务器无法访问互联网
**解决方案**：检查服务器网络连接，防火墙配置，DNS 设置。

**问题**：域名无法访问
**解决方案**：检查 DNS 解析是否生效，服务器防火墙是否开放 80、443 端口，Nginx 配置是否正确。

### 5. 性能优化

**问题**：服务响应缓慢
**解决方案**：
- 优化数据库查询，添加索引
- 配置 Redis 缓存
- 调整 Nginx 配置，增加并发连接数
- 调整后端服务的 worker 数量
- 使用 CDN 加速静态文件

**问题**：服务器负载过高
**解决方案**：
- 监控服务器资源使用情况
- 优化代码，减少资源消耗
- 考虑使用负载均衡，增加服务器数量

## 📊监控与维护

### 1. 监控

#### 1. 服务监控

- **Prometheus + Grafana**：监控服务器和容器状态
- **ELK Stack**：收集和分析日志
- **Uptime Robot**：监控网站可用性

#### 2. 日志管理

- **后端日志**：位于 `backend/logs` 目录
- **前端日志**：使用浏览器控制台查看
- **Nginx 日志**：位于 `/var/log/nginx` 目录

### 2. 维护

#### 1. 定期备份

```sh
# 备份数据库
mysqldump -u root -p fastapiadmin > fastapiadmin_$(date +%Y%m%d).sql

# 备份代码
zip -r fastapiadmin_$(date +%Y%m%d).zip FastapiAdmin/

# 备份配置文件
cp -r FastapiAdmin/backend/env /backup/env
cp -r FastapiAdmin/frontend/.env* /backup/frontend
```

#### 2. 定期更新

```sh
# 更新代码
git pull

# 更新依赖
cd FastapiAdmin/backend
source .venv/bin/activate
pip install -r requirements.txt

cd ../frontend
pnpm install
pnpm run build

# 重启服务
docker-compose up -d --build
```

#### 3. 故障排查

1. **查看日志**：`docker logs <容器名>`、`tail -f /var/log/nginx/error.log`
2. **检查服务状态**：`systemctl status <服务名>`、`docker ps`
3. **检查网络连接**：`ping <域名>`、`curl -I <URL>`
4. **检查资源使用**：`top`、`df -h`、`free -m`

## 📚参考文档

- **Docker 官方文档**：[https://docs.docker.com/](https://docs.docker.com/)
- **Docker Compose 官方文档**：[https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Nginx 官方文档**：[https://nginx.org/en/docs/](https://nginx.org/en/docs/)
- **FastAPI 官方文档**：[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Vue 官方文档**：[https://vuejs.org/](https://vuejs.org/)
- **Let's Encrypt 官方文档**：[https://letsencrypt.org/docs/](https://letsencrypt.org/docs/)

## 🤝常见问题

### 1. 部署后无法访问

**解决方案**：
1. 检查服务器防火墙是否开放 80、443 端口
2. 检查 Nginx 服务是否正常运行
3. 检查 DNS 解析是否生效
4. 检查 Docker 容器是否正常运行

### 2. API 请求返回 500 错误

**解决方案**：
1. 查看后端日志，了解具体错误信息
2. 检查数据库连接是否正常
3. 检查 Redis 连接是否正常
4. 检查环境变量配置是否正确

### 3. 前端页面显示空白

**解决方案**：
1. 检查浏览器控制台是否有错误信息
2. 检查前端构建是否成功
3. 检查 Nginx 配置是否正确
4. 检查 API 地址是否配置正确

### 4. 部署脚本执行失败

**解决方案**：
1. 检查脚本权限是否正确 `chmod +x start.sh`
2. 检查 Docker 和 Docker Compose 是否正确安装
3. 检查网络连接是否正常
4. 查看脚本执行日志，了解具体错误信息

## �FastApp 移动端部署

### 1. H5 部署

#### 1.1 构建 H5 版本

```bash
# 进入 FastApp 目录
cd FastApp

# 安装依赖
pnpm install

# 构建 H5 版本
pnpm run build:h5

# 构建产物在 dist/build/h5 目录
```

#### 1.2 部署到服务器

1. 将 `dist/build/h5` 目录复制到 Web 服务器的静态文件目录
2. 配置 Nginx 支持 SPA 路由：

```nginx
# /etc/nginx/conf.d/fastapp.conf
server {
    listen 80;
    server_name service.fastapiadmin.com;

    # FastApp H5
    location /app {
        alias /path/to/FastApp/dist/build/h5;
        index index.html;
        try_files $uri $uri/ /app/index.html;
    }

    # 其他配置...
}
```

3. 重启 Nginx：

```bash
sudo nginx -t
sudo systemctl restart nginx
```

#### 1.3 访问方式

部署完成后，可以通过以下地址访问 FastApp H5 版本：
- `http://service.fastapiadmin.com/app`

### 2. 微信小程序部署

#### 2.1 构建微信小程序版本

```bash
# 进入 FastApp 目录
cd FastApp

# 构建微信小程序版本
pnpm run build:mp-weixin

# 构建产物在 dist/build/mp-weixin 目录
```

#### 2.2 发布到微信小程序平台

1. 打开微信开发者工具
2. 点击「导入项目」
3. 选择 `dist/build/mp-weixin` 目录
4. 填写小程序 AppID（如果没有 AppID，可以使用测试号）
5. 点击「导入」按钮
6. 等待项目加载完成后，点击「上传」按钮
7. 填写版本号和更新日志
8. 点击「上传」按钮
9. 登录微信公众平台（mp.weixin.qq.com）
10. 进入「版本管理」页面
11. 找到刚刚上传的版本，点击「提交审核」
12. 等待审核通过后，点击「发布」按钮

### 3. 支付宝小程序部署

#### 3.1 构建支付宝小程序版本

```bash
# 进入 FastApp 目录
cd FastApp

# 构建支付宝小程序版本
pnpm run build:mp-alipay

# 构建产物在 dist/build/mp-alipay 目录
```

#### 3.2 发布到支付宝小程序平台

1. 打开支付宝小程序开发者工具
2. 点击「导入项目」
3. 选择 `dist/build/mp-alipay` 目录
4. 填写小程序 AppID
5. 点击「导入」按钮
6. 等待项目加载完成后，点击「上传」按钮
7. 填写版本号和更新日志
8. 点击「上传」按钮
9. 登录支付宝开放平台
10. 进入「小程序管理」页面
11. 找到刚刚上传的版本，点击「提交审核」
12. 等待审核通过后，点击「发布」按钮

### 4. App 部署

#### 4.1 使用 HBuilderX 打包

1. 下载并安装 [HBuilderX](https://www.dcloud.io/hbuilderx.html)
2. 打开 HBuilderX
3. 点击「文件」->「导入」->「从本地目录导入」
4. 选择 FastApp 项目目录
5. 等待项目加载完成后，点击「发行」->「原生 App-云打包」
6. 填写 App 名称、版本号等信息
7. 选择打包平台（Android、iOS 或两者都选）
8. 配置证书信息（如果没有证书，可以使用测试证书）
9. 点击「打包」按钮
10. 等待打包完成后，下载安装包

#### 4.2 发布到应用商店

##### Android 应用商店

1. 登录 [Google Play 开发者控制台](https://play.google.com/console/) 或其他 Android 应用商店
2. 创建应用
3. 填写应用信息
4. 上传 APK 文件
5. 提交审核
6. 等待审核通过后，应用会在应用商店上线

##### iOS App Store

1. 登录 [Apple Developer](https://developer.apple.com/) 网站
2. 进入 App Store Connect
3. 创建新应用
4. 填写应用信息
5. 上传 IPA 文件（需要使用 Xcode 进行签名）
6. 提交审核
7. 等待审核通过后，应用会在 App Store 上线

### 5. 部署注意事项

#### 5.1 API 地址配置

在部署 FastApp 之前，需要确保 API 地址配置正确：

```bash
# FastApp/.env.production
# API 基础地址
VITE_API_BASE_URL=https://service.fastapiadmin.com

# API 前缀
VITE_APP_BASE_API=/api
```

#### 5.2 跨域配置

如果 FastApp 部署在不同的域名下，需要确保后端服务支持跨域请求：

```python
# FastapiAdmin/backend/app/core/middlewares.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 5.3 性能优化

- **压缩静态文件**：使用 gzip 压缩静态文件，减少传输大小
- **启用缓存**：配置浏览器缓存，减少重复请求
- **使用 CDN**：将静态资源部署到 CDN，提高访问速度
- **优化图片**：压缩图片大小，使用适当的图片格式

### 6. 常见问题及解决方案

#### 6.1 H5 部署问题

**问题**：H5 页面刷新后显示 404
**解决方案**：配置 Nginx 支持 SPA 路由，使用 `try_files` 指令

**问题**：H5 页面无法调用 API
**解决方案**：检查 API 地址配置是否正确，确保后端服务支持跨域请求

#### 6.2 小程序部署问题

**问题**：小程序审核失败
**解决方案**：根据审核反馈修改代码，确保符合小程序平台的规范

**问题**：小程序无法调用 API
**解决方案**：在微信公众平台设置合法域名，或在开发者工具中开启「不校验合法域名」选项

#### 6.3 App 部署问题

**问题**：App 打包失败
**解决方案**：检查证书配置是否正确，确保打包环境网络连接正常

**问题**：App 无法调用 API
**解决方案**：检查 API 地址配置是否正确，确保网络连接正常

## �📄许可协议

FastapiAdmin 项目采用 MIT 许可协议，详见 [LICENSE](https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE) 文件。
