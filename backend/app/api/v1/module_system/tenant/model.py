from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.common.enums import PermissionFilterStrategy
from app.core.base_model import ModelMixin


class TenantModel(ModelMixin):
    """
    租户模型

    - 系统租户(id=1)：平台管理，由超级管理员维护
    - 普通租户(id>1)：独立组织数据，通过业务表的 tenant_id 隔离
    """

    __tablename__: str = "sys_tenant"
    __table_args__: dict[str, str] = {"comment": "租户表"}
    __permission_strategy__: PermissionFilterStrategy = PermissionFilterStrategy.DATA_SCOPE

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="租户名称")
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="租户编码")
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None, comment="开始时间"
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None, comment="结束时间"
    )

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if not name or not name.strip():
            raise ValueError("名称不能为空")
        return name

    @validates("code")
    def validate_code(self, key: str, code: str) -> str:
        if not code or not code.strip():
            raise ValueError("编码不能为空")
        if not code.isalnum():
            raise ValueError("编码只能包含字母和数字")
        return code
