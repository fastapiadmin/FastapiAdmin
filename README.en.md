<div align="center">
     <p align="center">
          <img src="https://gitee.com/tao__tao/FastDocs/raw/main/src/public/logo.png" width="150" height="150" alt="logo" /> 
     </p>
     <h1>FastApiAdmin <img src="https://img.shields.io/badge/Version-v2.0.0-blue" alt="Version"></h1>
     <h3>Modern Full-Stack Rapid Development Platform</h3>
     <p>If you like this project, please give it a ⭐️ to show your support!</p>
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

English | [简体中文](./README.md)

</div>

## 📘 Project Introduction

**FastApiAdmin** is a **completely open-source, highly modular, and technologically advanced modern rapid development platform** designed to help developers efficiently build high-quality enterprise-level backend and frontend systems. This project adopts a **frontend-backend separation architecture**, integrating the Python backend framework `FastAPI` and the mainstream frontend framework `Vue3` to achieve unified development across multiple terminals, providing a one-stop out-of-the-box development experience.

> **Design Philosophy**: With modularity and loose coupling at its core, it pursues rich functional modules, simple and easy-to-use interfaces, detailed development documentation, and convenient maintenance methods. By unifying frameworks and components, it reduces the cost of technology selection, follows development specifications and design patterns, builds a powerful code hierarchical model, and comes with comprehensive local language support. It is specifically tailored for team and enterprise development scenarios.

## 🔗 Source Repositories

| Platform | Repository |
|----------|------------|
| GitHub | [FastapiAdmin Main](https://github.com/1014TaoTao/FastapiAdmin.git) \| [FastDocs Website](https://github.com/1014TaoTao/FastDocs.git) \| [FastApp Mobile](https://github.com/1014TaoTao/FastApp.git) |
| Gitee  | [FastapiAdmin Main](https://gitee.com/tao__tao/FastapiAdmin.git) \| [FastDocs Website](https://gitee.com/tao__tao/FastDocs.git) \| [FastApp Mobile](https://gitee.com/tao__tao/FastApp.git) |

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

## 📦 Engineering Structure Overview

```sh
FastapiAdmin
├─ backend               # Backend project (FastAPI + Python)
├─ frontend              # Web frontend project (Vue3 + Element Plus)
├─ fastapp               # Mobile project (UniApp + Wot Design Uni)
├─ fastdocs              # Documentation project (VitePress)
├─ devops                # Deployment configurations
├─ docker-compose.yaml   # Docker orchestration file
├─ deploy.sh             # One-click deployment script
├─ LICENSE               # Open source license
|─ README.en.md          # English documentation
└─ README.md             # Chinese documentation
```

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
| **Database** | MySQL / MongoDB | Support for relational and document databases |
| **Cache** | Redis | High-performance cache database |
| **Documentation** | Swagger / Redoc | Automatically generate API documentation |
| **Deployment** | Docker / Nginx / Docker Compose | Containerized deployment solution |

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

## 🍪 Demo Environment

- 🌐 Official Website: [https://service.fastapiadmin.com](https://service.fastapiadmin.com)
- 💻 Web Demo: [https://service.fastapiadmin.com/web](https://service.fastapiadmin.com/web)
- 📱 Mobile: [https://service.fastapiadmin.com/app](https://service.fastapiadmin.com/app)
- 👤 Login Account: `admin` Password: `123456`

## 🚀 Quick Start

### Environment Requirements

| Type | Technology Stack | Version |
|------|------------------|---------|
| Backend | Python | ≥ 3.10 |
| Backend | FastAPI | 0.109+ |
| Frontend | Node.js | ≥ 20.0 |
| Frontend | Vue3 | 3.3+ |
| Database | MySQL | 8.0+ |
| Cache | Redis | 7.0+ |

### Get the Code

```bash
# Clone the repository to your local machine
git clone https://gitee.com/tao__tao/FastapiAdmin.git
# Or
git clone https://github.com/1014TaoTao/FastapiAdmin.git
```

### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip3 install -r requirements.txt

# Start the backend service: ensure that MySQL and Redis are running
python main.py run
# Or specify environment
python main.py run --env=dev

# Generate migration files
python main.py revision --env=dev
# Apply migrations
python main.py upgrade --env=dev
```

### Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
pnpm install

# Start the development server
pnpm run dev

# Build for production
pnpm run build
```

### Mobile Setup

```bash
# Navigate to the mobile directory
cd fastapp

# Install dependencies
pnpm install

# Start the H5 development server
pnpm run dev:h5

# Build for H5 production
pnpm run build:h5
```

### Documentation Setup

```bash
# Navigate to the documentation directory
cd fastdocs

# Install dependencies
pnpm install

# Start the documentation development server
pnpm run docs:dev

# Build documentation for production
pnpm run docs:build
```

### Access URLs

- 🏠 Official Website: [http://localhost:5180](http://localhost:5180)
- 🖥️ Web Interface: [http://localhost:5180/web](http://localhost:5180/web)
- 📱 Mobile Interface: [http://localhost:5180/app](http://localhost:5180/app)

Default accounts:
- Admin: `admin` / `123456`

## 🐳 Docker Deployment

```bash
# Copy the deployment script to the server and grant execution permissions
chmod +x deploy.sh

# Execute one-click deployment
./deploy.sh

# Common Docker commands
# View running containers
docker compose ps

# View container logs
docker logs -f <container_name>

# Stop services
docker compose down
```

## 🔧 Models

| Module | Screenshot |
|------------|---------------------------------|
| Login      | ![Login](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/login.png) |
| Dashboard  | ![Dashboard](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/dashboard.png) |
| Analysis   | ![Analysis](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/analysis.png) |
| Menu       | ![Menu](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/menu.png) |
| Department | ![Department](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/dept.png) |
| Position   | ![Position](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/position.png) |
| Role       | ![Role](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/role.png) |
| User       | ![User](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/user.png) |
| Log        | ![Log](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/log.png) |
| Config     | ![Config](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/config.png) |
| OnlineUser | ![OnlineUser](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/online.png) |
| Server     | ![Server](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/service.png) |
| Cache      | ![Cache](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/cache.png) |
| Task       | ![Task](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/job.png) |
| Dict       | ![Dict](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/dict.png) |
| API Docs   | ![API Docs](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/docs.png) |
| Theme      | ![Theme](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/theme.png) |
| Document   | ![Document](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/help.png) |
| Lock       | ![Lock](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/lock.png) |
| Form       | ![Form](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/form.png) |
| Generator  | ![Generator](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/gencode.png) |
| Workflow   | ![Workflow](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/workflow.png) |
| File       | ![File](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/file.png) |
| MyApps    | ![MyApps](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/myapp.png) |
| Setting  | ![Setting](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/setting.png) |
| AI       | ![AI](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/ai.png) |

### Mobile

| Module <div style="width:60px"/> | Details | Module <div style="width:60px"/> | Details | Module <div style="width:60px"/> | Details |
|----------|------|----------|------|----------|------|
| Login    | ![Mobile Login](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_login.png) | Home      | ![Mobile Home](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_home.png) | Profile      | ![Mobile Profile](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_mine.png) |
| Personal  | ![Mobile Personal Info](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_profile.png) | Settings   | ![Mobile Settings](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_setting.png) | Workbench      | ![Mobile Workbench](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/app_work.png) |

## 🛠️ Secondary Development Tutorial

### Backend Part

1. **Write the Entity Class Layer**: Create the ORM model for the demo in `backend/app/api/v1/models/demo/example_model.py` (corresponding to the entity class layer in Spring Boot).
2. **Write the Data Model Layer**: Create the demo data model in `backend/app/api/v1/schemas/demo/example_schema.py` (corresponding to the DTO layer in Spring Boot).
3. **Write the Query Parameter Model Layer**: Create the query parameter model for the demo in `backend/app/v1/params/demo/example_param.py` (corresponding to the DTO layer in Spring Boot).
4. **Write the Persistence Layer**: Create the demo data layer in `backend/app/api/v1/cruds/demo/example_crud.py` (corresponding to the Mapper or DAO layer in Spring Boot).
5. **Write the Business Layer**: Create the demo data layer in `backend/app/api/v1/services/demo/example_service.py` (corresponding to the Service layer in Spring Boot).
6. **Write the Interface Layer**: Create the demo data layer in `backend/app/api/v1/controllers/demo/example_controller.py` (corresponding to the Controller layer in Spring Boot).
7. **Register Backend Routes**: Register the demo routes in `backend/app/api/v1/urls/demo_url.py`.
8. **Register Routes to the FastAPI Service**: Register the routes in `backend/plugin/init_app.py`.
9. **Add the Demo Module to the System Initialization Script**: Add it in `backend/app/scripts/initialize.py` (if necessary, you can configure the demo menu permissions in `backend/app/scripts/data/system_menu.json` and `backend/app/scripts/data/system_role_menus.json` or from the frontend page menu).
10. **Add the Demo Module to the Database Migration Script**: Add it in `backend/app/alembic/env.py`.

### Code Generation Tutorial

The code generation module is one of the core features of this project, which can help developers quickly generate complete CRUD code and greatly improve development efficiency. This module is based on the Jinja2 template engine and can generate integrated front-end and back-end functional modules.

#### Code Generation Process

1. **Create or Import Data Tables**:
   - Method 1: Create a new table directly in the system through the "Create Table" function
   - Method 2: Import existing database tables into the code generator through the "Import" function

2. **Configure Generation Parameters**:
   - Basic Configuration:
     - Table name, table description, entity class name
   - Generation Configuration:
     - Generation package path (package_name): e.g., `student`
     - Generation module name (module_name): e.g., `student`
     - Generation business name (business_name): e.g., `student`
     - Generation function name (function_name): e.g., `Student Management`
     - Code generation method: zip package download or project directory write
     - Parent menu: Select the menu category to which the generated function belongs

3. **Field Configuration**:
   - Configure each field:
     - Field column type, Python type, Python field name
     - Whether it is a primary key, auto-increment, required
     - Whether it is an insert field, edit field, list field, query field
     - Query method (equal, not equal, greater than, less than, range)
     - Display type (text box, text area, dropdown box, checkbox, radio button, date control)
     - Dictionary type (for dropdown data source)

4. **Code Preview**:
   - Preview the code to be generated
   - Support preview of backend (Python), frontend (Vue/TS), and database (SQL) code
   - Filter preview content by type

5. **Code Generation**:
   - Click "Download Code" to generate and download a zip package
   - Click "Write to Local" to write directly to the project directory

#### Generated File Structure

The code generator will generate a complete front-end and back-end code structure:

**Backend Files**:
- Controller layer: `backend/app/api/v1/module_{module_name}/{business_name}/controller.py`
- Service layer: `backend/app/api/v1/module_{module_name}/{business_name}/service.py`
- Data access layer: `backend/app/api/v1/module_{module_name}/{business_name}/crud.py`
- Data model layer: `backend/app/api/v1/module_{module_name}/{business_name}/model.py`
- Data schema layer: `backend/app/api/v1/module_{module_name}/{business_name}/schema.py`
- Query parameter layer: `backend/app/api/v1/module_{module_name}/{business_name}/param.py`

**Frontend Files**:
- API interface file: `frontend/src/api/module_{module_name}/{business_name}.ts`
- Page component file: `frontend/src/views/module_{module_name}/{business_name}/index.vue`

**Database Files**:
- Menu SQL file: `backend/sql/module_{module_name}/{business_name}_menu.sql`

#### Usage Example

1. Create a new table in the database, such as `sys_student`
2. Log in to the system and enter the **Code Generation** module
3. Click "Import" and select the `sys_student` table
4. Configure generation parameters:
   - Generation package path: `student`
   - Generation module name: `student`
   - Generation business name: `student`
   - Generation function name: `Student Management`
   - Parent menu: System Management
5. Configure field properties (such as setting which fields need to be displayed, queried, edited, etc.)
6. Click "Preview Code" to view the generated code
7. Click "Download Code" or "Write to Local" to generate a complete functional module
8. Restart the service, and the new function module is ready to use

### Frontend Part

1. **Configure the Frontend to Access the Backend Interface Address**: Configure it in `frontend/src/api/demo/example.ts`.
2. **Write the Frontend Page**: Write it in `frontend/src/views/demo/example/index.vue`.

### Mobile Part

1. **Configure the mobile access address for backend interfaces**: Write the code in `fastapp/src/api`.
2. **Write mobile pages**: Write the code in `fastapp/src/pages`.

## ℹ️ Help

For more details, please check the [Official Documentation](https://service.fastapiadmin.com)

## 👥 Contributors

<a href="https://github.com/1014TaoTao/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=1014TaoTao/FastapiAdmin"/>
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

| WeChat QR Code | Group QR Code | WeChat Pay QR Code |
| --- | --- | --- |
| ![WeChat QR Code](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/wechat.jpg) | ![Group QR Code](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/group.jpg) | ![WeChat Pay QR Code](https://gitee.com/tao__tao/FastDocs/raw/main/src/public/wechatPay.jpg) |

## ❤️ Support the Project

If you like this project, please give it a ⭐️ Star to show your support! Thank you very much!

[![Stargazers over time](https://starchart.cc/1014TaoTao/FastapiAdmin.svg?variant=adaptive)](https://starchart.cc/1014TaoTao/FastapiAdmin)
