from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.common_util import (
    get_child_id_map,
    get_child_recursion,
    get_parent_id_map,
    get_parent_recursion,
    traversal_to_tree,
)

from .crud import MenuCRUD
from .schema import (
    MenuCreateSchema,
    MenuOutSchema,
    MenuQueryParam,
    MenuUpdateSchema,
)


class MenuService:
    """
    菜单模块服务层
    """

    @classmethod
    async def _validate_parent_child_type(
        cls, auth: AuthSchema, parent_id: int | None, child_type: int
    ) -> None:
        """
        父子类型约束：目录下仅允许目录/菜单/外链；菜单下仅允许按钮；按钮与外链下不可挂子级。
        无父级时仅允许目录、菜单、外链（与前端一致）。
        """
        if parent_id is None:
            if child_type not in (1, 2, 4):
                raise CustomException(msg="顶级菜单仅允许目录、菜单或外链类型")
            return
        parent = await MenuCRUD(auth).get_by_id_crud(id=parent_id)
        if not parent:
            raise CustomException(msg="父级菜单不存在")
        pt = parent.type
        if pt == 1:
            if child_type not in (1, 2, 4):
                raise CustomException(msg="目录下仅允许新增目录、菜单或外链")
        elif pt == 2:
            if child_type != 3:
                raise CustomException(msg="菜单下仅允许新增按钮")
        else:
            raise CustomException(msg="菜单或链接类型下不允许新增子菜单")

    @classmethod
    async def _validate_parent_child_client(
        cls, auth: AuthSchema, parent_id: int | None, client: str
    ) -> None:
        """子菜单终端须与父菜单一致。"""
        if parent_id is None:
            return
        parent = await MenuCRUD(auth).get_by_id_crud(id=parent_id)
        if not parent:
            return
        p_client = getattr(parent, "client", None) or "pc"
        if p_client != client:
            raise CustomException(msg="子菜单终端须与父菜单一致（均为 pc 或均为 app）")

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
    async def get_menu_tree_service(
        cls,
        auth: AuthSchema,
        search: MenuQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
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
        menu_list = await MenuCRUD(auth).get_tree_list_crud(
            search=search.__dict__, order_by=order_by
        )
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
        search: dict[str, Any] = {"title": data.title}
        if data.parent_id is not None:
            search["parent_id"] = data.parent_id
        menu = await MenuCRUD(auth).get(**search)
        if menu:
            raise CustomException(msg="创建失败，该菜单已存在")

        await cls._validate_parent_child_type(auth, data.parent_id, data.type)
        await cls._validate_parent_child_client(auth, data.parent_id, data.client)

        new_menu = await MenuCRUD(auth).create(data=data)
        new_menu_dict = MenuOutSchema.model_validate(new_menu).model_dump()
        return new_menu_dict

    @classmethod
    async def update_menu_service(cls, auth: AuthSchema, id: int, data: MenuUpdateSchema) -> dict:
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
            raise CustomException(msg="更新失败，该菜单不存在")
        await cls._validate_parent_child_type(auth, data.parent_id, data.type)
        await cls._validate_parent_child_client(auth, data.parent_id, data.client)
        search: dict[str, Any] = {"title": data.title}
        if data.parent_id is not None:
            search["parent_id"] = data.parent_id
        exist_menu = await MenuCRUD(auth).get(**search)
        if exist_menu and exist_menu.id != id:
            raise CustomException(msg="更新失败，菜单标题重复")

        if data.parent_id:
            parent_menu = await MenuCRUD(auth).get_by_id_crud(id=data.parent_id)
            if not parent_menu:
                raise CustomException(msg="更新失败，父级菜单不存在")
            data.parent_name = parent_menu.title
        new_menu = await MenuCRUD(auth).update(id=id, data=data)

        await cls.set_menu_available_service(
            auth=auth, data=BatchSetAvailable(ids=[id], status=data.status)
        )

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
            raise CustomException(msg="删除失败，删除对象不能为空")

        # 获取所有菜单列表，用于构建树形关系
        all_menus = await MenuCRUD(auth).get_list_crud()

        # 构建子菜单ID映射
        child_id_map = get_child_id_map(model_list=all_menus)

        # 收集所有需要删除的菜单ID，包括直接指定的ID和它们的所有子菜单ID
        delete_ids_set = set()

        for id in ids:
            # 递归获取该ID的所有子菜单ID
            all_descendants = get_child_recursion(id=id, id_map=child_id_map)
            delete_ids_set.update(all_descendants)

        # 将集合转换为列表
        delete_ids = list(delete_ids_set)

        # 执行批量删除操作
        await MenuCRUD(auth).delete(ids=delete_ids)

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

        if data.status == "0":
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
