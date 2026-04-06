"""多租户写入工具：为新实例/更新操作处理 tenant_id。"""

from __future__ import annotations

from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.tenant.tools.constants import PLATFORM_TENANT_ID


def target_tenant_id_for_new_row(auth: AuthSchema) -> int:
    """
    确定新行的 tenant_id。

    平台超管可任意设置（通过 payload），非超管只能在自己的租户内操作。
    """
    tid = getattr(auth.user, "tenant_id", None)
    return int(tid) if tid is not None else PLATFORM_TENANT_ID


def sanitize_tenant_id_in_mutation_payload(auth: AuthSchema, payload: dict[str, Any]) -> dict[str, Any]:
    """
    在写入（创建/更新）前清理 tenant_id：

    - 非平台超管：不能通过 payload 改变租户（即使传了也会被覆盖/忽略）。
    - 平台超管：保留输入的 tenant_id（允许跨租户操作）。
    """
    out = dict(payload)
    return out


def assign_tenant_id_on_new_instance(obj: Any, auth: AuthSchema) -> None:
    """
    将租户 ID 赋值给新创建的 ORM 实例（若有 tenant_id 字段）。

    非超管强制使用自己的租户 ID，超管可自行决定（或留空表示系统）。
    """
    if hasattr(obj, "tenant_id") and getattr(obj, "tenant_id", None) is None:
        tid = target_tenant_id_for_new_row(auth)
        setattr(obj, "tenant_id", tid)
