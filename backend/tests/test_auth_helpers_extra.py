"""认证权限收集与登录响应组装。"""

from __future__ import annotations

from types import SimpleNamespace

from app.modules.system.auth.service import LoginService


def test_collect_permissions() -> None:
    menu=SimpleNamespace(id=1,status=0,permission="a:b:c")
    role=SimpleNamespace(status=0,menus=[menu])
    assert LoginService._collect_permissions(SimpleNamespace(is_superuser=False,roles=[role]))==(["a:b:c"],[1])
    assert LoginService._collect_permissions(SimpleNamespace(is_superuser=True,roles=[role]))==([],[])
    off_role=SimpleNamespace(status=1,menus=[menu])
    assert LoginService._collect_permissions(SimpleNamespace(is_superuser=False,roles=[off_role]))==([],[])
    off_menu=SimpleNamespace(id=2,status=1,permission="x")
    role2=SimpleNamespace(status=0,menus=[off_menu])
    assert LoginService._collect_permissions(SimpleNamespace(is_superuser=False,roles=[role2]))==([],[])


def test_build_login_out() -> None:
    from app.modules.system.auth.schema import JWTOutSchema
    token=JWTOutSchema(access_token="a",refresh_token="r",expires_in=1,token_type="bearer")
    user=SimpleNamespace(id=1,username="u",name="U",avatar=None,is_superuser=False,mobile="13800000000")
    out=LoginService.build_login_out(token,user)
    assert out.user_info["username"]=="u" and "mobile" not in out.user_info
    out2=LoginService.build_login_out(token,user,with_mobile=True)
    assert out2.user_info["mobile"]=="13800000000"
