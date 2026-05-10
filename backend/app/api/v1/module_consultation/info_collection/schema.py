"""
咨询会信息聚合 - 数据验证Schema
"""

from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr


class ThirdPartyUploadSchema(BaseModel):
    """第三方上传咨询会信息模型"""

    # 基本信息
    title: str = Field(..., description="咨询会标题", min_length=2, max_length=200)
    description: str | None = Field(default=None, description="咨询会描述")

    # 主办方信息
    organizer: str = Field(..., description="主办方", min_length=2, max_length=200)
    organizer_type: str | None = Field(default=None, description="主办方类型")
    organizer_nature: str | None = Field(default=None, description="主办机构性质")

    # 第三方机构信息
    has_third_party: bool = Field(default=False, description="是否有第三方机构参与")
    third_party_info: dict | None = Field(default=None, description="第三方机构信息")

    # 时间和地点
    start_date: DateStr = Field(..., description="开始日期")
    end_date: DateStr | None = Field(default=None, description="结束日期")
    start_time: str | None = Field(default=None, description="开始时间", max_length=10)
    end_time: str | None = Field(default=None, description="结束时间", max_length=10)

    # 地理位置
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)
    address: str | None = Field(default=None, description="详细地址", max_length=500)

    # 参与高校信息
    participating_universities: list | None = Field(default=None, description="参与高校列表")
    university_count: int = Field(default=0, description="参与高校数量")

    # 规模和费用
    estimated_visitors: int | None = Field(default=None, description="预计参观人数")
    booth_fee: float | None = Field(default=None, description="展位费用")

    # 联系人信息
    contact_person: str | None = Field(default=None, description="联系人", max_length=100)
    contact_phone: str | None = Field(default=None, description="联系电话", max_length=20)
    contact_email: str | None = Field(default=None, description="联系邮箱", max_length=100)

    # 报名信息
    registration_email: str | None = Field(default=None, description="报名接收邮箱", max_length=100)

    model_config = ConfigDict(from_attributes=True)


class InfoCollectionCreateSchema(BaseModel):
    """新增咨询会信息模型"""

    # 基本信息
    title: str = Field(..., description="咨询会标题", min_length=2, max_length=200)
    description: str | None = Field(default=None, description="咨询会描述")

    # 主办方信息
    organizer: str = Field(..., description="主办方", min_length=2, max_length=200)
    organizer_type: str | None = Field(default=None, description="主办方类型")
    organizer_nature: str | None = Field(default=None, description="主办机构性质")

    # 第三方机构信息
    has_third_party: bool = Field(default=False, description="是否有第三方机构参与")
    third_party_info: dict | None = Field(default=None, description="第三方机构信息")

    # 时间和地点
    start_date: DateStr = Field(..., description="开始日期")
    end_date: DateStr | None = Field(default=None, description="结束日期")
    start_time: str | None = Field(default=None, description="开始时间", max_length=10)
    end_time: str | None = Field(default=None, description="结束时间", max_length=10)

    # 地理位置
    province: str | None = Field(default=None, description="省份", max_length=50)
    city: str | None = Field(default=None, description="城市", max_length=50)
    district: str | None = Field(default=None, description="区县", max_length=50)
    address: str | None = Field(default=None, description="详细地址", max_length=500)

    # 参与高校信息
    participating_universities: list | None = Field(default=None, description="参与高校列表")
    university_count: int = Field(default=0, description="参与高校数量")

    # 规模和费用
    estimated_visitors: int | None = Field(default=None, description="预计参观人数")
    booth_fee: float | None = Field(default=None, description="展位费用")
    fee_description: str | None = Field(default=None, description="费用说明")

    # 协办方
    co_organizers: list | None = Field(default=None, description="协办方列表")

    # 场馆和坐标
    venue_name: str | None = Field(default=None, description="场馆名称", max_length=200)
    longitude: float | None = Field(default=None, description="经度")
    latitude: float | None = Field(default=None, description="纬度")

    # 来源信息
    source_type: str = Field(default="crawler", description="信息来源")
    source_url: str | None = Field(default=None, description="来源链接", max_length=1000)

    # 报名信息
    registration_email: str | None = Field(default=None, description="报名接收邮箱", max_length=100)

    @field_validator("title", "organizer")
    @classmethod
    def validate_required_string(cls, v: str) -> str:
        """验证必填字符串字段"""
        v = v.strip()
        if not v:
            raise ValueError("该字段不能为空")
        return v

    @model_validator(mode="after")
    def validate_dates(self):
        """验证日期逻辑"""
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValueError("结束日期不能早于开始日期")
        return self


class InfoCollectionUpdateSchema(InfoCollectionCreateSchema):
    """更新咨询会信息模型"""

    pass


class InfoCollectionOutSchema(InfoCollectionCreateSchema, BaseSchema, UserBySchema):
    """咨询会信息响应模型"""

    model_config = ConfigDict(from_attributes=True)

    # 状态信息
    status: str | None = Field(default=None, description="状态")
    review_comment: str | None = Field(default=None, description="审核意见")
    reviewed_by: int | None = Field(default=None, description="审核人ID")
    reviewed_time: DateTimeStr | None = Field(default=None, description="审核时间")

    # 合规评分
    compliance_score: float | None = Field(default=None, description="合规评分(0-10)")
    compliance_level: str | None = Field(default=None, description="合规等级(A/B/C/D)")
    risk_factors: list | None = Field(default=None, description="风险因素列表")

    # 归档信息
    is_archived: bool | None = Field(default=None, description="是否归档")
    archived_time: DateTimeStr | None = Field(default=None, description="归档时间")
    archived_by: int | None = Field(default=None, description="归档人ID")

    # 去重信息
    is_duplicate: bool | None = Field(default=None, description="是否为重复记录")
    duplicate_of_id: int | None = Field(default=None, description="关联的原始记录ID")

    # 搜索关键词
    search_keywords: str | None = Field(default=None, description="搜索关键词")


@dataclass
class InfoCollectionQueryParam:
    """咨询会信息查询参数"""

    def __init__(
        self,
        title: str | None = Query(None, description="咨询会标题"),
        organizer: str | None = Query(None, description="主办方"),
        province: str | None = Query(None, description="省份"),
        city: str | None = Query(None, description="城市"),
        start_date_begin: DateStr | None = Query(None, description="开始日期范围-开始"),
        start_date_end: DateStr | None = Query(None, description="开始日期范围-结束"),
        status: str | None = Query(None, description="状态"),
        source_type: str | None = Query(None, description="信息来源"),
        is_archived: bool | None = Query(None, description="是否归档"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
    ) -> None:
        from app.common.enums import QueueEnum

        # 模糊查询字段
        if title:
            self.title = (QueueEnum.like.value, title)
        if organizer:
            self.organizer = (QueueEnum.like.value, organizer)

        # 精确查询字段
        if province:
            self.province = (QueueEnum.eq.value, province)
        if city:
            self.city = (QueueEnum.eq.value, city)
        if status:
            self.status = (QueueEnum.eq.value, status)
        if source_type:
            self.source_type = (QueueEnum.eq.value, source_type)
        if is_archived is not None:
            self.is_archived = (QueueEnum.eq.value, is_archived)

        # 日期范围查询
        if start_date_begin and start_date_end:
            self.start_date = (QueueEnum.between.value, (start_date_begin, start_date_end))

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = (QueueEnum.between.value, (created_time[0], created_time[1]))
