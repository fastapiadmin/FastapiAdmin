"""多租户：为 API 出参写入嵌套 ``tenant``（需 ORM 已加载 tenant 关系或仅有 tenant_id）。"""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

TOut = TypeVar("TOut", bound=BaseModel)


def enrich_tenant_fields(obj: Any, data: dict[str, Any]) -> dict[str, Any]:
    """
    合并已有序列化结果，并写入嵌套 ``tenant``；去掉扁平的 tenant_* 字段。

    参数:
    - obj: 带 ``tenant_id``、可选 ``tenant`` 关系的 ORM 实例。
    - data: 已 ``model_dump()`` 的字典。

    返回:
    - dict: 含 ``tenant: { id, name, code } | None``。
    """
    out = dict(data)
    out.pop("tenant_id", None)
    out.pop("tenant_name", None)
    out.pop("tenant_code", None)
    tid = getattr(obj, "tenant_id", None)
    t = getattr(obj, "tenant", None)
    if t is not None:
        out["tenant"] = {
            "id": getattr(t, "id", tid),
            "name": getattr(t, "name", None),
            "code": getattr(t, "code", None),
        }
    elif tid is not None:
        out["tenant"] = {"id": tid, "name": None, "code": None}
    else:
        out["tenant"] = None
    return out


def dump_out_with_tenant(schema: type[TOut], obj: Any) -> dict[str, Any]:
    """将 ORM ``obj`` 用 ``schema`` 校验后 ``model_dump``，再合并租户展示字段。"""
    return enrich_tenant_fields(obj, schema.model_validate(obj).model_dump())
