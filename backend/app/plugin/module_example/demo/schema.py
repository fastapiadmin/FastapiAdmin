from dataclasses import dataclass

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.core.base_schema import BaseSchema, UserBySchema
from app.core.validator import DateStr, DateTimeStr, TimeStr


class DemoCreateSchema(BaseModel):
    """新增模型"""

    name: str = Field(..., description="名称")
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, description="描述")
    a: int | None = Field(default=None, description="整数")
    b: int | None = Field(default=None, description="大整数")
    c: float | None = Field(default=None, description="浮点数")
    d: bool = Field(default=True, description="布尔型")
    e: DateStr | None = Field(default=None, description="日期")
    f: TimeStr | None = Field(default=None, description="时间")
    g: DateTimeStr | None = Field(default=None, description="日期时间")
    h: str | None = Field(default=None, description="长文本")
    i: dict | None = Field(default=None, description="元数据(JSON格式)")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证名称字段的格式和内容"""
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
        if self.status not in ["0", "1"]:
            raise ValueError("是否启用必须为0或1")
        # 描述校验：描述最大长度
        if self.description and len(self.description) > 255:
            raise ValueError("描述长度不能超过255个字符")
        return self


class DemoUpdateSchema(DemoCreateSchema):
    """更新模型"""


class DemoOutSchema(DemoCreateSchema, BaseSchema, UserBySchema):
    """响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class DemoQueryParam:
    """示例查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        description: str | None = Query(None, description="描述"),
        status: str | None = Query(None, description="是否启用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:
        # 模糊查询字段
        self.name = ("like", name)
        if description:
            self.description = ("like", description)

        # 精确查询字段
        if status:
            self.status = ("eq", status)

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))

        # 关联查询字段
        if created_id:
            self.created_id = ("eq", created_id)
        if updated_id:
            self.updated_id = ("eq", updated_id)
