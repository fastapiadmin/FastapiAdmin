"""模型扫描工具覆盖。"""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column
from app.core.base_model import MappedBase as Base
from app.utils.import_util import ImportUtil


class ModelA(Base):
    __tablename__ = "test_model_a"
    __table_args__ = {"extend_existing": True}
    id = mapped_column(Integer, primary_key=True)


class AbstractModel(Base):
    __abstract__ = True


def test_find_root_and_valid_models() -> None:
    assert ImportUtil.find_project_root().name
    assert ImportUtil.is_valid_model(ModelA, Base) is True
    assert ImportUtil.is_valid_model(Base, Base) is False
    assert ImportUtil.is_valid_model(AbstractModel, Base) is False
    assert ImportUtil.is_valid_model(object, Base) is False


def test_find_models_contains_real_models() -> None:
    models = ImportUtil.find_models(Base)
    assert isinstance(models, list)
    assert any(getattr(m, "__tablename__", "") == "sys_user" for m in models)
    assert len(models) == len(set(models))


def test_find_apscheduler_model(monkeypatch) -> None:
    models = []; seen_models = set(); seen_tables = set()
    ImportUtil._find_apscheduler_model(Base, models, seen_models, seen_tables)
    assert isinstance(models, list)
