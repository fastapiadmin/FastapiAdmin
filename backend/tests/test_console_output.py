"""启动/关闭控制台面板渲染。"""

from __future__ import annotations

import pytest

import app.utils.console as console_mod


def test_console_start_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    printed = []
    monkeypatch.setattr(console_mod, "console", type("C", (), {"print": staticmethod(lambda x: printed.append(x))})())
    console_mod.console_start("127.0.0.1", 8000, True, database_type="postgres", database_ready=True, redis_ready=True, scheduler_ready=True)
    assert printed


def test_console_start_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    printed = []
    monkeypatch.setattr(console_mod, "console", type("C", (), {"print": staticmethod(lambda x: printed.append(x))})())
    console_mod.console_start("0.0.0.0", 80, False, database_type=None, database_ready=False, redis_ready=None, scheduler_ready=False)
    assert printed


def test_console_end(monkeypatch: pytest.MonkeyPatch) -> None:
    printed = []
    monkeypatch.setattr(console_mod, "console", type("C", (), {"print": staticmethod(lambda x: printed.append(x))})())
    console_mod.console_end()
    assert printed
