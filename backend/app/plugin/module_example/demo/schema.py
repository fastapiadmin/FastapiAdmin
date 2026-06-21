from dataclasses import dataclass

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.common.enums import QueueEnum
from app.core.base_params import BaseQueryParam, TenantByQueryParam, UserByQueryParam
from app.core.base_schema import BaseSchema, TenantBySchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr, TimeStr


class DemoCreateSchema(BaseModel):
    """新增模型"""

    name: str = Field(..., description="名称")
    status: int = Field(default=0, ge=0, le=1, description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, description="描述")
    int_val: int | None = Field(default=None, description="整数")
    bigint_val: int | None = Field(default=None, description="大整数")
    float_val: float | None = Field(default=None, description="浮点数")
    bool_val: bool = Field(default=True, description="布尔型")
    date_val: DateStr | None = Field(default=None, description="日期")
    time_val: TimeStr | None = Field(default=None, description="时间")
    datetime_val: DateTimeStr | None = Field(default=None, description="日期时间")
    text_val: str | None = Field(default=None, description="长文本")
    json_val: dict | None = Field(default=None, description="元数据(JSON格式)")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        验证名称字段的格式和内容。

        参数:
        - v (str): 原始名称。

        返回:
        - str: 去空白后的名称。

        异常:
        - ValueError: 名称为空时抛出。
        """
        # 去除首尾空格
        v = v.strip()
        if not v:
            raise ValueError("名称不能为空")
        return v

    @model_validator(mode="after")
    def _after_validation(self):
        """
        核心业务规则校验
        """
        # 长度校验：名称最小长度
        if len(self.name) < 2 or len(self.name) > 50:
            raise ValueError("名称长度必须在2-50个字符之间")
        # 格式校验：名称只能包含字母、数字、下划线和中划线
        if not self.name.isalnum() and not all(c in "-_" for c in self.name):
            raise ValueError("名称只能包含字母、数字、下划线和中划线")
        if self.status not in [0, 1]:
            raise ValueError("是否启用必须为0或1")
        # 描述校验：描述最大长度
        if self.description and len(self.description) > 255:
            raise ValueError("描述长度不能超过255个字符")
        return self


class DemoUpdateSchema(DemoCreateSchema):
    """更新模型"""


class DemoOutSchema(DemoCreateSchema, BaseSchema, UserBySchema, TenantBySchema):
    """响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class DemoQueryParam(BaseQueryParam, UserByQueryParam, TenantByQueryParam):
    """示例查询参数（演示 Mixin 继承用法）"""

    name: str | None = Query(None, description="名称")
    description: str | None = Query(None, description="描述")
    status: str | None = Query(None, description="是否启用")

    def __post_init__(self) -> None:
        if self.name:
            self.name = (QueueEnum.like.value, self.name)
        if self.description:
            self.description = (QueueEnum.like.value, self.description)
        if self.status:
            self.status = (QueueEnum.eq.value, self.status)
