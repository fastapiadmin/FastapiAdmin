from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ChatMessageCRUD
from .schema import (
    ChatMessageCreateSchema,
    ChatMessageOutSchema,
    ChatMessageQueryParam,
    ChatMessageUpdateSchema,
)


class ChatMessageService:
    """
    聊天消息管理模块服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 消息ID

        返回:
        - dict: 消息模型实例字典
        """
        obj = await ChatMessageCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该消息不存在")
        result = ChatMessageOutSchema.model_validate(obj).model_dump()
        return result

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ChatMessageQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (ChatMessageQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 消息模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await ChatMessageCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        result_list = [ChatMessageOutSchema.model_validate(obj).model_dump() for obj in obj_list]
        return result_list

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ChatMessageQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (ChatMessageQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ChatMessageCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def get_by_session_id_service(
        cls,
        auth: AuthSchema,
        session_id: int,
        page_no: int = 1,
        page_size: int = 50,
    ) -> dict:
        """
        按会话ID获取消息列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - session_id (int): 会话ID
        - page_no (int): 页码
        - page_size (int): 每页数量

        返回:
        - dict: 分页数据
        """
        offset = (page_no - 1) * page_size
        result = await ChatMessageCRUD(auth).get_by_session_id_crud(
            session_id=session_id,
            offset=offset,
            limit=page_size,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: ChatMessageCreateSchema) -> dict:
        """
        创建

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (ChatMessageCreateSchema): 消息创建模型

        返回:
        - dict: 消息模型实例字典
        """
        obj = await ChatMessageCRUD(auth).create_crud(data=data)
        result = ChatMessageOutSchema.model_validate(obj).model_dump()
        content = result.get('content')
        log.info(f"创建聊天消息成功: {content[:50] if content else ''}...")
        return result

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: ChatMessageUpdateSchema) -> dict:
        """
        更新

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 消息ID
        - data (ChatMessageUpdateSchema): 消息更新模型

        返回:
        - dict: 消息模型实例字典
        """
        obj = await ChatMessageCRUD(auth).update_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，该消息不存在")
        result = ChatMessageOutSchema.model_validate(obj).model_dump()
        content = result.get('content')
        log.info(f"更新聊天消息成功: {content[:50] if content else ''}...")
        return result

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 消息ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        for id in ids:
            obj = await ChatMessageCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，ID为{id}的消息不存在")

        await ChatMessageCRUD(auth).delete_crud(ids=ids)
        log.info(f"删除聊天消息成功: {ids}")
