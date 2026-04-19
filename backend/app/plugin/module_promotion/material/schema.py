"""
物料管理 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class MaterialCreateSchema(BaseModel):
    """新增物料模型"""

    material_name: str = Field(..., description="物料名称", min_length=2, max_length=200)
    material_code: str | None = Field(default=None, description="物料编码", max_length=50)
    material_type: str = Field(default="other", description="物料类型")

    specification: str | None = Field(default=None, description="规格", max_length=200)
    unit: str | None = Field(default=None, description="单位", max_length=20)

    total_stock: int = Field(default=0, description="总库存")
    available_stock: int = Field(default=0, description="可用库存")
    reserved_stock: int = Field(default=0, description="预留库存")

    low_stock_threshold: int = Field(default=10, description="库存预警阈值")
    unit_price: float | None = Field(default=None, description="单价")

    supplier_name: str | None = Field(default=None, description="供应商名称", max_length=200)
    supplier_contact: str | None = Field(default=None, description="供应商联系人", max_length=100)
    supplier_phone: str | None = Field(default=None, description="供应商电话", max_length=20)

    image_url: str | None = Field(default=None, description="物料图片", max_length=500)
    description: str | None = Field(default=None, description="物料描述")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")

    @field_validator("material_name")
    @classmethod
    def validate_material_name(cls, v: str) -> str:
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
        material_name: str | None = Query(None, description="物料名称"),
        material_code: str | None = Query(None, description="物料编码"),
        material_type: str | None = Query(None, description="物料类型"),
        status: str | None = Query(None, description="状态"),
        supplier_name: str | None = Query(None, description="供应商名称"),
    ) -> None:
        from app.common.enums import QueueEnum

        if material_name:
            self.material_name = (QueueEnum.like.value, material_name)
        if material_code:
            self.material_code = (QueueEnum.eq.value, material_code)
        if material_type:
            self.material_type = (QueueEnum.eq.value, material_type)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if supplier_name:
            self.supplier_name = (QueueEnum.like.value, supplier_name)


class MaterialApplyCreateSchema(BaseModel):
    """新增物料申请模型"""

    material_id: int = Field(..., description="物料ID")
    material_name: str | None = Field(default=None, description="物料名称", max_length=200)
    material_type: str | None = Field(default=None, description="物料类型")
    apply_quantity: int = Field(default=1, ge=1, description="申请数量")
    usage: str | None = Field(default=None, description="用途说明")
    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)


class MaterialApplyUpdateSchema(MaterialApplyCreateSchema):
    """更新物料申请模型"""
    pass


class MaterialApplyOutSchema(MaterialApplyCreateSchema, BaseSchema, UserBySchema):
    """物料申请响应模型"""

    model_config = ConfigDict(from_attributes=True)

    apply_no: str | None = Field(default=None, description="申请单号")
    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称")
    applicant_id: int | None = Field(default=None, description="申请人ID")
    applicant_name: str | None = Field(default=None, description="申请人姓名")
    approved_quantity: int | None = Field(default=None, description="批准数量")
    issued_quantity: int | None = Field(default=None, description="已发放数量")
    apply_status: str | None = Field(default=None, description="申请状态")
    approval_comment: str | None = Field(default=None, description="审批意见")
    approver_id: int | None = Field(default=None, description="审批人ID")
    approver_name: str | None = Field(default=None, description="审批人姓名")
    approval_time: DateTimeStr | None = Field(default=None, description="审批时间")
    issuer_id: int | None = Field(default=None, description="发放人ID")
    issuer_name: str | None = Field(default=None, description="发放人姓名")
    issue_time: DateTimeStr | None = Field(default=None, description="发放时间")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class MaterialApplyQuerySchema(BaseModel):
    """物料申请查询参数模型"""

    def __init__(
        self,
        apply_no: str | None = Query(None, description="申请单号"),
        material_id: int | None = Query(None, description="物料ID"),
        material_name: str | None = Query(None, description="物料名称"),
        team_id: int | None = Query(None, description="招生组ID"),
        applicant_id: int | None = Query(None, description="申请人ID"),
        applicant_name: str | None = Query(None, description="申请人姓名"),
        apply_status: str | None = Query(None, description="申请状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if apply_no:
            self.apply_no = (QueueEnum.like.value, apply_no)
        if material_id is not None:
            self.material_id = (QueueEnum.eq.value, material_id)
        if material_name:
            self.material_name = (QueueEnum.like.value, material_name)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if applicant_id is not None:
            self.applicant_id = (QueueEnum.eq.value, applicant_id)
        if applicant_name:
            self.applicant_name = (QueueEnum.like.value, applicant_name)
        if apply_status:
            self.apply_status = (QueueEnum.eq.value, apply_status)