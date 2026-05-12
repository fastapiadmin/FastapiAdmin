<div align="center">
     <p align="center">
          <img src="backend/data/logo.png" width="150" height="150" alt="logo" /> 
     </p>
     <h1>FastApiAdmin <img src="https://img.shields.io/badge/Version-v2.0.0-blue" alt="Version"></h1>
     <h3>Modern Full-Stack Rapid Development Platform</h3>
     <p>If you like this project, please give it a ⭐️ to show your support!</p>
     <p align="center">
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://gitee.com/fastapiadmin/FastapiAdmin/badge/star.svg?theme=dark" alt="Gitee Stars">
          </a>
          <a href="https://github.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://img.shields.io/github/stars/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Stars">
          </a>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank">
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

English | [简体中文](./README.md)

</div>

## 📘 Project Introduction

**FastApiAdmin** is a **completely open-source, highly modular, and technologically advanced modern rapid development platform** designed to help developers efficiently build high-quality enterprise-level backend and frontend systems. This project adopts a **frontend-backend separation architecture**, integrating the Python backend framework `FastAPI` and the mainstream frontend framework `Vue3` to achieve unified development across multiple terminals, providing a one-stop out-of-the-box development experience.

> **Design Philosophy**: With modularity and loose coupling at its core, it pursues rich functional modules, simple and easy-to-use interfaces, detailed development documentation, and convenient maintenance methods. By unifying frameworks and components, it reduces the cost of technology selection, follows development specifications and design patterns, builds a powerful code hierarchical model, and comes with comprehensive local language support. It is specifically tailored for team and enterprise development scenarios.

<a id="packaging-philosophy"></a>

## 📐 Packaging philosophy: two layouts and this project’s choice

This is about **how source directories are split** (package by feature vs by layer), not whether the code uses MVC or Controller–Service–CRUD **logic layers**—those layers still exist in this project; the difference is the **first** split: by business domain or by technical tier.

| Approach | Idea | Typical layout (example) |
|----------|------|---------------------------|
| **Package by layer** | Group files by technical role | Top-level `models/`, `schemas/`, `cruds/`, `services/`, `controllers/`, … |
| **Package by feature** (vertical slice) | Group files by business domain | Under `app/api/v1/module_*/<domain>/`: `controller.py`, `service.py`, `crud.py`, `model.py`, `schema.py`; optional features under `app/plugin/...` |

**This project (backend) uses: package by feature (vertical slices).**

**Why (design intent)**

- **Decoupling follows business boundaries**: modules such as system admin, monitoring, and business subdomains; collaborators touch different folders instead of one global `models/` / `services/`.
- **Future extraction**: moving a module to its own repo or package is naturally **one tree**; layer-first layouts often require pulling files from many top-level folders.
- **Layers are not gone**: Controller → Service → CRUD → Model / Schema still applies **inside** each domain package, not as the only top-level organization.

**Trade-off**: layer-first can suit small teams that want to browse one technical tier at a glance; this project prioritizes **domain decoupling** and **parallel work by module**. For schema overview, use IDE, DB tools, and Alembic rather than switching to a single global `models/` tree.

---

## 📖 Start Here (New Users)

| I want to… | Go to |
|------------|--------|
| **Run the project locally ASAP** | **Quick Start** → **“First-time local setup (in order)”** (env, deps, run; **first backend start auto-inits DB schema & seed data**) |
| **Architecture diagram & default ports (5180 / 8001, …)** | **“Local Architecture & Default Ports”** (matches `.env*.example`) |
| **See what the project offers** | **Built-in Functional Modules**, **Demo Environment** (credentials) |
| **Extend / plugin development** | **Secondary Development Tutorial**; **[Packaging philosophy](#packaging-philosophy)**; backend layout & CLI: [**backend/README.md**](backend/README.md) |
| **API docs** | With template env: **`http://127.0.0.1:8001/docs`** (see `SERVER_PORT`) |

## 🎯 Core Advantages

| Advantage | Description |
| ---- | ---- |
| 🔥 **Modern Tech Stack** | Built with cutting-edge technologies like FastAPI + Vue3 + TypeScript |
| ⚡ **High Performance** | Leveraging FastAPI's asynchronous features and Redis caching for optimized response speed |
| 🔐 **Secure & Reliable** | JWT + OAuth2 authentication mechanism with RBAC permission control model |
| 🧱 **Modular Design** | Highly decoupled system architecture for easy expansion and maintenance |
| 🌐 **Full-Stack Support** | Integrated solution for Web + Mobile(H5) + Backend |
| 🚀 **Rapid Deployment** | One-click Docker deployment for quick production rollout |
| 📖 **Comprehensive Docs** | Detailed documentation and tutorials to reduce learning curve |
| 🤖 **Intelligent Agent Framework** | Based on Agno, develop intelligent agents |

## 🍪 Demo Environment

- 💻 Web: [https://service.fastapiadmin.com/web](https://service.fastapiadmin.com/web)
- 📱 Mobile: [https://service.fastapiadmin.com/app](https://service.fastapiadmin.com/app)
- 👤 Login Account: `admin` Password: `123456`

## 🔗 Source Repositories

| Platform | Repository |
|----------|------------|
| GitHub | [FastapiAdmin Main](https://github.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs Website](https://github.com/fastapiadmin/FastDocs.git) \| [FastApp Mobile](https://github.com/fastapiadmin/FastApp.git) |
| Gitee  | [FastapiAdmin Main](https://gitee.com/fastapiadmin/FastapiAdmin.git) \| [FastDocs Website](https://gitee.com/fastapiadmin/FastDocs.git) \| [FastApp Mobile](https://gitee.com/fastapiadmin/FastApp.git) |

## 📦 Engineering Structure Overview

```sh
FastapiAdmin
├─ backend               # Backend project (FastAPI + Python)
├─ frontend              # Frontend project directory
│   ├── web              # Web frontend (Vue3 + Element Plus)
│   ├── app              # Mobile (UniApp)
│   └── docs             # Documentation site (VitePress)
├─ docker                # Docker configuration
│   ├── backend          # Backend Dockerfile
│   ├── nginx            # Nginx configuration and static files
│   ├── mysql            # MySQL data directory
│   └── redis            # Redis data directory
├─ deploy.sh             # One-click deployment script (Linux)
├─ deploy.bat            # One-click startup script (Windows)
├─ LICENSE               # Open source license
|─ README.en.md          # English documentation
└─ README.md             # Chinese documentation
```

## 🏗️ Local Architecture & Default Ports

Aligned with **`backend/env/.env.dev.example`** and **`frontend/web/.env.development`**; if you changed `.env.dev` / `.env.development`, use your local values.

```mermaid
flowchart LR
  subgraph client[Browser]
    U[User]
  end
  subgraph fe[Frontend Development]
    V[Vue3 Web] -->|5173| U
    A[UniApp H5] -->|8080| U
    D[VitePress Docs] -->|5174| U
  end
  subgraph be[Backend]
    F[FastAPI / Uvicorn] -->|8001| V
    F -->|8001| A
    F -->|8001| D
  end
  subgraph data[Data Layer]
    DB[(Database)]
    R[(Redis)]
  end
  F --> DB
  F --> R
```

| Component | Config key | Example default (dev template) |
|-------------|------------|--------------------------------|
| Web Frontend | `frontend/web/.env.development` → `VITE_PORT` | **5173** → **`http://127.0.0.1:5173`** |
| Mobile H5 | `frontend/app` dev server | **8080** → **`http://127.0.0.1:8080`** |
| Docs Site | `frontend/docs` dev server | **5174** → **`http://127.0.0.1:5174`** |
| Backend HTTP | `backend/env/.env.dev` → `SERVER_HOST` / `SERVER_PORT` | **`0.0.0.0:8001`** → **`http://127.0.0.1:8001`** |
| API base URL | `VITE_API_BASE_URL` | **`http://127.0.0.1:8001`** |
| API prefix | `ROOT_PATH` (backend) | **`/api/v1`** |
| Swagger / Redoc | — | **`http://127.0.0.1:8001/docs`**, `/redoc` |
| WebSocket (optional) | `VITE_APP_WS_ENDPOINT` | e.g. **`ws://127.0.0.1:8001`** |
| DB port | `DATABASE_PORT` | Template uses MySQL **`3306`**; PostgreSQL often **`5432`** |
| Redis | `REDIS_HOST` / `REDIS_PORT` | Example **`localhost:6379`** |

## 🛠️ Technology Stack Overview

| Type | Technology Selection | Description |
|------|----------------------|-------------|
| **Backend Framework** | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | Modern, high-performance asynchronous framework with mandatory type constraints and data migration capabilities |
| **ORM** | SQLAlchemy 2.0 | Powerful ORM library |
| **Scheduled Tasks** | APScheduler | Easily implement scheduled tasks |
| **Authentication** | PyJWT | Implement JWT authentication |
| **Frontend Framework** | Vue3 / Vite5 / Pinia / TypeScript | Rapidly develop Vue3 applications |
| **Web UI** | ElementPlus | Enterprise-level UI component library |
| **Mobile** | UniApp / Wot Design Uni | Cross-platform mobile application framework |
| **Database** | MySQL / PostgreSQL / Sqlite | Support for relational and document databases |
| **Cache** | Redis | High-performance cache database |
| **Documentation** | Swagger / Redoc | Automatically generate API documentation |
| **Deployment** | Docker / Nginx / Docker Compose | Containerized deployment solution |
| **Intelligent Agent Framework** | Agno | Intelligent agent framework based on Agno |

## 📐 Backend Conventions (Dates & Serialization)

With **Pydantic v2** and **PostgreSQL (asyncpg)**, ORM writes expect native Python date/time types; JSON responses need serializable strings. The project uses **`PlainSerializer(..., when_used='json')`** on `DateStr` / `TimeStr` / `DateTimeStr` in `backend/app/core/validator.py`; unified responses use **`jsonable_encoder`** in `backend/app/common/response.py`; when writing to Redis, use **`model_dump(mode='json')`** before `json.dumps`. See [backend/README.md](backend/README.md) for alignment with the root README.

## 📌 Built-in Functional Modules

| Module | Features | Description |
|------|------|------|
| 📊 **Dashboard** | Workbench, Analysis Page | System overview and data analysis |
| ⚙️ **System Management** | Users, Roles, Menus, Departments, Positions, Dictionaries, Configurations, Announcements | Core system management functions |
| 👀 **Monitoring** | Online Users, Server Monitoring, Cache Monitoring | System runtime status monitoring |
| 📋 **Task Management** | Scheduled Tasks | Asynchronous task scheduling management |
| 📝 **Log Management** | Operation Logs | User behavior auditing |
| 🧰 **Development Tools** | Code Generation, Form Builder, API Documentation | Tools to enhance development efficiency |
| 📁 **File Management** | File Storage | Unified file management |

## 🔧 Models

| Module | Screenshot |
|------------|---------------------------------|
| Login      | ![login](backend/data/login.png) |
| Dashboard  | ![Dashboard](backend/data/dashboard.png) |
| Generator  | ![Generator](backend/data/gencode.png) |
| AI       | ![AI](backend/data/ai.png) |

### Mobile

| Login <div style="width:60px"/> | Home <div style="width:60px"/> | Profile <div style="width:60px"/> |
|----------|----------|----------|
| ![Mobile Login](backend/data/app_login.png) | ![Mobile Home](backend/data/app_home.png) | ![Mobile Personal Info](backend/data/app_mine.png) |

## 🚀 Quick Start

### First-time local setup (in order)

1. **Install runtimes**: Python ≥ 3.10, Node.js ≥ 20, [pnpm](https://pnpm.io/), local **MySQL or PostgreSQL** (or SQLite if configured in `backend/env/.env.dev`), and **Redis** matching your `.env.dev`.
2. **Clone the repo**: see “Get the Code” below.
3. **Env files**: copy `backend/env/.env.dev.example` → `backend/env/.env.dev`, and `frontend/.env.development.example` → `frontend/.env.development`; fill in **DB, Redis, JWT secret**, etc. Create an empty database first.
4. **Backend dependencies**: `cd backend`, run **`uv sync`** (recommended) or `pip install -r requirements.txt`.
5. **Start backend**: `uv run main.py run --env=dev`. **The first start automatically initializes tables and seed data**—you usually **do not** need to run `upgrade` first.
6. **Frontend**: `cd frontend`, `pnpm install`, `pnpm run dev`.
7. **Browser**: with the template env, open **`http://127.0.0.1:5180`** (`VITE_APP_PORT=5180`); log in with the admin account (same as [Demo Environment](#-demo-environment) unless you changed seed data).

> Use **`revision` / `upgrade`** only when you change ORM models and manage migrations with Alembic (see FAQ below).

### Environment Requirements

| Type | Technology Stack | Version |
|------|------------------|---------|
| Backend | Python | ≥ 3.10 (3.12 recommended) |
| Backend | FastAPI | 0.109+ |
| Frontend | Node.js | ≥ 20.0 |
| Frontend | Vue3 | 3.3+ |
| Database | MySQL / PostgreSQL / SQLite | As in `backend/env` |
| Cache | Redis | 6.x / 7.x (match `.env`) |

### Get the Code

```bash
# Clone the repository to your local machine
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git
# Or
git clone https://github.com/fastapiadmin/FastapiAdmin.git
```

> **Backend Note**: After cloning the code, you need to rename the `.env.dev.example` file in the `backend/env` directory to `.env.dev`, and rename the `.env.prod.example` file in the `backend/env` directory to `.env.prod`. Then modify the database connection information, Redis connection information, etc., according to the actual situation.

> **Frontend Note**: After cloning the code, you need to rename the `.env.development.example` file in the `frontend` directory to `.env.development`, and rename the `.env.production.example` file in the `frontend` directory to `.env.production`. Then modify the interface address, etc., according to the actual situation.

### Backend Setup

#### Using uv (recommended, matches `backend/pyproject.toml`)

```bash
cd backend
uv sync
# First start auto-inits schema & data; no need to run upgrade beforehand
uv run main.py run --env=dev
# uv run main.py run --env=prod
```

> Without `uv`: `pip install -r requirements.txt`, then `python main.py run --env=dev`. Use `upgrade` when you need Alembic after model changes.

#### Using pip / venv

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py run --env=dev
```

### Frontend Setup

#### Web Frontend (Vue3)

```bash
cd frontend/web
pnpm install
pnpm run dev
# Build production version
pnpm run build
```

#### Mobile (UniApp)

```bash
cd frontend/app
pnpm install
pnpm run dev:h5  # Start H5 development server
# Build production version
pnpm run build:h5
```

#### Documentation Site (VitePress)

```bash
cd frontend/docs
pnpm install
pnpm run dev
# Build production version
pnpm run build
```

### After startup

When using **`.env.dev.example` / `.env.development`** as-is:

| Service | URL (example) |
|---------|----------------|
| Web Frontend (Vite) | `http://127.0.0.1:5173` |
| Mobile H5 (UniApp) | `http://127.0.0.1:8080` |
| Documentation Site (VitePress) | `http://127.0.0.1:5174` |
| Backend base | `http://127.0.0.1:8001` |
| Swagger | `http://127.0.0.1:8001/docs` |
| API prefix | `http://127.0.0.1:8001/api/v1` (matches `ROOT_PATH`) |

### 🐳 Docker Deployment

#### Method 1: Use deploy.sh script (Recommended)

```bash
# 1. Clone the repository to server
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git
cd FastapiAdmin

# 2. Grant execution permissions and deploy
chmod +x deploy.sh
./deploy.sh

# View container logs
./deploy.sh logs

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# Only update code and restart (without rebuilding images)
./deploy.sh update

# Skip frontend build (use uploaded static files)
./deploy.sh --skip-frontend

# Enable frontend build (build on server)
./deploy.sh --build-frontend
```

#### Method 2: Execute script outside project

```bash
# 1. Copy the deployment script to server
cp deploy.sh /home/
cd /home
chmod +x deploy.sh

# 2. Execute one-click deployment (will auto clone project)
./deploy.sh

# View container logs
./deploy.sh logs

# Stop services
./deploy.sh stop

# Restart services
./deploy.sh restart

# Update code and restart (without rebuilding images, suitable for backend hot update)
./deploy.sh update
```

> **Note**:
> - First deployment will automatically pull code and build images
> - Frontend uses locally built dist directory, please build locally and commit to repository if you need to update frontend
> - Ensure `devops/nginx/ssl/` directory contains SSL certificate files (if using HTTPS)

## 🛠️ Secondary Development Tutorial

### Backend Development

The project adopts a **plugin-based architecture design**, and it is recommended to carry out secondary development in the `backend/app/plugin` directory. The system will **automatically discover and register** all routes that meet the specifications, facilitating module management and upgrade maintenance.

#### Plugin Architecture Features

- **Automatic Route Discovery**: The system automatically scans all `controller.py` files in the `backend/app/plugin/` directory
- **Automatic Route Registration**: All routes are automatically registered to the corresponding prefix path (module_xxx -> /xxx)
- **Modular Management**: Code is organized by functional modules for easy maintenance and extension
- **Support for Multi-level Nesting**: Support for multi-level nested structures within modules

#### Plugin Directory Structure

```sh
backend/app/plugin/
├── module_application/  # Application module (automatically mapped to /application)
│   └── ai/              # AI submodule
│       ├── controller.py # Controller file
│       ├── model.py      # Data model file
│       ├── schema.py     # Data validation file
│       ├── service.py    # Business logic file
│       └── crud.py       # Data access file
├── module_example/      # Example module (automatically mapped to /example)
│   └── demo/            # Submodule
│       ├── controller.py # Controller file
│       ├── model.py      # Data model file
│       ├── schema.py     # Data validation file
│       ├── service.py    # Business logic file
│       └── crud.py       # Data access file
├── module_generator/    # Code generation module (automatically mapped to /generator)
└── init_app.py          # Plugin initialization file
```

#### Automatic Route Registration Mechanism

The system will **automatically discover and register** all routes that meet the following conditions:
1. Controller files must be named `controller.py`
2. Routes are automatically mapped: `module_xxx` -> `/xxx`
3. Support for multiple `APIRouter` instances
4. Automatic route deduplication

#### Secondary Development Steps

1. **Create Plugin Module**: Create a new module directory under `backend/app/plugin/`, such as `module_yourfeature`
2. **Write Data Model**: Define database models in `model.py`
3. **Write Data Validation**: Define data validation models in `schema.py`
4. **Write Data Access Layer**: Write database operation logic in `crud.py`
5. **Write Business Logic Layer**: Write business logic in `service.py`
6. **Write Controller**: Define routes and handling functions in `controller.py`
7. **Automatic Registration**: The system automatically scans and registers all routes, no manual configuration required

#### Controller Example

```python
# backend/app/plugin/module_yourfeature/yourcontroller/controller.py
from fastapi import APIRouter, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import YourFeatureService

# Create route instance
YourFeatureRouter = APIRouter(
    route_class=OperationLogRoute, 
    prefix="/yourcontroller", 
    tags=["Your Feature Module"]
)

@YourFeatureRouter.get("/detail/{id}", summary="Get Detail")
async def get_detail(
    id: int = Path(..., description="Feature ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_yourfeature:yourcontroller:detail"]))
) -> JSONResponse:
    """
    Get feature detail
    
    Parameters:
    - id (int): Feature ID
    - auth (AuthSchema): Authentication information model
    
    Returns:
    - JSONResponse: JSON response containing feature detail
    """
    result = await YourFeatureService.detail_service(id=id, auth=auth)
    return SuccessResponse(data=result)

@YourFeatureRouter.get("/list", summary="Get List")
async def get_list(
    auth: AuthSchema = Depends(AuthPermission(["module_yourfeature:yourcontroller:list"]))
) -> JSONResponse:
    """
    Get feature list
    
    Parameters:
    - auth (AuthSchema): Authentication information model
    
    Returns:
    - JSONResponse: JSON response containing feature list
    """
    result = await YourFeatureService.list_service(auth=auth)
    return SuccessResponse(data=result)
```

#### Development Specifications

1. **Naming Convention**: Module names use `module_xxx` format, controller names use camelCase naming
2. **Permission Control**: All API interfaces must add permission control decorators
3. **Log Recording**: Use `OperationLogRoute` class to automatically record operation logs
4. **Return Format**: Use `SuccessResponse` or `ErrorResponse` uniformly for responses
5. **Code Comments**: Add detailed docstrings for all API interfaces

#### Notes

- Plugin module names must start with `module_`
- Controller files must be named `controller.py`
- Routes are automatically mapped to corresponding prefix paths
- No manual route registration required, the system automatically discovers and registers

### Frontend Part

1. **Configure Frontend API**: Create corresponding API files in `frontend/src/api/` directory
2. **Write Page Components**: Create page components in `frontend/src/views/` directory
3. **Register Routes**: Register routes in `frontend/src/router/index.ts`

### Code Generator Usage

The project has a built-in code generator that can automatically generate front-end and back-end code based on database table structures, greatly improving development efficiency.

#### Generation Steps

1. **Login System**: Login to the system using an administrator account
2. **Enter Code Generation Module**: Click "Code Generation" in the left menu
3. **Import Table Structure**: Select the database table to generate code for
4. **Configure Generation Parameters**: Fill in module name, function name, etc.
5. **Generate Code**: Click the "Generate Code" button
6. **Download or Write**: Choose to download the code package or write directly to the project directory

#### Generated File Structure

```sh
# Backend files
backend/app/plugin/module_yourmodule/
└── yourfeature/
    ├── controller.py # Controller file
    ├── model.py      # Data model file
    ├── schema.py     # Data validation file
    ├── service.py    # Business logic file
    └── crud.py       # Data access file

# Frontend files
frontend/src/
├── api/module_yourmodule/
│   └── yourfeature.ts # API call file
└── views/module_yourmodule/
    └── yourfeature/
        └── index.vue # Page component
```

#### Generated Code Example

```python
# Generated controller code example
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
    tags=["Your Feature Module"]
)

@YourFeatureRouter.get("/detail/{id}")
async def get_detail(
    id: int, 
    auth: AuthSchema = Depends(AuthPermission(["module_yourmodule:yourfeature:detail"]))
) -> JSONResponse:
    result = await YourFeatureService.detail_service(id=id, auth=auth)
    return SuccessResponse(data=result)
```

### Development Tools

- **Code Generator**: Automatically generate front-end and back-end CRUD code
- **API Documentation**: Automatically generate Swagger/Redoc API documentation
- **Database**: Auto schema & seed on first start; Alembic supported for schema evolution
- **Log System**: Built-in log recording and query functions
- **Monitoring System**: Built-in server monitoring and cache monitoring functions

### Development Process

1. **Requirement Analysis**: Clarify functional requirements and business logic
2. **Database Design**: Design database table structure
3. **Code Generation**: Use code generator to generate basic code
4. **Business Logic Development**: Perfect business logic and interfaces
5. **Frontend Development**: Develop frontend pages and interactions
6. **Testing**: Conduct unit testing and integration testing
7. **Deployment**: Deploy to production environment

### Development Notes

1. **Permission Control**: All API interfaces must add permission control
2. **Data Validation**: All input data must be validated
3. **Exception Handling**: Uniformly handle API exceptions
4. **Log Recording**: Key operations must be logged
5. **Performance Optimization**: Pay attention to API performance optimization, avoid slow queries
6. **Code Specification**: Follow PEP8 and project code specifications

### Common Questions

#### Q: How to add a new functional module?
A: Follow the secondary development steps, create a new module directory under `backend/app/plugin/` directory, and write related code.

#### Q: How to configure the database?
A: Configure database connection information in `backend/env/.env.dev` or `backend/env/.env.prod` files.

#### Q: How to configure Redis?
A: Configure Redis connection information in `backend/env/.env.dev` or `backend/env/.env.prod` files.

#### Q: How to generate database migration files?
A: Use the command `python main.py revision --env=dev` to generate migration files.

#### Q: How to apply database migrations?
A: Run `python main.py upgrade --env=dev` (or `uv run ...`) when you **need Alembic migrations**. **First start usually does not require this**—the app initializes automatically.

#### Q: How to start the development server?
A: From `backend`, run `uv run main.py run --env=dev` (or `python main.py run --env=dev`). **First start auto-initializes the database and seed data**; no manual `upgrade` is required beforehand.

#### Q: Do I need to run migrations before the first start?
A: **Usually no.** The first backend start initializes schema and data. Use `revision` / `upgrade` only when you change models and use Alembic.

#### Q: How to build the frontend production version?
A: Use the command `pnpm run build` to build the frontend production version.

#### Q: How to deploy to production environment?
A: Use the `./deploy.sh` script for one-click deployment to production environment.

## ℹ️ Help

For more details, please check the [Official Documentation](https://service.fastapiadmin.com)

## 👥 Contributors

<a href="https://github.com/fastapiadmin/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapiadmin/FastapiAdmin"/>
</a>

## 🙏 Special Thanks

Thanks to the contributions and support of the following open-source projects:

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

## 🎨 Community

| Group QR Code | WeChat Pay QR Code |
| --- | --- |
| ![Group QR Code](backend/data/group.jpg) | ![WeChat Pay QR Code](backend/data/wechatPay.jpg) |

## ❤️ Support the Project

If you like this project, please give it a ⭐️ Star to show your support! Thank you very much!

[![Stargazers over time](https://starchart.cc/fastapiadmin/FastapiAdmin.svg?variant=adaptive)](https://starchart.cc/fastapiadmin/FastapiAdmin)
