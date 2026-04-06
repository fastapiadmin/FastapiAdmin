"""租户侧访问控制：登录与请求阶段校验租户是否可用；租户表管理权限。"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.tenant.model import TenantModel
from app.api.v1.module_system.user.model import UserModel
from app.core.exceptions import CustomException

from .constants import PLATFORM_TENANT_ID


def _naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def ensure_platform_tenant_management(auth: AuthSchema) -> None:
    """
    租户表 ``sys_tenant`` 无 ``tenant_id`` 列，ORM 无法自动按租户过滤行。

    凡增删改查租户元数据，必须仅限「平台超级管理员」（与 ``should_skip_tenant_filter`` 一致），
    否则仅依赖菜单权限时误配可能导致看见或操作全部租户，破坏多租户隔离。
    """
    raise CustomException(msg="无权访问租户管理，仅平台管理员可操作", code=10403, status_code=403)


async def ensure_tenant_allows_access(db: AsyncSession, user: UserModel) -> None:
    """
    非超级管理员：所属租户须存在、状态为启用，且在 start_time ~ end_time 有效期内（若配置）。

    超级管理员、系统租户（平台租户）下用户不拦截。
    """
    if getattr(user, "is_superuser", False):
        return
    tid = getattr(user, "tenant_id", None)
    if tid is None:
        raise CustomException(msg="用户未关联租户", code=10401, status_code=403)
    if tid == PLATFORM_TENANT_ID:
        return

    result = await db.execute(select(TenantModel).where(TenantModel.id == tid))
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise CustomException(msg="租户不存在", code=10401, status_code=403)
    if tenant.status == "1":
        raise CustomException(msg="租户已停用，无法使用", code=10401, status_code=403)

    now = datetime.now()
    if tenant.start_time:
        st = _naive(tenant.start_time)
        if now < st:
            raise CustomException(msg="租户未生效，请在生效时间后重试", code=10401, status_code=403)
    if tenant.end_time:
        et = _naive(tenant.end_time)
        if now > et:
            raise CustomException(msg="租户已过期，请联系管理员", code=10401, status_code=403)
