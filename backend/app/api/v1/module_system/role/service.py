from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil

from .crud import RoleCRUD
from .schema import (
    RoleCreateSchema,
    RoleOutSchema,
    RolePermissionSettingSchema,
    RoleQueryParam,
    RoleUpdateSchema,
)


class RoleService:
    """角色模块服务层"""

    @classmethod
    async def get_role_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取角色详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 角色ID

        返回:
        - dict: 角色详情字典
        """
        role = await RoleCRUD(auth).get_by_id_crud(id=id)
        return RoleOutSchema.model_validate(role).model_dump()

    @classmethod
    async def get_role_list_service(
        cls,
        auth: AuthSchema,
        search: RoleQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        获取角色列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (RoleQueryParam | None): 查询参数模型
        - order_by (list[dict[str, str]] | None): 排序参数列表

        返回:
        - list[dict]: 角色详情字典列表
        """
        role_list = await RoleCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [RoleOutSchema.model_validate(role).model_dump() for role in role_list]

    @classmethod
    async def create_role_service(cls, auth: AuthSchema, data: RoleCreateSchema) -> dict:
        """
        创建角色

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (RoleCreateSchema): 创建角色模型

        返回:
        - dict: 新创建的角色详情字典
        """
        role = await RoleCRUD(auth).get(name=data.name)
        if role:
            raise CustomException(msg="创建失败，该角色已存在")
        obj = await RoleCRUD(auth).get(code=data.code)
        if obj:
            raise CustomException(msg="创建失败，编码已存在")
        new_role = await RoleCRUD(auth).create(data=data)
        return RoleOutSchema.model_validate(new_role).model_dump()

    @classmethod
    async def update_role_service(cls, auth: AuthSchema, id: int, data: RoleUpdateSchema) -> dict:
        """
        更新角色

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 角色ID
        - data (RoleUpdateSchema): 更新角色模型

        返回:
        - dict: 更新后的角色详情字典
        """
        role = await RoleCRUD(auth).get_by_id_crud(id=id)
        if not role:
            raise CustomException(msg="更新失败，该角色不存在")
        exist_role = await RoleCRUD(auth).get(name=data.name)
        if exist_role and exist_role.id != id:
            raise CustomException(msg="更新失败，角色名称重复")
        updated_role = await RoleCRUD(auth).update(id=id, data=data)
        return RoleOutSchema.model_validate(updated_role).model_dump()

    @classmethod
    async def delete_role_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除角色

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 角色ID列表

        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")
        for id in ids:
            role = await RoleCRUD(auth).get_by_id_crud(id=id)
            if not role:
                raise CustomException(msg="删除失败，该角色不存在")
        await RoleCRUD(auth).delete(ids=ids)

    @classmethod
    async def set_role_permission_service(
        cls, auth: AuthSchema, data: RolePermissionSettingSchema
    ) -> None:
        """
        设置角色权限

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (RolePermissionSettingSchema): 角色权限设置模型

        返回:
        - None
        """
        # 设置角色菜单权限
        await RoleCRUD(auth).set_role_menus_crud(role_ids=data.role_ids, menu_ids=data.menu_ids)

        # 设置数据权限范围
        await RoleCRUD(auth).set_role_data_scope_crud(
            role_ids=data.role_ids, data_scope=data.data_scope
        )

        # 设置自定义数据权限部门
        if data.data_scope == 5 and data.dept_ids:
            await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=data.dept_ids)
        else:
            await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=[])

    @classmethod
    async def set_role_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        设置角色可用状态

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量设置可用状态模型

        返回:
        - None
        """
        await RoleCRUD(auth).set_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def export_role_list_service(cls, role_list: list[dict[str, Any]]) -> bytes:
        """
        导出角色列表

        参数:
        - role_list (list[dict[str, Any]]): 角色详情字典列表

        返回:
        - bytes: Excel文件字节流
        """
        # 字段映射配置
        mapping_dict = {
            "id": "角色编号",
            "name": "角色名称",
            "order": "显示顺序",
            "data_scope": "数据权限",
            "status": "状态",
            "description": "备注",
            "created_time": "创建时间",
            "updated_time": "更新时间",
            "created_id": "创建者ID",
            "updated_id": "更新者ID",
        }

        # 数据权限映射
        data_scope_map = {
            1: "仅本人数据权限",
            2: "本部门数据权限",
            3: "本部门及以下数据权限",
            4: "全部数据权限",
            5: "自定义数据权限",
        }

        # 处理数据
        data = role_list.copy()
        for item in data:
            item["status"] = "启用" if item.get("status") == "0" else "停用"
            item["data_scope"] = data_scope_map.get(item.get("data_scope", 1), "")
            item["creator"] = (
                item.get("creator", {}).get("name", "未知")
                if isinstance(item.get("creator"), dict)
                else "未知"
            )

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)
