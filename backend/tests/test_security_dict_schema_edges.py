"""JWT 解析/字典 schema 错误分支。"""

from __future__ import annotations

from types import SimpleNamespace

import jwt
import pytest

from app.core.exceptions import CustomException
import app.core.security as S


def test_decode_token_edges(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(CustomException):
        S.decode_access_token("")
    def bad(*a, **k): raise jwt.DecodeError("x")
    monkeypatch.setattr(S.jwt, "decode", bad)
    with pytest.raises(CustomException):
        S.decode_access_token("x")
    class Expired(jwt.ExpiredSignatureError): pass
    def expired(*a, **k): raise Expired()
    monkeypatch.setattr(S.jwt, "decode", expired)
    with pytest.raises(CustomException):
        S.decode_access_token("x")
    def invalid(*a, **k): raise jwt.InvalidTokenError("x")
    monkeypatch.setattr(S.jwt, "decode", invalid)
    with pytest.raises(CustomException):
        S.decode_access_token("x")
    monkeypatch.setattr(S.jwt, "decode", lambda *a, **k: {"sub": ""})
    with pytest.raises(CustomException):
        S.decode_access_token("x")


def test_oauth2_scheme_no_auto_error() -> None:
    scheme = S.CustomOAuth2PasswordBearer(token_url="x", auto_error=False)
    import asyncio
    req = SimpleNamespace(headers={})
    assert asyncio.run(scheme(req)) is None


def test_dict_schema_errors() -> None:
    from app.modules.system.dict.schema import DictDataCreateSchema, DictTypeCreateSchema
    with pytest.raises(Exception):
        DictTypeCreateSchema(dict_name=" ", dict_type="a")
    with pytest.raises(Exception):
        DictTypeCreateSchema(dict_name="a", dict_type=" ")
    with pytest.raises(Exception):
        DictTypeCreateSchema(dict_name="a", dict_type="1bad")
    with pytest.raises(Exception):
        DictDataCreateSchema(dict_label=" ", dict_value="1", dict_type="a", dict_type_id=1)
    with pytest.raises(Exception):
        DictDataCreateSchema(dict_label="a", dict_value=" ", dict_type="a", dict_type_id=1)
    with pytest.raises(Exception):
        DictDataCreateSchema(dict_label="a", dict_value="1", dict_type=" ", dict_type_id=1)
    with pytest.raises(Exception):
        DictDataCreateSchema(dict_label="a", dict_value="1", dict_type="a", dict_type_id=0)
