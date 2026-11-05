<div align="center">
     <p align="center">
          <img src="./frontend/web/public/logo.png" width="150" height="150" alt="logo" />
     </p>
     <h1>FastApiAdmin <sup style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.4em; vertical-align: super; margin-left: 5px;">v3.0.0</sup></h1>
     <h3>🚀 一套代码交付 Web / H5 / 小程序，AI 代码生成 + RBAC + Docker 开箱即用</h3>
     <p>基于 <b>FastAPI + Vue3 + TypeScript</b> 的企业级全栈底座：类型共享、权限完整、三端同源</p>
     <p align="center">
          <a href="https://github.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://img.shields.io/github/stars/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Stars">
          </a>
          <a href="https://github.com/fastapiadmin/FastapiAdmin/forks" target="_blank">
               <img src="https://img.shields.io/github/forks/fastapiadmin/FastapiAdmin?style=social" alt="GitHub Forks">
          </a>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://gitee.com/fastapiadmin/FastapiAdmin/badge/star.svg?theme=dark" alt="Gitee Stars">
          </a>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin.git" target="_blank">
               <img src="https://gitee.com/fastapiadmin/FastapiAdmin/badge/fork.svg?theme=dark" alt="Gitee Forks">
          </a>
          <a href="https://atomgit.com/fastapiadmin/FastapiAdmin" target="_blank">
               <img src="https://atomgit.com/fastapiadmin/FastapiAdmin/star/badge.svg" alt="AtomGit G-Star">
          </a>
          <br>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank">
               <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
          </a>
          <a href="https://github.com/fastapiadmin/FastapiAdmin/commits" target="_blank">
               <img src="https://img.shields.io/github/commit-activity/m/fastapiadmin/FastapiAdmin?style=flat&label=commits" alt="Commit Activity">
          </a>
          <img src="https://img.shields.io/badge/Python-≥3.12-blue">
          <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue">
          <img src="https://img.shields.io/badge/MySQL-≥8.0-blue">
          <img src="https://img.shields.io/badge/Redis-≥7.0-blue">
     </p>

简体中文 | [English](./README.en.md)

</div>

## 🤖 让 AI 在这个项目里干活

把这个仓库交给 AI 时，先让它读根目录的 [`SKILL.md`](./SKILL.md)：

- 工程地图与前后端约定；
- 本地启动、测试、构建命令；
- 测试用例设计、`e2e_` 测试数据和清理规范；
- 时间/消息/调度契约；
- 生产部署、备份和不可逆操作边界；
- 当前已统一的账号/角色编码契约。

测试覆盖与执行记录见 [`docs/COVERAGE-PLAN.md`](./docs/COVERAGE-PLAN.md)。AI 不应只凭“页面能打开”判断功能通过，写操作必须真实执行并清理测试数据。

## 🖥️ 界面一览

**Web 端**

![仪表盘](frontend/web/public/dashboard.png)

**移动端（H5 / 小程序 / App 同一套代码）**

<p>
<img src="frontend/web/public/app_login.png" width="180" alt="登录与拼图验证" />
<img src="frontend/web/public/app_home.png" width="180" alt="移动端工作台" />
<img src="frontend/web/public/app_mine.png" width="180" alt="个人中心" />
</p>

> 三端共享同一套品牌 Token：Logo、主色、圆角、间距、深色层级与危险操作语义保持一致。

## 💡 为什么选择 FastapiAdmin？

| 你需要的 | FastapiAdmin | Django Admin | 纯前端模板 |
|---------|:-----------:|:-----------:|:---------:|
| 🎯 **开箱即用**的后台系统 | ✅ | ⚠️ 功能有限 | ❌ 只有 UI |
| ⚡ **FastAPI 异步**高性能后端 | ✅ | ❌ 同步为主 | ❌ 无后端 |
| 🔐 **RBAC** 菜单/按钮/数据三级权限 | ✅ | ❌ 基础 | ❌ |
| 🤖 **代码生成器**（选表 → 出前后端代码） | ✅ | ❌ | ❌ |
| 📱 **移动端**（H5 + 小程序）一体 | ✅ | ❌ | ❌ |
| 🐳 **Docker 一键部署**（含 Nginx + SSL） | ✅ | ❌ | ❌ |

> 👉 详细技术选型对比：[为什么选择 FastapiAdmin？](https://service.fastapiadmin.com/guide/why)

### ✅ 适合这些场景

- 需要在 **1–4 周**内交付可用的企业后台、运营系统或客户项目；
- 团队希望 **前后端类型共享**，减少接口联调与重复建模；
- 同一业务要同时覆盖 **Web 管理端 + 移动端 / 小程序**；
- 需要代码生成、RBAC、审计日志、定时任务等“底座能力”，而不是从零搭。

### ⚠️ 不适合

- 需要完整 IM（文件、撤回、已读回执、多端同步）的场景；
- 一开始就要求多实例水平扩展的实时聊天 / 调度场景（当前按单实例设计）。

## 🍪 在线体验

| 端 | 地址 | 账号 |
|----|------|------|
| 💻 Web 端 | [service.fastapiadmin.com/web](https://service.fastapiadmin.com/web) | `admin` / `123456` |
| 📱 移动端 | [service.fastapiadmin.com/app](https://service.fastapiadmin.com/app) | `admin` / `123456` |
| 📖 官方文档 | [service.fastapiadmin.com](https://service.fastapiadmin.com) | 无需登录 |

## 🚀 5–15 分钟本地跑起来

```bash
# 1. 克隆
git clone https://gitee.com/fastapiadmin/FastapiAdmin.git

# 2. 配置环境
cp backend/env/.env.example backend/env/.env.dev
cp frontend/web/.env.development.example frontend/web/.env.development

# 3. 启动后端（首次自动建表 + 初始化数据）
cd backend && uv sync && uv run main.py run --env=dev

# 4. 启动前端
cd ../frontend/web && pnpm install && pnpm run dev

# ✅ 浏览器打开 http://127.0.0.1:5173，用 admin/123456 登录
```

> 首次启动会自动建表并写入演示数据；后端默认 `8001`，前端默认 `5173`。生产环境请使用 Alembic 迁移与独立密钥。

| 环境要求 | |
|---------|------|
| Python ≥ 3.12 | Node.js ≥ 20.0 + pnpm |
| MySQL 8.0+ / PostgreSQL 14+ | Redis 6.x / 7.x |

### 🐳 或者：Docker 一键部署

```bash
cp docker/.env.example docker/.env    # 填写 MySQL / Redis 密码
./deploy.sh                           # 自动构建镜像并启动全栈（含 Nginx + SSL）
```

> 端口、SSL 证书、前端构建等细节见 [Docker 部署文档](docker/README.md)。

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

## 🧱 技术栈

| 层 | 技术 |
| --- | --- |
| 后端 | FastAPI · Pydantic 2 · SQLAlchemy 2 · Alembic · Redis |
| Web | Vue 3 · TypeScript · Vite · Element Plus · Pinia · Tailwind |
| 移动端 | UniApp · Vue 3 · Wot Design Uni |
| AI | Agno · 可切换模型供应商 |
| 部署 | Docker Compose · Nginx · SSL |

## 📌 内置功能

> **200+ REST 接口** · MySQL / PostgreSQL / SQLite 三方言 · SFTP / S3 / OSS / COS / OBS 五种存储协议 · `ENABLED_MODULES` 一行开关裁剪模块

### 核心模块（始终启用，不可裁剪）

| 模块 | 包含能力 |
|------|---------|
| 📊 仪表盘 | 工作台、数据分析 |
| ⚙️ 系统管理 | 用户 / 角色 / 菜单 / 部门 / 岗位 / 字典 / 参数 / 公告 / 工单 / 版本 |
| 👀 监控管理 | 在线用户 / 服务器监控 / 缓存监控 |
| 📝 日志管理 | 操作日志审计 |
| 🧰 开发工具 | 接口文档 |

### 扩展模块（默认启用，可用 `ENABLED_MODULES` 裁剪）

| 模块 | 包含能力 | 裁剪开关 |
|------|---------|---------|
| 🧩 任务管理 | 定时任务调度 + 可视化工作流编排（内置业务节点） | `task` |
| 🔧 代码生成器 | 选表 → 生成前后端全量代码 | `generator` |
| 📁 数据存储 | 统一文件 / 对象存储（SFTP / S3 / OSS / COS / OBS） | `storage` |
| 🤖 AI 对话 | 基于 Agno 的智能体对话 | `ai` |
| 💬 内部聊天 | 系统内用户**纯文字**私聊 / 群聊（WebSocket 实时推送 + 未读角标） | `chat` |

## 🔧 模块裁剪

扩展模块可通过 `backend/app/config/setting.py` 中的 `ENABLED_MODULES` 按需启用 / 停用——**移除列表项即可，无需删除任何代码或菜单**，对应的 REST 接口、WebSocket 端点与初始化逻辑将自动不加载：

```python
# 例如：停用内部聊天与 AI 对话，保留其余扩展模块
ENABLED_MODULES = ["generator", "task", "storage"]
```

## 🚦 部署说明

- **聊天边界**：内部聊天定位为**轻量内部沟通**，仅支持纯文字消息，**不含文件传输、撤回、已读回执、多端同步等 IM 能力**；如有强 IM 需求，请对接企业微信 / 钉钉 / 飞书等成熟产品。随时可在 `ENABLED_MODULES` 中移除 `chat` 停用。
- **单实例部署**：实时功能（内部聊天 WebSocket、定时任务调度器）基于单实例内存连接与本地调度实现，请以**单实例方式**部署。如需水平扩展，请自行引入 Redis Pub/Sub 或消息队列。
- **密钥安全**：所有第三方密钥（AI、云存储等）请配置在 `backend/env/.env.*` 环境变量中，**切勿提交到仓库或写入数据库**。
- **数据库迁移**：正式环境请使用 Alembic 迁移（`uv run alembic upgrade head`）管理表结构变更，`create_all` 仅用于首次初始化的兜底。

## 📷 更多截图

| 登录 + 拼图验证 | 代码生成 | AI 助手 |
| ---- | -------- | ------- |
| ![登录](frontend/web/public/login.png) | ![代码生成](frontend/web/public/gencode.png) | ![AI](frontend/web/public/ai.png) |

> 截图来自当前版本：浅色主题、真实接口数据与最新品牌视觉。

## ❓ 常见问题

**Q：启动后登录提示验证码错误？**  
A：确认后端 Redis 正常，并完成页面拼图验证；开发环境账号为 `admin / 123456`。

**Q：可以只用 Web 端吗？**  
A：可以。`frontend/web` 可独立启动；移动端工程独立，不影响 Web。

**Q：如何裁剪模块？**  
A：修改 `backend/app/config/setting.py` 的 `ENABLED_MODULES`，接口与初始化逻辑会自动卸载。

**Q：生产环境数据库怎么初始化？**  
A：使用 `uv run alembic upgrade head`，不要依赖 `create_all`。

## 📖 文档地址

- 🌐 [官网文档](https://service.fastapiadmin.com) — 完整开发指南、架构设计、二开教程
- 📁 子工程 README：[backend](backend/README.md) · [web](frontend/web/README.md) · [移动端](frontend/app/README.md) · [Docker](docker/README.md)

## 🤝 参与贡献

欢迎提交 Issue / PR！详见 [贡献指南](https://service.fastapiadmin.com/about/contributing)。

## 👥 社区与支持

<p>
<img src="frontend/web/public/group.png" width="200" height="260" style="margin-right:30px"/>
<img src="frontend/web/public/wechatPay.jpg" width="200" height="260" />
</p>

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=fastapiadmin/FastapiAdmin&type=Date)](https://star-history.com/#fastapiadmin/FastapiAdmin&Date)

## 👥 贡献者
> 感谢以下所有给 FastapiAdmin 贡献过代码的 开发者。

<a href="https://github.com/fastapiadmin/FastapiAdmin/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fastapiadmin/FastapiAdmin"/>
</a>

## 🙏 鸣谢

> 如果你觉得项目有用，请给一个 ⭐️ Star 支持！

- 后端：[FastAPI](https://fastapi.tiangolo.com/) · [Pydantic](https://docs.pydantic.dev/) · [SQLAlchemy](https://www.sqlalchemy.org/) · [APScheduler](https://github.com/agronholm/apscheduler)
- 前端：[Vue3](https://cn.vuejs.org/) · [TypeScript](https://www.typescriptlang.org/) · [Vite](https://vitejs.dev/) · [Element Plus](https://element-plus.org/)
- 移动端：[UniApp](https://uniapp.dcloud.net.cn/) · [Wot Design Uni](https://wot-ui.cn/)
- AI：[Agno](https://github.com/agno-agi/agno)
