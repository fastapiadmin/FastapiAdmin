"""登录响应/会话字典组装。"""

from __future__ import annotations

from types import SimpleNamespace

from app.modules.system.auth.service import LoginService


def test_build_login_out_with_mobile() -> None:
    token = SimpleNamespace(access_token="a", refresh_token="r", expires_in=1, token_type="Bearer")
    user = SimpleNamespace(id=1, username="u", name="N", avatar=None, is_superuser=False, mobile="138")
    out = LoginService.build_login_out(token, user, with_mobile=True)
    assert out.access_token == "a" and out.user_info["mobile"] == "138"


def test_build_session_dict() -> None:
    user = SimpleNamespace(id=1, is_superuser=False, status=0, name="N", username="u", dept_id=2, mobile=None, email=None, gender=None, avatar=None, last_login=None)
    ua = SimpleNamespace(os=SimpleNamespace(family="mac"), user_agent=SimpleNamespace(family="chrome"), device=SimpleNamespace(family="pc"))
    d = LoginService._build_session_dict(user, "sid", ["p"], [1], "127.0.0.1", "loc", ua, "PC")
    assert d["session_id"] == "sid" and d["permissions"] == ["p"]
