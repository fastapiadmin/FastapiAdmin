"""导入工具基础校验分支。"""

from __future__ import annotations

from app.core.base_model import MappedBase
from app.utils.import_util import ImportUtil


def test_is_valid_model_edges() -> None:
    assert ImportUtil.is_valid_model(object, MappedBase) is False
    assert ImportUtil.is_valid_model(MappedBase, MappedBase) is False

    class NoTable(MappedBase):
        __abstract__ = True
    assert ImportUtil.is_valid_model(NoTable, MappedBase) is False

