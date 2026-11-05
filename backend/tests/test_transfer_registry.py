"""传输取消标志注册表。"""

from app.modules.task.storage.transfer.registry import TransferTaskRegistry


def test_registry_cancel_clear() -> None:
    r = TransferTaskRegistry()
    assert r.is_canceled(1) is False
    r.mark_cancel(1)
    assert r.is_canceled(1) is True
    r.clear(1)
    assert r.is_canceled(1) is False
    r.clear(99)
