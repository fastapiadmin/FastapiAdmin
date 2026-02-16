from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import QueueEnum
from app.core.base_schema import BaseSchema, UserBySchema


class NodeCreateSchema(BaseModel):
    """创建节点模型"""

    name: str = Field(..., description="节点类型名称", min_length=2, max_length=64)
    code: str = Field(..., description="节点类型编码", min_length=2, max_length=32)
    category: str = Field(default="action", description="节点分类(trigger/action/condition/control/integration/custom)")
    config_schema: dict = Field(default_factory=dict, description="配置表单Schema(JSON Schema)")
    input_schema: dict | None = Field(default=None, description="输入数据Schema")
    output_schema: dict | None = Field(default=None, description="输出数据Schema")
    handler: str = Field(default="", description="处理器路径(如: app.workflow.handlers.custom_handler)")
    meta_data: dict | None = Field(default=None, description="元数据")
    status: str = Field(default="0", description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, description="描述")


class NodeUpdateSchema(BaseModel):
    """更新节点模型"""

    name: str | None = Field(default=None, description="节点类型名称", min_length=2, max_length=64)
    code: str | None = Field(default=None, description="节点类型编码", min_length=2, max_length=32)
    category: str | None = Field(default=None, description="节点分类")
    config_schema: dict | None = Field(default=None, description="配置表单Schema")
    input_schema: dict | None = Field(default=None, description="输入数据Schema")
    output_schema: dict | None = Field(default=None, description="输出数据Schema")
    handler: str | None = Field(default=None, description="处理器路径")
    meta_data: dict | None = Field(default=None, description="元数据")
    status: str | None = Field(default=None, description="是否启用(0:启用 1:禁用)")
    description: str | None = Field(default=None, description="描述")


class NodeOutSchema(NodeCreateSchema, BaseSchema, UserBySchema):
    """节点响应模型"""

    model_config = ConfigDict(from_attributes=True)


@dataclass
class NodeQueryParam:
    """节点查询参数"""

    name: str | None = field(default=None, metadata={"description": "节点名称"})
    code: str | None = field(default=None, metadata={"description": "节点编码"})
    category: str | None = field(default=None, metadata={"description": "节点分类"})
    status: str | None = field(default=None, metadata={"description": "是否启用(0:启用 1:禁用)"})

    def to_search_dict(self) -> dict:
        """转换为搜索字典"""
        search_dict = {}
        if self.name:
            search_dict["name"] = (QueueEnum.like.value, self.name)
        if self.code:
            search_dict["code"] = (QueueEnum.like.value, self.code)
        if self.category:
            search_dict["category"] = (QueueEnum.eq.value, self.category)
        if self.status:
            search_dict["status"] = (QueueEnum.eq.value, self.status)
        return search_dict
