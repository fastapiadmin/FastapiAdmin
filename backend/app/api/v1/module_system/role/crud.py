# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence, Optional, Union, Any

from app.core.base_crud import CRUDBase

from .model import RoleModel
from .schema import RoleCreateSchema, RoleUpdateSchema
from ..auth.schema import AuthSchema
from ..menu.crud import MenuCRUD
from ..dept.crud import DeptCRUD


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    """角色模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化角色模块数据层
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        self.auth = auth
        super().__init__(model=RoleModel, auth=auth)

    async def get_by_id_crud(self, id: int, preload: Optional[List[Union[str, Any]]] = None) -> Optional[RoleModel]:
        """
        根据id获取角色信息
        
        参数:
        - id (int): 角色ID
        - preload (Optional[List[Union[str, Any]]]): 预加载选项
        
        返回:
        - Optional[RoleModel]: 角色模型对象
        """
        return await self.get(id=id, preload=preload)

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[RoleModel]:
        """
        获取角色列表
        
        参数:
        - search (Optional[Dict]): 查询参数
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        - preload (Optional[List[Union[str, Any]]]): 预加载选项
        
        返回:
        - Sequence[RoleModel]: 角色模型对象列表
        """
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def set_role_menus_crud(self, role_ids: List[int], menu_ids: List[int]) -> None:
        """
        设置角色的菜单权限
        
        参数:
        - role_ids (List[int]): 角色ID列表
        - menu_ids (List[int]): 菜单ID列表

        返回:
        - None
        """
        roles = await self.list(search={"id": ("in", role_ids)})
        menus = await MenuCRUD(self.auth).get_list_crud(search={"id": ("in", menu_ids)})

        for obj in roles:
            relationship = obj.menus
            relationship.clear()
            relationship.extend(menus)
        await self.db.flush()

    async def set_role_data_scope_crud(self, role_ids: List[int], data_scope: int) -> None:
        """
        设置角色的数据范围
        
        参数:
        - role_ids (List[int]): 角色ID列表
        - data_scope (int): 数据范围
        
        返回:
        - None
        """
        await self.set(ids=role_ids, data_scope=data_scope)

    async def set_role_depts_crud(self, role_ids: List[int], dept_ids: List[int]) -> None:
        """
        设置角色的部门权限
        
        参数:
        - role_ids (List[int]): 角色ID列表
        - dept_ids (List[int]): 部门ID列表
        
        返回:
        - None
        """
        roles = await self.list(search={"id": ("in", role_ids)})
        depts = await DeptCRUD(self.auth).get_list_crud(search={"id": ("in", dept_ids)})

        for obj in roles:
            relationship = obj.depts
            relationship.clear()
            relationship.extend(depts)
        await self.db.flush()

    async def set_available_crud(self, ids: List[int], status: str) -> None:
        """
        设置角色的可用状态
        
        参数:
        - ids (List[int]): 角色ID列表
        - status (bool): 可用状态
        
        返回:
        - None
        """
        await self.set(ids=ids, status=status)