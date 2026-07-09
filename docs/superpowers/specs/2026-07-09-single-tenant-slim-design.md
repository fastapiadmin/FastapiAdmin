# CodataAdmin 第一阶段:禁用商业化模块 + 单租户化

日期:2026-07-09
状态:已实现(第一阶段,2026-07-09)
分支:`feat/single-tenant-slim`

## 背景与目标

CodataAdmin fork 自 FastapiAdmin,是一个 Python / FastAPI 全栈后台框架(后端约 36,000 行)。
它被选定为 Codata 的**控制面后端服务**,负责:权限、认证、定时、skills 治理。

FastapiAdmin 原本是**多租户 SaaS 商业化框架**,自带订单、发票、套餐售卖、租户自助开通等模块,
并把"多租户 + 套餐权限"焊进了 RBAC 内核。这些对我们的场景(公司内部私有部署、多部门共用一套)
是多余且干扰的。

**本阶段目标:** 让 CodataAdmin 干净地服务于"单公司、多部门"场景,做法是
**禁用商业化模块 + 单租户化**,而**不是删代码**。

### 为什么是"禁用/短路"而非"删除"

反向依赖检查发现:`module_system`(auth/role/user/dept)乃至核心的
`core/permission.py`、`core/base_model.py`、`core/dependencies.py` 都 import 了
`module_platform` 的 `tenant` / `package` / `menu`。`tenant` 被 13 个外部文件引用,`package` 13 个。

直接删除 = 拆内核炸弹,极易搞崩认证与 RBAC。在刚接手、系统尚未跑稳的阶段,
正确形态是**切断入口 + 短路内核商业化判断**,保留代码和字段:零迁移、可回退、几小时可落地。
彻底删除 SaaS 代码(尤其从内核剥离 tenant)留作**第二阶段**独立重构,且未必值得做。

## 关键代码定位(改造前已确认)

- 路由挂载入口:`app/init_app.py:101-104`,四行 `include_router`(common / monitor / platform / system)。
- 商业化路由聚合点:`app/api/v1/module_platform/__init__.py`。
- 系统路由聚合点:`app/api/v1/module_system/__init__.py`。
- 单租户内核短路点:
  - `app/core/base_model.py:15` —— 每张表挂 `tenant_id`(保留字段,不动)。
  - `app/core/permission.py:110` —— 权限校验查 `PackageService`(套餐决定可开菜单)。
  - `app/core/dependencies.py:295` —— 同上,依赖注入层查 package。
  - `app/core/ap_scheduler.py:606-607` —— 定时任务跑 `OrderService`/`TenantService` 账务逻辑。
  - `app/init_app.py:25` —— 启动时已引用 `TenantService`,可顺势建默认租户。

## 模块处置表

| 模块 | 行数 | 处置 |
|---|---|---|
| `module_system`(auth/user/role/dept/dict/log/notice/params/position) | 核心 | ✅ 保留 |
| `module_system/ticket`(工单) | 371 | ⚠️ 可选禁用(内部控制面用不到) |
| `module_platform/menu`(权限菜单) | 576 | ✅ 保留(RBAC 依赖) |
| `module_platform/email`(邮件) | 784 | ✅ 保留(通知可能需要) |
| `module_platform/tenant`(租户) | 1605 | ⚠️ 保留但后台化 + 固定默认租户 |
| `module_platform/order`(订单) | 1352 | ❌ 禁用 router + 关定时 job |
| `module_platform/package`(套餐售卖) | 552 | ❌ 禁用 router;内核判断短路 |
| `module_platform/invoice`(发票) | 729 | ❌ 禁用 router |
| `module_platform/self_service`(租户自助开通) | 871 | ❌ 禁用 router |
| `module_platform/plugin`(插件) | 544 | 🔸 视需要,默认保留 |
| `module_monitor`(cache/online/resource/server) | 1476 | ✅ 保留(运维看板,轻量) |
| `module_common`(file/monitoring) | 356 | ✅ 保留 |

## 改造方案

### A. 禁用商业化 API(改 1 个文件,零风险)

`module_platform/__init__.py`:注释掉以下 `include_router`,**import 语句保留不动**
(内核里的 `from ...package.service import` 仍需能 import,否则启动崩溃):

- ❌ `OrderRouter / PaymentRouter / RefundRouter / TenantOrderRouter`
- ❌ `PlatformInvoiceRouter / TenantInvoiceRouter`
- ❌ `PackageRouter`
- ❌ `TenantSelfServiceRouter`
- ✅ 保留 `MenuRouter`(RBAC)、`EmailRouter`(通知)
- ⚠️ `TenantRouter` 保留但后台化(见 D)

`module_system/__init__.py`:可选禁用 `TicketRouter`。

### B. 关闭商业化定时任务(改 `ap_scheduler.py`)

`ap_scheduler.py:606-607` 附近注册的、跑 `OrderService`/`TenantService` 的账务定时 job
(套餐到期、账单生成之类)——**关闭这些 job 的注册**。
**保留调度器本身**——它正是 Codata 控制面要用的定时能力。

### C. 单租户化(内核短路,谨慎改)

不删 tenant,固定成一个默认租户,所有部门/用户挂其下:

1. **默认租户**:启动初始化时确保存在一个 `default` 租户
   (`init_app.py:25` 已引 `TenantService`,顺势创建)。
2. **套餐权限短路**:`permission.py:110` 与 `dependencies.py:295` 中查 `PackageService`
   (套餐决定可开菜单)的逻辑,**短路成"不受套餐限制,全部菜单可用"**。
   权限自此只由 RBAC 角色 + 部门数据权限决定,套餐彻底退场。**这是单租户化最关键的一改。**
3. **保留 `tenant_id` 字段**:`base_model.py` 的 `tenant_id` 不动
   (拔字段要改所有表 + 迁移,风险大收益小);新数据一律写默认租户 id。
4. **tenant 后台化**:`TenantRouter` 从"用户可注册租户"改为"仅超管可见后台入口",
   或前端直接不暴露。

## 落地顺序与验证

| 步骤 | 改动 | 风险 | 验证方式 |
|---|---|---|---|
| 1 | 禁用商业化 router(A) | 极低 | 启动正常;Swagger 无 order/invoice/package/self_service |
| 2 | 关商业化定时 job(B) | 低 | 启动日志无账务 job;调度器仍在 |
| 3 | 建默认租户 + 套餐权限短路(C1/C2/C3) | 中 | 登录后可见全部菜单;RBAC 角色控制生效 |
| 4 | tenant 后台化(C4) | 低 | 普通用户看不到租户管理入口 |

每一步都应能独立启动验证,不一次性堆改动。

## 核心原则

**能"关"就不"删"。** 保留代码与字段,只切断入口和内核商业化判断。
零迁移、可回退。删代码属于第二阶段(如届时仍有必要)。

## 非目标(本阶段明确不做)

- 不从内核剥离 tenant / 不删 `tenant_id` 字段(第二阶段可选)。
- 不删除任何模块的物理代码文件。
- 不做企业 SSO 对接(OIDC/LDAP/企业微信等)—— 独立后续项目。
- 不做与 Codata FastAPI sidecar 的集成(token 流转、定时落地到本地执行)—— 独立后续项目。

## 后续阶段(备忘,非本次范围)

- 第二阶段(可选):从内核彻底剥离 tenant,删除商业化模块物理代码。
- 集成阶段:CodataAdmin 控制面 ↔ Codata FastAPI sidecar ↔ 前端壳;
  SSO token 流转、定时任务落地到本地执行、任务打 `execution_target: portable|local` 标记。
