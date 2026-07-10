# CodataAdmin 单租户化 + 禁用商业化模块 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 fork 自 FastapiAdmin 的 CodataAdmin 干净地服务于"单公司、多部门"场景 —— 禁用商业化 API 与账务定时任务,并让 RBAC 内核脱离"多租户套餐"约束,而不删除任何代码或数据库字段。

**Architecture:** 全程"能关就不删"。三条改造线:(1) 路由聚合层注释掉商业化 `include_router`;(2) 定时调度器拆分系统 job,只保留非商业化的日志清理;(3) 认证时不再注入 `tenant_id`,使内核中 `if auth.tenant_id:` 守卫的套餐逻辑自动短路。所有物理代码、`tenant_id` 字段、import 语句保留不动,零数据库迁移、可随时回退。

**Tech Stack:** Python 3.12 / FastAPI 0.115 / SQLAlchemy 2.0 async / APScheduler / pytest 9 (asyncio_mode=auto) / 测试用 SQLite。

## Global Constraints

- 不删除任何模块的物理代码文件。
- 不删除 `base_model.py` 的 `tenant_id` 字段;不产生数据库迁移。
- import 语句保留:内核仍 `from ...package.service import PackageService`,禁用只发生在 router 注册层与运行时判断层。
- 不做企业 SSO(OIDC/LDAP/企业微信);不做与 Codata FastAPI sidecar 的集成。这些是后续独立项目。
- 测试命令:在 `backend/` 目录下运行。项目用 `uv`;若 `uv run pytest` 不可用则回退 `python -m pytest`。
- 每个任务独立可启动验证,不一次性堆改动。分支:`feat/single-tenant-slim`。

---

### Task 1: 禁用商业化 API 路由

**Files:**
- Modify: `backend/app/api/v1/module_platform/__init__.py`
- Modify: `backend/app/api/v1/module_system/__init__.py`
- Test: `backend/tests/test_api_module_platform.py`, `backend/tests/test_api_module_system.py`

**Interfaces:**
- Consumes: 无(起始任务)。
- Produces: 禁用后,`/platform/order/*`、`/platform/payment/*`、`/platform/refund/*`、`/platform/package/*`、`/platform/invoice/*`(平台侧)、`/platform/self-service/*`、`/platform/tenant/*` 全部返回 404;`/platform/menu/*`、`/platform/email/*`、`/platform/plugin/*` 仍存活。`/system/ticket/*` 返回 404。

- [ ] **Step 1: 写一个断言"商业化路由已消失"的测试**

在 `backend/tests/test_api_module_platform.py` 末尾追加一个新类。`assert_route` 语义是"路由存在(状态码 != 404)",因此这里改用直接断言 404 来表达禁用:

```python
class TestCommercialRoutesDisabled:
    """单租户化:商业化路由应被禁用(404)。"""

    DISABLED_GETS = [
        "/platform/order/list",
        "/platform/package/list",
        "/platform/self-service/current",
        "/platform/tenant/list",
    ]

    def test_commercial_routes_return_404(self, test_client, auth_headers) -> None:
        for path in self.DISABLED_GETS:
            resp = test_client.get(path, headers=auth_headers)
            assert resp.status_code == 404, f"{path} 应已禁用,却返回 {resp.status_code}"
```

> 注意:`self-service` 与 `tenant` 的确切子路径以 controller 里的 `@router.get` 为准;若 `/platform/self-service/current` 不存在,换成该 controller 中任一 GET 路径。运行 Step 2 时若因路径拼写返回 404 反而"假通过",在 Step 3 完成后用 `openapi.json` 复核(见 Step 5)。

- [ ] **Step 2: 运行测试,确认此刻是失败的(路由仍在)**

Run: `cd backend && uv run pytest tests/test_api_module_platform.py::TestCommercialRoutesDisabled -v`
Expected: FAIL —— 因为路由此刻仍注册,GET 返回 200/401/422 等非 404 状态。

- [ ] **Step 3: 在 platform 聚合层注释掉商业化 include_router**

修改 `backend/app/api/v1/module_platform/__init__.py`,**保留全部 import**,仅注释掉商业化的 `include_router` 行:

```python
platform_router = APIRouter(prefix="/platform")

# ── 保留:RBAC / 通知 / 插件 ──
platform_router.include_router(MenuRouter)
platform_router.include_router(EmailRouter)
platform_router.include_router(PluginRouter)

# ── 单租户化禁用:租户后台化(见 Task 3),商业化售卖全部下线 ──
# platform_router.include_router(TenantRouter)
# platform_router.include_router(PackageRouter)
# platform_router.include_router(OrderRouter)
# platform_router.include_router(PaymentRouter)
# platform_router.include_router(RefundRouter)
# platform_router.include_router(PlatformInvoiceRouter)
# platform_router.include_router(TenantInvoiceRouter)
# platform_router.include_router(TenantOrderRouter)
# platform_router.include_router(TenantSelfServiceRouter)
```

修改 `backend/app/api/v1/module_system/__init__.py`,注释掉工单:

```python
# system_router.include_router(TicketRouter)  # 单租户化:内部控制面不需要工单
```

- [ ] **Step 4: 更新既有商业化测试类为"预期 404"**

`test_api_module_platform.py` 中 `TestTenant`、`TestPackage`、`TestOrder`、`TestPayment`、`TestRefund`、`TestInvoice`、`TestSelfService` 等类原本用 `assert_route`(断言 != 404),禁用后会全部失败。给这些类整体加 skip,避免误报回归。在每个受影响类的定义行上方加装饰器:

```python
import pytest

@pytest.mark.skip(reason="单租户化已禁用商业化路由,见 Task 1")
class TestTenant:
    ...

@pytest.mark.skip(reason="单租户化已禁用商业化路由,见 Task 1")
class TestPackage:
    ...

@pytest.mark.skip(reason="单租户化已禁用商业化路由,见 Task 1")
class TestOrder:
    ...
```

对 `TestPayment` / `TestRefund` / `TestInvoice` / `TestSelfService`(若存在,以文件实际类名为准)同样处理。`TestMenu`、`TestEmail`、`TestPlugin` **不加 skip**(仍存活)。
`test_api_module_system.py` 中若有 `TestTicket` 类,同样加 skip。

- [ ] **Step 5: 运行相关测试,确认新测试通过、旧测试被 skip、保留路由仍存活**

Run: `cd backend && uv run pytest tests/test_api_module_platform.py tests/test_api_module_system.py -v`
Expected: `TestCommercialRoutesDisabled` PASS;被 skip 的类显示 SKIPPED;`TestMenu`/`TestEmail`/`TestPlugin` 仍 PASS。
补充复核:`grep -c '"/platform/order' tests/openapi.json` 类操作可留待应用启动后再看,此处以 pytest 结果为准。

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/v1/module_platform/__init__.py backend/app/api/v1/module_system/__init__.py backend/tests/test_api_module_platform.py backend/tests/test_api_module_system.py
git commit -m "feat: 禁用商业化 API 路由(order/invoice/package/self-service/tenant/ticket)"
```

---

### Task 2: 关闭商业化账务定时任务

**Files:**
- Modify: `backend/app/core/ap_scheduler.py:600-655`(`_register_system_jobs` 方法)
- Test: `backend/tests/test_api_module_task.py`(或新增针对 scheduler 的断言)

**Interfaces:**
- Consumes: Task 1 已禁用商业化路由。
- Produces: 调度器启动后只注册 1 个系统 job:`system_cleanup_operation_log`(操作日志清理)。`system_tenant_expiry_check` / `system_grace_reminder` / `system_clean_expired` / `system_cancel_expired_orders` 不再注册。`SchedulerUtil.init_scheduler` 与 `_task_wrapper`(用户自定义 cron)能力完整保留。

- [ ] **Step 1: 写测试断言商业化 job 未注册**

在 `backend/tests/test_api_module_task.py` 末尾追加:

```python
def test_commercial_system_jobs_not_registered():
    from app.core.ap_scheduler import scheduler
    job_ids = {j.id for j in scheduler.get_jobs()}
    for jid in [
        "system_tenant_expiry_check",
        "system_grace_reminder",
        "system_clean_expired",
        "system_cancel_expired_orders",
    ]:
        assert jid not in job_ids, f"{jid} 应已在单租户化中移除"
    assert "system_cleanup_operation_log" in job_ids, "日志清理任务应保留"
```

> 前提:测试环境已 `init_scheduler`。若 `scheduler.get_jobs()` 在无 app lifespan 时为空,改为直接调用 `SchedulerUtil._register_system_jobs()` 后再断言(该方法是 classmethod)。以 conftest 现有 fixture 能否提供已初始化 scheduler 为准。

- [ ] **Step 2: 运行测试,确认失败(商业化 job 目前会被注册)**

Run: `cd backend && uv run pytest tests/test_api_module_task.py::test_commercial_system_jobs_not_registered -v`
Expected: FAIL —— 断言命中 `system_tenant_expiry_check` 仍存在。

- [ ] **Step 3: 在 `_register_system_jobs` 中移除商业化 job**

编辑 `backend/app/core/ap_scheduler.py` 的 `_register_system_jobs`。删除(或注释)租户到期检查、宽限期续费提醒、过期租户归档清理、超时订单取消四个 `scheduler.add_job(...)` 块,以及顶部 `from ...order.service import OrderService` / `from ...tenant.service import TenantService` 两行 import(它们仅此处使用)。**保留**操作日志清理 job:

```python
    @classmethod
    def _register_system_jobs(cls) -> None:
        """注册系统级定时任务(单租户化后仅保留日志清理;商业化账务任务已移除)。"""
        from apscheduler.triggers.cron import CronTrigger

        # 操作日志清理(每周日 3:00)
        from app.api.v1.module_system.log.service import OperationLogService

        scheduler.add_job(
            OperationLogService.cleanup_operation_log,
            trigger=CronTrigger(day_of_week="sun", hour=3, minute=0),
            id="system_cleanup_operation_log",
            name="操作日志清理",
            replace_existing=True,
        )
        logger.info("✅ 1 个系统周期任务已注册(操作日志清理)")
```

- [ ] **Step 4: 运行测试,确认通过**

Run: `cd backend && uv run pytest tests/test_api_module_task.py::test_commercial_system_jobs_not_registered -v`
Expected: PASS。

- [ ] **Step 5: Commit**

```bash
git add backend/app/core/ap_scheduler.py backend/tests/test_api_module_task.py
git commit -m "feat: 移除商业化账务定时任务,保留调度器与日志清理"
```

---

### Task 3: 认证不注入 tenant_id —— 套餐权限自动短路

**Files:**
- Modify: `backend/app/api/v1/module_system/auth/service.py:221`(以及登录出参构造 `tenant_id=user.tenant_id` 的位置)
- Test: `backend/tests/test_api_module_system.py`

**Interfaces:**
- Consumes: Task 1/2 完成。
- Produces: 登录后 `AuthSchema.tenant_id is None`,使 `permission.py:106` 的 `if self.auth.tenant_id and menu_ids:` 守卫短路 —— 菜单权限只由 RBAC 角色决定,不再与套餐求交集。`dependencies.py` 的 `_package_menu_cache` 路径不再被触发。

- [ ] **Step 1: 写测试断言登录 auth 的 tenant_id 为空、菜单不受套餐约束**

在 `backend/tests/test_api_module_system.py` 追加(用现有登录 fixture / auth_headers 拿到当前用户上下文;若无直接暴露 AuthSchema 的接口,则通过 `/system/auth/user/info` 之类"当前用户菜单"接口断言能拿到角色全量菜单):

```python
def test_login_auth_has_no_tenant(test_client, auth_headers):
    # 通过"当前用户信息"接口验证:单租户化后不返回租户绑定
    resp = test_client.get("/system/auth/user/info", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json().get("data", {})
    # tenant 字段应为空或不存在(单租户化)
    assert not data.get("tenant"), "单租户化后不应返回租户绑定信息"
```

> 确切接口路径以 `AuthRouter` controller 为准;若为 `/system/auth/getInfo` 等则替换。目的是验证"登录链路不再携带租户"。

- [ ] **Step 2: 运行测试,确认失败(当前仍注入 tenant)**

Run: `cd backend && uv run pytest tests/test_api_module_system.py::test_login_auth_has_no_tenant -v`
Expected: FAIL —— 当前 `AuthSchema(tenant_id=user.tenant_id)` 会带出租户。

- [ ] **Step 3: 在认证服务中将注入的 tenant_id 置空**

编辑 `backend/app/api/v1/module_system/auth/service.py`。将构造认证上下文处的 `tenant_id=user.tenant_id` 改为 `tenant_id=None`(第 221 行附近的 `tenants_auth = AuthSchema(...)`,以及登录出参 283 行附近的 `tenant_id=user.tenant_id`)。在改动处加注释说明:

```python
        # 单租户化:不注入租户上下文,使套餐权限校验自动短路(见 permission.py 守卫)
        tenants_auth = AuthSchema(db=db, user=user, tenant_id=None, check_data_scope=False)
```

> 只改"注入到运行时鉴权上下文"的 tenant_id。数据库 `user.tenant_id` 字段本身保留不动(用户仍归属默认租户)。若这些行还负责查询用户所属租户名用于展示,可一并将展示字段留空。

- [ ] **Step 4: 运行测试,确认通过**

Run: `cd backend && uv run pytest tests/test_api_module_system.py::test_login_auth_has_no_tenant -v`
Expected: PASS。

- [ ] **Step 5: 运行认证 + 权限相关测试,确认无回归**

Run: `cd backend && uv run pytest tests/test_api_module_system.py -v`
Expected: 认证、角色、菜单相关用例全部 PASS(菜单不再被套餐裁剪,不应减少可见项)。

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/v1/module_system/auth/service.py backend/tests/test_api_module_system.py
git commit -m "feat: 认证不注入 tenant_id,套餐权限校验自动短路(单租户化)"
```

---

### Task 4: 全量回归 + 应用可启动验证

**Files:**
- Test: 全部 `backend/tests/`
- Verify: 应用启动 + OpenAPI 快照

**Interfaces:**
- Consumes: Task 1-3 全部完成。
- Produces: 一次干净的全量测试通过 + 应用能正常 lifespan 启动且商业化路由确实不在 OpenAPI 中。

- [ ] **Step 1: 跑全量测试套件**

Run: `cd backend && uv run pytest -q`
Expected: 全绿(商业化相关用例为 SKIPPED,不计失败)。若有失败,定位到具体 Task 修正后重跑,不要在此处放行。

- [ ] **Step 2: 启动应用验证 lifespan 无异常**

Run: `cd backend && uv run python -c "from app.main import create_app; app = create_app(); print('routes:', len(app.routes))"`
（若入口不同,以 `pyproject`/`run.py` 中实际工厂为准,例如 `uvicorn app.main:create_app --factory` 冒烟启动 3 秒后 Ctrl-C。）
Expected: 无 import 错误、无 `PackageService`/`TenantService` 相关启动异常。

- [ ] **Step 3: 确认 OpenAPI 中商业化路由已消失、保留路由仍在**

Run:
```bash
cd backend && uv run python -c "
from app.main import create_app
app = create_app()
paths = {getattr(r,'path','') for r in app.routes}
gone = [p for p in paths if any(k in p for k in ['/platform/order','/platform/invoice','/platform/package','/platform/self','/platform/tenant','/system/ticket'])]
kept = [p for p in paths if any(k in p for k in ['/platform/menu','/platform/email','/system/role','/system/dept'])]
print('应为空:', gone)
print('应非空:', bool(kept))
assert not gone, gone
assert kept
print('OK')
"
```
Expected: `应为空: []`、`应非空: True`、`OK`。

- [ ] **Step 4: 更新设计文档状态并提交**

将 `docs/superpowers/specs/2026-07-09-single-tenant-slim-design.md` 顶部 `状态:` 改为 `已实现(第一阶段)`。

```bash
git add docs/superpowers/specs/2026-07-09-single-tenant-slim-design.md
git commit -m "docs: 标记第一阶段(禁用商业化+单租户化)已实现"
```

---

## Self-Review

**Spec coverage:**
- 禁用商业化 API(spec A)→ Task 1 ✅
- 关商业化定时 job(spec B)→ Task 2 ✅
- 单租户化 / 套餐权限短路(spec C1-C2)→ Task 3 ✅(利用 `if auth.tenant_id` 守卫,比 spec 设想的"改 PackageService 调用"更干净)
- 保留 tenant_id 字段(spec C3)→ Global Constraints + Task 3 Step 3 注释明确不动字段 ✅
- tenant 后台化(spec C4)→ Task 1 已将 `TenantRouter` 下线(比"后台化"更彻底,符合内部控制面无需租户管理;如日后需超管入口可单独恢复)✅
- 落地顺序 4 步 → Task 1-4 一一对应 ✅

**Placeholder scan:** 无 TBD/TODO;每个改代码步骤都给出真实代码块。带"以实际为准"的注解均为"路径/类名核对"提示,附了回退判据,非占位符。

**Type consistency:** `AuthSchema(tenant_id=None)` 与 `permission.py` 的 `self.auth.tenant_id` 守卫、`base_schema.py:56` 的 `tenant_id: int | None` 一致;job id 字符串(`system_cleanup_operation_log` 等)与 `ap_scheduler.py` 现有定义逐字一致。

**已知偏差(合理):** spec C4 说"tenant 后台化",本计划直接下线 `TenantRouter`。理由:内部单租户场景无租户管理需求,下线比保留后台入口更简洁,且可随时取消注释恢复。已在 Self-Review 标注。
