"""输入域 / 等价类 / 边界值 / 正交组合测试。

只验证 Pydantic 输入契约，不依赖数据库或网络；写接口集成测试时复用这些边界值。
每个用例的 ``case`` 字段就是测试设计编号，便于和测试用例表对应。
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from app.core.exceptions import CustomException

from app.modules.system.dept.schema import DeptCreateSchema
from app.modules.system.menu.schema import MenuCreateSchema
from app.modules.system.notice.schema import NoticeCreateSchema
from app.modules.system.params.schema import ParamsBaseSchema
from app.modules.system.position.schema import PositionCreateSchema
from app.modules.system.role.schema import RoleCreateSchema
from app.modules.system.user.schema import UserCreateSchema, UserUpdateSchema
from app.modules.task.cronjob.node.schema import NodeCreateSchema
from app.modules.task.storage.node.schema import StorageNodeConfigSchema


def _invalid(schema: type, data: dict[str, Any]) -> None:
    # 项目里部分自定义校验器抛出 CustomException（统一业务异常），其余抛 Pydantic
    # ValidationError；两者都代表输入被拒绝，测试契约按“拒绝”断言。
    with pytest.raises((ValidationError, CustomException)):
        schema.model_validate(data)


def _valid(schema: type, data: dict[str, Any]) -> Any:
    return schema.model_validate(data)


# ── 用户：账号 2-32、名称 32、手机号 11、邮箱、密码策略、状态 0/1 ──
@pytest.mark.parametrize(
    ("case", "username", "ok"),
    [
        ("USER-USERNAME-001", "a", False),
        ("USER-USERNAME-002", "a1", True),
        ("USER-USERNAME-003", "a" + "b" * 30, True),
        ("USER-USERNAME-004", "a" + "b" * 31, True),
        ("USER-USERNAME-005", "a" + "b" * 32, False),
        ("USER-USERNAME-006", "1abc", False),
        ("USER-USERNAME-007", "a_b.c-d", True),
        ("USER-USERNAME-008", "a b", False),
    ],
)
def test_user_username_boundary(case: str, username: str, ok: bool) -> None:
    data = {"username": username, "name": "E2E", "password": "E2e@Test12345"}
    if ok:
        assert _valid(UserCreateSchema, data).username == username
    else:
        _invalid(UserCreateSchema, data)


@pytest.mark.parametrize(
    ("case", "field", "value", "ok"),
    [
        ("USER-NAME-001", "name", "名" * 32, True),
        ("USER-NAME-002", "name", "名" * 33, False),
        ("USER-MOBILE-001", "mobile", "13800138000", True),
        ("USER-MOBILE-002", "mobile", "1380013800", False),
        ("USER-MOBILE-003", "mobile", "138001380001", False),
        ("USER-MOBILE-004", "mobile", "12800138000", False),
        ("USER-EMAIL-001", "email", "e2e@example.com", True),
        ("USER-EMAIL-002", "email", "not-an-email", False),
        ("USER-EMAIL-003", "email", "a@b", False),
        ("USER-GENDER-001", "gender", "0", True),
        ("USER-GENDER-002", "gender", "2", True),
        ("USER-GENDER-003", "gender", "3", False),
        ("USER-STATUS-001", "status", 0, True),
        ("USER-STATUS-002", "status", 1, True),
        ("USER-STATUS-003", "status", -1, False),
        ("USER-STATUS-004", "status", 2, False),
    ],
)
def test_user_fields_boundary(case: str, field: str, value: Any, ok: bool) -> None:
    data = {"username": "e2e_user", "name": "E2E", "password": "E2e@Test12345", field: value}
    if ok:
        _valid(UserCreateSchema, data)
    else:
        _invalid(UserCreateSchema, data)


@pytest.mark.parametrize(
    ("case", "password", "ok"),
    [
        ("USER-PWD-001", "a1", False),
        ("USER-PWD-002", "123456", False),
        ("USER-PWD-003", "abcdef", False),
        ("USER-PWD-004", "abc123", True),
        ("USER-PWD-005", "E2e@Test12345", True),
        ("USER-PWD-006", "A" * 128 + "1", False),
    ],
)
def test_user_password_boundary(case: str, password: str, ok: bool) -> None:
    data = {"username": "e2e_user", "name": "E2E", "password": password}
    if ok:
        _valid(UserCreateSchema, data)
    else:
        _invalid(UserCreateSchema, data)


def test_user_update_allows_omitted_password() -> None:
    # 编辑时省略 password 表示不改密码；显式 null 也应允许（数据库值由 CRUD 跳过）。
    assert _valid(UserUpdateSchema, {"name": "新名称"}).password is None
    _invalid(UserUpdateSchema, {"name": "名" * 33})


# ── 角色：编码 2-64、名称、排序、data_scope 1-3、status 0/1 ──
@pytest.mark.parametrize(
    ("case", "field", "value", "ok"),
    [
        ("ROLE-CODE-001", "code", "a", False),
        ("ROLE-CODE-002", "code", "ab", True),
        ("ROLE-CODE-003", "code", "a" + "b" * 63, True),
        ("ROLE-CODE-004", "code", "a" + "b" * 64, False),
        ("ROLE-CODE-005", "code", "1abc", False),
        ("ROLE-CODE-006", "code", "a b", False),
        ("ROLE-NAME-001", "name", "  ", False),
        ("ROLE-NAME-002", "name", "角色", True),
        ("ROLE-ORDER-001", "order", -1, False),
        ("ROLE-ORDER-002", "order", 0, True),
        ("ROLE-SCOPE-001", "data_scope", 0, False),
        ("ROLE-SCOPE-002", "data_scope", 1, True),
        ("ROLE-SCOPE-003", "data_scope", 3, True),
        ("ROLE-SCOPE-004", "data_scope", 4, False),
        ("ROLE-STATUS-001", "status", 0, True),
        ("ROLE-STATUS-002", "status", 1, True),
        ("ROLE-STATUS-003", "status", 2, False),
    ],
)
def test_role_boundary(case: str, field: str, value: Any, ok: bool) -> None:
    data = {"name": "E2E角色", "code": "e2e_role", "order": 1, "data_scope": 1, "status": 0, field: value}
    if ok:
        _valid(RoleCreateSchema, data)
    else:
        _invalid(RoleCreateSchema, data)


@pytest.mark.parametrize(
    ("scope", "status", "case"),
    [(scope, status, f"ROLE-ORTHO-{scope}-{status}") for scope in (1, 2, 3) for status in (0, 1)],
)
def test_role_orthogonal_scope_status(scope: int, status: int, case: str) -> None:
    result = _valid(
        RoleCreateSchema,
        {"name": f"角色{scope}{status}", "code": f"e2e_{scope}_{status}", "data_scope": scope, "status": status},
    )
    assert result.data_scope == scope
    assert result.status == status


# ── 部门 / 岗位 ──
@pytest.mark.parametrize(
    ("case", "schema", "data", "ok"),
    [
        ("DEPT-CODE-001", DeptCreateSchema, {"name": "部门", "code": "a"}, False),
        ("DEPT-CODE-002", DeptCreateSchema, {"name": "部门", "code": "ab"}, True),
        ("DEPT-NAME-001", DeptCreateSchema, {"name": "  ", "code": "ab"}, False),
        ("DEPT-PARENT-001", DeptCreateSchema, {"name": "部门", "code": "ab", "parent_id": 0}, False),
        ("DEPT-STATUS-001", DeptCreateSchema, {"name": "部门", "code": "ab", "status": 2}, False),
        ("POS-NAME-001", PositionCreateSchema, {"name": " ", "code": "a"}, False),
        ("POS-CODE-001", PositionCreateSchema, {"name": "岗位", "code": " "}, False),
        ("POS-STATUS-001", PositionCreateSchema, {"name": "岗位", "code": "a", "status": 2}, False),
        ("POS-OK-001", PositionCreateSchema, {"name": "岗位", "code": "a", "status": 0}, True),
    ],
)
def test_dept_position_boundary(case: str, schema: type, data: dict[str, Any], ok: bool) -> None:
    if ok:
        _valid(schema, data)
    else:
        _invalid(schema, data)


# ── 公告：标题 1-64、类型 1/2、状态 0-2、内容 XSS 清洗 ──
@pytest.mark.parametrize(
    ("case", "data", "ok"),
    [
        ("NOTICE-TITLE-001", {"notice_title": "", "notice_type": "1"}, False),
        ("NOTICE-TITLE-002", {"notice_title": "公告", "notice_type": "1"}, True),
        ("NOTICE-TITLE-003", {"notice_title": "标" * 64, "notice_type": "1"}, True),
        ("NOTICE-TITLE-004", {"notice_title": "标" * 65, "notice_type": "1"}, False),
        ("NOTICE-TYPE-001", {"notice_title": "公告", "notice_type": "1"}, True),
        ("NOTICE-TYPE-002", {"notice_title": "公告", "notice_type": "2"}, True),
        ("NOTICE-TYPE-003", {"notice_title": "公告", "notice_type": "3"}, False),
        ("NOTICE-STATUS-001", {"notice_title": "公告", "notice_type": "1", "status": 0}, True),
        ("NOTICE-STATUS-002", {"notice_title": "公告", "notice_type": "1", "status": 2}, True),
        ("NOTICE-STATUS-003", {"notice_title": "公告", "notice_type": "1", "status": 3}, False),
    ],
)
def test_notice_boundary(case: str, data: dict[str, Any], ok: bool) -> None:
    if ok:
        _valid(NoticeCreateSchema, data)
    else:
        _invalid(NoticeCreateSchema, data)


def test_notice_content_is_sanitized() -> None:
    result = _valid(
        NoticeCreateSchema,
        {"notice_title": "公告", "notice_type": "1", "notice_content": "<p>正常</p><script>alert(1)</script>"},
    )
    assert "<script" not in (result.notice_content or "").lower()


# ── 参数键：小写字母开头、允许 ._-、大小写归一 ──
@pytest.mark.parametrize(
    ("case", "key", "ok"),
    [
        ("PARAM-KEY-001", "a", True),
        ("PARAM-KEY-002", "1abc", False),
        ("PARAM-KEY-003", "a.b-c_d", True),
        ("PARAM-KEY-004", "a b", False),
        ("PARAM-KEY-005", "ABC", True),  # 当前实现会 trim + lower 后校验
    ],
)
def test_param_key(case: str, key: str, ok: bool) -> None:
    data = {"config_name": "参数", "config_key": key}
    if ok:
        assert _valid(ParamsBaseSchema, data).config_key == key.strip().lower()
    else:
        _invalid(ParamsBaseSchema, data)


# ── 菜单：名称 1-50、类型 1-4、排序、父 ID、范围枚举、组件路径 ──
@pytest.mark.parametrize(
    ("case", "data", "ok"),
    [
        ("MENU-NAME-001", {"name": "菜单", "type": 2, "order": 0, "route_name": "E2ERoute", "route_path": "/e2e", "component_path": "module_system/user/index"}, True),
        ("MENU-NAME-002", {"name": "名" * 50, "type": 2, "order": 0, "route_name": "E2ERoute", "route_path": "/e2e", "component_path": "module_system/user/index"}, True),
        ("MENU-NAME-003", {"name": "名" * 51, "type": 2, "order": 0}, False),
        ("MENU-TYPE-001", {"name": "菜单", "type": 1, "order": 0, "route_name": "E2EDir", "route_path": "/e2e-dir", "redirect": "/e2e"}, True),
        ("MENU-TYPE-002", {"name": "菜单", "type": 4, "order": 0, "route_name": "E2ELink", "link": "https://example.com"}, True),
        ("MENU-TYPE-003", {"name": "菜单", "type": 0, "order": 0}, False),
        ("MENU-TYPE-004", {"name": "菜单", "type": 5, "order": 0}, False),
        ("MENU-ORDER-001", {"name": "菜单", "type": 2, "order": -1}, False),
        ("MENU-PARENT-001", {"name": "菜单", "type": 2, "order": 0, "parent_id": 0}, False),
        ("MENU-SCOPE-001", {"name": "菜单", "type": 2, "order": 0, "route_name": "E2ERoute", "route_path": "/e2e", "component_path": "module_system/user/index", "scope": "web"}, True),
        ("MENU-SCOPE-002", {"name": "菜单", "type": 2, "order": 0, "route_name": "E2ERoute", "route_path": "/e2e", "component_path": "module_system/user/index", "scope": "app"}, True),
        ("MENU-SCOPE-003", {"name": "菜单", "type": 2, "order": 0, "scope": "other"}, False),
        ("MENU-COMPONENT-001", {"name": "菜单", "type": 2, "order": 0, "component_path": "/bad"}, False),
    ],
)
def test_menu_boundary(case: str, data: dict[str, Any], ok: bool) -> None:
    if ok:
        _valid(MenuCreateSchema, data)
    else:
        _invalid(MenuCreateSchema, data)


# ── 定时任务：trigger/trigger_args 正交、日期区间、编码 ──
@pytest.mark.parametrize(
    ("case", "data", "ok"),
    [
        ("CRON-TRIGGER-001", {"name": "任务", "func": "builtin:a.b", "trigger": "cron", "trigger_args": "0 3 * * *"}, True),
        ("CRON-TRIGGER-002", {"name": "任务", "func": "builtin:a.b", "trigger": "interval", "trigger_args": "60"}, True),
        ("CRON-TRIGGER-003", {"name": "任务", "func": "builtin:a.b", "trigger": "date", "trigger_args": "2026-01-01 00:00:00"}, True),
        ("CRON-TRIGGER-004", {"name": "任务", "func": "builtin:a.b", "trigger": "cron"}, False),
        ("CRON-TRIGGER-005", {"name": "任务", "func": "builtin:a.b", "trigger": "bad", "trigger_args": "x"}, False),
        ("CRON-FUNC-001", {"name": "任务", "func": ""}, False),
        ("CRON-CODE-001", {"name": "任务", "func": "builtin:a.b", "code": "a"}, False),
        ("CRON-CODE-002", {"name": "任务", "func": "builtin:a.b", "code": "ab"}, True),
        ("CRON-DATE-001", {"name": "任务", "func": "builtin:a.b", "start_date": "2026-01-02 00:00:00", "end_date": "2026-01-01 00:00:00"}, False),
        ("CRON-DATE-002", {"name": "任务", "func": "builtin:a.b", "start_date": "2026-01-01 00:00:00", "end_date": "2026-01-02 00:00:00"}, True),
    ],
)
def test_cron_boundary(case: str, data: dict[str, Any], ok: bool) -> None:
    if ok:
        _valid(NodeCreateSchema, data)
    else:
        _invalid(NodeCreateSchema, data)


# ── 存储源：协议必填、分片边界、编码、路径穿越 ──
@pytest.mark.parametrize(
    ("case", "data", "ok"),
    [
        ("STORAGE-S3-001", {"protocol": "s3", "bucket": "b", "endpoint": "https://s3.example.com"}, True),
        ("STORAGE-S3-002", {"protocol": "s3", "endpoint": "https://s3.example.com"}, False),
        ("STORAGE-S3-003", {"protocol": "s3", "bucket": "b"}, False),
        ("STORAGE-LOCAL-001", {"protocol": "local", "host": "static/upload"}, True),
        ("STORAGE-LOCAL-002", {"protocol": "local"}, False),
        ("STORAGE-PART-001", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_part_size": 4}, False),
        ("STORAGE-PART-002", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_part_size": 5}, True),
        ("STORAGE-PART-003", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_part_size": 5000}, True),
        ("STORAGE-PART-004", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_part_size": 5001}, False),
        ("STORAGE-CONC-001", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_concurrency": 0}, False),
        ("STORAGE-CONC-002", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_concurrency": 64}, True),
        ("STORAGE-CONC-003", {"protocol": "s3", "bucket": "b", "endpoint": "https://e", "multipart_concurrency": 65}, False),
        ("STORAGE-PREFIX-001", {"protocol": "local", "host": "x", "path_prefix": "../etc"}, False),
        ("STORAGE-ENCODING-001", {"protocol": "local", "host": "x", "encoding": "gbk"}, True),
        ("STORAGE-ENCODING-002", {"protocol": "local", "host": "x", "encoding": "not-a-codec"}, False),
    ],
)
def test_storage_boundary(case: str, data: dict[str, Any], ok: bool) -> None:
    if ok:
        _valid(StorageNodeConfigSchema, data)
    else:
        _invalid(StorageNodeConfigSchema, data)
