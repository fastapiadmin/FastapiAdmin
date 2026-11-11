"""Alembic 离线 SQL 生成（覆盖 env.py 离线分支）。"""

from __future__ import annotations

import os

import pytest

from alembic import command
from alembic.config import Config

from app.config.path_conf import BASE_DIR


pytestmark = pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="离线 PG 迁移")


def test_offline_upgrade(capsys) -> None:
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    command.upgrade(cfg, "head", sql=True)
    out = capsys.readouterr().out
    assert "CREATE TABLE" in out or "alembic_version" in out
