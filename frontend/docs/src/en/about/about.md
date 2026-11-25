---
layout: doc
title: About Us
editLink: true
lastUpdated: true
---

## Project Background

FastapiAdmin was born from a recurring pain in enterprise admin development: under the front-end/back-end separation architecture, even a simple CRUD page requires touching multiple directories, files, and technology stacks. The development experience is fragmented, and collaboration costs are high.

Traditional admin solutions (like Django Admin) are limited in functionality and hard to customize. Pure front-end templates (like AdminLTE, Ant Design Pro) lack backend support, requiring you to build the API layer from scratch. The market was missing a **truly out-of-the-box, full-stack, AI-capable** enterprise admin platform.

FastapiAdmin's mission: spin up a working MVP in 15-30 minutes; routine CRUD is auto-generated so the team can focus on what makes the product unique.

## Technical Philosophy

### ⚡ Full-Stack Async + High Performance

The backend uses FastAPI's native async/await architecture with Pydantic v2 auto-type validation and Redis caching for system performance from the ground up. The frontend is built with Vue3 + TypeScript for type-safe, component-driven development.

### 🧩 Vertical Slice Architecture

Instead of traditional layered architecture (Controller → Service → DAO), FastapiAdmin organizes code by business domain using Vertical Slice. Each module contains its own Controller, Service, Model, and Schema — zero coupling between modules. Multiple developers can work in parallel without conflicts, and extracting a module into a microservice is as simple as moving one directory.

### 🤖 AI-Powered Development

Starting from v2.0, the AI Code Generator allows you to select a database table and have AI automatically generate full CRUD code (Controller / Service / Model / Vue pages) — in practice this covers roughly 90% of routine CRUD, with the remaining 10% requiring customisation.

### 📱 Multi-Platform Delivery

Built on UniApp, one codebase generates H5, WeChat Mini Program, Alipay Mini Program, and native App simultaneously. The backend API layer naturally supports multi-platform reuse without duplicating interfaces.

## Project Highlights

| Dimension | Description |
|-----------|-------------|
| 🏗️ Architecture | Vertical Slice + modular design, flexible between monolith and microservices |
| 🔐 Permission | RBAC with three granularities (menu / button / data), JWT + OAuth2 dual auth |
| 🤖 AI Engine | Data-model-driven code generation, one-click CRUD for frontend + backend |
| 🐳 Deployment | Docker Compose orchestration (Nginx + SSL included), multi-env config management |
| 🧪 Quality | Comprehensive unit & integration tests, CI/CD automation |
| 📖 Documentation | Bilingual (CN/EN), from overview to custom development, with code examples |
| 📜 License | MIT — fully open, free to use and commercialize |

## Milestones

> Version history is strictly aligned with [CHANGELOG.md](/en/guide/changelog) to avoid drift.

**v1.0 (2024-08)** — Initial open-source release: Flask backend + Vue2 + Element UI monolithic architecture, with 12 core business modules built in.

**v2.0 (2025-02)** — Migrated backend from Flask to FastAPI async + Pydantic, fully decoupled frontend and backend, SQLAlchemy 2.0 + Alembic, Docker multi-stage build.

**v2.1 (2025-06)** — Frontend rewritten from Vue2 to Vue3 + TypeScript + Element Plus + Vite, complete engineering toolchain.

**v2.2 (2025-09)** — Code Generator 1.0 released (select table → auto-generate full-stack CRUD), System Config Center, three-channel notifications.

**v2.3 (2025-12)** — Server monitoring panel, Redis cache monitoring, APScheduler visual scheduled task management.

**v2.4 (2026-03)** — WebSocket real-time notifications, operation audit logs, OAuth2 authentication, RBAC granular to button level.

**v3.0 (2026-07)** — Vertical Slice refactor, UniApp mobile 1.0, enhanced code generator, AI integration across the stack.

> For the full milestone and future plans, see the [Roadmap](/en/guide/start) and [Changelog](/en/guide/changelog).

## Community Values

- **Open & Shared** — MIT license, fully open code, contributions and commercial use encouraged
- **Practical & Efficient** — No over-engineering, every line solves a real problem
- **Continuous Evolution** — Stay on the cutting edge, regular releases, ongoing iteration
- **Ecosystem Co-creation** — Issues, PRs, feature requests welcome — every contributor matters

## Roadmap

FastapiAdmin will continue to invest in:

- **Deep AI Integration** — From code generation to intelligent testing, auto deployment, smart ops
- **Low-Code Capabilities** — Visual form designer, workflow orchestration, report configuration
- **Plugin Ecosystem** — Official plugin marketplace supporting community extensions
- **Continuous Performance Optimization** — Cold start optimization, cache strategy upgrades, edge deployment support

## Team

We are an open-source team dedicated to building high-quality developer tools and solutions.

### Core Members

- **[@fastapiadmin](https://gitee.com/fastapiadmin)** — Project founder, enterprise system architecture

### Special Thanks

To every developer who has participated through Stars, Issues, and PRs — your one-click star, a single bug report, one line of code contribution — all of these make this project better.

Want to contribute? Feel free to participate via GitHub Issues or PRs.

## Contact

- **QQ**: 948080782
- **Email**: [948080782@qq.com](mailto:948080782@qq.com)

## Repositories

| Platform | Link |
|----------|------|
| GitHub | [FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin) |
| Gitee | [FastapiAdmin](https://gitee.com/fastapiadmin/FastapiAdmin) |
| AtomGit | [FastapiAdmin](https://atomgit.com/fastapiadmin/FastapiAdmin) |

If FastapiAdmin helps you, feel free to follow and support the project's development ❤️
