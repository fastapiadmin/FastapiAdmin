---
outline: "deep"
title: Quick Start
---
# Quick Start

## 🍪Demo Environment

- Official Website: <https://service.fastapiadmin.com>
- Demo Address: <https://service.fastapiadmin.com/web>
- Mini Program Address: <https://service.fastapiadmin.com/app>
- Admin Account: `admin` Password: `123456`
- Demo Account: `demo` Password: `123456`

## 👷Installation and Usage

### Version Description

| Type | Technology Stack | Version |
|------|-----------------|---------|
| Backend | Python | >=3.10 |
| Backend | FastAPI | 0.109 |
| Frontend | Node.js | >= 20.0 (recommended to use the latest version) |
| Frontend | npm | 16.14 |
| Frontend | Vue3 | 3.3 |
| Web UI | ElementPlus | 2.10.4 |
| Mobile | Uni App | 3.0.0 |
| App UI | Wot Design Uni | 1.9.1 |
| Database | MySQL | 8.0 (recommended to use the latest version) |
| Middleware | Redis | 7.0 (recommended to use the latest version) |

### Environment Preparation

#### 1. Install Python

```sh
# macOS
brew install python@3.10

# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# CentOS/RHEL
sudo dnf install python3.10 python3.10-venv python3.10-devel
```

#### 2. Install Node.js

```sh
# Using nvm installation (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20

# Or using package manager
# macOS
brew install node@20

# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# CentOS/RHEL
sudo dnf install nodejs npm
```

#### 3. Install Database and Cache

```sh
# Install MySQL
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql

# Install Redis
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis
```

### Get Code

```sh
# Clone code to local
# FastapiAdmin main project
git clone https://github.com/fastapiadmin/FastapiAdmin.git
# FastApp mobile
 git clone https://github.com/fastapiadmin/FastApp.git
# FastDocs official documentation
git clone https://github.com/fastapiadmin/FastDocs.git
```

### Local Backend Startup (FastapiAdmin Main Project)

#### 1. Configure Environment Variables

```sh
# Enter backend project directory
cd FastapiAdmin/backend

# Copy environment configuration file
cp env/.env.dev.example env/.env.dev

# Edit environment configuration file (modify according to actual situation)
# Main configuration items: database connection, Redis connection, JWT secret key, etc.
```

#### 2. Install Dependencies

```sh
# Create virtual environment (optional but recommended)
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Database Initialization

```sh
# Generate migration files
python main.py revision "Initial migration" --env=dev

# Apply migration
python main.py upgrade --env=dev

# Initialize system data
python main.py init
```

#### 4. Start Backend Service

```sh
# Development environment startup
python main.py run --env=dev

# Or use default environment (dev)
python main.py run

# Production environment startup
python main.py run --env=prod
```

### Local Frontend Startup (FastapiAdmin Main Project)

#### 1. Configure Environment Variables

```sh
# Enter frontend project directory
cd FastapiAdmin/frontend

# Copy environment configuration file
cp .env.development.example .env.development

# Edit environment configuration file (modify according to actual situation)
# Main configuration items: API base URL, etc.
```

#### 2. Install Dependencies

```sh
# Install pnpm (if not installed)
npm install -g pnpm

# Install frontend dependencies
pnpm install
```

#### 3. Start Frontend Service

```sh
# Development environment startup
pnpm run dev

# Build frontend, generate `dist` directory
pnpm run build
```

### Local Mini Program H5 Startup (FastApp Mobile)

#### 1. Configure Environment Variables

```sh
# Enter mobile project directory
cd FastApp

# Copy environment configuration file
cp .env.development .env.development

# Edit environment configuration file (modify according to actual situation)
# Main configuration items: API base URL, etc.
```

#### 2. Install Dependencies

```sh
# Install frontend dependencies
pnpm install
```

#### 3. Start H5 Service

```sh
# Start H5 development service
pnpm run dev:h5

# Build H5 version, generate `dist/build/h5` directory
pnpm run build:h5

# Start other platforms (such as WeChat Mini Program)
pnpm run dev:mp-weixin
```

### Local Project Official Website Startup (FastDocs Official Documentation)

```sh
# Enter FastDocs official documentation directory
cd FastDocs

# Install dependencies
pnpm install

# Run documentation project
pnpm run docs:dev

# Build documentation project, generate `dist` directory
pnpm run docs:build
```

---

### Local Access Addresses

- FastDocs Documentation Address: <http://127.0.0.1:5180>
- FastapiAdmin Frontend Address: <http://127.0.0.1:5173>
- FastAPI Interface Documentation: <http://127.0.0.1:8001/api/v1/docs>
- FastApp H5 Address: <http://127.0.0.1:5174>

### Default Account Password

- Admin Account: `admin` Password: `123456`
- Demo Account: `demo` Password: `123456`

## 🐳 Docker Deployment

### 1. Preparation

- Server needs to install Docker and Docker Compose
- Ensure server ports 80 (Nginx) and 8001 (backend) are available

### 2. Deployment Steps

```sh
# Enter FastapiAdmin main project directory
cd FastapiAdmin

# Copy environment configuration files
cp backend/env/.env.prod.example backend/env/.env.prod
cp frontend/.env.production.example frontend/.env.production

# Edit environment configuration files (modify according to actual server situation)
# Main configuration items: database connection, Redis connection, JWT secret key, API base URL, etc.

# Give script execution permission
chmod +x start.sh

# Execute deployment script
./start.sh

# Check deployment status
docker compose ps

# View logs
docker logs -f fastapiadmin-backend
```

### 3. Deployment File Description

| Configuration File | Description | Path |
|-------------------|-------------|------|
| Backend environment configuration | Production environment database, Redis and other configurations | `FastapiAdmin/backend/env/.env.prod` |
| Frontend environment configuration | Production environment API address and other configurations | `FastapiAdmin/frontend/.env.production` |
| Docker configuration | Container orchestration configuration | `FastapiAdmin/docker-compose.yaml` |
| Nginx configuration | Reverse proxy configuration | `FastapiAdmin/devops/nginx/nginx.conf` |

### 4. Common Docker Commands

```sh
# View images
docker images

# View containers
docker compose ps

# Stop service
docker compose down

# Restart service
docker compose up -d

# View container logs
docker logs -f <container name>

# Enter container
docker exec -it <container name> bash
```

## 🔧Module Display

### Web End

| Module Name <div style="width:60px"/> | Screenshot |
|-------------|------------|
| Dashboard | ![Dashboard](/dashboard.png) |
| Code Generation | ![Code Generation](/gencode.png) |
| Intelligent Assistant | ![Intelligent Assistant](/ai.png) |

### Mobile End

| Login <div style="width:60px"/> | Home <div style="width:60px"/> | Profile <div style="width:60px"/> |
|----------|----------|----------|
| ![Mobile Login](/app_login.png) | ![Mobile Home](/app_home.png) | ![Mobile Personal Info](/app_mine.png) |

## 🚀Secondary Development Tutorial

### Backend Part (FastapiAdmin Main Project)

1. **Write entity class layer**: Create example ORM model in `FastapiAdmin/backend/app/api/v1/models/demo/example_model.py` (corresponding to entity class layer in Spring Boot)
2. **Write data model layer**: Create example data model in `FastapiAdmin/backend/app/api/v1/schemas/demo/example_schema.py` (corresponding to DTO layer in Spring Boot)
3. **Write query parameter model layer**: Create example query parameter model in `FastapiAdmin/backend/app/api/v1/params/demo/example_param.py` (corresponding to DTO layer in Spring Boot)
4. **Write persistence layer**: Create example data layer in `FastapiAdmin/backend/app/api/v1/cruds/demo/example_crud.py` (corresponding to Mapper or DAO layer in Spring Boot)
5. **Write business layer**: Create example data layer in `FastapiAdmin/backend/app/api/v1/services/demo/example_service.py` (corresponding to Service layer in Spring Boot)
6. **Write interface layer**: Create example data layer in `FastapiAdmin/backend/app/api/v1/controllers/demo/example_controller.py` (corresponding to Controller layer in Spring Boot)
7. **Register backend route**: Register example route in `FastapiAdmin/backend/app/api/v1/urls/demo/example_url.py`
8. **Register route to FastAPI service**: Register route in `FastapiAdmin/backend/plugin/init_app.py`
9. **Add demo module to system initialization script**: Add in `FastapiAdmin/backend/app/scripts/initialize.py` (if needed, you can configure demo's menu permissions in `FastapiAdmin/backend/app/scripts/data/system_menu.json` and `FastapiAdmin/backend/app/scripts/data/system_role_menus.json` or add from frontend page menu)
10. **Add demo module to database migration script**: Add in `FastapiAdmin/backend/app/alembic/env.py`

### Frontend Part (FastapiAdmin Main Project)

1. **Frontend access backend interface address**: Configure in `FastapiAdmin/frontend/src/api/demo/example.ts`
2. **Write frontend page**: Write in `FastapiAdmin/frontend/src/views/demo/example/index.vue`

### Mobile Part (FastApp Mobile)

1. **Mobile access backend interface address**: Write in `FastApp/src/api`
2. **Write mobile page**: Write in `FastApp/src/pages`

## 💡Common Problems and Solutions

### 1. Backend Startup Failure

**Problem**: Database connection failure
**Solution**: Check if the database connection information in the environment configuration file is correct, ensure the database service is running, and the username and password are correct.

**Problem**: Redis connection failure
**Solution**: Check if the Redis connection information in the environment configuration file is correct, ensure the Redis service is running.

**Problem**: Dependency installation failure
**Solution**: Ensure the Python version is correct (>=3.10), you can try to reinstall dependencies using a virtual environment.

### 2. Frontend Startup Failure

**Problem**: Dependency installation failure
**Solution**: Ensure the Node.js version is correct (>=20.0), you can try to clear the cache and reinstall: `pnpm cache clean && pnpm install`.

**Problem**: API request failure
**Solution**: Check if the API base URL in the frontend environment configuration file is correct, ensure the backend service is running.

### 3. Deployment Problems

**Problem**: Docker deployment failure
**Solution**: Ensure the server has installed Docker and Docker Compose, check if ports are occupied, view container logs to understand specific error information.

**Problem**: Nginx configuration error
**Solution**: Check if the reverse proxy settings in the Nginx configuration file are correct, ensure the backend service address is configured correctly.

### 4. Other Problems

**Problem**: System initialization failure
**Solution**: Ensure the database has been correctly initialized, and migrations have been applied, you can try to re-execute the initialization command: `python main.py init`.

**Problem**: Insufficient permissions
**Solution**: Check user role permission settings, ensure the current user has sufficient permissions to access the required functions.
