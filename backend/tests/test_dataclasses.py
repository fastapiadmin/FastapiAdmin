"""请求/令牌/上传等轻量数据结构。"""

from __future__ import annotations

from datetime import datetime

from fastapi import Response

from app.common.dataclasses import (
    AccessToken, NewToken, RefreshToken, RequestCallNext, SnowflakeInfo,
    TokenPayload, UploadUrl, UserAgentInfo,
)


def test_dataclasses_instantiation() -> None:
    now = datetime.now()
    assert UserAgentInfo("ua", "mac", "chrome", "desktop").browser == "chrome"
    resp = Response()
    assert RequestCallNext("0", "ok", None, resp).response is resp
    assert AccessToken("a", now, "s").session_uuid == "s"
    assert RefreshToken("r", now).refresh_token == "r"
    assert NewToken("a", now, "r", now, "s").new_refresh_token == "r"
    assert TokenPayload(1, "s", now).id == 1
    assert UploadUrl("u").url == "u"
    assert SnowflakeInfo(1, "d", 2, 3, 4).sequence == 4
