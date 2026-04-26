"""
组织架构管理 - 服务层
"""

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import TeamCRUD
from .model import PromotionTeamModel
from .schema import (
    TeamOutSchema,
    TeamQuerySchema,
)


class TeamService:
    """
    招生组管理服务层
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
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的招生组模型实例字典
        """
        if data.get("team_code"):
            existing = await TeamCRUD(auth).get_by_team_code_crud(data["team_code"])
            if existing:
                raise CustomException(msg="招生组编码已存在")

        if data.get("parent_id"):
            parent = await TeamCRUD(auth).get_by_id_crud(data["parent_id"])
            if not parent:
                raise CustomException(msg="上级招生组不存在")
            data["level_depth"] = parent.level_depth + 1
            data["level_path"] = f"{parent.level_path}{parent.id}/" if parent.level_path else f"/{parent.id}/"
        else:
            data["level_depth"] = 1
            data["level_path"] = "/"

        obj = await TeamCRUD(auth).create_crud(data=data)
        log.info(f"创建招生组成功: {obj.id}")
        return TeamOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生组ID
        - data (dict): 更新数据

        返回:
        - dict: 更新的招生组模型实例字典
        """
        existing = await TeamCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生组不存在")

        if data.get("team_code") and data["team_code"] != existing.team_code:
            code_existing = await TeamCRUD(auth).get_by_team_code_crud(data["team_code"])
            if code_existing:
                raise CustomException(msg="招生组编码已存在")

        if data.get("parent_id"):
            if data["parent_id"] == id:
                raise CustomException(msg="不能将自己设为上级招生组")
            parent = await TeamCRUD(auth).get_by_id_crud(data["parent_id"])
            if not parent:
                raise CustomException(msg="上级招生组不存在")
            data["level_depth"] = parent.level_depth + 1
            data["level_path"] = f"{parent.level_path}{parent.id}/" if parent.level_path else f"/{parent.id}/"

        obj = await TeamCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新招生组成功: {id}")
        return TeamOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生组ID
        """
        existing = await TeamCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生组不存在")

        children = await TeamCRUD(auth).get_children_crud(id)
        if children:
            raise CustomException(msg="该招生组存在下级组织，无法删除")

        await TeamCRUD(auth).delete_crud(id=id)
        log.info(f"删除招生组成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除招生组

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 招生组ID列表
        """
        for team_id in ids:
            children = await TeamCRUD(auth).get_children_crud(team_id)
            if children:
                raise CustomException(msg=f"招生组ID {team_id} 存在下级组织，无法删除")

        await TeamCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除招生组成功: {ids}")

    @classmethod
    async def tree_service(cls, auth: AuthSchema) -> list[dict]:
        """
        获取招生组树形结构

        参数:
        - auth (AuthSchema): 认证信息模型

       返回:
        - list[dict]: 树形结构的招生组列表
        """
        root_teams = await TeamCRUD(auth).get_root_teams_crud()
        result = []
        for root in root_teams:
            tree_node = await cls._build_tree(auth, root)
            result.append(tree_node)
        return result

    @classmethod
    async def _build_tree(cls, auth: AuthSchema, team: PromotionTeamModel) -> dict:
        """递归构建树形结构"""
        children = await TeamCRUD(auth).get_children_crud(team.id)
        children_list = []
        for child in children:
            child_node = await cls._build_tree(auth, child)
            children_list.append(child_node)

        return {
            "id": team.id,
            "name": team.name,
            "parent_id": team.parent_id,
            "level": team.level,
            "leader_id": team.leader_id,
            "responsible_area": team.responsible_area,
            "status": team.status,
            "children": children_list,
        }

    @classmethod
    async def set_status_service(cls, auth: AuthSchema, id: int, status: str) -> dict:
        """
        设置招生组状态

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 招生组ID
        - status (str): 状态

        返回:
        - dict: 更新后的招生组模型实例字典
        """
        existing = await TeamCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该招生组不存在")

        obj = await TeamCRUD(auth).update_crud(id=id, data={"status": status})
        log.info(f"设置招生组状态成功: {id}, status={status}")
        return TeamOutSchema.model_validate(obj).model_dump()
