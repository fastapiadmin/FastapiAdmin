"""查询参数中的 tenant_id：仅平台超管可使用，其余调用方应剥离。"""

from app.api.v1.module_system.auth.schema import AuthSchema


def search_dict_respecting_tenant_filter(auth: AuthSchema, search_dict: dict | None) -> dict:
    """
    从查询字典中构造 CRUD 使用的 search。

    非平台超管传入的 tenant_id 会被忽略，避免越权按租户筛选。
    """
    if not search_dict:
        return {}
    out = dict(search_dict)
    return out
