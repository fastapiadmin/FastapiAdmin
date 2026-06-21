<div align="center">
     <p align="center">
          <img src="frontend/web/public/logo.svg" width="150" height="150" alt="logo" />
     </p>
     <h1>FastApiAdmin <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">v3.0.0</sup></h1>
     <h3>🚀 追求极致代码质量，五分钟搭建企业级中后台，开箱即用</h3>
     <p>基于 <b>FastAPI + Vue3 + TypeScript</b> 的全栈快速开发平台，Web / H5 / 小程序一站式交付</p>
     <p align="center">
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://gitee.com/fastapiadmin/FastapiAdmin/badge/star.svg?theme=dark" alt="Gitee Stars">
          </a>
          <a href="https://github.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://img.shields.io/github/stars/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Stars">
          </a>
          <a href="https://github.com/fastapiadmin/FastapiAdmin/forks" target="_blank">
               <img src="https://img.shields.io/github/forks/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Forks">
          </a>
          <br>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank">
               <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
          </a>
          <img src="https://img.shields.io/badge/Python-≥3.12-blue">
          <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue">
          <img src="https://img.shields.io/badge/MySQL-≥8.0-blue">
          <img src="https://img.shields.io/badge/Redis-≥7.0-blue">
     </p>

简体中文 | [English](./README.en.md)

</div>

## 💡 为什么选择 FastapiAdmin？

| 你需要的 | FastapiAdmin | Django Admin | 纯前端模板 |
|---------|:-----------:|:-----------:|:---------:|
| 🎯 **开箱即用**的后台系统 | ✅ | ⚠️ 功能有限 | ❌ 只有 UI |
| ⚡ **FastAPI 异步**高性能后端 | ✅ | ❌ 同步为主 | ❌ 无后端 |
| 🔐 **RBAC** 菜单/按钮/数据三级权限 | ✅ | ❌ 基础 | ❌ |
| 🏢 **多租户 SaaS** 数据隔离 + 配额 + 个性化 | ✅ | ❌ | ❌ |
| 🤖 **代码生成器**（选表 → 出前后端代码） | ✅ | ❌ | ❌ |
| 📱 **移动端**（H5 + 小程序）一体 | ✅ | ❌ | ❌ |
| 🐳 **Docker 一键部署**（含 Nginx + SSL） | ✅ | ❌ | ❌ |

> 👉 详细技术选型对比：[为什么选择 FastapiAdmin？](https://service.fastapiadmin.com/guide/why)

## 🍪 在线体验

| 端 | 地址 | 账号 |
|----|------|------|
| 💻 Web 端 | [service.fastapiadmin.com/web](https://service.fastapiadmin.com/web) | `admin` / `123456` |
| 📱 移动端 | [service.fastapiadmin.com/app](https://service.fastapiadmin.com/app) | `admin` / `123456` |
| 📖 官方文档 | [service.fastapiadmin.com](https://service.fastapiadmin.com) | 无需登录 |

## 🚀 5 分钟本地跑起来

```bash
# 1. 克隆
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git

# 2. 配置环境
cp backend/env/.env.dev.example backend/env/.env.dev
cp frontend/web/.env.development.example frontend/web/.env.development

# 3. 启动后端（首次自动建表 + 初始化数据）
cd backend && uv sync && uv run main.py run --env=dev

# 4. 启动前端
cd ../frontend/web && pnpm install && pnpm run dev

# ✅ 浏览器打开 http://127.0.0.1:5173，用 admin/123456 登录
```

| 环境要求 | |
|---------|------|
| Python ≥ 3.12 | Node.js ≥ 20.0 + pnpm |
| MySQL 8.0+ / PostgreSQL 14+ | Redis 6.x / 7.x |

## 📦 工程结构

```
FastapiAdmin/            # Monorepo 全栈工程
├─ backend/              # FastAPI 后端（Pydantic 2.0 + SQLAlchemy + Alembic）
├─ frontend/
│   ├── web/             # Vue3 Web 前端（Element Plus + TypeScript）
│   ├── app/             # UniApp 移动端（H5 + 小程序 + App）
│   └── docs/            # VitePress 文档网站
├─ docker/               # Docker Compose 一键部署（Nginx + SSL）
├─ deploy.sh             # 一键部署脚本
└─ LICENSE               # MIT 开源协议
```

## 📌 内置功能（开箱即用）

| 模块 | 包含能力 |
|------|---------|
| 📊 仪表盘 | 工作台、数据分析 |
| ⚙️ 系统管理 | 用户 / 角色 / 菜单 / 部门 / 岗位 / 字典 / 配置 / 公告 |
| 🏢 多租户 | 租户管理 / 数据隔离 / 配额控制 / 个性化配置 / 菜单权限 |
| 👀 监控管理 | 在线用户 / 服务器监控 / 缓存监控 |
| 📋 任务管理 | 定时任务调度 |
| 📝 日志管理 | 操作日志审计 |
| 🧰 开发工具 | 代码生成、表单构建、接口文档 |
| 📁 文件管理 | 统一文件管理 |
| 🤖 智能体 | 基于 Agno 的智能体框架 |

## 🔧 截图展示

| 登录 | 仪表盘 | 代码生成 | AI 助手 |
| ---- | ------ | -------- | ------- |
| ![登录](frontend/web/public/login.png) | ![仪表盘](frontend/web/public/dashboard.png) | ![代码生成](frontend/web/public/gencode.png) | ![AI](frontend/web/public/ai.png) |

## 📖 文档地址

- 🌐 [官网文档](https://service.fastapiadmin.com) — 完整开发指南、架构设计、二开教程
- 📁 子工程 README：[backend](backend/README.md) · [web](frontend/web/README.md) · [移动端](frontend/app/README.md) · [Docker](docker/README.md)

## 🤝 参与贡献

欢迎提交 Issue / PR！详见 [贡献指南](https://service.fastapiadmin.com/about/contributing)。

## 👥 社区与支持

| 微信群 | 赞赏支持 |
| ------ | -------- |
| ![群组二维码](frontend/web/public/group.jpg) | ![微信支付](frontend/web/public/wechatPay.jpg) |

> 如果你觉得项目有用，请给一个 ⭐️ Star 支持！

[![Stargazers over time](https://starchart.cc/fastapiadmin/FastapiAdmin.svg?variant=adaptive)](https://starchart.cc/fastapiadmin/FastapiAdmin)

## 👥 贡献者

<a href="https://github.com/fastapiadmin/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapiadmin/FastapiAdmin"/>
</a>

## 🙏 鸣谢

- 后端：[FastAPI](https://fastapi.tiangolo.com/) · [Pydantic](https://docs.pydantic.dev/) · [SQLAlchemy](https://www.sqlalchemy.org/) · [APScheduler](https://github.com/agronholm/apscheduler)
- 前端：[Vue3](https://cn.vuejs.org/) · [TypeScript](https://www.typescriptlang.org/) · [Vite](https://vitejs.dev/) · [Element Plus](https://element-plus.org/)
- 移动端：[UniApp](https://uniapp.dcloud.net.cn/) · [Wot Design Uni](https://wot-ui.cn/)
- AI：[Agno](https://github.com/agno-agi/agno)
