"""时间字段对外展示：数据库 UTC 时间统一按服务器展示时区输出。"""

from datetime import UTC, datetime

from pydantic import BaseModel

from app.core.validator import DateTimeStr


class _TimeModel(BaseModel):
    t: DateTimeStr | None = None


def test_aware_utc_datetime_is_rendered_in_server_timezone() -> None:
    model = _TimeModel(t=datetime(2026, 1, 1, 0, 0, tzinfo=UTC))
    assert model.model_dump(mode="json")["t"] == "2026-01-01 08:00:00"


def test_naive_utc_datetime_is_rendered_in_server_timezone() -> None:
    model = _TimeModel(t=datetime(2026, 1, 1, 0, 0))
    assert model.model_dump(mode="json")["t"] == "2026-01-01 08:00:00"
