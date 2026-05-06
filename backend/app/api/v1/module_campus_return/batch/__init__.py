"""
批次管理模块
"""

from app.api.v1.module_campus_return.batch.model import CampusReturnBatchModel
from app.core.base_model import ModelMixin, UserMixin

__all__ = ["CampusReturnBatchModel", "ModelMixin", "UserMixin"]
