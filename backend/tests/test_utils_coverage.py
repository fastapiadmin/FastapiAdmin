"""小工具模块的全分支覆盖：banner / excel / password。"""

from __future__ import annotations

from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

import pytest
from openpyxl import Workbook, load_workbook

from app.utils import banner as banner_mod
from app.utils.excel_util import ExcelUtil
from app.utils.password_util import PwdUtil


def test_banner_reads_file_and_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    p = tmp_path / "banner.txt"
    p.write_text("FASTAPIADMIN", encoding="utf-8")
    monkeypatch.setattr(banner_mod, "BANNER_FILE", p)
    assert banner_mod.worship() == "FASTAPIADMIN"
    monkeypatch.setattr(banner_mod, "BANNER_FILE", tmp_path / "missing.txt")
    assert banner_mod.worship() == ""


def _xlsx(rows: list[list[object]]) -> bytes:
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    out = BytesIO()
    wb.save(out)
    return out.getvalue()


def test_excel_read_dicts_and_async() -> None:
    payload = _xlsx([["名称", "值", None], ["a", 1, None], [None, None, None], ["b", 2, None]])
    rows = ExcelUtil.read_excel_to_dicts(payload)
    assert rows == [{"名称": "a", "值": 1}, {"名称": "b", "值": 2}]


async def test_excel_async_read() -> None:
    payload = _xlsx([["h"], ["v"]])
    assert await ExcelUtil.aread_excel_to_dicts(payload) == [{"h": "v"}]


def test_excel_read_rejects_non_xlsx() -> None:
    with pytest.raises(Exception):
        ExcelUtil.read_excel_to_dicts(b"not an xlsx")


def test_excel_template_with_options_and_export() -> None:
    tpl = ExcelUtil.get_excel_template(
        header_list=["名称", "状态"],
        selector_header_list=["状态"],
        option_list=[{"状态": ["正常", "停用"]}],
    )
    wb = load_workbook(BytesIO(tpl))
    assert wb.active is not None
    assert wb.active["A1"].value == "名称"
    assert wb.active["B1"].value == "状态"

    data = ExcelUtil.export_list2excel(
        [{"name": "a", "created": datetime(2026, 1, 1, tzinfo=UTC)}],
        {"name": "名称", "created": "创建时间"},
    )
    ws = load_workbook(BytesIO(data)).active
    assert ws is not None
    assert ws["A2"].value == "a"
    assert ws["B2"].value.tzinfo is None


async def test_excel_async_export() -> None:
    data = await ExcelUtil.aexport_list2excel([{"name": "a"}], {"name": "名称"})
    assert len(data) > 100


def test_password_hash_verify_and_invalid_format() -> None:
    h = PwdUtil.hash_password("Abc123!x")
    assert PwdUtil.verify_password("Abc123!x", h) is True
    assert PwdUtil.verify_password("wrong", h) is False
    assert PwdUtil.verify_password("x", "bad-format") is False
    assert PwdUtil.verify_password("x", "$pbkdf2-sha256$1$bad$bad") is False
    assert PwdUtil.verify_password("x", "$unknown$600000$bad$bad") is False


async def test_password_async_hash_verify() -> None:
    h = await PwdUtil.ahash_password("Abc123!x")
    assert await PwdUtil.averify_password("Abc123!x", h) is True


def test_password_strength_and_generate() -> None:
    assert PwdUtil.check_password_strength("123456") is not None
    assert PwdUtil.check_password_strength("abcdef") is not None
    assert PwdUtil.check_password_strength("abc123") is None
    with pytest.raises(ValueError):
        PwdUtil.generate_strong_password(7)
    p = PwdUtil.generate_strong_password(12)
    assert len(p) == 12
    assert any(c.isupper() for c in p)
    assert any(c.islower() for c in p)
    assert any(c.isdigit() for c in p)
    assert any(not c.isalnum() for c in p)
