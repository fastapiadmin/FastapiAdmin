"""OAuth 提供方令牌/用户信息映射。"""

from __future__ import annotations

import pytest

from app.core.exceptions import CustomException
from app.modules.system.auth import oauth_service as o


async def test_exchange_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gh(method, url, **kw): return {"access_token": "g"}
    monkeypatch.setattr(o, "_http_json", gh)
    assert await o.exchange_github_token("i", "s", "c", "r") == "g"
    async def gitee(method, url, **kw): return {"access_token": "e"}
    monkeypatch.setattr(o, "_http_json", gitee)
    assert await o.exchange_gitee_token("i", "s", "c", "r") == "e"
    async def wechat(method, url, **kw): return {"access_token": "w", "openid": "oid"}
    monkeypatch.setattr(o, "_http_json", wechat)
    assert await o.exchange_wechat_token("i", "s", "c") == ("w", "oid")
    async def text(method, url, **kw): return "access_token=q&x=1"
    async def me(method, url, **kw): return {"openid": "qid"}
    monkeypatch.setattr(o, "_http_text", text); monkeypatch.setattr(o, "_http_json", me)
    assert await o.exchange_qq_token("i", "s", "c", "r") == ("q", "qid")


async def test_exchange_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(method, url, **kw): return []
    monkeypatch.setattr(o, "_http_json", bad)
    with pytest.raises(CustomException): await o.exchange_gitee_token("i", "s", "c", "r")
    async def no_token(method, url, **kw): return {}
    monkeypatch.setattr(o, "_http_json", no_token)
    with pytest.raises(CustomException): await o.exchange_wechat_token("i", "s", "c")
    async def text(method, url, **kw): return "x=1"
    monkeypatch.setattr(o, "_http_text", text)
    with pytest.raises(CustomException): await o.exchange_qq_token("i", "s", "c", "r")


async def test_profiles(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gh(method, url, **kw):
        if url.endswith("/emails"): return [{"primary": True, "email": "e@x"}]
        return {"login": "l", "name": "N"}
    monkeypatch.setattr(o, "_http_json", gh)
    assert await o.fetch_github_profile("t") == ("l", "N", "e@x")
    async def gitee(method, url, **kw): return {"login": "l", "email": "e"}
    monkeypatch.setattr(o, "_http_json", gitee)
    assert await o.fetch_gitee_profile("t") == ("l", "l", "e")
    async def wx(method, url, **kw): return {"nickname": "W", "unionid": "u"}
    monkeypatch.setattr(o, "_http_json", wx)
    assert await o.fetch_wechat_profile("t", "o") == ("u", "W")
    async def qq(method, url, **kw): return {"ret": 0, "nickname": "Q"}
    monkeypatch.setattr(o, "_http_json", qq)
    assert await o.fetch_qq_profile("t", "a", "o") == ("o", "Q")


async def test_profile_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def bad(method, url, **kw): return []
    monkeypatch.setattr(o, "_http_json", bad)
    for fn in (o.fetch_github_profile, o.fetch_gitee_profile):
        with pytest.raises(CustomException): await fn("t")
    with pytest.raises(CustomException): await o.fetch_wechat_profile("t", "o")
    async def qq(method, url, **kw): return {"ret": 1, "msg": "bad"}
    monkeypatch.setattr(o, "_http_json", qq)
    with pytest.raises(CustomException): await o.fetch_qq_profile("t", "a", "o")


async def test_ensure_oauth_user(monkeypatch: pytest.MonkeyPatch) -> None:
    class U:
        def __init__(self,*a): pass
        async def get(self,**kw): return "existing"
    monkeypatch.setattr(o,"UserCRUD",U)
    assert await o.ensure_oauth_user(db=object(),provider="github",unique_id="1",display_name="n") == "existing"
    async def auto(**kw): return "new"
    monkeypatch.setattr(o,"auto_register_login_user",auto)
    class U2(U):
        async def get(self,**kw): return None
    monkeypatch.setattr(o,"UserCRUD",U2)
    assert await o.ensure_oauth_user(db=object(),provider="github",unique_id="1",display_name="n") == "new"


async def test_complete_oauth_login_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    from types import SimpleNamespace
    class R:
        def __init__(self,*a): self.store={o.STATE_PREFIX+"s": json.dumps({"provider":"github","frontend_redirect":"https://f"})}
        async def get(self,k): return self.store.get(k)
        async def delete(self,*ks): return True
    monkeypatch.setattr(o,"RedisCURD",R)
    async def cb(req,provider): return "https://cb"
    monkeypatch.setattr(o,"_callback_url",cb)
    monkeypatch.setattr(o,"_require_credentials",lambda p:("i","s"))
    async def gt(*a): return "a"
    async def fp(tok): return ("login","Name",None)
    async def ensure(**kw): return "user"
    async def prep(**kw): return "user"
    async def token(**kw): return "tok"
    monkeypatch.setattr(o,"exchange_github_token",gt); monkeypatch.setattr(o,"fetch_github_profile",fp)
    monkeypatch.setattr(o,"ensure_oauth_user",ensure)
    class L:
        prepare_user_for_login=staticmethod(prep)
        create_token=staticmethod(token)
    monkeypatch.setattr(o,"LoginService",L)
    tok,front = await o.complete_oauth_login(request=object(),redis=object(),db=object(),provider="github",code="c",state="s")
    assert tok == "tok" and front == "https://f"


async def test_complete_oauth_login_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    class R:
        def __init__(self, raw): self.raw=raw
        async def get(self,k): return self.raw
        async def delete(self,*k): return True
    async def call(raw, provider="github"):
        monkeypatch.setattr(o,"RedisCURD",lambda *a: R(raw))
        return await o.complete_oauth_login(request=object(),redis=object(),db=object(),provider=provider,code="c",state="s")
    with pytest.raises(CustomException, match="失效"):
        await call(None)
    with pytest.raises(CustomException, match="不匹配"):
        await call(json.dumps({"provider":"qq"}))
    with pytest.raises(CustomException, match="前端回调"):
        await call(json.dumps({"provider":"github"}))


async def test_oauth_state_and_start(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    class R:
        def __init__(self, getval=None, setok=True): self.getval=getval; self.setok=setok; self.sets=[]
        async def get(self,k): return self.getval
        async def set(self,key,value,expire=None,**kw): self.sets.append((key,value,expire)); return self.setok
    monkeypatch.setattr(o,"RedisCURD",lambda redis: redis)
    r=R(); await o.save_oauth_state(redis=r,state="s",provider="github",frontend_redirect="https://f")
    assert r.sets
    class Bad(R):
        async def set(self,key,value,expire=None,**kw): return False
    with pytest.raises(CustomException, match="缓存"):
        await o.save_oauth_state(redis=Bad(),state="s",provider="github",frontend_redirect="x")
    assert await o._state_frontend_redirect(R(),None,"fb") == "fb"
    assert await o._state_frontend_redirect(R(),"s","fb") == "fb"
    assert await o._state_frontend_redirect(R("bad"),"s","fb") == "fb"
    assert await o._state_frontend_redirect(R(json.dumps({"frontend_redirect":"u"})),"s","fb") == "u"
    fallback = await o.start_oauth_login(request=object(),redis=r,provider="github",redirect_uri=None)
    assert "oauth_error" in fallback


async def test_finish_oauth_login(monkeypatch: pytest.MonkeyPatch) -> None:
    async def front(redis,state,fallback): return "https://f"
    monkeypatch.setattr(o,"_state_frontend_redirect",front)
    async def missing(**kw): raise AssertionError("should not call")
    monkeypatch.setattr(o,"complete_oauth_login",missing)
    out = await o.finish_oauth_login(request=object(),redis=object(),db=object(),provider="github",code=None,state=None)
    assert "oauth_error" in out
    async def err(**kw): raise CustomException(msg="bad")
    monkeypatch.setattr(o,"complete_oauth_login",err)
    assert "oauth_error=bad" in await o.finish_oauth_login(request=object(),redis=object(),db=object(),provider="github",code="c",state="s")
    class T:
        access_token="a"; refresh_token="r"; token_type="bearer"
    async def ok(**kw): return T(), "https://f"
    monkeypatch.setattr(o,"complete_oauth_login",ok)
    out = await o.finish_oauth_login(request=object(),redis=object(),db=object(),provider="github",code="c",state="s")
    assert "access_token=a" in out


async def test_start_oauth_login_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def save(**kw): return None
    monkeypatch.setattr(o,"save_oauth_state",save)
    monkeypatch.setattr(o,"_callback_url",lambda req,p:"https://cb")
    monkeypatch.setattr(o,"build_authorize_url",lambda **kw:"https://auth")
    assert await o.start_oauth_login(request=object(),redis=object(),provider="github",redirect_uri="https://f") == "https://auth"


async def test_finish_oauth_login_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from urllib.parse import unquote
    async def front(redis,state,fallback): return "https://f"
    monkeypatch.setattr(o,"_state_frontend_redirect",front)
    async def crash(**kw): raise RuntimeError()
    monkeypatch.setattr(o,"complete_oauth_login",crash)
    out = await o.finish_oauth_login(request=object(),redis=object(),db=object(),provider="github",code="c",state="s")
    assert "登录服务暂时不可用" in unquote(out)


async def test_oauth_extra_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    async def bad_save(**kw): raise RuntimeError()
    monkeypatch.setattr(o,"save_oauth_state",bad_save)
    out=await o.start_oauth_login(request=object(),redis=object(),provider="github",redirect_uri="https://f")
    assert "oauth_error" in out
    class R:
        def __init__(self,v): self.v=v
        async def get(self,k): return self.v
    monkeypatch.setattr(o,"RedisCURD",lambda r:r)
    raw=json.dumps({"frontend_redirect":"u"}).encode()
    assert await o._state_frontend_redirect(R(raw),"s","fb") == "u"
    assert await o._state_frontend_redirect(R(json.dumps({"frontend_redirect":""})),"s","fb") == "fb"


def test_username_for_oauth() -> None:
    assert o._username_for_oauth("github","abc").startswith("oauth_github_")


async def test_http_text(monkeypatch: pytest.MonkeyPatch) -> None:
    class R:
        text="hi"
        def raise_for_status(self): pass
    class C:
        async def __aenter__(self): return self
        async def __aexit__(self,*a): return False
        async def request(self,*a,**k): return R()
    class H:
        AsyncClient=lambda *a,**k:C()
    monkeypatch.setattr(o,"httpx",H)
    assert await o._http_text("GET","http://x") == "hi"


async def test_oauth_http_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    class R:
        def __init__(self,data=None,text="t",bad=False): self._d=data; self.text=text; self.bad=bad
        def raise_for_status(self): return None
        def json(self):
            if self.bad: raise json.JSONDecodeError("x","x",0)
            return self._d
    class C:
        def __init__(self,r): self.r=r
        async def __aenter__(self): return self
        async def __aexit__(self,*a): return False
        async def request(self,*a,**k): return self.r
    def H(r): return type("H",(),{"AsyncClient":lambda *a,**k:C(r)})
    monkeypatch.setattr(o,"httpx",H(R({"a":1})))
    assert await o._http_json("GET","http://x")=={"a":1}
    assert await o._http_text("GET","http://x")=="t"
    monkeypatch.setattr(o,"httpx",H(R(bad=True)))
    with pytest.raises(json.JSONDecodeError):
        await o._http_json("GET","http://x")


def test_oauth_redirects() -> None:
    err=o._frontend_error_redirect("https://f/login?x=1","bad msg")
    assert "oauth_error=" in err and "bad" in err
    ok=o._frontend_success_redirect("https://f", "a b", "r", "bearer")
    assert "access_token=a+b" in ok and "refresh_token=r" in ok


def test_build_authorize_all_providers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(o.settings,"OAUTH_GITHUB_CLIENT_ID","gh")
    monkeypatch.setattr(o.settings,"OAUTH_GITHUB_CLIENT_SECRET","s")
    assert "github.com/login/oauth/authorize" in o.build_authorize_url(provider="github",callback_url="https://cb",state="st")
    monkeypatch.setattr(o.settings,"OAUTH_GITEE_CLIENT_ID","ge")
    monkeypatch.setattr(o.settings,"OAUTH_GITEE_CLIENT_SECRET","s")
    assert "gitee.com/oauth/authorize" in o.build_authorize_url(provider="gitee",callback_url="https://cb",state="st")
    monkeypatch.setattr(o.settings,"OAUTH_WECHAT_OPEN_APP_ID","wx")
    monkeypatch.setattr(o.settings,"OAUTH_WECHAT_OPEN_APP_SECRET","s")
    assert "#wechat_redirect" in o.build_authorize_url(provider="wechat",callback_url="https://cb",state="st")
    monkeypatch.setattr(o.settings,"OAUTH_QQ_APP_ID","qq")
    monkeypatch.setattr(o.settings,"OAUTH_QQ_APP_SECRET","s")
    assert "graph.qq.com/oauth2.0/authorize" in o.build_authorize_url(provider="qq",callback_url="https://cb",state="st")


def test_require_credentials_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(o.settings,"OAUTH_GITHUB_CLIENT_ID","")
    with pytest.raises(RuntimeError, match="未配置"):
        o._require_credentials("github")
    with pytest.raises(CustomException, match="不支持"):
        o._require_credentials("bad")


async def _complete_for(monkeypatch, provider, exchange, fetch, fetch_name=None, fetch_fn=None):
    import json
    class R:
        def __init__(self): self.d={o.STATE_PREFIX+"s":json.dumps({"provider":provider,"frontend_redirect":"https://f"})}
        async def get(self,k): return self.d.get(k)
        async def delete(self,*k): return True
    monkeypatch.setattr(o,"RedisCURD",lambda *a:R())
    monkeypatch.setattr(o,"_callback_url",lambda req,p:"https://cb")
    monkeypatch.setattr(o,"_require_credentials",lambda p:("i","s"))
    monkeypatch.setattr(o,exchange,fetch)
    if fetch_name: monkeypatch.setattr(o,fetch_name,fetch_fn)
    async def ensure(**kw): return "u"
    async def prep(**kw): return "u"
    async def token(**kw): return "tok"
    monkeypatch.setattr(o,"ensure_oauth_user",ensure)
    class L:
        prepare_user_for_login=staticmethod(prep); create_token=staticmethod(token)
    monkeypatch.setattr(o,"LoginService",L)
    return await o.complete_oauth_login(request=object(),redis=object(),db=object(),provider=provider,code="c",state="s")


async def test_complete_gitee(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gt(*a): return "a"
    async def fp(t): return ("l","N",None)
    async def full(monkeypatch=monkeypatch):
        import json
        class R:
            async def get(self,k): return json.dumps({"provider":"gitee","frontend_redirect":"https://f"})
            async def delete(self,*k): return True
        monkeypatch.setattr(o,"RedisCURD",lambda *a:R())
        monkeypatch.setattr(o,"exchange_gitee_token",gt); monkeypatch.setattr(o,"fetch_gitee_profile",fp)
        return await _complete_for(monkeypatch,"gitee","exchange_gitee_token",gt)
    assert (await full())[0]=="tok"


async def test_complete_wechat_qq(monkeypatch: pytest.MonkeyPatch) -> None:
    async def wx_ex(*a): return ("a","o")
    async def wx_fetch(*a): return ("uid","N")
    assert (await _complete_for(monkeypatch,"wechat","exchange_wechat_token",wx_ex,"fetch_wechat_profile",wx_fetch))[0]=="tok"
    async def qq_ex(*a): return ("a","o")
    async def qq_fetch(*a): return ("uid","N")
    assert (await _complete_for(monkeypatch,"qq","exchange_qq_token",qq_ex,"fetch_qq_profile",qq_fetch))[0]=="tok"


async def test_oauth_specific_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def gitee(method,url,**kw): return {"error_description":"gitee bad"}
    monkeypatch.setattr(o,"_http_json",gitee)
    with pytest.raises(CustomException, match="gitee bad"):
        await o.exchange_gitee_token("i","s","c","r")
    async def wx(method,url,**kw): return {"errmsg":"wx bad"}
    monkeypatch.setattr(o,"_http_json",wx)
    with pytest.raises(CustomException, match="wx bad"):
        await o.exchange_wechat_token("i","s","c")
    async def text(method,url,**kw): return "access_token=q"
    async def me(method,url,**kw): return {"ret":0}
    monkeypatch.setattr(o,"_http_text",text); monkeypatch.setattr(o,"_http_json",me)
    with pytest.raises(CustomException, match="openid"):
        await o.exchange_qq_token("i","s","c","r")
