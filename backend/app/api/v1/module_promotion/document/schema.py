"""
活动撰写 - 数据验证Schema
"""

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class DocumentCreateSchema(BaseModel):
    """新增活动撰写模型"""

    document_no: str | None = Field(default=None, description="文档编号")
    activity_id: int | None = Field(default=None, description="活动ID")
    activity_name: str | None = Field(default=None, description="活动名称")
    document_title: str | None = Field(default=None, description="文档标题")
    document_type: str | None = Field(default=None, description="文档类型")
    document_content: str | None = Field(default=None, description="文档内容")
    document_summary: str | None = Field(default=None, description="文档摘要")
    keywords: str | None = Field(default=None, description="关键词")
    cover_image: str | None = Field(default=None, description="封面图片")
    author_id: int | None = Field(default=None, description="作者ID")
    author_name: str | None = Field(default=None, description="作者姓名")
    team_id: int | None = Field(default=None, description="团队ID")
    team_name: str | None = Field(default=None, description="团队名称")
    document_status: str | None = Field(default=None, description="文档状态")
    publish_time: DateTimeStr | None = Field(default=None, description="发布时间")
    view_count: int | None = Field(default=None, description="浏览次数")
    is_top: int | None = Field(default=None, description="是否置顶")
    is_featured: int | None = Field(default=None, description="是否精选")
    attachment_urls: str | None = Field(default=None, description="附件URLs")
    attachment_names: str | None = Field(default=None, description="附件名称")
    remark: str | None = Field(default=None, description="备注")
    display_order: int | None = Field(default=None, description="显示排序")


class DocumentUpdateSchema(DocumentCreateSchema):
    """更新活动撰写模型"""

    pass


class DocumentOutSchema(DocumentCreateSchema, BaseSchema, UserBySchema):
    """活动撰写响应模型"""

    model_config = ConfigDict(from_attributes=True)

    created_by_name: str | None = Field(default=None, description="创建人")
    updated_by_name: str | None = Field(default=None, description="更新人")


class DocumentQuerySchema(BaseModel):
    """活动撰写查询参数模型"""

    def __init__(
        self,
        document_no: str | None = Query(None, description="文档编号"),
        document_type: str | None = Query(None, description="文档类型"),
        author_name: str | None = Query(None, description="作者姓名"),
        document_status: str | None = Query(None, description="文档状态"),
    ) -> None:
        from app.common.enums import QueueEnum

        if document_no:
            self.document_no = (QueueEnum.like.value, document_no)
        if document_type:
            self.document_type = (QueueEnum.eq.value, document_type)
        if author_name:
            self.author_name = (QueueEnum.like.value, author_name)
        if document_status:
            self.document_status = (QueueEnum.eq.value, document_status)
