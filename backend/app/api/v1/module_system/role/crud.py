from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.dept.crud import DeptCRUD
from app.api.v1.module_system.menu.crud import MenuCRUD
from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException

from .model import RoleModel
from .schema import RoleCreateSchema, RoleUpdateSchema


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    """角色模块数据层"""

    def __init__(self, auth: AuthSchema, db: AsyncSession) -> None:
        super().__init__(model=RoleModel, auth=auth, db=db)

    async def set_role_menus_crud(self, role_ids: list[int], menu_ids: list[int]) -> None:
        """设置角色的菜单权限

        参数:
        - role_ids (list[int]): 角色ID列表
        - menu_ids (list[int]): 菜单ID列表

        返回:
        - None
        """
        if not role_ids:
            raise CustomException(msg="角色ID列表不能为空")

        roles = await self.get_list(search={"id": ("in", role_ids)}, preload=["menus"])
        if len(roles) != len(set(role_ids)):
            missing = sorted(set(role_ids) - {r.id for r in roles})
            raise CustomException(msg=f"角色不存在: {missing}")

        menus = [] if not menu_ids else await MenuCRUD(self.auth, self.db).get_list(search={"id": ("in", menu_ids)})

        if menu_ids and len(menus) != len(set(menu_ids)):
            missing = sorted(set(menu_ids) - {m.id for m in menus})
            raise CustomException(msg=f"菜单不存在: {missing}")

        for obj in roles:
            obj.menus.clear()
            obj.menus.extend(menus)
        await self.db.flush()

    async def set_role_depts_crud(self, role_ids: list[int], dept_ids: list[int]) -> None:
        """设置角色的部门权限（含存在性校验）"""
        if not role_ids:
            raise CustomException(msg="角色ID列表不能为空")

        roles = await self.get_list(search={"id": ("in", role_ids)}, preload=["depts"])
        if len(roles) != len(set(role_ids)):
            missing = sorted(set(role_ids) - {r.id for r in roles})
            raise CustomException(msg=f"角色不存在: {missing}")

        depts = [] if not dept_ids else await DeptCRUD(self.auth, self.db).get_list(search={"id": ("in", dept_ids)})
        if dept_ids and len(depts) != len(set(dept_ids)):
            missing = sorted(set(dept_ids) - {d.id for d in depts})
            raise CustomException(msg=f"部门不存在: {missing}")

        for obj in roles:
            relationship = obj.depts
            relationship.clear()
            relationship.extend(depts)
        await self.db.flush()

    async def get_options(self) -> list[dict[str, Any]]:
        """获取角色下拉选项，返回 [{value, label}]（自动按状态过滤）"""
        items = await self.get_list(search={"status": 0})
        return [{"value": item.id, "label": item.name} for item in items]
