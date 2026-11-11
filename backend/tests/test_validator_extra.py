"""请求字段校验器边界。"""

from __future__ import annotations

from datetime import date, datetime, time

import pytest

from app.core.exceptions import CustomException
from app.core import validator as V


def test_datetime_date_time_validators() -> None:
    assert V.datetime_validator("2024-01-02 03:04:05") == datetime(2024, 1, 2, 3, 4, 5)
    assert V.date_validator("2024-01-02") == date(2024, 1, 2)
    assert V.time_validator("03:04:05") == time(3, 4, 5)
    for fn, bad in ((V.datetime_validator, "bad"), (V.date_validator, "bad"), (V.time_validator, "bad")):
        with pytest.raises(CustomException):
            fn(bad)


def test_email_validator() -> None:
    assert V.email_validator("a@b.com") == "a@b.com"
    for bad in ("a@", "a b@c.com", ""):
        with pytest.raises(CustomException):
            V.email_validator(bad)


def test_password_validator() -> None:
    assert V.password_validator("Abc123!x") == "Abc123!x"
    for bad in ("short", "12345678"):
        with pytest.raises(ValueError):
            V.password_validator(bad)


def test_mobile_code_validators() -> None:
    assert V.mobile_validator("13800138000") == "13800138000"
    assert V.mobile_validator(None) is None
    with pytest.raises(CustomException):
        V.mobile_validator("123")
    with pytest.raises(ValueError):
        V.validate_required_code("")
    assert V.validate_required_code("Abc_1") == "Abc_1"



def test_menu_request_validator_branches() -> None:
    from types import SimpleNamespace
    menu = SimpleNamespace(type=2, route_name="r", route_path="/p", component_path="c", redirect=None, client="pc")
    assert V.menu_request_validator(menu) is menu
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=9))
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=1, route_name="r", route_path="/p", redirect=None, client="pc"))
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=2, route_name="r", route_path="/p", component_path="", client="pc"))
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=4, route_name="r", route_path="/p", client="pc"))
    with pytest.raises(CustomException):
        V.menu_request_validator(SimpleNamespace(type=4, route_name="r", route_path="/p", link="u", client="bad"))


def test_role_permission_validator() -> None:
    from types import SimpleNamespace
    role = SimpleNamespace(data_scope=3, role_ids=[1])
    assert V.role_permission_request_validator(role) is role
    with pytest.raises(CustomException):
        V.role_permission_request_validator(SimpleNamespace(data_scope=9, role_ids=[1]))
    with pytest.raises(CustomException):
        V.role_permission_request_validator(SimpleNamespace(data_scope=1, role_ids=[]))
