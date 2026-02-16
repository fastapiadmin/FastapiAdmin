
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import NodeCRUD
from .schema import (
    NodeCreateSchema,
    NodeOutSchema,
    NodeUpdateSchema,
)


class NodeService:
    """节点管理模块服务层"""

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取节点类型详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 节点类型ID

        返回:
        - dict: 节点类型模型实例字典
        """
        obj = await NodeCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该节点不存在")
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: dict | None = None,
        order_by: list[dict] | None = None,
    ) -> dict:
        """
        分页查询节点类型

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (dict | None): 查询条件
        - order_by (list[dict] | None): 排序条件

        返回:
        - dict: 分页查询结果
        """
        offset = (page_no - 1) * page_size
        return await NodeCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by,
            search=search,
        )

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: NodeCreateSchema) -> dict:
        """
        创建节点类型

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (NodeCreateSchema): 节点类型创建模型

        返回:
        - dict: 节点类型模型实例字典
        """
        existing = await NodeCRUD(auth).get_by_code_crud(code=data.code)
        if existing:
            raise CustomException(msg=f"节点类型编码 {data.code} 已存在")

        obj = await NodeCRUD(auth).create_crud(data=data)
        if not obj:
            raise CustomException(msg="创建失败，节点类型创建失败")
        log.info(f"创建节点类型成功: {data.name}")
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: NodeUpdateSchema) -> dict:
        """
        更新节点类型

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 节点类型ID
        - data (NodeUpdateSchema): 节点类型更新模型

        返回:
        - dict: 节点类型模型实例字典
        """
        obj = await NodeCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="更新失败，该节点类型不存在")

        if data.code and data.code != obj.code:
            existing = await NodeCRUD(auth).get_by_code_crud(code=data.code)
            if existing:
                raise CustomException(msg=f"节点类型编码 {data.code} 已存在")

        obj = await NodeCRUD(auth).update_crud(id=id, data=data)
        if not obj:
            raise CustomException(msg="更新失败，节点类型更新失败")
        log.info(f"更新节点类型成功: {obj.name}")
        return NodeOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除节点类型

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 节点类型ID列表

        返回:
        - None
        """
        for id in ids:
            obj = await NodeCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f"删除失败，节点类型ID {id} 不存在")

        await NodeCRUD(auth).delete_crud(ids=ids)
        log.info(f"删除节点类型成功: {ids}")

    @classmethod
    async def list_service(cls, auth: AuthSchema) -> list[dict]:
        """
        获取节点类型列表

        参数:
        - auth (AuthSchema): 认证信息模型

        返回:
        - list[dict]: 节点类型模型实例字典列表
        """
        result = await NodeCRUD(auth).page_crud(
            offset=0,
            limit=1000,
            search={"status": ("eq", "0")},
            order_by=[{"updated_time": "desc"}],
        )
        return result.get("items", [])
