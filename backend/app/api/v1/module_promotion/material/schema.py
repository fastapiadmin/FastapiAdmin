"""
物料管理 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class MaterialCreateSchema(BaseModel):
    """新增物料模型"""

    name: str = Field(..., description="物料名称", min_length=2, max_length=200)
    material_type: str | None = Field(default=None, description="物料类型")
    specification: str | None = Field(default=None, description="规格")
    total_stock: int = Field(default=0, description="总库存数量")
    available_stock: int = Field(default=0, description="可用库存数量")
    low_stock_threshold: int = Field(default=10, description="库存预警阈值")
    unit: str | None = Field(default=None, description="单位")
    storage_location: str | None = Field(default=None, description="存放位置")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证物料名称"""
        v = v.strip()
        if not v:
            raise ValueError("物料名称不能为空")
        return v


class MaterialUpdateSchema(MaterialCreateSchema):
    """更新物料模型"""

    pass


class MaterialOutSchema(MaterialCreateSchema, BaseSchema, UserBySchema):
    """物料响应模型"""

    model_config = ConfigDict(from_attributes=True)

    status: str | None = Field(default=None, description="状态")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class MaterialQuerySchema(BaseModel):
    """物料查询参数模型"""

    def __init__(
        self,
        name: str | None = Query(None, description="物料名称"),
        material_type: str | None = Query(None, description="物料类型"),
        status: str | None = Query(None, description="状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if name:
            self.name = (QueueEnum.like.value, name)
        if material_type:
            self.material_type = (QueueEnum.eq.value, material_type)
        if status:
            self.status = (QueueEnum.eq.value, status)


class MaterialApplyCreateSchema(BaseModel):
    """新增物料申领模型"""

    material_id: int = Field(..., description="物料ID")
    apply_quantity: int = Field(..., description="申请数量")
    use_date: DateTimeStr | None = Field(default=None, description="使用日期")
    use_purpose: str | None = Field(default=None, description="使用目的")
    remarks: str | None = Field(default=None, description="备注")


class MaterialApplyUpdateSchema(MaterialApplyCreateSchema):
    """更新物料申领模型"""

    pass


class MaterialApplyOutSchema(MaterialApplyCreateSchema, BaseSchema, UserBySchema):
    """物料申领响应模型"""

    model_config = ConfigDict(from_attributes=True)

    apply_no: str | None = Field(default=None, description="申领单号")
    material_name: str | None = Field(default=None, description="物料名称")
    status: str | None = Field(default=None, description="状态")
    approved_quantity: int | None = Field(default=None, description="批准数量")
    issued_quantity: int | None = Field(default=None, description="发放数量")
    approval_comment: str | None = Field(default=None, description="审批意见")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class MaterialApplyQuerySchema(BaseModel):
    """物料申领查询参数模型"""

    def __init__(
        self,
        material_name: str | None = Query(None, description="物料名称"),
        status: str | None = Query(None, description="状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if material_name:
            self.material_name = (QueueEnum.like.value, material_name)
        if status:
            self.status = (QueueEnum.eq.value, status)
