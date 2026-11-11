"""真实 Redis 滑块验证码签发/校验/消费。"""

from __future__ import annotations

import os

import pytest
from redis.asyncio import Redis
from starlette.requests import Request

from app.core.exceptions import CustomException
from app.modules.system.auth.service import CaptchaService

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="需要真实 Redis：设置 RUN_INTEGRATION=1",
)


def _req() -> Request:
    return Request({"type": "http", "method": "POST", "path": "/", "headers": [(b"user-agent", b"pytest")], "client": ("127.0.0.1", 1)})


async def _redis() -> Redis:
    return Redis(host="localhost", port=6379, db=1, decode_responses=True)


async def test_captcha_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.auth import service as mod
    monkeypatch.setattr(mod.settings, "CAPTCHA_ENABLE", False)
    r = await _redis()
    try:
        assert (await CaptchaService.get_captcha(r, _req())).enable is False
    finally:
        await r.aclose()


async def test_captcha_slider_and_consume(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.auth import service as mod
    monkeypatch.setattr(mod.settings, "CAPTCHA_ENABLE", True)
    monkeypatch.setattr(mod.settings, "CAPTCHA_MIN_VERIFY_SECONDS", 0)
    r = await _redis()
    try:
        out = await CaptchaService.get_captcha(r, _req())
        assert out.enable and out.key
        key = str(out.key)
        state = await CaptchaService._read_state(redis=r, captcha_key=key)
        with pytest.raises(CustomException, match="拖动滑块"):
            await CaptchaService.slider_complete(r, _req(), key)
        with pytest.raises(CustomException, match="位置不正确"):
            await CaptchaService.slider_complete(r, _req(), key, int(state["target_x"]) + 20)
        ok = await CaptchaService.slider_complete(r, _req(), key, int(state["target_x"]))
        assert ok["verified"] is True
        with pytest.raises(CustomException, match="已使用"):
            await CaptchaService.slider_complete(r, _req(), key, int(state["target_x"]))
        assert await CaptchaService.check_captcha(redis=r, request=_req(), key=key) is True
        with pytest.raises(CustomException, match="过期|请先完成"):
            await CaptchaService.check_captcha(redis=r, request=_req(), key=key)
    finally:
        await r.aclose()


async def test_captcha_invalid_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.modules.system.auth import service as mod
    monkeypatch.setattr(mod.settings, "CAPTCHA_ENABLE", True)
    r = await _redis()
    try:
        with pytest.raises(CustomException):
            await CaptchaService.slider_complete(r, _req(), "")
        with pytest.raises(CustomException):
            await CaptchaService.slider_complete(r, _req(), "missing")
    finally:
        await r.aclose()
