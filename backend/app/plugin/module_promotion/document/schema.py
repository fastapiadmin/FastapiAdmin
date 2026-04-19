"""
活动撰写 - 数据验证Schema
"""
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr, DateStr


class DocumentCreateSchema(BaseModel):
    """新增活动撰写模型"""

    activity_id: int | None = Field(default=None, description="关联活动ID")
    activity_name: str | None = Field(default=None, description="关联活动名称", max_length=200)

    document_title: str = Field(..., description="文档标题", max_length=500)
    document_type: str = Field(default="other", description="文档类型")

    document_content: str | None = Field(default=None, description="文档内容")
    document_summary: str | None = Field(default=None, description="文档摘要")
    keywords: str | None = Field(default=None, description="关键词", max_length=500)
    cover_image: str | None = Field(default=None, description="封面图片URL", max_length=500)

    author_id: int | None = Field(default=None, description="作者ID")
    author_name: str | None = Field(default=None, description="作者姓名", max_length=100)

    team_id: int | None = Field(default=None, description="招生组ID")
    team_name: str | None = Field(default=None, description="招生组名称", max_length=200)

    is_top: bool = Field(default=False, description="是否置顶")
    is_featured: bool = Field(default=False, description="是否推荐")

    attachment_urls: list[str] | None = Field(default=None, description="附件URL列表")
    attachment_names: list[str] | None = Field(default=None, description="附件名称列表")

    remark: str | None = Field(default=None, description="备注")
    display_order: int = Field(default=0, description="显示排序")


class DocumentUpdateSchema(DocumentCreateSchema):
    """更新活动撰写模型"""
    pass


class DocumentOutSchema(DocumentCreateSchema, BaseSchema, UserBySchema):
    """活动撰写响应模型"""

    model_config = ConfigDict(from_attributes=True)

    document_no: str | None = Field(default=None, description="文档编号")
    document_status: str | None = Field(default=None, description="文档状态")
    publish_time: DateTimeStr | None = Field(default=None, description="发布时间")
    view_count: int | None = Field(default=None, description="阅读量")
    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class DocumentQuerySchema(BaseModel):
    """活动撰写查询参数模型"""

    def __init__(
        self,
        document_no: str | None = Query(None, description="文档编号"),
        document_title: str | None = Query(None, description="文档标题"),
        document_type: str | None = Query(None, description="文档类型"),
        activity_id: int | None = Query(None, description="关联活动ID"),
        author_id: int | None = Query(None, description="作者ID"),
        author_name: str | None = Query(None, description="作者姓名"),
        team_id: int | None = Query(None, description="招生组ID"),
        document_status: str | None = Query(None, description="文档状态"),
        is_top: bool | None = Query(None, description="是否置顶"),
        is_featured: bool | None = Query(None, description="是否推荐"),
        publish_time_begin: DateStr | None = Query(None, description="发布时间范围-开始"),
        publish_time_end: DateStr | None = Query(None, description="发布时间范围-结束"),
    ) -> None:
        from app.common.enums import QueueEnum

        if document_no:
            self.document_no = (QueueEnum.like.value, document_no)
        if document_title:
            self.document_title = (QueueEnum.like.value, document_title)
        if document_type:
            self.document_type = (QueueEnum.eq.value, document_type)
        if activity_id is not None:
            self.activity_id = (QueueEnum.eq.value, activity_id)
        if author_id is not None:
            self.author_id = (QueueEnum.eq.value, author_id)
        if author_name:
            self.author_name = (QueueEnum.like.value, author_name)
        if team_id is not None:
            self.team_id = (QueueEnum.eq.value, team_id)
        if document_status:
            self.document_status = (QueueEnum.eq.value, document_status)
        if is_top is not None:
            self.is_top = (QueueEnum.eq.value, is_top)
        if is_featured is not None:
            self.is_featured = (QueueEnum.eq.value, is_featured)
        if publish_time_begin and publish_time_end:
            self.publish_time = (QueueEnum.between.value, (publish_time_begin, publish_time_end))