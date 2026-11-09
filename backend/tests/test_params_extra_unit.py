"""系统参数未登录/缓存同步边界。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.modules.system.params.service as mod
from app.core.exceptions import CustomException
from app.modules.system.params.schema import ParamsUpdateSchema
from app.modules.system.params.service import ParamsService


async def test_update_requires_login(monkeypatch: pytest.MonkeyPatch) -> None:
    class C:
        def __init__(self,*a): pass
        async def get_or_404(self,**kw): return SimpleNamespace(config_key="k")
        async def update(self,**kw): return SimpleNamespace(config_name="n",config_key="k",config_value="1",config_type=False,status=0,id=1)
    monkeypatch.setattr(mod,"ParamsCRUD",C)
    s=ParamsService(SimpleNamespace(user=None), object())
    with pytest.raises(CustomException, match="未登录"):
        await s.update(object(),1,ParamsUpdateSchema(config_name="n",config_key="k",config_value="1"))


async def test_sync_configs_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class R:
        def __init__(self,*a): pass
        async def set(self,*a,**k): return True
    monkeypatch.setattr(mod,"RedisCURD",R)
    cfg=SimpleNamespace(config_name="n",config_key="k",config_value="1",config_type=False,status=0,id=1)
    out=await ParamsService._sync_configs_to_redis(object(),[cfg])
    assert out and out[0]["config_key"]=="k"


async def test_load_all_configs(monkeypatch: pytest.MonkeyPatch) -> None:
    class Ctx:
        async def __aenter__(self): return object()
        async def __aexit__(self,*a): return False
    class C:
        def __init__(self,*a): pass
        async def get_list(self): return ["cfg"]
    monkeypatch.setattr(mod,"async_db_session",lambda: Ctx())
    monkeypatch.setattr(mod,"ParamsCRUD",C)
    assert await ParamsService._load_all_configs_from_db()==["cfg"]
