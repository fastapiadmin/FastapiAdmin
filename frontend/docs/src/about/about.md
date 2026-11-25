---
layout: doc
title: 关于我们
editLink: true
lastUpdated: true
---

## 项目背景

FastapiAdmin 诞生于企业级中后台开发中反复出现的痛点：前后端分离架构下，一个简单的 CRUD 页面需要跨越多个目录、多个文件、多种技术栈，开发体验割裂，协作成本高昂。

传统的 Admin 方案（如 Django Admin）功能受限且难以定制；纯前端模板（如 AdminLTE、Ant Design Pro）没有后端支撑，仍需从零搭建 API 层。市场缺少一个**真正开箱即用、全栈一体、且具备 AI 能力**的企业级后台解决方案。

FastapiAdmin 的目标是:用 15-30 分钟跑通一个可演示的 MVP,核心 CRUD 不用手写,团队聚焦业务定制。

## 技术理念

### ⚡ 全栈异步 + 高性能

后端采用 FastAPI 原生 async/await 架构，配合 Pydantic v2 自动类型校验与 Redis 缓存加速，从底层保障系统性能。前端基于 Vue3 + TypeScript 构建，组件化开发、类型安全，兼顾开发体验与运行效率。

### 🧩 Vertical Slice 竖切架构

摒弃传统的分层架构（Controller → Service → DAO），采用 Vertical Slice 架构按业务领域组织代码。每个模块自包含完整的 Controller、Service、Model、Schema，模块边界清晰、依赖最小化。多人协作时互不干扰，需要拆分独立微服务时直接整目录搬走。

### 🤖 AI 驱动的开发效率

从 2.0 版本开始引入 AI 代码生成器：选择数据库表 → AI 自动生成前后端完整 CRUD 代码（Controller / Service / Model / Vue 页面）。实践中可覆盖约 90% 的常规 CRUD，剩余 10% 仍需定制开发。

### 📱 多端统一交付

基于 UniApp 的移动端方案，一套代码同时生成 H5、微信小程序、支付宝小程序、App 等多端应用。后端 API 层天然支持多端复用，无需为每个端重复开发同一套接口。

## 项目亮点

| 维度 | 说明 |
|------|------|
| 🏗️ 架构模式 | Vertical Slice + 模块化，支持单体与微服务灵活切换 |
| 🔐 权限体系 | RBAC 三级粒度（菜单 / 按钮 / 数据），JWT + OAuth2 双认证 |
| 🤖 AI 能力 | 数据模型驱动代码生成，前后端 CRUD 一键生成 |
| 🐳 部署运维 | Docker Compose 全栈编排（含 Nginx + SSL），多环境配置管理 |
| 🧪 质量保障 | 完整的单元测试、集成测试体系，CI/CD 自动化 |
| 📖 文档体系 | 中英双语文档，从概述到二开的完整教程，配套示例代码 |
| 📜 开源协议 | MIT 协议，完全开放，可自由使用和商用 |

## 发展历程

> 历史版本与 `changelog.md` 严格对齐(避免"装嫩",详情见 [CHANGELOG](/guide/changelog))

**v1.0 (2024-08)** — 项目首版开源:Flask 后端 + Vue2 + Element UI 单体架构,内置 12 个核心业务模块。

**v2.0 (2025-02)** — 后端从 Flask 迁移到 FastAPI 异步 + Pydantic,前后端彻底分离,SQLAlchemy 2.0 + Alembic 迁移,Docker 多阶段构建。

**v2.1 (2025-06)** — 前端从 Vue2 重写为 Vue3 + TypeScript + Element Plus + Vite,完整工程化工具链。

**v2.2 (2025-09)** — 代码生成器 1.0 上线(选表 → 自动生成前后端 CRUD),系统配置中心,三通道通知。

**v2.3 (2025-12)** — 服务监控面板、Redis 缓存监控、APScheduler 可视化定时任务。

**v2.4 (2026-03)** — WebSocket 实时通知、操作日志审计、OAuth2 认证、RBAC 细化到按钮级。

**v3.0 (2026-07)** — Vertical Slice 重构,UniApp 移动端 1.0 上线,代码生成器增强,AI 全场景集成。

> 完整里程碑与未来规划见 [路线图](#/guide/start) 与 [更新日志](/guide/changelog)。

## 社区价值观

- **开放共享** — MIT 协议，代码完全开放，鼓励社区贡献和商业使用
- **务实高效** — 不做过度设计，每一行代码都为解决实际问题
- **持续进化** — 紧跟技术前沿，定期发布版本，持续迭代优化
- **生态共建** — 欢迎 Issue、PR、功能建议，每一位贡献者都是项目的一部分

## 展望未来

FastapiAdmin 将持续在以下方向深耕：

- **深度 AI 集成** — 从代码生成延伸到智能测试、自动部署、智能运维
- **低代码能力** — 可视化表单设计、工作流编排、报表配置
- **生态插件** — 官方插件市场，支持社区开发扩展
- **性能持续优化** — 冷启动优化、缓存策略升级、边缘部署支持

## 团队介绍

我们是一支热爱开源的团队，致力于为开发者提供高质量的开发工具和解决方案。

### 核心成员

- **[@fastapiadmin](https://gitee.com/fastapiadmin)** — 项目创始人，深耕企业级系统架构多年

### 特别感谢

感谢每一位通过 Star、Issue、PR 参与项目的开发者。你的一键 Star、一次 Bug 反馈、一行代码贡献，都在推动这个项目变得更好。

想要参与贡献？欢迎通过 GitHub Issues 或 PR 参与到项目中来。

## 联系方式

- **QQ**：948080782
- **邮箱**：[948080782@qq.com](mailto:948080782@qq.com)

## 项目仓库

| 平台 | 地址 |
| ------ | ------ |
| GitHub | [FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin) |
| Gitee | [FastapiAdmin](https://gitee.com/fastapiadmin/FastapiAdmin) |
| AtomGit | [FastapiAdmin](https://atomgit.com/fastapiadmin/FastapiAdmin) |

如果 FastapiAdmin 对你有帮助，欢迎持续关注和支持项目发展 ❤️
