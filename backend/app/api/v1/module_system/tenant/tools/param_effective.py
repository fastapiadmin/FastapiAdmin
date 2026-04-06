"""系统参数：平台租户为全局默认，其它租户可按同 key 覆盖。"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.params.model import ParamsModel

from .constants import PLATFORM_TENANT_ID


async def get_effective_param_row(
    db: AsyncSession, tenant_id: int, config_key: str
) -> ParamsModel | None:
    """本租户优先；否则（非平台租户）回退到平台全局行。"""
    local = await _row_by_tenant_and_key(db, tenant_id, config_key)
    if local is not None:
        return local
    if tenant_id == PLATFORM_TENANT_ID:
        return None
    return await _row_by_tenant_and_key(db, PLATFORM_TENANT_ID, config_key)


async def _row_by_tenant_and_key(
    db: AsyncSession, tenant_id: int, config_key: str
) -> ParamsModel | None:
    r = await db.execute(
        select(ParamsModel).where(
            ParamsModel.tenant_id == tenant_id,
            ParamsModel.config_key == config_key,
        )
    )
    return r.scalar_one_or_none()


async def list_param_rows_for_tenant(db: AsyncSession, tenant_id: int) -> list[ParamsModel]:
    r = await db.execute(
        select(ParamsModel)
        .where(ParamsModel.tenant_id == tenant_id)
        .order_by(ParamsModel.id)
    )
    return list(r.scalars().all())
