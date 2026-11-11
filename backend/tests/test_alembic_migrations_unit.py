"""历史自动迁移脚本的 Python 逻辑（op 以记录器替代，不触库）。"""

from __future__ import annotations

import importlib

from alembic import op as real_op


class _Batch:
    def __init__(self, calls): self.calls = calls
    def __getattr__(self, name):
        def f(*a, **k): self.calls.append((name, a, k)); return None
        return f
    def __enter__(self): return self
    def __exit__(self, *a): return False


class _Op:
    def __init__(self): self.calls = []
    def __getattr__(self, name):
        def f(*a, **k):
            self.calls.append((name, a, k))
            return _Batch(self.calls) if name == "batch_alter_table" else None
        return f
    def f(self, name): return name


def test_initial_migration_upgrade_downgrade(monkeypatch) -> None:
    module = importlib.import_module("app.alembic.versions.2026_10_22_2240_e082c18b2f01")
    fake = _Op()
    monkeypatch.setattr(module, "op", fake)
    module.upgrade()
    module.downgrade()
    names = [c[0] for c in fake.calls]
    assert "create_table" in names and "drop_table" in names
    assert "batch_alter_table" in names
