from collections.abc import Sequence

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase
from app.core.exceptions import CustomException

from .model import ChatSessionModel
from .schema import (
    ChatSessionCreateSchema,
    ChatSessionOutSchema,
    ChatSessionUpdateSchema,
)


class ChatSessionCRUD(CRUDBase[ChatSessionModel, ChatSessionCreateSchema, ChatSessionUpdateSchema]):
    """聊天会话数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=ChatSessionModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: list[str] | None = None) -> ChatSessionModel | None:
        """
        详情

        参数:
        - id (int): 会话ID
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项

        返回:
        - ChatSessionModel | None: 会话模型实例或None
        """
        return await self.get(id=id, preload=preload)

    async def list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict] | None = None,
        preload: list[str] | None = None,
    ) -> Sequence[ChatSessionModel]:
        """
        列表查询

        参数:
        - search (dict | None): 查询参数
        - order_by (list[dict] | None): 排序参数
        - preload (list[str] | None): 预加载关系，未提供时使用模型默认项

        返回:
        - Sequence[ChatSessionModel]: 会话模型实例序列
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def create_crud(self, data: ChatSessionCreateSchema) -> ChatSessionModel:
        """
        创建

        参数:
        - data (ChatSessionCreateSchema): 会话创建模型

        返回:
        - ChatSessionModel: 会话模型实例
        """
        return await self.create(data=data)

    async def update_crud(self, id: int, data: ChatSessionUpdateSchema) -> ChatSessionModel:
        """
        更新

        参数:
        - id (int): 会话ID
        - data (ChatSessionUpdateSchema): 会话更新模型

        返回:
        - ChatSessionModel: 会话模型实例
        """
        obj = await self.get(id=id, preload=[])
        if not obj:
            raise CustomException(msg="更新对象不存在")

        obj_dict = data.model_dump(exclude_unset=True) if not isinstance(data, dict) else data

        if self.auth.user and hasattr(obj, "updated_id"):
            setattr(obj, "updated_id", self.auth.user.id)

        for key, value in obj_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        await self.auth.db.flush()
        await self.auth.db.refresh(obj)
        return obj

    async def delete_crud(self, ids: list[int]) -> None:
        """
        批量删除

        参数:
        - ids (list[int]): 会话ID列表

        返回:
        - None
        """
        from sqlalchemy import delete

        if not ids:
            raise CustomException(msg="删除失败，删除对象不能为空")

        sql = delete(self.model).where(self.model.id.in_(ids))
        await self.auth.db.execute(sql)
        await self.auth.db.flush()

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict] | None = None,
        search: dict | None = None,
        preload: list | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (list[dict] | None): 排序参数
        - search (dict | None): 查询参数
        - preload (list | None): 预加载关系，未提供时使用模型默认项

        返回:
        - dict: 分页数据
        """
        order_by_list = order_by or [{"id": "desc"}]
        search_dict = search or {}

        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by_list,
            search=search_dict,
            out_schema=ChatSessionOutSchema,
            preload=preload,
        )
