"""
组织架构管理 - 服务层
"""

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import TeamCRUD
from .schema import (
    TeamCreateSchema,
    TeamOutSchema,
    TeamQuerySchema,
    TeamUpdateSchema,
)


class TeamService:
    """
    招生组管理服务层

    职责：招生组的增删改查、树形结构构建、层级路径(level_path/level_depth)维护、状态切换
    约束：存在下级组织时禁止删除；不能将自己设为上级组织
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生组ID

        返回:
        - dict: 招生组模型实例字典
        """
        obj = await TeamCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该招生组不存在")
        return TeamOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: TeamQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (TeamQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 招生组模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await TeamCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [TeamOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: TeamQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (TeamQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await TeamCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: TeamCreateSchema) -> dict:
        """
        创建招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (TeamCreateSchema): 创建数据

        返回:
        - dict: 创建的招生组模型实例字典
        """
        data_dict = data.model_dump()
        extra_fields = ["team_name", "team_code", "team_level", "display_order", "remark"]
        for field in extra_fields:
            data_dict.pop(field, None)

        obj = await TeamCRUD(auth).create_crud(data=data_dict)
        log.info(f"创建招生组成功: {obj.id}")
        return TeamOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: TeamUpdateSchema) -> dict:
        """
        更新招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生组ID
        - data (TeamUpdateSchema): 更新数据

        返回:
        - dict: 更新的招生组模型实例字典
        """
        existing = await TeamCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生组不存在")

        if data.parent_id:
            if data.parent_id == id:
                raise CustomException(msg="不能将自己设为上级组织")
            parent = await TeamCRUD(auth).get_by_id_crud(data.parent_id)
            if not parent:
                raise CustomException(msg="上级招生组不存在")

        data_dict = data.model_dump()
        extra_fields = ["team_name", "team_code", "team_level", "display_order", "remark"]
        for field in extra_fields:
            data_dict.pop(field, None)
        obj = await TeamCRUD(auth).update_crud(id=id, data=data_dict)
        log.info(f"更新招生组成功: {obj.id}")
        return TeamOutSchema.model_validate(obj).model_dump()
