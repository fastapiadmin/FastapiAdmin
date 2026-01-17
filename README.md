<div align="center">
     <p align="center">
          <img src="https://gitee.com/tao__tao/FastDocs/raw/main/src/public/logo.png" width="150" height="150" alt="logo" />  
     </p>
     <h1>FastApiAdmin <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">v2.0.0</h1>
     <h3>现代化全栈快速开发平台</h3>
     <p>如果你喜欢这个项目，给个 ⭐️ 支持一下吧！</p>
     <p align="center">
          <a href="https://gitee.com/tao__tao/FastapiAdmin.git" target="_blank">
               <img src="https://gitee.com/tao__tao/FastapiAdmin/badge/star.svg?theme=dark" alt="Gitee Stars">
          </a>
          <a href="https://github.com/1014TaoTao/FastapiAdmin.git" target="_blank">
               <img src="https://img.shields.io/github/stars/1014TaoTao/FastapiAdmin?style=social" alt="GitHub Stars">
          </a>
          <a href="https://gitee.com/tao__tao/FastapiAdmin/blob/master/LICENSE" target="_blank">
               <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
          </a>
          <img src="https://img.shields.io/badge/Python-≥3.10-blue"> 
          <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue"> 
          <img src="https://img.shields.io/badge/MySQL-≥8.0-blue"> 
          <img src="https://img.shields.io/badge/Redis-≥7.0-blue"> 
          <img src="https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/> 
          <img src="https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3"/> 
          <img src="https://img.shields.io/badge/-JavaScript-563D7C?style=flat-square&logo=bootstrap"/> 
     </p>

简体中文 | [English](./README.en.md)

</div>

## 📘 项目介绍

**FastApiAdmin** 是一套 **完全开源、高度模块化、技术先进的现代化快速开发平台**，旨在帮助开发者高效搭建高质量的企业级中后台系统。该项目采用 **前后端分离架构**，融合 Python 后端框架 `FastAPI` 和前端主流框架 `Vue3` 实现多端统一开发，提供了一站式开箱即用的开发体验。

> **设计初心**: 以模块化、松耦合为核心，追求丰富的功能模块、简洁易用的接口、详尽的开发文档和便捷的维护方式。通过统一框架和组件，降低技术选型成本，遵循开发规范和设计模式，构建强大的代码分层模型，搭配完善的本地中文化支持，专为团队和企业开发场景量身定制。

## 🎯 核心优势

| 优势 | 描述 |
| ---- | ---- |
| 🔥 **现代化技术栈** | 基于 FastAPI + Vue3 + TypeScript 等前沿技术构建 |
| ⚡ **高性能异步** | 利用 FastAPI 异步特性和 Redis 缓存优化响应速度 |
| 🔐 **安全可靠** | JWT + OAuth2 认证机制，RBAC 权限控制模型 |
| 🧱 **模块化设计** | 高度解耦的系统架构，便于扩展和维护 |
| 🌐 **全栈支持** | Web端 + 移动端(H5) + 后端一体化解决方案 |
| 🚀 **快速部署** | Docker 一键部署，支持生产环境快速上线 |
| 📖 **完善文档** | 详细的开发文档和教程，降低学习成本 |
| 🤖 **智能体框架** | 基于Langchain和Langgraph的开发智能体 |

## 🍪 演示环境

- 💻 网页端：[https://service.fastapiadmin.com/web](https://service.fastapiadmin.com/web)
- 📱 移动端：[https://service.fastapiadmin.com/app](https://service.fastapiadmin.com/app)
- 👤 登录账号：`admin` 密码：`123456`

## 🔗 源码仓库

| 平台 | 仓库地址 |
|------|----------|
| GitHub | [FastapiAdmin主工程](https://github.com/1014TaoTao/FastapiAdmin.git) \| [FastDocs官网](https://github.com/1014TaoTao/FastDocs.git) \| [FastApp移动端](https://github.com/1014TaoTao/FastApp.git) |
| Gitee  | [FastapiAdmin主工程](https://gitee.com/tao__tao/FastapiAdmin.git) \| [FastDocs官网](https://gitee.com/tao__tao/FastDocs.git) \| [FastApp移动端](https://gitee.com/tao__tao/FastApp.git) |

## 📦 工程结构概览

```sh
FastapiAdmin
├─ backend               # 后端工程 (FastAPI + Python)
├─ frontend              # Web前端工程 (Vue3 + Element Plus)
├─ devops                # 部署配置
├─ docker-compose.yaml   # Docker编排文件
├─ deploy.sh             # 一键部署脚本
├─ LICENSE               # 开源协议
|─ README.en.md          # 英文文档
└─ README.md             # 中文文档
```

## 🛠️ 技术栈概览

| 类型 | 技术选型 | 描述 |
|------|----------|------|
| **后端框架** | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | 现代、高性能的异步框架，强制类型约束，数据迁移 |
| **ORM** | SQLAlchemy 2.0 | 强大的 ORM 库 |
| **定时任务** | APScheduler | 轻松实现定时任务 |
| **权限认证** | PyJWT | 实现 JWT 认证 |
| **前端框架** | Vue3 / Vite5 / Pinia / TypeScript | 快速开发 Vue3 应用 |
| **Web UI** | ElementPlus | 企业级 UI 组件库 |
| **移动端** | UniApp / Wot Design Uni | 跨端移动应用框架 |
| **数据库** | MySQL / PostgreSQL / Sqlite | 关系型和文档型数据库支持 |
| **缓存** | Redis | 高性能缓存数据库 |
| **文档** | Swagger / Redoc | 自动生成 API 文档 |
| **部署** | Docker / Nginx / Docker Compose | 容器化部署方案 |
| **智能体框架** | Langchain / Langgraph | 基于Langchain和Langgraph的智能体框架 |

## 📌 内置功能模块

| 模块 | 功能 | 描述 |
|------|------|------|
| 📊 **仪表盘** | 工作台、分析页 | 系统概览和数据分析 |
| ⚙️ **系统管理** | 用户、角色、菜单、部门、岗位、字典、配置、公告 | 核心系统管理功能 |
| 👀 **监控管理** | 在线用户、服务器监控、缓存监控 | 系统运行状态监控 |
| 📋 **任务管理** | 定时任务 | 异步任务调度管理 |
| 📝 **日志管理** | 操作日志 | 用户行为审计 |
| 🧰 **开发工具** | 代码生成、表单构建、接口文档 | 提升开发效率的工具 |
| 📁 **文件管理** | 文件存储 | 统一文件管理 |

## 🔧 模块展示

### web 端

| 模块名 <div style="width:60px"/> | 截图 |
| ----- | --- |
| 仪表盘   | ![仪表盘](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/dashboard.png) |
| 代码生成  | ![代码生成](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/gencode.png) |
| 智能助手  | ![智能助手](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/ai.png) |

### 移动端

| 登录 <div style="width:60px"/> | 首页 <div style="width:60px"/> | 个人中心 <div style="width:60px"/> |
|----------|----------|----------|
| ![移动端登录](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_login.png) | ![移动端首页](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_home.png) | ![移动端个人中心](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_mine.png) |
| 个人  |

## 🚀 快速开始

### 环境要求

| 类型 | 技术栈 | 版本 |
|------|--------|------|
| 后端 | Python | 3.12 ≥ 3.10 |
| 后端 | FastAPI | 0.109+ |
| 前端 | Node.js | ≥ 20.0 |
| 前端 | Vue3 | 3.3+ |
| 数据库 | MySQL/PostgreSQL | 8.0+/17+ |
| 缓存 | Redis | 7.0+ |

### 获取代码

```bash
# 克隆代码到本地
git clone https://gitee.com/tao__tao/FastapiAdmin.git
# 或者
git clone https://github.com/1014TaoTao/FastapiAdmin.git
```

> **后端注意**：克隆下的代码需要修改 `backend/env` 目录下的 `.env.dev.example` 文件为 `.env.dev`，修改 `backend/env` 目录下的 `.env.prod.example` 文件为 `.env.prod`，然后根据实际情况修改数据库连接信息、Redis连接信息等。

> **前端注意**：克隆下的代码需要修改 `frontend` 目录下的 `.env.development.example` 文件为 `.env.development`，修改 `frontend` 目录下的 `.env.production.example` 文件为 `.env.production`，然后根据实际情况修改接口地址等。

### 后端启动

#### 使用 uv 管理项目（推荐）

```bash
# 进入后端工程目录
cd backend
# 使用 uv 安装依赖
uv add -r requirements.txt
# 启动后端服务：启动之前保证mysql中创建好了数据库、redis服务
uv run main.py run
# 或指定环境
uv run main.py run --env=dev or --env=prod
```

#### 使用传统 pip 方式

```bash
# 进入后端工程目录
cd backend
# 安装依赖
pip3 install -r requirements.txt
# 启动后端服务：启动之前保证mysql中创建好了数据库、redis服务
python main.py run
# 或指定环境
python main.py run --env=dev or --env=prod
```

### 前端启动

```bash
# 进入前端工程目录
cd frontend
# 安装依赖
pnpm install
# 启动开发服务器
pnpm run dev
# 构建生产版本
pnpm run build
```

### 🐳 Docker 部署

```bash
# 复制部署脚本到服务器并赋予执行权限
chmod +x deploy.sh
# 执行一键部署
./deploy.sh or ./deploy.sh --start
# 查看容器日志
./deploy.sh --logs
# 停止服务
./deploy.sh --stop
```

## 🛠️ 二开教程

### 后端开发

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

#### 自动路由注册机制

系统会**自动发现并注册**所有符合以下条件的路由：
1. 控制器文件必须命名为 `controller.py`
2. 路由会自动映射：`module_xxx` -> `/xxx`
3. 支持多个 `APIRouter` 实例
4. 自动处理路由去重

#### 二次开发步骤

1. **创建插件模块**：在 `backend/app/plugin/` 目录下创建新的模块目录，如 `module_yourfeature`
2. **编写数据模型**：在 `model.py` 中定义数据库模型
3. **编写数据验证**：在 `schema.py` 中定义数据验证模型
4. **编写数据访问层**：在 `crud.py` 中编写数据库操作逻辑
5. **编写业务逻辑层**：在 `service.py` 中编写业务逻辑
6. **编写控制器**：在 `controller.py` 中定义路由和处理函数
7. **自动注册**：系统会自动扫描并注册所有路由，无需手动配置

#### 控制器示例

```python
# backend/app/plugin/module_yourfeature/yourcontroller/controller.py
from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import YourFeatureService

# 创建路由实例
YourFeatureRouter = APIRouter(
    route_class=OperationLogRoute, 
    prefix="/yourcontroller", 
    tags=["你的功能模块"]
)

@YourFeatureRouter.get("/detail/{id}", summary="获取详情")
async def get_detail(
    id: int = Path(..., description="功能ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_yourfeature:yourcontroller:detail"]))
) -> JSONResponse:
    result = await YourFeatureService.detail_service(id=id, auth=auth)
    return SuccessResponse(data=result)

@YourFeatureRouter.get("/list", summary="获取列表")
async def get_list(
    auth: AuthSchema = Depends(AuthPermission(["module_yourfeature:yourcontroller:list"]))
) -> JSONResponse:
    result = await YourFeatureService.list_service(auth=auth)
    return SuccessResponse(data=result)
```

#### 开发规范

1. **命名规范**：模块名采用 `module_xxx` 格式，控制器名采用驼峰命名法
2. **权限控制**：所有API接口必须添加权限控制装饰器
3. **日志记录**：使用 `OperationLogRoute` 类自动记录操作日志
4. **返回格式**：统一使用 `SuccessResponse` 或 `ErrorResponse` 返回响应
5. **代码注释**：为所有API接口添加详细的文档字符串

#### 注意事项

- 插件模块名必须以 `module_` 开头
- 控制器文件必须命名为 `controller.py`
- 路由会自动映射到对应的前缀路径
- 无需手动注册路由，系统会自动发现并注册

### 前端部分

1. **配置前端API**：在 `frontend/src/api/` 目录下创建对应的API文件
2. **编写页面组件**：在 `frontend/src/views/` 目录下创建页面组件
3. **注册路由**：在 `frontend/src/router/index.ts` 中注册路由

### 移动端部分

1. **配置移动端API**：在 `fastapp/src/api/` 目录下创建对应的API文件
2. **编写页面组件**：在 `fastapp/src/pages/` 目录下创建页面组件
3. **注册路由**：在 `fastapp/src/router/index.ts` 中注册路由

### 代码生成器使用

项目内置代码生成器，可以根据数据库表结构自动生成前后端代码，大幅提升开发效率。

#### 生成步骤

1. **登录系统**：使用管理员账号登录系统
2. **进入代码生成模块**：在左侧菜单中点击"代码生成"
3. **导入表结构**：选择要生成代码的数据库表
4. **配置生成参数**：填写模块名称、功能名称等
5. **生成代码**：点击"生成代码"按钮
6. **下载或写入**：选择下载代码包或直接写入项目目录

#### 生成文件结构

```sh
# 后端文件
backend/app/plugin/module_yourmodule/
└── yourfeature/
    ├── controller.py # 控制器文件
    ├── model.py      # 数据模型文件
    ├── schema.py     # 数据验证文件
    ├── service.py    # 业务逻辑文件
    └── crud.py       # 数据访问文件

# 前端文件
frontend/src/
├── api/module_yourmodule/
│   └── yourfeature.ts # API调用文件
└── views/module_yourmodule/
    └── yourfeature/
        └── index.vue # 页面组件
```

#### 生成代码示例

```python
# 生成的控制器代码示例
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import YourFeatureService
from .schema import (
    YourFeatureCreateSchema,
    YourFeatureUpdateSchema,
    YourFeatureQueryParam
)

YourFeatureRouter = APIRouter(
    route_class=OperationLogRoute, 
    prefix="/yourfeature", 
    tags=["你的功能模块"]
)

@YourFeatureRouter.get("/detail/{id}")
async def get_detail(
    id: int, 
    auth: AuthSchema = Depends(AuthPermission(["module_yourmodule:yourfeature:detail"]))
) -> JSONResponse:
    result = await YourFeatureService.detail_service(id=id, auth=auth)
    return SuccessResponse(data=result)
```

### 开发工具

- **代码生成器**：自动生成前后端CRUD代码
- **API文档**：自动生成Swagger/Redoc API文档
- **数据库迁移**：支持Alembic数据库迁移
- **日志系统**：内置日志记录和查询功能
- **监控系统**：内置服务器监控和缓存监控功能

### 开发流程

1. **需求分析**：明确功能需求和业务逻辑
2. **数据库设计**：设计数据库表结构
3. **代码生成**：使用代码生成器生成基础代码
4. **业务逻辑开发**：完善业务逻辑和接口
5. **前端开发**：开发前端页面和交互
6. **测试**：进行单元测试和集成测试
7. **部署**：部署到生产环境

### 开发注意事项

1. **权限控制**：所有API接口必须添加权限控制
2. **数据验证**：所有输入数据必须进行验证
3. **异常处理**：统一处理API异常
4. **日志记录**：关键操作必须记录日志
5. **性能优化**：注意API性能优化，避免慢查询
6. **代码规范**：遵循PEP8和项目代码规范

### 常见问题

#### Q：如何添加新功能模块？
A：按照二次开发步骤，在 `backend/app/plugin/` 目录下创建新的模块目录，编写相关代码即可。

#### Q：如何配置数据库？
A：在 `backend/env/.env.dev` 或 `backend/env/.env.prod` 文件中配置数据库连接信息。

#### Q：如何配置Redis？
A：在 `backend/env/.env.dev` 或 `backend/env/.env.prod` 文件中配置Redis连接信息。

#### Q：如何生成数据库迁移文件？
A：使用 `python main.py revision --env=dev` 命令生成迁移文件。

#### Q：如何应用数据库迁移？
A：使用 `python main.py upgrade --env=dev` 命令应用迁移。

#### Q：如何启动开发服务器？
A：使用 `python main.py run --env=dev` 命令启动开发服务器。

#### Q：如何构建前端生产版本？
A：使用 `pnpm run build` 命令构建前端生产版本。

#### Q：如何部署到生产环境？
A：使用 `./deploy.sh` 脚本一键部署到生产环境。

## ℹ️ 帮助

更多详情请查看 [官方文档](https://service.fastapiadmin.com)

## 👥 贡献者

<a href="https://github.com/1014TaoTao/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=1014TaoTao/FastapiAdmin"/>
</a>

## 🙏 特别鸣谢

感谢以下开源项目的贡献和支持：

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [APScheduler](https://github.com/agronholm/apscheduler)
- [Vue3](https://cn.vuejs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://github.com/vitejs/vite)
- [Element Plus](https://element-plus.org/)
- [UniApp](https://uniapp.dcloud.net.cn/)
- [Wot-Design-UI](https://wot-ui.cn/)

## 🎨 社区交流

| 群组二维码 | 微信支付二维码 |
| --- | --- |
| ![群组二维码](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/group.jpg) | ![微信支付二维码](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/wechatPay.jpg) |

## ❤️ 支持项目

如果你喜欢这个项目，请给我一个 ⭐️ Star 支持一下吧！非常感谢！

[![Stargazers over time](https://starchart.cc/1014TaoTao/FastapiAdmin.svg?variant=adaptive)](https://starchart.cc/1014TaoTao/FastapiAdmin)
