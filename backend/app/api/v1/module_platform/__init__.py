from fastapi import APIRouter

from app.api.v1.module_platform.email.controller import EmailRouter
from app.api.v1.module_platform.invoice.controller import PlatformInvoiceRouter, TenantInvoiceRouter
from app.api.v1.module_platform.menu.controller import MenuRouter
from app.api.v1.module_platform.order.controller import (
    OrderRouter,
    PaymentRouter,
    RefundRouter,
    TenantOrderRouter,
)
from app.api.v1.module_platform.package.controller import PackageRouter
from app.api.v1.module_platform.plugin.controller import PluginRouter
from app.api.v1.module_platform.self_service.controller import TenantSelfServiceRouter
from app.api.v1.module_platform.tenant.controller import TenantRouter

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
