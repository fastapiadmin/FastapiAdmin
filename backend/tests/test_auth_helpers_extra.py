"""认证权限收集与登录响应组装。"""

from __future__ import annotations

import pytest
from types import SimpleNamespace

from app.core.exceptions import CustomException
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


async def test_captcha_state(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    import app.modules.system.auth.service as mod
    class R:
        def __init__(self,v): self.v=v; self.sets=[]
        async def get(self,k): return self.v
        async def set(self,**kw): self.sets.append(kw); return True
    monkeypatch.setattr(mod,"RedisCURD",lambda r:r)
    from app.core.exceptions import CustomException
    with pytest.raises(CustomException, match="过期"):
        await mod.CaptchaService._read_state(R(None),"k")
    assert (await mod.CaptchaService._read_state(R("plain"),"k"))["status"]=="plain"
    assert (await mod.CaptchaService._read_state(R("[]"),"k"))["status"]==""
    state=json.dumps({"status":"ok","fingerprint":"f","issued_at":1,"target_x":2})
    assert (await mod.CaptchaService._read_state(R(state),"k"))["target_x"]==2
    r=R(None)
    await mod.CaptchaService._write_state(r,"k","ok","f",1,2)
    assert r.sets and "fingerprint" in r.sets[0]["value"]


def test_captcha_matches(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    monkeypatch.setattr(mod,"get_client_fingerprint",lambda req:"f")
    assert mod.CaptchaService._matches({"fingerprint":""},object()) is True
    assert mod.CaptchaService._matches({"fingerprint":"f"},object()) is True
    assert mod.CaptchaService._matches({"fingerprint":"x"},object()) is False


async def test_logout(monkeypatch: pytest.MonkeyPatch) -> None:
    import app.modules.system.auth.service as mod
    class R:
        def __init__(self): self.deleted=[]
        async def delete(self,k): self.deleted.append(k); return True
    monkeypatch.setattr(mod,"RedisCURD",lambda r:r)
    monkeypatch.setattr(mod,"decode_access_token",lambda token: SimpleNamespace(sub="s"))
    r=R(); assert await mod.LoginService.logout(r,"t") is True and len(r.deleted)==3
    monkeypatch.setattr(mod,"decode_access_token",lambda token: SimpleNamespace(sub=None))
    with pytest.raises(CustomException, match="会话编号"):
        await mod.LoginService.logout(r,"t")
