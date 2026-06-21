<div align="center">
     <p align="center">
          <img src="frontend/web/public/logo.svg" width="150" height="150" alt="logo" />
     </p>
     <h1>FastApiAdmin <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">v3.0.0</sup></h1>
     <h3>🚀 Exceptional Code Quality, Production-Ready Admin Dashboard in 5 Minutes</h3>
     <p>Full-stack rapid development platform powered by <b>FastAPI + Vue3 + TypeScript</b>. Web, H5, and Mini Program — all in one project.</p>
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

English | [简体中文](./README.md)

</div>

## 💡 Why FastapiAdmin?

| You Need | FastapiAdmin | Django Admin | Frontend-Only |
|----------|:-----------:|:-----------:|:-------------:|
| 🎯 **Ready-to-use** admin system | ✅ | ⚠️ Limited | ❌ UI only |
| ⚡ **FastAPI async** high-performance backend | ✅ | ❌ Sync-first | ❌ No backend |
| 🔐 **RBAC** menu/button/data level permissions | ✅ | ❌ Basic | ❌ |
| 🤖 **Code generator** (table → full CRUD) | ✅ | ❌ | ❌ |
| 📱 **Mobile** (H5 + Mini Program) included | ✅ | ❌ | ❌ |
| 🐳 **Docker** one-click deploy (Nginx + SSL) | ✅ | ❌ | ❌ |

> 👉 Full comparison: [Why FastapiAdmin?](https://service.fastapiadmin.com/en/guide/why)

## 🍪 Live Demo

| | URL | Account |
|---|-----|---------|
| 💻 Web | [service.fastapiadmin.com/web](https://service.fastapiadmin.com/web) | `admin` / `123456` |
| 📱 Mobile | [service.fastapiadmin.com/app](https://service.fastapiadmin.com/app) | `admin` / `123456` |
| 📖 Official Docs | [service.fastapiadmin.com](https://service.fastapiadmin.com) | No login |

## 🚀 5-Minute Quick Start

```bash
# 1. Clone
git clone https://github.com/fastapiadmin/FastapiAdmin.git

# 2. Configure environments
cp backend/env/.env.dev.example backend/env/.env.dev
cp frontend/web/.env.development.example frontend/web/.env.development

# 3. Start backend (auto-creates tables + seed data on first run)
cd backend && uv sync && uv run main.py run --env=dev

# 4. Start frontend
cd ../frontend/web && pnpm install && pnpm run dev

# ✅ Open http://127.0.0.1:5173, login with admin/123456
```

| Requirements | |
|-------------|------|
| Python ≥ 3.12 | Node.js ≥ 20 + pnpm |
| MySQL 8.0+ / PostgreSQL 14+ | Redis 6.x / 7.x |

## 📦 Structure

```
FastapiAdmin/            # Monorepo full-stack project
├─ backend/              # FastAPI backend (Pydantic 2.0 + SQLAlchemy + Alembic)
├─ frontend/
│   ├── web/             # Vue3 Web (Element Plus + TypeScript)
│   ├── app/             # UniApp Mobile (H5 + Mini Program + App)
│   └── docs/            # VitePress documentation
├─ docker/               # Docker Compose deploy (Nginx + SSL)
├─ deploy.sh             # One-click deploy script
└─ LICENSE               # MIT
```

## 📌 Built-in Features

| Module | Capabilities |
|--------|-------------|
| 📊 Dashboard | Workbench, Analytics |
| ⚙️ System | Users, Roles, Menus, Departments, Positions, Dicts, Config, Notices |
| 👀 Monitoring | Online users, Server, Cache |
| 📋 Tasks | Scheduled task management |
| 📝 Logs | Operation auditing |
| 🧰 Dev Tools | **Code Generator** (table → full CRUD), Form Builder, API Docs |
| 📁 Files | Unified file management |
| 🤖 AI Agent | Agno-powered assistant |

## 🔧 Screenshots

| Login | Dashboard | Code Generator | AI Assistant |
| ----- | --------- | -------------- | ------------ |
| ![Login](frontend/web/public/login.png) | ![Dashboard](frontend/web/public/dashboard.png) | ![Code Generator](frontend/web/public/gencode.png) | ![AI](frontend/web/public/ai.png) |

## 📖 Documentation

- 🌐 [Official Docs](https://service.fastapiadmin.com) — Full guides, architecture, custom development
- 📁 Sub-project READMEs: [backend](backend/README.md) · [web](frontend/web/README.md) · [mobile](frontend/app/README.md) · [Docker](docker/README.md)

## 🤝 Contributing

Issues and PRs are welcome! See [Contributing Guide](https://service.fastapiadmin.com/en/about/contributing).

## 👥 Community

| WeChat Group | Support |
| ------------ | ------- |
| ![Group QR](frontend/web/public/group.jpg) | ![WeChat Pay](frontend/web/public/wechatPay.jpg) |

> If you find this project useful, please give it a ⭐️ Star!

[![Stargazers over time](https://starchart.cc/fastapiadmin/FastapiAdmin.svg?variant=adaptive)](https://starchart.cc/fastapiadmin/FastapiAdmin)

## 👥 Contributors

<a href="https://github.com/fastapiadmin/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapiadmin/FastapiAdmin"/>
</a>

## 🙏 Acknowledgments

- Backend: [FastAPI](https://fastapi.tiangolo.com/) · [Pydantic](https://docs.pydantic.dev/) · [SQLAlchemy](https://www.sqlalchemy.org/) · [APScheduler](https://github.com/agronholm/apscheduler)
- Frontend: [Vue3](https://vuejs.org/) · [TypeScript](https://www.typescriptlang.org/) · [Vite](https://vitejs.dev/) · [Element Plus](https://element-plus.org/)
- Mobile: [UniApp](https://uniapp.dcloud.net.cn/) · [Wot Design Uni](https://wot-ui.cn/)
- AI: [Agno](https://github.com/agno-agi/agno)
