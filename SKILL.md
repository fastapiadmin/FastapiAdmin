---
name: "fastapiadmin-dev"
description: "FastapiAdmin full-stack dev guide: repo map, run/verify commands, backend module & frontend web conventions. Invoke before writing code, creating modules/pages, debugging, or running builds/tests in this repo."
---

# FastapiAdmin 全栈开发指南

在本仓库做任何开发、调试、构建之前，先按本 skill 对齐工程结构与约定，避免跨端改漏、命名错位。

## 1. 工程地图

| 目录 | 说明 | 技术栈 |
| --- | --- | --- |
| `backend/` | 后端服务（入口 `main.py`，本地端口见 `app/config/setting.py` 的 SERVER_PORT，通常 8001） | FastAPI + SQLAlchemy + Alembic + Redis + uv |
| `frontend/web/` | 管理后台（pnpm 包，Node >= 20） | Vue3 + Vite + TS + Element Plus + Tailwind4 + Pinia |
| `frontend/app/` | 小程序/移动端 | uni-app（有独立约定，见 `frontend/app/.agents/skills/wot-ui-*`） |
| `frontend/docs/` | 项目文档站（中英双语 `src/guide` 与 `src/en/guide`） | VitePress |
| `docker/` | 部署（backend/mysql/nginx/redis） | docker-compose |
| 根目录 | `README.md`、`REQUIREMENTS.md`、`CONTRIBUTING.md` | 需求与规范，做大功能前先读 |

### backend/app 关键位置

| 位置 | 说明 |
| --- | --- |
| `modules/<模块>/<功能>/` | 业务模块：controller/service/crud/model/schema + 模块根 `plugin.toml` |
| `plugin/` | 独立插件目录（如 `plugin/module_example/demo`），与 modules 同构、可插拔 |
| `api/v1/routers.py` | 全部路由的注册处 |
| `core/` | 基建：database、base_crud、base_model、security、permission、dependencies、exceptions、ap_scheduler（定时任务）、sse_manager、middlewares |
| `scripts/initialize.py` | 启动时自动执行迁移并导入 `sql/*.json` 种子数据 |
| `sql/*.json` | 菜单/角色/用户/部门/字典/参数等种子数据 |
| `templates/{python,ts,vue}/` | 代码生成器 jinja2 模板 |
| `tests/` | pytest（conftest 自建临时库并初始化数据） |
| `utils/` | crypto/password/excel/upload/xss 等工具函数 |

### frontend/web/src 关键位置

| 位置 | 说明 |
| --- | --- |
| `api/module_x/` | API 层，与后端模块一一对应 |
| `views/module_x/` | 业务页面；页面私有组件放同目录 `components/` |
| `components/` | 公共组件 FaXxx（forms/tables/charts/modal/display 等）——写页面前先找现成的 |
| `hooks/core/` | 开发套件：useTable、useCrudForm、useCrudDialog、useTableColumns、useAuth、useImportExport、useConfirm |
| `directives/permission/` | `v-hasPerm` 按钮权限指令 |
| `router/` | `routes.ts` 静态壳 + guards/MenuProcessor/RouteRegistry 动态路由管道 |
| `store/modules/` | pinia stores（user/worktab/menu/setting/dict…），持久化用 pinia-plugin-persistedstate |
| `locales/langs/` | i18n 词条（zh.json / en.json） |
| `utils/` | http(request 封装)、auth、storage、navigation、download、sse 等 |

## 2. 常用命令

后端（`cd backend`，优先用 uv）：

```bash
uv run main.py run --env=dev          # 启动（dev 默认，DEBUG=True 时自动 reload）
uv run main.py revision -m "说明"      # 生成 Alembic 迁移（autogenerate）
uv run main.py upgrade --env=dev      # 应用迁移到 head
uv run pytest                         # 跑 tests/
```

前端 web（`cd frontend/web`）：

```bash
pnpm i            # 安装
pnpm dev          # 开发
pnpm ts:check     # vue-tsc 类型检查（改完 TS/Vue 必跑）
pnpm lint         # eslint + prettier + stylelint
pnpm test         # vitest
pnpm build        # 构建
```

`frontend/app`、`frontend/docs` 各自目录内 `pnpm` 管理自己。

### 首次启动（新人跑通）

1. 复制 `backend/env/.env.example` 为 `.env.dev`，按文件头注释修改必改项（`DATABASE_PASSWORD` / `REDIS_PASSWORD` / `OPENAI_API_KEY`）；`DATABASE_TYPE` 支持 mysql / postgres / sqlite——本地体验用 sqlite 可零配置起跑
2. `uv sync && uv run main.py run --env=dev`：**启动时自动执行迁移并导入 `sql/*.json` 种子数据**（菜单/角色/用户/字典等），无需手动建表导数；dev 环境检测到模型变更还会自动生成并应用迁移
3. 前端：`frontend/web` 内 `pnpm install && pnpm dev`（小程序/App H5 调试用 `pnpm dev:h5`）
4. 默认账号：`super` / `admin` / `user`，密码均为 `123456`（已校验种子 bcrypt 哈希；官方文档见 `frontend/docs/src/guide/start.md`，部署后应立即修改）
5. 访问地址：Web 前端 `http://localhost:{VITE_PORT}`（`frontend/web/.env` 为 5180）；后端 `http://localhost:8001`、Swagger `http://localhost:8001/docs`、API 前缀 `/api/v1`
- Docker 一键部署：根目录 `./deploy.sh`（详见 `docker/README.md`）

前端代理：vite 将 `VITE_APP_BASE_API` 前缀代理到 `VITE_API_BASE_URL`（见 `vite.config.ts`），本地开发无 CORS 问题；AI WebSocket 用 `VITE_APP_WS_ENDPOINT` 直连后端（不走代理）。

## 3. 后端约定（backend/app）

- 模块结构：`app/modules/<模块>/<功能>/`，固定文件划分
  - `controller.py` 路由层、`service.py` 业务层、`crud.py` 数据层、`model.py` ORM、`schema.py` Pydantic
  - 模块根放 `plugin.toml`（name/title/version/description）
- 路由统一在 `app/api/v1/routers.py` 注册；路由类用 `OperationLogRoute`（自动操作日志）
- 权限：`Security(AuthPermission(["模块:资源:操作"]))`，如 `module_ai:chat:query`
- 响应：`SuccessResponse(data=..., msg=...)` + `response_model=ResponseSchema[T]`；业务错误抛 `CustomException`
- 基建都在 `app/core/`：`base_crud.py`、`base_model.py`、`base_schema.py`、`redis_crud.py`、`dependencies.py`、`exceptions.py`、`logger.py`（loguru，占位符用 `{}`)
- 配置：`app/config/setting.py` + `backend/env/.env`（模板见 `env/.env.example`）
- 改了 model 必须生成并执行 Alembic 迁移；初始菜单/角色等数据在 `backend/sql/*.json`
- 新模块两种放法：常规业务放 `app/modules/`，可插拔/示例性质放 `app/plugin/`（结构相同，都有 `plugin.toml`）
- 代码生成：`backend/templates/{python,ts,vue}/*.jinja2` 配合 generator 模块（后台「代码生成」功能可视化生成）；**生成/修改代码后必须重启后端**——dev reload 只在文件变更时重载，动态路由发现（`app/core/discover.py`）只在启动时执行，不重启新模块不生效且会静默失败

## 4. 前端 web 约定（frontend/web/src）

- API 层：`api/module_x/xxx.ts`，对象字面量方法 + `request`（来自 `@utils`），泛型用全局 `ApiResponse<T>` / `PageResult<T>`；URL 与后端 controller 对齐（如 `/system/dict/type/list`）
- 页面：`views/module_x/...`；页面私有子组件放同目录 `components/` 下，公共组件命名 `FaXxx`
- CRUD 页面优先复用现成套件：列表用 `useTable` + `FaTable` + `FaSearchBar`，弹窗表单用 `useCrudDialog`/`useCrudForm` + `FaDialog`，列定义用 `useTableColumns`，导入导出用 `useImportExport`——参考已有 `views/module_system/` 页面写法，不要手写 ElTable/ElDialog
- 权限控制：按钮级用 `v-hasPerm="'sys:user:add'"`（支持数组）；代码内判断用 `useAuth().hasAuth(...)`；后端标识 `模块:资源:操作` 三段式，前后端保持一致
- i18n：文案用 `$t('key')`，词条加到 `locales/langs/zh.json` 与 `en.json` 两份
- 自动导入：vue API（`ref`/`computed`/`watch`/`onMounted` 等）无需 import；Element Plus 组件模板内直接用；`ElMessage` 等按现有文件习惯可显式 import
- 路由：静态壳路由在 `router/routes.ts`；业务路由来自后端菜单（`guards.ts` → `MenuProcessor` → `RouteRegistry` 动态 addRoute）。新增页面要在「菜单管理」配置 route_path/route_name/component_path/keep_alive
- KeepAlive 与工作栏按「组件名」匹配：`defineOptions({ name })` 必须与菜单的 route_name 一致，否则页面缓存/缓存排除（exclude）会失灵
- 有副作用页面（WebSocket/定时器/全局事件监听）必须实现 `onActivated`/`onDeactivated`：deactivated 时释放资源，activated 时按需恢复。`onUnmounted` 只在缓存被驱逐时触发，不能作为唯一清理点（详见第 7 节）
- 路由视图缓存为**单层**：目录路由不挂组件，`KeepAlive` 只存在于 `layouts/fa-page-content/index.vue` 一处，缓存键是叶子路由 `path`（query 变化不重挂载，改键逻辑见同文件 `routeViewCacheKey`）
- 环境变量：公共 `.env`（`VITE_APP_BASE_API=/api/v1` 请求前缀、`VITE_PORT=5180`）；`.env.development`（`VITE_API_BASE_URL=http://127.0.0.1:8001` 代理目标；AI WebSocket `VITE_APP_WS_ENDPOINT=ws://localhost:8001` 直连）
- WebSocket 鉴权（AI chat）：token 经 `Sec-WebSocket-Protocol` 传 `["access_token", "access_token." + jwt]`，后端在握手阶段 `websocket_authenticate` 校验
- 图标：`FaSvgIcon` + iconify（`ri:` / `ep:` / `line-md:`）；i18n 用 `$t(...)`

## 5. 新增一个业务功能（全栈流程）

1. 后端建模块（参考 `app/modules/system/dict/`；标准 CRUD 表可先用后台「代码生成」可视化产出，再调整）
2. `app/api/v1/routers.py` 注册路由
3. `uv run main.py revision` + `upgrade` 做迁移；菜单/按钮权限写入 sys_menu（后台「菜单管理」配置 route_path/route_name/component_path/keep_alive/按钮权限）
4. 前端新建 `api/module_x/xxx.ts` 与 `views/module_x/` 页面（复用 useTable/FaTable 套件）
5. 前后端权限标识保持一致（`模块:资源:操作`），页面按钮加 `v-hasPerm`
6. 验证：后端 `uv run pytest`；前端 `pnpm ts:check`、`pnpm lint`、`pnpm test`

## 6. 提交规范

- husky + commitlint + git-cz（`pnpm commit` 交互式生成）；type 用 feat/fix/refactor/chore/docs/test 等
- lint-staged 会自动格式化暂存文件，不要绕过 hook

## 7. KeepAlive 缓存与连接类资源（踩过坑，勿回退）

- KeepAlive 的 `include` 来自 worktab `opened`（`layouts/fa-page-content/index.vue`），`opened` 为空时 include 为 `undefined`——KeepAlive 对 undefined include **不做 prune**，不要以为「标签清了缓存就没了」
- KeepAlive 内部缓存无法从外部直接清空，唯一手段是改变 `include`/`exclude` 触发内部 prune。登出场景由 `worktab.store.ts` 的 `clearAll()` 把待删标签组件名写入 `keepAliveExclude` 驱逐旧实例（下次 `openTab` 的 `removeKeepAliveExclude` 自动移出），改 store 时勿删这段
- WebSocket 守卫必须覆盖握手期：`if (ws && ws.readyState !== WebSocket.CLOSED) return`。只挡 `OPEN` 会在 CONNECTING 期间重入时创建新连接并覆盖旧引用，泄漏的连接照样握手成功并弹提示（AI chat 曾因此登出→登录后出现多条 ws + 多条「连接成功」）
- 主动断开先摘 `onopen/onmessage/onerror/onclose` 回调再 `close()`，避免关闭竞态触发提示或状态回调
- 路由出口 KeepAlive **只能有一层**，且不要给它加 `:max`：动态目录路由的 `component` 必须保持 `undefined`（`MenuProcessor.mapMenuNode` / `RouteTransformer.handleNormalRoute`），靠 vue-router 的 RouterView 深度跳级直达叶子页面。历史上给目录挂过壳组件（`NestedRouterParent`），壳实例会随缓存同时存活多份、同一页面被重复挂载，导致切换菜单时接口重复请求；`:max` 的 LRU 则会在标签仍打开时挤掉最早的页面，切回时同样无谓重挂载。缓存集合只由 `include`/`exclude` 表达
- 排查「重复弹窗/重复连接/重复请求」类 bug 的路径：先 grep 提示文案定位全库唯一来源（N 次弹窗 = N 个实例或 N 次重入）→ 查 KeepAlive include/exclude 计算与登出→登录导航链（登录守卫 404→replace 重定向会叠加竞态窗口）→ 菜单配置查 `backend/sql/sys_menu.json`（确认 route_name 唯一、keep_alive）排除后端

## 8. 已知注意点

- 静态前端托管：`register_frontend`（`app/__init__.py`）检查与挂载必须用同一个 `path_conf.FRONTEND_DIST_DIR`（backend/dist）。曾因检查用 path_conf、挂载硬编码 `frontend/web/dist` 导致 500：`check_dir=False` 时启动不报错，**首次请求才炸**，必须看 loguru 日志（`backend/logs/fastapiadmin.log`）才能定位
- 模板/脚本里不要用 `{% for %}` + `{% set %}` 累计布尔标志：Jinja2 for 块作用域隔离，循环外读到的仍是初值。用过滤器一次性计算，如 `{% set has_x = columns | selectattr('python_type', 'equalto', 'date') | list | length > 0 %}`（代码生成器 schema.py.jinja2 曾因此漏生成 validator import，生成产物 NameError、后端起不来）
- 跨端需求（web + 小程序）要同时评估 `frontend/web` 与 `frontend/app` 两套代码，API 层各自维护
- 小程序侧有自己的 skills（`frontend/app/.agents/skills/`），改小程序 UI 时遵循 wot-ui 约定
- 文档站改动记得中英两份（`src/guide/` 与 `src/en/guide/`）

## 9. 前端产物验证（dist）

**源码已修 ≠ 部署已修。** dist 是生成物、不入库（`.gitignore`），但仓库内存在多份预构建副本并直接被打进部署，改完前端源码必须重建并同步，否则线上仍跑旧行为（AI chat 重复「连接成功」就因此漏判过一轮：源码 `e39a369b` 已修，三份 dist 仍停在修复前）。

**三份产物与各自的服务入口**

| 产物 | 服务入口 |
| --- | --- |
| `frontend/web/dist` | 构建输出（`pnpm build:prod` 的 outDir） |
| `docker/nginx/web/dist` | docker 部署的 `/web`（`nginx.conf` 的 `alias /usr/share/nginx/html/web/dist`） |
| `backend/dist` | 一体化部署时 `app.frontend("/")` 托管（`path_conf.FRONTEND_DIST_DIR`） |

移动端同理：`docker/nginx/app/dist/build/h5`（nginx 的 `/app`）。

**重建 + 同步**

```bash
cd frontend/web && pnpm build:prod          # 输出 frontend/web/dist
cd ../.. && rsync -a --delete frontend/web/dist/ docker/nginx/web/dist/ \
              && rsync -a --delete frontend/web/dist/ backend/dist/
```

必须带 `--delete`：产物文件名带 content hash，不带会把旧 chunk 留在目录里。

**验证要核到产物，不能只看 `src/`**（minify 后函数名/注释会丢，但 `WebSocket.CLOSED` 这类属性访问、以及提示文案字符串会保留）：

```bash
grep -l "ai/chat/ws" docker/nginx/web/dist/js/*.js                    # 定位 chunk
grep -oE '.{0,60}readyState.{0,60}' <chunk> | grep -i websocket       # 核守卫（-oE 重复上限 255）
```

例：旧包 `if (ws?.readyState === WebSocket.OPEN) return;`（`CLOSED` 命中 0 次）；修复后 `if (ws && ws.readyState !== WebSocket.CLOSED) return;`。

**收到「源码没改好」的线上反馈时，第一步先核 dist 产物特征字符串**，再回源码；docker 部署还要重新打镜像/重传 `docker` 目录才算生效。

## 10. 本地开发与测试环境（当前实操）

- 本地配置：`backend/env/.env.dev`（不要提交真实密码/Key）。
- 启动后端：`cd backend && uv run main.py run --env=dev`，默认 `http://localhost:8001`。
- 启动 Web：`cd frontend/web && pnpm dev`，当前 Vite 端口为 **5180**（以启动输出为准），访问 `/web`。
- 本地 dev 自动执行 Alembic 与种子数据；改动 model 后必须生成/应用迁移。
- 生产：`https://service.fastapiadmin.com`，健康检查 `/api/v1/monitor/health/check`，Web `/web/`。
- 生产当前 `DEMO_ENABLE=true` 时会统一拦截写操作并返回“演示环境，禁止操作”；测试写接口前先确认环境，不要把该返回误判为代码故障。

## 11. 测试用例与测试数据规范

### 11.1 用例设计

新增功能至少覆盖：

1. **等价类**：合法/非法/空值/null/格式错误；
2. **边界值**：`min-1/min/min+1/max-1/max/max+1`；
3. **输入域**：类型、长度、枚举、关联字段、状态流转；
4. **正交组合**：角色 × 状态、数据权限 × 状态、协议 × 分片参数等；
5. **接口**：正常路径、非法输入、越权、重复提交、批量部分失败；
6. **UI**：空值校验、成功创建、按钮/弹窗/富文本/下拉等真实交互。

### 11.2 已有测试资产

- `backend/tests/test_input_domain_boundaries.py`：输入域/边界值/正交组合，约 120 个参数化用例；
- `backend/tests/`：服务层、SQL 控制台、SSH、调度器、存储、时区等回归；
- `frontend/web/src/__tests__/`：路由/HTTP/冒烟测试；
- `docs/TEST-COVERAGE.md`：覆盖矩阵、执行记录和剩余缺口，改测试状态时同步更新。

### 11.3 测试数据

- 统一使用 `e2e_` 前缀，每次运行生成唯一后缀；
- 由 AI 创建、使用、清理；不要依赖用户手工准备测试数据；
- 清理时先 API 删除，再按需硬删除遗留的软删除行，并清理对象存储桶/对象；
- 不把真实密码、SSH 私钥、第三方 Key 写进测试文件或提交记录。

### 11.4 执行命令

```bash
cd backend && UV_CACHE_DIR=/tmp/uv-cache-test uv run --no-sync pytest -q
cd frontend/web && pnpm test && pnpm ts:check && pnpm build
```

### 11.5 浏览器自动化

- 使用隔离的临时浏览器 profile；
- 启用 `--password-store=basic --use-mock-keychain --disable-sync`，不要复用用户日常浏览器/钥匙串；
- 对动态表单按 **字段名** 定位，不要写死输入框索引（菜单类型切换会改变字段顺序）；
- Element Plus 下拉/富文本优先用真实鼠标坐标点击，而不是只改 DOM value。

## 12. 时间、消息与调度契约（已验证，勿回退）

- 数据库统一存 UTC；接口/页面统一按 `settings.TIMEZONE`（默认 `Asia/Shanghai`）展示。
- 时间输出统一走 `app/core/validator.py::to_local_datetime` 或响应编码器；裸 `datetime` 在响应层也要做时区转换。
- 用户导入导出：
  - Excel 导出前必须把 aware datetime 转成 naive（openpyxl 不支持时区）；
  - 导入模板中文性别映射：男→0、女→1、未知→2；
  - 空/损坏 Excel 返回 400，不允许 500。
- SQL 控制台：多语句、未确认写操作、超 200 行、敏感列都有既有约束；不要为了“显示方便”强行给裸 DATETIME 加 8 小时。
- 全局消息：`frontend/web/src/utils/message.ts` 对 success/error 做短时合并；新增页面不要再叠加多条同义提示。
- 调度器：`reconcile_node_jobs` 启动时会刷新已存在 job；改 node.func/trigger 后必须确认旧 job 参数被替换，否则会出现“数据库已改、调度器仍报旧原因”。

## 13. 生产部署与备份

- 部署前必须确认并备份：后端源码、`docker/nginx/web`、数据库 dump；
- 生产备份目录：`/home/FastapiAdmin/backups/release-<时间戳>/`；
- 部署后验证：health、web、登录、关键列表、调度器日志；
- 生产是演示模式时，写操作/导出被拦截是配置行为；
- 不把生产凭据、dump、密钥写入仓库。

## 14. 当前统一契约

- 用户账号：**3–32 位**，字母开头，仅字母/数字/`_ . -`；
- 角色编码：**2–64 位**，字母开头，仅字母/数字/下划线；
- 角色数据权限：1/2/3；状态：0/1；
- 菜单类型：1 目录、2 菜单、3 按钮、4 外链；
- 公告类型：1 通知、2 公告；状态 0/1/2；
- 存储对象 key 不接受 `..`；对象存储绝对路径会被规范化为桶内路径。

## 15. AI 协作流程

1. 先读本 skill 与 `docs/TEST-COVERAGE.md`，确认现有覆盖和已知缺口；
2. 修改前先查现有组件/套件，避免重复造轮子；
3. 改完执行对应验证，至少“单元/接口 + 类型/构建”两类；
4. 涉及生产写操作、部署、master、凭据时先获得当次明确确认；
5. 不把“页面能打开”当成“功能通过”；写操作要真实提交并清理测试数据；
6. 交付时说明：改了什么、验证了什么、未覆盖什么。
