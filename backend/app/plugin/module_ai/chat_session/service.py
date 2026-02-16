from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ChatSessionCRUD
from .model import ChatSessionModel
from .schema import (
    ChatSessionCreateSchema,
    ChatSessionOutSchema,
    ChatSessionQueryParam,
    ChatSessionUpdateSchema,
)


class ChatSessionService:
    """
    聊天会话管理模块服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (str): 会话ID

        返回:
        - dict: 会话模型实例字典
        """
        obj: ChatSessionModel | None = await ChatSessionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该会话不存在")
        result = ChatSessionOutSchema.model_validate(obj).model_dump()
        return result

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ChatSessionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (ChatSessionQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 会话模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await ChatSessionCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        result_list = [ChatSessionOutSchema.model_validate(obj).model_dump() for obj in obj_list]
        return result_list

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ChatSessionQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (ChatSessionQueryParam | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ChatSessionCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: ChatSessionCreateSchema) -> dict:
        """
        创建

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (ChatSessionCreateSchema): 会话创建模型

        返回:
        - dict: 会话模型实例字典
        """
        obj = await ChatSessionCRUD(auth).create_crud(data=data)
        result = ChatSessionOutSchema.model_validate(obj).model_dump()
        log.info(f"创建聊天会话成功: {result.get('title')}")
        return result

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: ChatSessionUpdateSchema) -> dict:
        """
        更新

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 会话ID
        - data (ChatSessionUpdateSchema): 会话更新模型

        返回:
        - dict: 会话模型实例字典
        """
        obj = await ChatSessionCRUD(auth).update_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，该会话不存在")
        result = ChatSessionOutSchema.model_validate(obj).model_dump()
        log.info(f"更新聊天会话成功: {result.get('title')}")
        return result

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 会话ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        for id in ids:
            obj = await ChatSessionCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，ID为{id}的会话不存在")

        await ChatSessionCRUD(auth).delete_crud(ids=ids)
        log.info(f"删除聊天会话成功: {ids}")
