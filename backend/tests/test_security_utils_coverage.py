"""crypto / lazy_sdk / agno factory 分支覆盖。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.utils import ai_factory
from app.utils.crypto_util import CryptoUtil
from app.utils.lazy_sdk import LazyModule, lazy_module, sdk_exception


def test_crypto_roundtrip_and_invalid() -> None:
    assert CryptoUtil.encrypt("") == ""
    assert CryptoUtil.decrypt("") == ""
    token = CryptoUtil.encrypt("secret")
    assert CryptoUtil.decrypt(token) == "secret"
    assert CryptoUtil.is_token(token) is True
    assert CryptoUtil.is_token("plain") is False
    assert CryptoUtil.decrypt_or_keep("plain") == "plain"
    assert CryptoUtil.decrypt_or_keep(token) == "secret"
    with pytest.raises(RuntimeError):
        CryptoUtil.decrypt("gAAAAA" + "x" * 60)


def test_lazy_module_and_exception() -> None:
    mod = LazyModule("json")
    assert mod.dumps({"a": 1}) == '{"a": 1}'
    assert "已导入" in repr(mod)
    assert lazy_module("json").loads("1") == 1
    exc = sdk_exception("json", "JSONDecodeError")
    assert issubclass(exc, ValueError)


def test_agno_factory_defaults_and_runtime_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    class FakeAgent:
        def __init__(self, **kwargs):
            captured["agent"] = kwargs

    class FakeTeam:
        def __init__(self, **kwargs):
            captured["team"] = kwargs

    class FakeModel:
        def __init__(self, **kwargs):
            captured["model"] = kwargs

    monkeypatch.setattr(ai_factory, "Agent", FakeAgent)
    monkeypatch.setattr(ai_factory, "Team", FakeTeam)
    monkeypatch.setattr(ai_factory, "OpenAILike", FakeModel)
    factory = ai_factory.AgnoFactory()
    factory.create_agent("u1", "t1", "s1")
    assert captured["agent"]["id"] == "u1"
    assert captured["team"]["id"] == "t1"
    assert captured["model"]["temperature"] == factory.AGENT_TEMPERATURE

    factory.create_agent(
        "u2",
        "t2",
        "s2",
        db=SimpleNamespace(),
        model_config={"base_url": "http://x", "api_key": "k", "model_id": "m", "temperature": 0.2},
        tools=[lambda: None],
    )
    assert captured["model"] == {"id": "m", "api_key": "k", "base_url": "http://x", "temperature": 0.2, "timeout": factory.REQUEST_TIMEOUT}
    assert len(captured["agent"]["tools"]) == 1
