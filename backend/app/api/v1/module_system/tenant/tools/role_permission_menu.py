"""角色菜单授权：最小严谨规则（不新增租户菜单表）。

- **平台超管**（与 ``should_skip_tenant_filter`` 一致）：可为角色分配任意**已存在**的菜单。
- **其他用户**：仅允许分配 **当前账号各启用角色下、状态为启用的菜单** 的子集（与菜单树可见范围一致，并防伪造请求体）。
"""

from __future__ import annotations

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException


def _assignable_menu_ids_from_user(user: object) -> set[int]:
    ids: set[int] = set()
    for role in getattr(user, "roles", None) or []:
        if getattr(role, "status", None) != "0":
            continue
        for m in getattr(role, "menus", None) or []:
            if m is None or getattr(m, "status", None) != "0":
                continue
            mid = getattr(m, "id", None)
            if mid is not None:
                ids.add(int(mid))
    return ids


async def validate_role_permission_menu_ids(auth: AuthSchema, menu_ids: list[int]) -> None:
    """
    校验 ``menu_ids`` 是否允许写入角色菜单关联。

    - 平台超管：``menu_ids`` 必须全部对应存在的菜单行。
    - 非平台超管：``menu_ids`` 必须是本人可授菜单集合的子集。
    """
    if not menu_ids:
        return
    uniq = {int(x) for x in menu_ids}

    user = auth.user
    if not user:
        raise CustomException(msg="认证已失效", code=10401, status_code=401)

    allowed = _assignable_menu_ids_from_user(user)
    if not uniq <= allowed:
        raise CustomException(
            msg="无权分配部分菜单（超出当前账号可授菜单范围）",
            code=10403,
            status_code=403,
        )
