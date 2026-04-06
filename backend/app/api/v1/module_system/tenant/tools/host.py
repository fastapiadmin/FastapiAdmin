"""请求 Host（通配二级子域）与当前用户租户 ``code`` 一致性（可选开启）。"""

from __future__ import annotations

import ipaddress

from fastapi import Request

from app.api.v1.module_system.user.model import UserModel
from app.config.setting import settings
from app.core.exceptions import CustomException

from .constants import PLATFORM_TENANT_ID


def _host_without_port(raw: str) -> str:
    raw = raw.strip().lower()
    if not raw:
        return ""
    if raw.startswith("["):
        end = raw.find("]")
        return raw[: end + 1] if end != -1 else raw
    return raw.split(":")[0]


def _is_ip_host(host: str) -> bool:
    if host.startswith("["):
        inner = host[1:-1] if host.endswith("]") else host[1:]
        try:
            ipaddress.ip_address(inner)
            return True
        except ValueError:
            return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def parse_tenant_code_from_host(host_header: str | None) -> str | None:
    """
    从 ``Host`` 解析租户编码：``{code}.{TENANT_HOST_BASE_DOMAIN}`` → ``code``。

    - ``localhost`` / 纯 IP / 非本 ``base`` 域：返回 ``None``（调用方不强制校验）。
    - 首段在 ``TENANT_HOST_IGNORE_PREFIXES`` 内（如 ``api``、``www``）：返回 ``None``，便于独立 API 域名。
    """
    base = (settings.TENANT_HOST_BASE_DOMAIN or "").strip().lower()
    if not base:
        return None
    host = _host_without_port(host_header or "")
    if not host or host == "localhost" or _is_ip_host(host):
        return None
    suffix = "." + base
    if not host.endswith(suffix) or host == base:
        return None
    prefix = host[: -len(suffix)]
    if not prefix:
        return None
    first = prefix.split(".")[0]
    ignore = {x.strip().lower() for x in settings.TENANT_HOST_IGNORE_PREFIXES if x.strip()}
    if first in ignore:
        return None
    return first


def ensure_tenant_host_matches_user(request: Request, user: UserModel) -> None:
    """
    若开启 ``TENANT_HOST_ENFORCE`` 且能从 Host 解析出租户 code，则须与用户所属租户 code 一致。

    平台超管（与 ``should_skip_tenant_filter`` 一致：超管且平台租户）不校验。
    """
    if not settings.TENANT_HOST_ENFORCE:
        return
    if not (settings.TENANT_HOST_BASE_DOMAIN or "").strip():
        return

    if getattr(user, "is_superuser", False) and getattr(user, "tenant_id", None) == PLATFORM_TENANT_ID:
        return

    code_from_host = parse_tenant_code_from_host(request.headers.get("host"))
    if code_from_host is None:
        return

    tenant = getattr(user, "tenant", None)
    tcode = (getattr(tenant, "code", None) or "").strip().lower()
    if not tcode or tcode != code_from_host.lower():
        raise CustomException(
            msg="当前访问域名与账号所属租户不一致",
            code=10403,
            status_code=403,
        )
