---
title: 项目概述
outline: "deep"
---

<div style="text-align: center;">
  <div align="center">
     <img src="/logo.png" width="150" height="150" alt="logo" />
  </div>
  <h1>FastApiAdmin <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">v2.0.0</sup></h1>
  <h3>一套现代、开源、全栈融合的中后台快速开发平台</h3>
  <p>如果你喜欢这个项目，给个 ⭐️ 支持一下吧！</p>
  <p align="center" style="display: flex; justify-content: center; align-items: center; margin-top: 10px;">
    <a href="https://gitee.com/fastapiadmin/FastapiAdmin"><img src="https://gitee.com/fastapiadmin/FastapiAdmin/badge/star.svg?theme=dark" alt="Gitee Stars"></a>
    <a href="https://github.com/fastapiadmin/FastapiAdmin"><img src="https://img.shields.io/github/stars/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Stars"></a>
    <a href="https://github.com/fastapiadmin/FastApp"><img src="https://img.shields.io/github/stars/fastapiadmin/FastApp?style=social" alt="FastApp Stars"></a>
    <a href="https://github.com/fastapiadmin/FastDocs"><img src="https://img.shields.io/github/stars/fastapiadmin/FastDocs?style=social" alt="FastDocs Stars"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License"></a>
    <img src="https://img.shields.io/badge/Python-≥3.10-blue" alt="Python">
    <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue" alt="NodeJS">
    <img src="https://img.shields.io/badge/MySQL-≥8.0-blue" alt="MySQL">
    <img src="https://img.shields.io/badge/Redis-≥7.0-blue" alt="Redis">
  </p>
</div>

## 📘项目介绍

**FastApiAdmin** 是一套 **完全开源、高度模块化、技术先进的现代化快速开发平台**，旨在帮助开发者高效搭建高质量的企业级中后台系统。该项目采用 **前后端分离架构**，融合 Python 后端框架 `FastAPI` 和前端主流框架 `Vue3` 实现多端统一开发，提供了一站式开箱即用的开发体验。

> **设计初心**: 以模块化、松耦合为核心，追求丰富的功能模块、简洁易用的接口、详尽的开发文档和便捷的维护方式。通过统一框架和组件，降低技术选型成本，遵循开发规范和设计模式，构建强大的代码分层模型，搭配完善的本地中文化支持，专为团队和企业开发场景量身定制。

## 📦工程结构概览

项目已拆分为三个独立的仓库，便于独立开发和维护：

### 1. FastapiAdmin 主工程

```sh
FastapiAdmin/
├─ backend/              # 后端工程
│  ├─ app/              # 应用核心代码
│  │  ├─ api/           # API 接口
│  │  │  └─ v1/         # API 版本
│  │  │     ├─ module_common/    # 公共模块
│  │  │     ├─ module_monitor/   # 监控模块
│  │  │     └─ module_system/    # 系统模块
│  │  ├─ common/        # 公共代码
│  │  ├─ config/        # 配置管理
│  │  ├─ core/          # 核心功能
│  │  ├─ plugin/        # 插件系统
│  │  │  ├─ module_application/  # 应用模块
│  │  │  ├─ module_example/      # 示例模块
│  │  │  └─ module_generator/    # 代码生成模块
│  │  ├─ scripts/       # 脚本工具
│  │  └─ utils/         # 工具函数
│  ├─ alembic/          # 数据库迁移
│  ├─ env/              # 环境配置
│  ├─ static/           # 静态资源
│  ├─ tests/            # 测试代码
│  ├─ README.md         # 后端文档
│  ├─ main.py           # 后端入口
│  └─ requirements.txt  # Python 依赖
├─ frontend/            # 前端工程
│  ├─ src/              # 源代码
│  │  ├─ api/           # API 接口
│  │  ├─ assets/        # 资源文件
│  │  ├─ components/    # 组件
│  │  ├─ composables/   # 组合式函数
│  │  ├─ constants/     # 常量定义
│  │  ├─ directives/    # 指令
│  │  ├─ enums/         # 枚举定义
│  │  ├─ lang/          # 国际化
│  │  ├─ layouts/       # 布局
│  │  ├─ plugins/       # 插件
│  │  ├─ router/        # 路由
│  │  ├─ store/         # 状态管理
│  │  ├─ styles/        # 样式
│  │  ├─ types/         # 类型定义
│  │  ├─ utils/         # 工具函数
│  │  └─ views/         # 页面
│  ├─ public/           # 静态资源
│  ├─ package.json      # 前端依赖
│  └─ README.md         # 前端文档
├─ devops/              # 部署工程
│  ├─ backend/          # 后端部署配置
│  ├─ nginx/            # Nginx 配置
│  └─ redis/            # Redis 配置
├─ docker-compose.yaml  # 部署文件
├─ deploy.sh            # 部署脚本
├─ LICENSE              # 许可协议
└─ README.md            # 项目文档
```

### 2. FastApp 移动端

```sh
FastApp/
├─ src/                 # 源代码目录
│  ├─ api/             # API 接口
│  │  ├─ auth.ts       # 认证相关接口
│  │  ├─ file.ts       # 文件相关接口
│  │  └─ user.ts       # 用户相关接口
│  ├─ components/      # 组件
│  │  ├─ cu-date-query/ # 日期查询组件
│  │  ├─ cu-picker/     # 选择器组件
│  │  ├─ qiun-error/    # 错误提示组件
│  │  └─ qiun-loading/  # 加载组件
│  ├─ composables/     # 组合式函数
│  │  ├─ useNavigationBar.ts # 导航栏管理
│  │  ├─ useStomp.ts   # WebSocket 管理
│  │  └─ useTabbar.ts  # 标签栏管理
│  ├─ constants/       # 常量定义
│  │  ├─ index.ts      # 常量定义
│  │  └─ storage.constant.ts # 存储键名
│  ├─ enums/           # 枚举定义
│  │  ├─ api-code.enum.ts # API 错误码
│  │  └─ api-header.enum.ts # API 头部
│  ├─ layouts/         # 布局组件
│  │  ├─ default.vue   # 默认布局
│  │  └─ tabbar.vue    # 标签栏布局
│  ├─ pages/           # 页面文件
│  │  ├─ index/        # 首页
│  │  │  ├─ data.ts     # 数据定义
│  │  │  ├─ index.vue   # 首页组件
│  │  │  └─ types.ts    # 类型定义
│  │  ├─ login/        # 登录页
│  │  │  └─ index.vue   # 登录组件
│  │  ├─ mine/         # 个人中心
│  │  │  ├─ about/      # 关于页面
│  │  │  ├─ faq/        # FAQ页面
│  │  │  ├─ feedback/   # 反馈页面
│  │  │  ├─ profile/    # 个人资料
│  │  │  ├─ settings/   # 设置页面
│  │  │  └─ index.vue   # 个人中心组件
│  │  └─ work/         # 工作台
│  │     ├─ data.ts     # 数据定义
│  │     ├─ index.vue   # 工作台组件
│  │     └─ types.ts    # 类型定义
│  ├─ router/          # 路由配置
│  │  └─ index.ts      # 路由配置文件
│  ├─ static/          # 静态资源
│  │  ├─ icons/        # 图标
│  │  ├─ images/       # 图片
│  │  └─ logo.png      # Logo
│  ├─ store/           # 状态管理
│  │  ├─ modules/      # 模块
│  │  │  ├─ theme.store.ts # 主题管理
│  │  │  └─ user.store.ts # 用户管理
│  │  └─ index.ts      # 状态管理配置
│  ├─ styles/          # 样式文件
│  │  └─ index.scss    # 全局样式
│  ├─ types/           # TypeScript 类型定义
│  ├─ utils/           # 工具函数
│  │  ├─ auth.ts       # 认证工具
│  │  ├─ color.ts      # 颜色工具
│  │  ├─ index.ts      # 工具函数
│  │  ├─ request.ts    # 请求工具
│  │  └─ storage.ts    # 存储工具
│  ├─ App.vue          # 应用根组件
│  ├─ main.ts          # 应用入口文件
│  ├─ manifest.json    # 应用配置文件
│  ├─ pages.json       # 页面路由配置
│  └─ theme.json       # 主题配置
├─ public/             # 静态资源
├─ .env.development    # 开发环境配置
├─ .env.production     # 生产环境配置
├─ package.json        # 项目依赖
├─ pages.config.ts     # 页面配置
├─ tsconfig.json       # TypeScript 配置
├─ unocss.config.ts    # UnoCSS 配置
└─ vite.config.ts      # Vite 配置
```

### 3. FastDocs 官网文档

```sh
FastDocs/
├─ docs/               # 文档源码
│  ├─ development/     # 开发文档
│  ├─ en/              # 英文文档
│  ├─ overview/        # 概述文档
│  ├─ quickstart/      # 快速开始
│  ├─ public/          # 静态资源
│  └─ index.md         # 首页
├─ .vitepress/         # VitePress 配置
│  ├─ theme/           # 主题配置
│  └─ config.ts        # 站点配置
├─ package.json        # 项目依赖
└─ README.md           # 项目文档
```

## ✨核心亮点

| 特性 | 描述 |
| ---- | ---- |
| 🔭 快速开发 | 一套完全开源的现代化快速开发平台，旨在帮助开发者高效搭建高质量的企业级中后台系统。 |
| 🌐 全栈整合 | 前后端分离，融合 Python (FastAPI) + Vue3 多端开发，支持 Web 端和移动端。 |
| 🧱 模块化设计 | 系统功能高度解耦，插件化架构，支持自动路由发现和注册，便于扩展和维护。 |
| ⚡️ 高性能异步 | 使用 FastAPI 异步框架 + Redis 缓存优化接口响应速度。 |
| 🔒 安全认证 | 支持 JWT OAuth2 认证机制，保障系统安全。 |
| 📊 权限管理 | RBAC 模型实现菜单、按钮、数据级别的细粒度权限控制。 |
| 🚀 快速部署 | 支持 Docker/Docker Compose/Nginx 一键部署。 |
| 📄 开发友好 | 提供完善的中文文档 + 中文化界面 + 可视化工具链，降低学习成本。 |
| 🧩 快速接入 | 基于 Vue3、Vite5、Pinia、ElementPlus 等主流前端技术栈，开箱即用。 |
| 📱 移动端支持 | 基于 UniApp 开发的 FastApp 移动端，支持多端运行（H5、微信小程序、支付宝小程序、App 等）。 |
| 🤖 智能体框架 | 集成智能体框架，提供 AI 能力。 |
| 🎨 主题定制 | 支持深色/浅色主题切换，提供个性化界面体验。 |
| 🌍 国际化支持 | 内置国际化框架，支持多语言切换。 |
| 📈 数据可视化 | 集成图表库，提供丰富的数据可视化能力。 |
| 🛠️ 代码生成 | 内置代码生成工具，提升开发效率。 |

## 🛠️技术栈概览

| 类型     | 技术选型            | 描述 |
|----------|---------------------|---------------------|
| 后端框架 | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | 现代、高性能的异步框架，强制类型约束，数据迁移。 |
| ORM      | SQLAlchemy 2.0      | 强大的 ORM 库。 |
| 定时任务 | APScheduler         | 轻松实现定时任务。 |
| 权限认证 | PyJWT               | 实现 JWT 认证。 |
| 前端框架 | Vue3 / Vite5 / Pinia / TypeScript | 快速开发 Vue3 应用。 |
| 前端工具 | ESLint / Prettier / Stylelint | 代码质量和风格工具。 |
| 移动端框架 | UniApp / Vue3 / TypeScript | 跨平台移动应用开发。 |
| UI 库    | ElementPlus (Web) / Wot Design Uni (移动端) | 企业级 UI 组件库。 |
| CSS 框架 | UnoCSS / SCSS       | 原子化 CSS 和预处理器。 |
| 数据库   | MySQL / PostgreSQL / SQLite | 关系型数据库支持。 |
| 缓存     | Redis               | 强大的缓存数据库。 |
| 文档     | Swagger / Redoc     | 自动生成 API 文档。 |
| 部署     | Docker / Nginx / Docker Compose | 快速部署项目。 |
| 监控     | 内置服务器监控 / 缓存监控 | 系统运行状态监控。 |
| 国际化   | i18n                | 多语言支持。 |
| 数据可视化 | ECharts             | 图表库。 |

## 📌内置模块

### FastapiAdmin 主工程模块

| 模块名     | 子模块名 | 描述 |
|----------|---------------------|---------------------|
| 仪表盘    | 工作台、分析页 | 系统概览和数据分析 |
| 系统管理  | 用户、角色、菜单、部门、岗位、字典、配置、公告 | 核心系统管理功能 |
| 监控管理  | 在线用户、服务器监控、缓存监控 | 系统运行状态监控 |
| 任务管理  | 定时任务 | 异步任务调度管理 |
| 日志管理  | 操作日志 | 用户行为审计 |
| 开发工具  | 代码生成、表单构建、接口文档 | 提升开发效率的工具 |

### FastApp 移动端模块

| 模块名     | 子模块名 | 描述 |
|----------|---------------------|---------------------|
| 首页      | 轮播图、快捷导航、通知公告、数据统计 | 移动端首页展示 |
| 工作台    | 业务功能入口，支持权限控制 | 移动端核心功能区 |
| 个人中心  | 个人信息、设置、FAQ、问题反馈 | 用户个人相关功能 |
| 用户认证  | 登录、注册、密码重置 | 用户身份验证 |
| 数据统计  | 实时访客数、浏览量等数据展示 | 业务数据可视化 |