"""日期/口令/编码/菜单验证器边缘。"""

from __future__ import annotations

from datetime import UTC, date, datetime, time
from types import SimpleNamespace

import pytest

import app.core.validator as V
from app.core.exceptions import CustomException


def test_datetime_converters() -> None:
    assert V.to_local_datetime("x") == "x"
    assert V.to_local_datetime(datetime(2026, 1, 1)) is not None
    assert V.datetime_validator(datetime(2026, 1, 1)) == datetime(2026, 1, 1)
    assert V.date_validator(date(2026, 1, 1)) == date(2026, 1, 1)
    assert V.time_validator(time(1, 2, 3)) == time(1, 2, 3)
    with pytest.raises(CustomException):
        V.date_validator("bad")
    with pytest.raises(CustomException):
        V.time_validator("bad")


def test_password_and_code_validators() -> None:
    assert V.password_validator(None) is None
    with pytest.raises(ValueError):
        V.password_validator("   ")
    with pytest.raises(ValueError):
        V.password_validator("a")
    with pytest.raises(ValueError):
        V.password_validator("a" * 1000)
    assert V.code_validator(None) is None
    assert V.code_validator("  ") is None
    with pytest.raises(CustomException):
        V.code_validator("1bad")
    with pytest.raises(CustomException):
        V.code_validator("x")
    assert V.code_validator(" ab ") == "ab"


def test_menu_validator() -> None:
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=99))
