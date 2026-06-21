from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateTimeStr


class EmailConfigCreateSchema(BaseModel):
    """创建 SMTP 配置"""

    name: str | None = Field(default=None, max_length=100, description="配置名称")
    smtp_host: str | None = Field(default=None, max_length=255, description="SMTP 服务器地址")
    smtp_port: int | None = Field(default=None, ge=1, le=65535, description="SMTP 端口")
    smtp_user: str | None = Field(default=None, max_length=255, description="SMTP 登录用户名")
    smtp_password: str | None = Field(default=None, max_length=255, description="SMTP 授权密码")
    from_name: str | None = Field(default=None, max_length=100, description="发件人显示名")
    use_tls: bool | None = Field(default=None, description="是否启用 SSL/TLS")
    is_default: bool | None = Field(default=None, description="是否设为默认配置")
    timeout: int | None = Field(default=None, ge=5, le=120, description="连接超时（秒）")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="备注")


class EmailConfigUpdateSchema(EmailConfigCreateSchema):
    """更新 SMTP 配置"""


class EmailConfigOutSchema(EmailConfigCreateSchema, BaseSchema):
    """SMTP 配置响应（不含密码）"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class EmailConfigQueryParam(BaseQueryParam):
    """SMTP 配置查询参数"""

    name: str | None = Query(None, description="配置名称")
    status: int | None = Query(None, description="状态")
    is_default: bool | None = Query(None, description="是否默认配置")

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.status is not None:
            self.status = (QueueEnum.eq.value, self.status)
        if self.is_default is not None:
            self.is_default = (QueueEnum.eq.value, self.is_default)


class EmailTemplateCreateSchema(BaseModel):
    """创建邮件模板"""

    name: str | None = Field(default=None, max_length=100, description="模板名称")
    template_code: str | None = Field(default=None, max_length=100, description="模板编码")
    subject: str | None = Field(default=None, max_length=255, description="邮件主题")
    body_html: str | None = Field(default=None, description="邮件正文 HTML")
    body_text: str | None = Field(default=None, description="纯文本版本")
    variables: str | None = Field(default=None, description="变量说明 JSON")
    status: int = Field(default=0, ge=0, le=1, description="状态(0:启动 1:停用)")
    description: str | None = Field(default=None, max_length=255, description="备注")


class EmailTemplateUpdateSchema(EmailTemplateCreateSchema):
    """更新邮件模板"""


class EmailTemplateOutSchema(EmailTemplateCreateSchema, BaseSchema):
    """邮件模板响应"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class EmailTemplateQueryParam(BaseQueryParam):
    """邮件模板查询参数"""

    name: str | None = Query(None, description="模板名称")
    template_code: str | None = Query(None, description="模板编码")

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.template_code:
            self.template_code = (QueueEnum.like.value, self.template_code)


class EmailSendSchema(BaseModel):
    """手动发送邮件（测试用）"""

    to_email: str = Field(..., min_length=5, max_length=255, description="收件人邮箱")
    to_name: str | None = Field(default=None, max_length=100, description="收件人姓名")
    template_code: str = Field(..., min_length=1, max_length=100, description="模板编码")
    variables: dict = Field(default_factory=dict, description="模板变量 {key: value}")
    config_id: int | None = Field(default=None, gt=0, description="指定 SMTP 配置 ID")
    biz_type: str = Field(default="other", max_length=50, description="业务类型")


class EmailLogOutSchema(BaseSchema, UserBySchema):
    """邮件日志响应"""

    model_config = ConfigDict(from_attributes=True)

    config_id: int | None = Field(default=None, description="SMTP 配置 ID")
    template_code: str | None = Field(default=None, description="模板编码")
    to_email: str = Field(..., description="收件人邮箱")
    to_name: str | None = Field(default=None, description="收件人姓名")
    subject: str = Field(..., description="邮件主题")
    biz_type: str = Field(..., description="业务类型")
    error_msg: str | None = Field(default=None, description="错误信息")
    retry_count: int = Field(..., description="重试次数")
    sent_time: DateTimeStr | None = Field(default=None, description="发送时间")


@dataclass
class EmailLogQueryParam(BaseQueryParam, UserByQueryParam):
    """邮件日志查询参数"""

    to_email: str | None = Query(None, description="收件人邮箱")
    biz_type: str | None = Query(None, description="业务类型")
    status: int | None = Query(None, description="状态")
    template_code: str | None = Query(None, description="模板编码")

    def __post_init__(self) -> None:
        if self.to_email:
            self.to_email = (QueueEnum.like.value, self.to_email)
        if self.biz_type:
            self.biz_type = (QueueEnum.eq.value, self.biz_type)
        if self.status is not None:
            self.status = (QueueEnum.eq.value, self.status)
        if self.template_code:
            self.template_code = (QueueEnum.eq.value, self.template_code)


class EmailTestSchema(BaseModel):
    """测试 SMTP 连接"""

    config_id: int = Field(..., gt=0, description="SMTP 配置 ID")
    to_email: str = Field(..., min_length=5, max_length=255, description="测试收件人")
