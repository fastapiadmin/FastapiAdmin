# FastApiAdmin - Backend

一个基于 FastAPI 框架构建企业级后端架构解决方案，为前端 Vue3 管理系统提供完整的 API 服务支持。

## 🚀 项目特性

- **现代技术栈**: FastAPI + SQLAlchemy 2.0 + Pydantic 2.x
- **多数据库支持**: MySQL、PostgreSQL、SQLite
- **异步架构**: 支持高并发异步数据库操作
- **权限管理**: 完整的 RBAC 权限控制体系
- **任务调度**: 基于 APScheduler 的定时任务系统
- **日志监控**: 完整的操作日志和系统监控
- **代码生成**: 智能化代码生成工具
- **AI 集成**: 支持 OpenAI 大模型调用
- **云存储**: 支持阿里云 OSS 对象存储

## 🏗️ 系统架构

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115.2 | 现代 Web 框架 |
| SQLAlchemy | 2.0.36 | ORM 框架 |
| Alembic | 1.15.1 | 数据库迁移工具 |
| Pydantic | 2.x | 数据验证与序列化 |
| APScheduler | 3.11.0 | 定时任务调度 |
| Redis | 5.2.1 | 缓存与会话存储 |
| Uvicorn | 0.30.6 | ASGI 服务器 |
| Python | 3.10+ | 运行环境 |

### 架构设计

```txt
📦 分层架构 (MVC)
├── 🎯 Controller   # 控制器层 - 处理HTTP请求
├── 🏢 Service      # 业务层 - 核心业务逻辑
├── 💾 CRUD         # 数据访问层 - 数据库操作
└── 📊 Model        # 模型层 - 数据模型定义
```

## 📁 项目结构

```txt
FastapiAdmin/backend/
├── 📁 app/                     # 项目核心代码
│   ├── 💾 alembic/             # 数据库迁移管理
│   ├── 🌐 api/                 # API 接口模块
│   │   └── v1/               # API v1 版本
│   │       ├── module_system/  # 系统管理模块
│   │       ├── module_monitor/ # 系统监控模块
│   │       ├── module_ai/      # AI 功能模块
│   │       └── module_*/       # 其他业务模块
│   ├── 📄 common/              # 公共组件（常量、枚举、响应封装）
│   ├── ⚙️ config/              # 项目配置文件
│   ├── 💖 core/                # 核心模块（数据库、中间件、安全）
│   ├── ⏰ module_task/         # 定时任务模块
│   ├── 🔌 plugin/              # 插件模块
│   ├── 📜 scripts/             # 初始化脚本和数据
│   └── 🛠️ utils/               # 工具类（验证码、文件上传等）
├── 🌍 env/                     # 环境配置文件
├── 📄 logs/                    # 日志输出目录
├── 📊 sql/                     # SQL 初始化脚本
├── 📷 static/                  # 静态资源文件
├── 🚀 main.py                  # 项目启动入口
├── 📄 alembic.ini              # Alembic 迁移配置
├── 📎 requirements.txt         # Python 依赖包
└── 📝 README.md                # 项目说明文档
```

### 模块设计

每个业务模块采用统一的分层结构：

```txt
module_*/
├── controller.py    # 控制器 - HTTP 请求处理
├── service.py       # 服务层 - 业务逻辑处理
├── crud.py          # 数据层 - 数据库操作
├── model.py         # ORM 模型 - 数据库表定义
├── schema.py        # Pydantic 模型 - 数据验证
└── param.py         # 参数模型 - 请求参数
```

## 🚀 快速开始

### 环境要求

- **Python**: 3.10+
- **数据库**: MySQL 8.0+ / PostgreSQL 13+ / SQLite 3.x
- **Redis**: 6.0+ (可选)

#### 1. 数据库初始化

```bash
# 生成迁移文件（仅首次或模型变更时）
python main.py revision  --env=dev(不加默认为dev)

# 应用数据库迁移
python main.py upgrade --env=dev(不加默认为dev)

# 如果是uv管理管理python则是
uv run main.py revision  --env=dev(不加默认为dev)
uv run main.py upgrade --env=dev(不加默认为dev)
```

#### 2. 启动服务

```bash
# 创建虚拟环境
python -m venv .venv
# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 如果是uv管理管理python则是
uv venv (默认创建.venv)


# 安装依赖
pip install -r requirements.txt
# 如果是uv管理管理python则是
uv add -r requirements.txt
或
uv sync

# 开发环境启动
python main.py run --env=dev (不加默认为dev)

# 生产环境启动
python main.py run --env=prod (不加默认为dev)

# 如果是uv管理管理python则是
uv run main.py run --env=dev (不加默认为dev)
uv run main.py run --env=prod (不加默认为dev)
```

#### 3.代码格式化

```bash
# 检查当前目录所有 Python 文件
ruff check
# 检查并自动修复问题
ruff check --fix
# 监听文件变化并重新检查
ruff check --watch

# 如果是uv管理管理python则是
uv run ruff check
uv run ruff check --fix
uv run ruff check --watch
```

## 📜 相关链接

- **FastAPI 官方文档**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **SQLAlchemy 文档**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)
- **Pydantic 文档**: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)

## 💬 支持与反馈

如果您在使用过程中遇到问题或有任何建议，请通过以下方式联系我们：

- 🐛 **Bug 报告**: 请在 GitHub Issues 中提交
- 💡 **功能建议**: 请在 GitHub Discussions 中讨论
- 💬 **技术交流**: 欢迎参与项目讨论

---

❤️ **感谢您的关注和支持！** 如果这个项目对您有帮助，请给我们一个 ⭐️ Star！
