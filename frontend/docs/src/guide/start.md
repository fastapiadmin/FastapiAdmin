---
outline: "deep"
title: 快速开始
---
# 快速开始

## 🍪演示环境

- 官网地址：<https://service.fastapiadmin.com>
- 演示地址：<https://service.fastapiadmin.com/web>
- 小程序地址：<https://service.fastapiadmin.com/app>
- 管理员账号：`admin` 密码：`123456`
- 演示账号：`demo` 密码：`123456`

## 👷安装和使用

### 版本说明

| 类型     | 技术栈     | 版本       |
|----------|------------|------------|
| 后端     | Python         | >=3.10       |
| 后端     | FastAPI        | 0.109+      |
| 前端     | Node.js        | >= 20.0（推荐使用最新版）|
| 前端     | pnpm           | >= 9.0      |
| 前端     | Vue3           | 3.5.22+     |
| Web UI  | ElementPlus     | 2.10.4+        |
| 移动端  | Uni App         | 3.0.0+       |
| App UI  | Wot Design Uni  | 1.9.1+        |
| 数据库   | MySQL           | 8.0+ （推荐使用最新版）|
| 中间件   | Redis           | 7.0+ （推荐使用最新版）|

### 环境准备

#### 1. 安装 Python

```sh
# macOS
brew install python@3.10

# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# CentOS/RHEL
sudo dnf install python3.10 python3.10-venv python3.10-devel
```

#### 2. 安装 Node.js

```sh
# 使用 nvm 安装（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20

# 或使用包管理器
# macOS
brew install node@20

# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# CentOS/RHEL
sudo dnf install nodejs npm

# 安装 pnpm
npm install -g pnpm
```

#### 3. 安装数据库和缓存

```sh
# 安装 MySQL
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql

# 安装 Redis
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis
```

### 获取代码

```sh
# 克隆代码到本地
# FastapiAdmin 主工程
git clone https://github.com/fastapiadmin/FastapiAdmin.git
# 或使用 Gitee
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git

# FastApp 移动端
git clone https://github.com/fastapiadmin/FastApp.git
# 或使用 Gitee
git clone https://gitee.com/fastapiadmin/FastApp.git

# FastDocs 官网文档
git clone https://github.com/fastapiadmin/FastDocs.git
# 或使用 Gitee
git clone https://gitee.com/fastapiadmin/FastDocs.git
```

### 本地后端启动（FastapiAdmin 主工程）

#### 1. 配置环境变量

```sh
# 进入后端工程目录
cd FastapiAdmin/backend

# 复制环境配置文件
cp env/.env.dev.example env/.env.dev

# 编辑环境配置文件（根据实际情况修改）
# 主要配置项说明：
# - DATABASE_URL: 数据库连接地址
# - REDIS_URL: Redis连接地址
# - SECRET_KEY: JWT签名密钥
# - ACCESS_TOKEN_EXPIRE_MINUTES: 访问令牌过期时间
# - REFRESH_TOKEN_EXPIRE_DAYS: 刷新令牌过期时间
# - API_PREFIX: API前缀
# - CORS_ORIGINS: 跨域来源
```

#### 2. 安装依赖

```sh
# 使用 uv 管理项目（推荐）
uv add -r requirements.txt

# 或使用传统 pip 方式
# 创建虚拟环境（可选但推荐）
python3 -m venv .venv

# 激活虚拟环境
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 数据库初始化

```sh
# 生成迁移文件
python main.py revision "初始化迁移" --env=dev

# 应用迁移
python main.py upgrade --env=dev

# 初始化系统数据
python main.py init
```

#### 4. 启动后端服务

```sh
# 使用 uv 启动
uv run main.py run

# 或使用传统方式
# 开发环境启动
python main.py run --env=dev

# 或使用默认环境（dev）
python main.py run

# 生产环境启动
python main.py run --env=prod
```

### 本地前端启动（FastapiAdmin 主工程）

#### 1. 配置环境变量

```sh
# 进入前端工程目录
cd FastapiAdmin/frontend

# 复制环境配置文件
cp .env.development.example .env.development

# 编辑环境配置文件（根据实际情况修改）
# 主要配置项说明：
# - VITE_API_BASE_URL: 后端API基础地址
# - VITE_APP_BASE_API: API前缀
# - VITE_APP_TITLE: 应用标题
# - VITE_APP_VERSION: 应用版本
```

#### 2. 安装依赖

```sh
# 安装前端依赖
pnpm install
```

#### 3. 启动前端服务

```sh
# 开发环境启动
pnpm run dev

# 构建前端, 生成 `dist` 目录
pnpm run build
```

### 本地移动端启动（FastApp 移动端）

#### 1. 环境要求

- **Node.js** >= 22
- **pnpm** >= 9

#### 2. 配置环境变量

```sh
# 进入移动端工程目录
cd FastApp

# 复制环境配置文件
cp .env.development.example .env.development
cp .env.production.example .env.production

# 编辑环境配置文件（根据实际情况修改）
# 主要配置项说明：
# - VITE_APP_ENV: 环境模式
# - VITE_APP_TITLE: 应用标题
# - VITE_API_BASE_URL: 后端API基础地址
# - VITE_APP_BASE_API: API前缀（/api/v1）
# - VITE_APP_PORT: 开发服务器端口
# - VITE_TIMEOUT: 请求超时时间
# - VITE_APP_WS_ENDPOINT: WebSocket服务器地址
```

#### 3. 安装依赖

```sh
# 进入移动端工程目录
cd FastApp

# 安装前端依赖
pnpm install
```

#### 4. 启动开发服务器

##### H5 开发

```bash
# 启动 H5 开发服务器
pnpm run dev:h5

# 访问地址
# http://localhost:5180/app
```

##### 微信小程序开发

```bash
# 启动微信小程序开发服务器
pnpm run dev:mp-weixin

# 在微信开发者工具中导入项目目录：FastApp/dist/dev/mp-weixin
```

##### 其他平台开发

```bash
# 启动支付宝小程序开发服务器
pnpm run dev:mp-alipay

# 启动百度小程序开发服务器
pnpm run dev:mp-baidu

# 启动字节跳动小程序开发服务器
pnpm run dev:mp-toutiao

# 启动 QQ 小程序开发服务器
pnpm run dev:mp-qq
```

### 本地项目官网启动（FastDocs 官网文档）

```sh
# 进入 FastDocs 官网文档目录
cd FastDocs

# 安装依赖
pnpm install

# 运行文档工程
pnpm run docs:dev

# 构建文档工程, 生成 `dist` 目录
pnpm run docs:build
```

---

### 本地访问地址

- FastDocs 文档地址: <http://127.0.0.1:5180>
- FastapiAdmin 前端地址: <http://127.0.0.1:5173>
- FastAPI 接口文档: <http://127.0.0.1:8001/api/v1/docs>
- FastApp H5地址: <http://127.0.0.1:5180/app>

### 默认账号密码

- 管理员账号：`admin` 密码：`123456`
- 演示账号：`demo` 密码：`123456`

## 🐳 Docker 部署

### 1. 准备工作

- 服务器需安装 Docker 和 Docker Compose
- 确保服务器端口 80（Nginx）、8001（后端）可用

### 2. 部署步骤

```sh
# 进入 FastapiAdmin 主工程目录
cd FastapiAdmin

# 复制环境配置文件
cp backend/env/.env.prod.example backend/env/.env.prod
cp frontend/.env.production.example frontend/.env.production

# 编辑环境配置文件（根据实际服务器情况修改）
# 主要配置项：数据库连接、Redis连接、JWT密钥、API基础URL等

# 赋予脚本执行权限
chmod +x deploy.sh

# 执行部署脚本
./deploy.sh

# 查看部署状态
docker compose ps

# 查看日志
docker logs -f fastapiadmin-backend
```

### 3. 部署文件说明

| 配置文件 | 说明 | 路径 |
|---------|------|------|
| 后端环境配置 | 生产环境数据库、Redis等配置 | `FastapiAdmin/backend/env/.env.prod` |
| 前端环境配置 | 生产环境API地址等配置 | `FastapiAdmin/frontend/.env.production` |
| Docker配置 | 容器编排配置 | `FastapiAdmin/docker-compose.yaml` |
| Nginx配置 | 反向代理配置 | `FastapiAdmin/devops/nginx/nginx.conf` |

### 4. 常用 Docker 命令

```sh
# 查看镜像
docker images

# 查看容器
docker compose ps

# 停止服务
docker compose down

# 重启服务
docker compose up -d

# 查看容器日志
docker logs -f <容器名>

# 进入容器
docker exec -it <容器名> bash
```

## 🔧模块展示

### web 端

| 模块名 <div style="width:60px"/>  | 截图 |
|----------|------|
| 仪表盘    | ![仪表盘](/dashboard.png) |
| 代码生成  | ![代码生成](/gencode.png) |
| 智能助手  | ![智能助手](/ai.png) |

### 移动端

| 登录 <div style="width:60px"/> | 首页 <div style="width:60px"/> | 个人中心 <div style="width:60px"/> |
|----------|----------|----------|
| ![移动端登录](/app_login.png) | ![移动端首页](/app_home.png) | ![移动端个人中心](/app_mine.png) |

## 🚀二开教程

### 后端部分（FastapiAdmin 主工程）

项目采用**插件化架构设计**，二次开发建议在 `backend/app/plugin` 目录下进行，系统会**自动发现并注册**所有符合规范的路由，便于模块管理和升级维护。

#### 插件化架构特性

- **自动路由发现**：系统会自动扫描 `backend/app/plugin/` 目录下所有 `controller.py` 文件
- **自动路由注册**：所有路由会被自动注册到对应的前缀路径 (module_xxx -> /xxx)
- **模块化管理**：按功能模块组织代码，便于维护和扩展
- **支持多层级嵌套**：支持模块内部多层级嵌套结构

#### 插件目录结构

```sh
backend/app/plugin/
├── module_application/  # 应用模块（自动映射为 /application）
│   └── ai/              # AI子模块
│       ├── controller.py # 控制器文件
│       ├── model.py      # 数据模型文件
│       ├── schema.py     # 数据验证文件
│       ├── service.py    # 业务逻辑文件
│       └── crud.py       # 数据访问文件
├── module_example/      # 示例模块（自动映射为 /example）
│   └── demo/            # 子模块
│       ├── controller.py # 控制器文件
│       ├── model.py      # 数据模型文件
│       ├── schema.py     # 数据验证文件
│       ├── service.py    # 业务逻辑文件
│       └── crud.py       # 数据访问文件
├── module_generator/    # 代码生成模块（自动映射为 /generator）
└── init_app.py          # 插件初始化文件
```

#### 二次开发步骤

1. **创建插件模块**：在 `backend/app/plugin/` 目录下创建新的模块目录，如 `module_yourfeature`
2. **编写数据模型**：在 `model.py` 中定义数据库模型
3. **编写数据验证**：在 `schema.py` 中定义数据验证模型
4. **编写数据访问层**：在 `crud.py` 中编写数据库操作逻辑
5. **编写业务逻辑层**：在 `service.py` 中编写业务逻辑
6. **编写控制器**：在 `controller.py` 中定义路由和处理函数
7. **自动注册**：系统会自动扫描并注册所有路由，无需手动配置

### 前端部分（FastapiAdmin 主工程）

1. **配置前端API**：在 `frontend/src/api/` 目录下创建对应的API文件
2. **编写页面组件**：在 `frontend/src/views/` 目录下创建页面组件
3. **注册路由**：在 `frontend/src/router/index.ts` 中注册路由

### 移动端部分（FastApp 移动端）

1. **配置移动端API**：在 `FastApp/src/api/` 目录下创建对应的API文件
2. **编写移动端页面**：在 `FastApp/src/pages/` 目录下创建页面组件
3. **配置页面路由**：在 `FastApp/src/pages.json` 中配置页面路由

## 💡常见问题及解决方案

### 1. 后端启动失败

**问题**：数据库连接失败
**解决方案**：检查环境配置文件中的数据库连接信息是否正确，确保数据库服务正在运行，且用户名密码正确。

**问题**：Redis连接失败
**解决方案**：检查环境配置文件中的Redis连接信息是否正确，确保Redis服务正在运行。

**问题**：依赖安装失败
**解决方案**：确保Python版本正确（>=3.10），可以尝试使用虚拟环境重新安装依赖。

### 2. 前端启动失败

**问题**：依赖安装失败
**解决方案**：确保Node.js版本正确（>=20.0），可以尝试清除缓存后重新安装：`pnpm cache clean && pnpm install`。

**问题**：API请求失败
**解决方案**：检查前端环境配置文件中的API基础URL是否正确，确保后端服务正在运行。

### 3. 移动端启动失败

**问题**：依赖安装失败
**解决方案**：确保Node.js版本正确（>=22.0），pnpm版本正确（>=9.0），可以尝试清除缓存后重新安装：`pnpm cache clean && pnpm install`。

**问题**：H5页面空白
**解决方案**：检查浏览器控制台是否有错误信息，确保API基础URL配置正确，后端服务正在运行。

### 4. 部署问题

**问题**：Docker部署失败
**解决方案**：确保服务器已安装Docker和Docker Compose，检查端口是否被占用，查看容器日志了解具体错误信息。

**问题**：Nginx配置错误
**解决方案**：检查Nginx配置文件中的反向代理设置是否正确，确保后端服务地址配置正确。

### 5. 其他问题

**问题**：系统初始化失败
**解决方案**：确保数据库已正确初始化，且迁移已应用，可以尝试重新执行初始化命令：`python main.py init`。

**问题**：权限不足
**解决方案**：检查用户角色权限设置，确保当前用户有足够的权限访问所需功能。

**问题**：代码生成失败
**解决方案**：确保数据库表结构正确，代码生成配置参数填写完整。
