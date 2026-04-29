"""
批次管理模块
"""
from app.core.base_model import ModelMixin, UserMixin
from app.api.v1.module_campus_return.batch.model import CampusReturnBatchModel

__all__ = ["CampusReturnBatchModel", "ModelMixin", "UserMixin"]
