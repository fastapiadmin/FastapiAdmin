---
outline: "deep"
title: Project Overview
---
# Project Overview

## 📋FastApiAdmin Introduction

**FastApiAdmin** is a **completely open-source, highly modular, and technologically advanced modern rapid development platform** designed to help developers efficiently build high-quality enterprise-level backend systems. The project adopts a **frontend-backend separation architecture**, integrating the Python backend framework `FastAPI` and the mainstream frontend framework `Vue3` to achieve multi-end unified development, providing a one-stop out-of-the-box development experience.

### Core Values

- **Reduce Development Costs**: Out-of-the-box functional modules reduce repetitive development work
- **Improve Development Efficiency**: Unified technology stack and development specifications accelerate project delivery
- **Ensure System Quality**: Strict code quality control and testing processes
- **Flexible Scalability**: Modular design supports business customization and function extension

### Technical Advantages

- **Backend**: Based on FastAPI asynchronous framework, excellent performance, automatically generates API documentation
- **Frontend**: Based on Vue3 + TypeScript + ElementPlus, type-safe, good development experience
- **Mobile**: Based on Uni App, supports multi-platform deployment
- **Database**: Supports MySQL and MongoDB to meet different business scenario needs
- **Cache**: Integrated Redis to improve system response speed
- **Deployment**: Supports Docker containerized deployment, simplifying operation and maintenance work

## 🎯Application Scenarios

- **Enterprise Internal Management Systems**: Human resources, finance, OA and other systems
- **Business Operation Platforms**: E-commerce, content management, customer management and other systems
- **Data Analysis Platforms**: Data visualization, report statistics and other systems
- **API Management Platforms**: Interface management, documentation management and other systems
- **Multi-platform Applications**: Application scenarios that require both Web and mobile terminals

## 📦Project Structure Overview

The project has been split into three independent repositories for separate development and maintenance:

### 1. FastapiAdmin Main Project

```sh
FastapiAdmin/
├─ backend/              # Backend project
│  ├─ app/              # Core application code
│  │  ├─ api/           # API interfaces
│  │  │  └─ v1/         # API version
│  │  │     ├─ module_common/    # Common module
│  │  │     ├─ module_monitor/   # Monitoring module
│  │  │     └─ module_system/    # System module
│  │  ├─ common/        # Common code
│  │  ├─ config/        # Configuration management
│  │  ├─ core/          # Core functionality
│  │  ├─ plugin/        # Plugin system
│  │  │  ├─ module_application/  # Application module
│  │  │  ├─ module_example/      # Example module
│  │  │  └─ module_generator/    # Code generation module
│  │  ├─ scripts/       # Script tools
│  │  └─ utils/         # Utility functions
│  ├─ alembic/          # Database migration
│  ├─ env/              # Environment configuration
│  ├─ static/           # Static resources
│  ├─ tests/            # Test code
│  ├─ README.md         # Backend documentation
│  ├─ main.py           # Backend entry
│  └─ requirements.txt  # Python dependencies
├─ frontend/            # Frontend project
│  ├─ src/              # Source code
│  │  ├─ api/           # API interfaces
│  │  ├─ assets/        # Resource files
│  │  ├─ components/    # Components
│  │  ├─ composables/   # Composables
│  │  ├─ constants/     # Constants
│  │  ├─ directives/    # Directives
│  │  ├─ enums/         # Enums
│  │  ├─ lang/          # Internationalization
│  │  ├─ layouts/       # Layouts
│  │  ├─ plugins/       # Plugins
│  │  ├─ router/        # Router
│  │  ├─ store/         # State management
│  │  ├─ styles/        # Styles
│  │  ├─ types/         # Type definitions
│  │  ├─ utils/         # Utility functions
│  │  └─ views/         # Pages
│  ├─ public/           # Static resources
│  ├─ package.json      # Frontend dependencies
│  └─ README.md         # Frontend documentation
├─ devops/              # DevOps project
│  ├─ backend/          # Backend deployment configuration
│  ├─ nginx/            # Nginx configuration
│  └─ redis/            # Redis configuration
├─ docker-compose.yaml  # Deployment file
├─ deploy.sh            # Deployment script
├─ LICENSE              # License
└─ README.md            # Project documentation
```

### 2. FastApp Mobile Application

```sh
FastApp/
├─ src/                 # Source code directory
│  ├─ api/             # API interfaces
│  │  ├─ auth.ts       # Authentication interfaces
│  │  ├─ file.ts       # File interfaces
│  │  └─ user.ts       # User interfaces
│  ├─ components/      # Components
│  │  ├─ cu-date-query/ # Date query component
│  │  ├─ cu-picker/     # Picker component
│  │  ├─ qiun-error/    # Error component
│  │  └─ qiun-loading/  # Loading component
│  ├─ composables/     # Composables
│  │  ├─ useNavigationBar.ts # Navigation bar management
│  │  ├─ useStomp.ts   # WebSocket management
│  │  └─ useTabbar.ts  # Tabbar management
│  ├─ constants/       # Constants
│  │  ├─ index.ts      # Constants definition
│  │  └─ storage.constant.ts # Storage keys
│  ├─ enums/           # Enums
│  │  ├─ api-code.enum.ts # API error codes
│  │  └─ api-header.enum.ts # API headers
│  ├─ layouts/         # Layout components
│  │  ├─ default.vue   # Default layout
│  │  └─ tabbar.vue    # Tabbar layout
│  ├─ pages/           # Page files
│  │  ├─ index/        # Home page
│  │  │  ├─ data.ts     # Data definition
│  │  │  ├─ index.vue   # Home page component
│  │  │  └─ types.ts    # Type definitions
│  │  ├─ login/        # Login page
│  │  │  └─ index.vue   # Login component
│  │  ├─ mine/         # Personal center
│  │  │  ├─ about/      # About page
│  │  │  ├─ faq/        # FAQ page
│  │  │  ├─ feedback/   # Feedback page
│  │  │  ├─ profile/    # Profile page
│  │  │  ├─ settings/   # Settings page
│  │  │  └─ index.vue   # Personal center component
│  │  └─ work/         # Workbench
│  │     ├─ data.ts     # Data definition
│  │     ├─ index.vue   # Workbench component
│  │     └─ types.ts    # Type definitions
│  ├─ router/          # Router configuration
│  │  └─ index.ts      # Router configuration file
│  ├─ static/          # Static resources
│  │  ├─ icons/        # Icons
│  │  ├─ images/       # Images
│  │  └─ logo.png      # Logo
│  ├─ store/           # State management
│  │  ├─ modules/      # Modules
│  │  │  ├─ theme.store.ts # Theme management
│  │  │  └─ user.store.ts # User management
│  │  └─ index.ts      # State management configuration
│  ├─ styles/          # Style files
│  │  └─ index.scss    # Global styles
│  ├─ types/           # TypeScript definitions
│  ├─ utils/           # Utility functions
│  │  ├─ auth.ts       # Authentication utility
│  │  ├─ color.ts      # Color utility
│  │  ├─ index.ts      # Utility functions
│  │  ├─ request.ts    # Request utility
│  │  └─ storage.ts    # Storage utility
│  ├─ App.vue          # Application root component
│  ├─ main.ts          # Application entry file
│  ├─ manifest.json    # Application configuration file
│  ├─ pages.json       # Page router configuration
│  └─ theme.json       # Theme configuration
├─ public/             # Static resources
├─ .env.development    # Development environment configuration
├─ .env.production     # Production environment configuration
├─ package.json        # Project dependencies
├─ pages.config.ts     # Page configuration
├─ tsconfig.json       # TypeScript configuration
├─ unocss.config.ts    # UnoCSS configuration
└─ vite.config.ts      # Vite configuration
```

### 3. FastDocs Official Documentation

```sh
FastDocs/
├─ docs/               # Documentation source
│  ├─ development/     # Development documentation
│  ├─ en/              # English documentation
│  ├─ overview/        # Overview documentation
│  ├─ quickstart/      # Quick start
│  ├─ public/          # Static resources
│  └─ index.md         # Home page
├─ .vitepress/         # VitePress configuration
│  ├─ theme/           # Theme configuration
│  └─ config.ts        # Site configuration
├─ package.json        # Project dependencies
└─ README.md           # Project documentation
```

## ✨Core Highlights

| Feature | Description |
| ---- | ---- |
| 🔭 Rapid Development | A completely open-source modern rapid development platform designed to help developers efficiently build high-quality enterprise-level backend systems. |
| 🌐 Full-Stack Integration | Frontend-backend separation, integrating Python (FastAPI) + Vue3 multi-end development, supporting Web and mobile terminals. |
| 🧱 Modular Design | System functions are highly decoupled, plugin-based architecture, supporting automatic route discovery and registration, easy to extend and maintain. |
| ⚡️ High Performance | Using FastAPI asynchronous framework + Redis cache to optimize interface response speed. |
| 🔒 Secure Authentication | Support for JWT OAuth2 authentication mechanism to ensure system security. |
| 📊 Permission Management | RBAC model implements fine-grained permission control at the menu, button, and data levels. |
| 🚀 Quick Deployment | Support for Docker/Docker Compose/Nginx one-click deployment. |
| 📄 Developer-Friendly | Provide comprehensive Chinese documentation + Chinese interface + visual toolchain, reducing learning costs. |
| 🧩 Quick Integration | Based on Vue3, Vite5, Pinia, ElementPlus and other mainstream frontend technology stacks, out-of-the-box. |
| 📱 Mobile Support | FastApp mobile application developed based on UniApp, supporting multi-end operation (H5, WeChat Mini Program, Alipay Mini Program, App, etc.). |
| 🤖 Agent Framework | Integrated agent framework, providing AI capabilities. |
| 🎨 Theme Customization | Support for dark/light theme switching, providing personalized interface experience. |
| 🌍 Internationalization Support | Built-in internationalization framework, supporting multi-language switching. |
| 📈 Data Visualization | Integrated chart library, providing rich data visualization capabilities. |
| 🛠️ Code Generation | Built-in code generation tool, improving development efficiency. |

## 🔧Technology Stack

| Category | Technology | Description |
|---------|------------|-------------|
| **Backend Framework** | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | Modern, high-performance asynchronous framework with enforced type constraints and data migration |
| **ORM** | SQLAlchemy 2.0 | Powerful ORM library |
| **Scheduled Tasks** | APScheduler | Easily implement scheduled tasks |
| **Authentication** | PyJWT | Implement JWT authentication |
| **Frontend Framework** | Vue3 / Vite5 / Pinia / TypeScript | Rapidly develop Vue3 applications |
| **Frontend Tools** | ESLint / Prettier / Stylelint | Code quality and style tools |
| **Mobile Framework** | UniApp / Vue3 / TypeScript | Cross-platform mobile application development |
| **UI Library** | ElementPlus (Web) / Wot Design Uni (Mobile) | Enterprise-level UI component library |
| **CSS Framework** | UnoCSS / SCSS | Atomic CSS and preprocessor |
| **Database** | MySQL / PostgreSQL / SQLite | Relational database support |
| **Cache** | Redis | Powerful cache database |
| **API Documentation** | Swagger / Redoc | Automatically generate API documentation |
| **Deployment** | Docker / Nginx / Docker Compose | Rapid project deployment |
| **Monitoring** | Built-in Server Monitoring / Cache Monitoring | System operation status monitoring |
| **Internationalization** | i18n | Multi-language support |
| **Data Visualization** | ECharts | Rich data visualization capabilities |

## ✨Built-in Modules

### FastapiAdmin Main Project Modules

| Module Name | Submodules | Description |
|---------|------------|-------------|
| **Dashboard** | Workbench, Analysis Page | System overview and data analysis |
| **System Management** | User, Role, Menu, Department, Position, Dictionary, Configuration, Announcement | Core system management functions |
| **Monitoring Management** | Online Users, Server Monitoring, Cache Monitoring | System operation status monitoring |
| **Task Management** | Scheduled Tasks | Asynchronous task scheduling management |
| **Log Management** | Operation Logs | User behavior auditing |
| **Development Tools** | Code Generation, Form Builder, API Documentation | Tools to improve development efficiency |

### FastApp Mobile Application Modules

| Module Name | Submodules | Description |
|---------|------------|-------------|
| **Home** | Carousel, Quick Navigation, Announcements, Data Statistics | Mobile home page display |
| **Workbench** | Business function entry, supports permission control | Mobile core function area |
| **Personal Center** | Personal Information, Settings, FAQ, Feedback | User personal related functions |
| **User Authentication** | Login, Registration, Password Reset | User identity verification |
| **Data Statistics** | Real-time visitor count, page views and other data display | Business data visualization |

## 📞Contact Information

If you have any questions or suggestions about the project, please contact us through the following ways:

- **GitHub**: [fastapiadmin/FastapiAdmin](https://github.com/fastapiadmin/FastapiAdmin)
- **Gitee**: [fastapiadmin/FastapiAdmin](https://gitee.com/fastapiadmin/FastapiAdmin)
- **Email**: 948080782@qq.com

## 🤝Contribution Guide

We welcome community contributions, including but not limited to:

- Submit bug reports and feature suggestions
- Improve code quality and performance
- Perfect documentation and examples
- Develop new functional modules

## 📄License

This project adopts the MIT license. For details, see the [LICENSE](https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE) file.