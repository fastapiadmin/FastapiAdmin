# -*- coding: utf-8 -*-

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.common_util import (
    get_parent_id_map,
    get_parent_recursion,
    get_child_id_map,
    get_child_recursion,
    traversal_to_tree
)

from ..auth.schema import AuthSchema
from .crud import MenuCRUD
from .schema import (
    MenuCreateSchema,
    MenuUpdateSchema,
    MenuOutSchema,
    MenuQueryParam
)


class MenuService:
    """
    菜单模块服务层
    """

    @classmethod
    async def get_menu_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取菜单详情。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - id (int): 菜单ID。
        
        返回:
        - dict: 菜单详情对象。
        """
        menu = await MenuCRUD(auth).get_by_id_crud(id=id)
        # 创建实例后再设置parent_name属性
        menu_out = MenuOutSchema.model_validate(menu)
        if menu and menu.parent_id:
            parent = await MenuCRUD(auth).get_by_id_crud(id=menu.parent_id)
            if parent:
                menu_out.parent_name = parent.name
        
        return menu_out.model_dump()

    @classmethod
    async def get_menu_tree_service(cls, auth: AuthSchema, search: MenuQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """
        获取菜单树形列表。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - search (MenuQueryParam | None): 查询参数对象。
        - order_by (list[dict] | None): 排序参数列表。
        
        返回:
        - list[dict]: 菜单树形列表对象。
        """
        # 使用树形结构查询，预加载children关系
        menu_list = await MenuCRUD(auth).get_tree_list_crud(search=search.__dict__, order_by=order_by)
        # 转换为字典列表
        menu_dict_list = [MenuOutSchema.model_validate(menu).model_dump() for menu in menu_list]
        # 使用traversal_to_tree构建树形结构
        return traversal_to_tree(menu_dict_list)

    @classmethod
    async def create_menu_service(cls, auth: AuthSchema, data: MenuCreateSchema) -> dict:
        """
        创建菜单。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - data (MenuCreateSchema): 创建参数对象。
        
        返回:
        - dict: 创建的菜单对象。
        """
        menu = await MenuCRUD(auth).get(name=data.name)
        if menu:
            raise CustomException(msg='创建失败，该菜单已存在')

        new_menu = await MenuCRUD(auth).create(data=data)
        new_menu_dict = MenuOutSchema.model_validate(new_menu).model_dump()
        return new_menu_dict

    @classmethod
    async def update_menu_service(cls, auth: AuthSchema,id:int, data: MenuUpdateSchema) -> dict:
        """
        更新菜单。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - id (int): 菜单ID。
        - data (MenuUpdateSchema): 更新参数对象。
        
        返回:
        - dict: 更新的菜单对象。
        """
        menu = await MenuCRUD(auth).get_by_id_crud(id=id)
        if not menu:
            raise CustomException(msg='更新失败，该菜单不存在')
        exist_menu = await MenuCRUD(auth).get(name=data.name)
        if exist_menu and exist_menu.id != id:
            raise CustomException(msg='更新失败，菜单名称重复')
        
        if data.parent_id:
            parent_menu = await MenuCRUD(auth).get_by_id_crud(id=data.parent_id)
            if not parent_menu:
                raise CustomException(msg='更新失败，父级菜单不存在')
            data.parent_name = parent_menu.name
        new_menu = await MenuCRUD(auth).update(id=id, data=data)
        
        await cls.set_menu_available_service(auth=auth, data=BatchSetAvailable(ids=[id], status=data.status))
        
        new_menu_dict = MenuOutSchema.model_validate(new_menu).model_dump()
        return new_menu_dict
    
    @classmethod
    async def delete_menu_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除菜单。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - ids (list[int]): 菜单ID列表。
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            menu = await MenuCRUD(auth).get_by_id_crud(id=id)
            if not menu:
                raise CustomException(msg='删除失败，该菜单不存在')
        # 校验是否存在子级菜单，存在则禁止删除
        menu_list = await MenuCRUD(auth).get_list_crud()
        id_map = get_child_id_map(model_list=menu_list)
        for id in ids:
            descendants = get_child_recursion(id=id, id_map=id_map)
            if len(descendants) > 1:
                raise CustomException(msg='删除失败，存在子级菜单，请先删除子级菜单')
        await MenuCRUD(auth).delete(ids=ids)

    @classmethod
    async def set_menu_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        递归获取所有父、子级菜单，然后批量修改菜单可用状态。
        
        参数:
        - auth (AuthSchema): 认证对象。
        - data (BatchSetAvailable): 批量设置可用参数对象。
        
        返回:
        - None
        """
        menu_list = await MenuCRUD(auth).get_list_crud()
        total_ids = []
        
        if data.status:
            # 激活，则需要把所有父级菜单都激活
            id_map = get_parent_id_map(model_list=menu_list)
            for menu_id in data.ids:
                enable_ids = get_parent_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            # 禁止，则需要把所有子级菜单都禁止
            id_map = get_child_id_map(model_list=menu_list)
            for menu_id in data.ids:
                disable_ids = get_child_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await MenuCRUD(auth).set_available_crud(ids=total_ids, status=data.status)