from typing import Any

from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.dependencies import require_superadmin
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
    MenuTreeOutSchema,
    MenuUpdateSchema,
)


class MenuService:
    """菜单管理服务（查询操作租户可见，写操作仅超级管理员可操作）"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def _validate_parent_child_type(self, parent_id: int | None, child_type: int) -> None:
        if parent_id is None:
            if child_type is None:
                return
            if child_type not in (1, 2, 4):
                raise CustomException(msg="顶级菜单仅允许目录、菜单或外链类型")
            return
        parent = await MenuCRUD(self.auth).get(id=parent_id)
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

    async def _validate_parent_child_client(self, parent_id: int | None, client: str) -> None:
        if parent_id is None or client is None:
            return
        parent = await MenuCRUD(self.auth).get(id=parent_id)
        if not parent:
            return
        p_client = getattr(parent, "client", None) or "pc"
        if p_client != client:
            raise CustomException(msg="子菜单终端须与父菜单一致（均为 pc 或均为 app）")

    async def detail(self, id: int) -> MenuOutSchema:
        menu = await MenuCRUD(self.auth).get(id=id, preload=["roles"])
        if not menu:
            raise CustomException(msg="菜单不存在")
        menu_out = MenuOutSchema.model_validate(menu)
        if menu.parent_id:
            parent = await MenuCRUD(self.auth).get(id=menu.parent_id)
            if parent:
                menu_out.parent_name = parent.name
        return menu_out

    async def tree(
        self,
        search: MenuQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
        menu_list = await MenuCRUD(self.auth).tree_list(search=vars(search) if search else None, order_by=order_by)
        menu_dict_list = [MenuTreeOutSchema.model_validate(menu).model_dump() for menu in menu_list]
        return traversal_to_tree(menu_dict_list)

    @require_superadmin
    async def create(self, data: MenuCreateSchema) -> MenuOutSchema:
        search: dict[str, Any] = {}
        if data.title is not None:
            search["title"] = data.title
            if data.parent_id is not None:
                search["parent_id"] = data.parent_id
            menu = await MenuCRUD(self.auth).get(**search)
            if menu:
                raise CustomException(msg="创建失败，该菜单已存在")

        await self._validate_parent_child_type(data.parent_id, data.type)
        await self._validate_parent_child_client(data.parent_id, data.client)

        new_menu = await MenuCRUD(self.auth).create(data=data)
        return MenuOutSchema.model_validate(new_menu)

    @require_superadmin
    async def update(self, id: int, data: MenuUpdateSchema) -> MenuOutSchema:
        _ = await MenuCRUD(self.auth).get_or_404(id=id, msg="更新失败，该菜单不存在")
        await self._validate_parent_child_type(data.parent_id, data.type)
        await self._validate_parent_child_client(data.parent_id, data.client)
        if data.title is not None:
            search: dict[str, Any] = {"title": data.title}
            if data.parent_id is not None:
                search["parent_id"] = data.parent_id
            exist_menu = await MenuCRUD(self.auth).get(**search)
            if exist_menu and exist_menu.id != id:
                raise CustomException(msg="更新失败，菜单标题重复")

        if data.parent_id:
            parent_menu = await MenuCRUD(self.auth).get(id=data.parent_id)
            if not parent_menu:
                raise CustomException(msg="更新失败，父级菜单不存在")

        new_menu = await MenuCRUD(self.auth).update(id=id, data=data)

        if data.status is not None:
            await self.set_available(data=BatchSetAvailable(ids=[id], status=data.status))

        menu_out = MenuOutSchema.model_validate(new_menu)
        if menu_out.parent_id:
            parent = await MenuCRUD(self.auth).get(id=menu_out.parent_id)
            if parent:
                menu_out.parent_name = parent.name
        return menu_out

    @require_superadmin
    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        all_menus = await MenuCRUD(self.auth).get_list()
        child_id_map = get_child_id_map(model_list=all_menus)

        delete_ids_set = set()
        for mid in ids:
            all_descendants = get_child_recursion(id=mid, id_map=child_id_map)
            delete_ids_set.update(all_descendants)

        delete_ids = list(delete_ids_set)
        await MenuCRUD(self.auth).delete(ids=delete_ids)

    @require_superadmin
    async def set_available(self, data: BatchSetAvailable) -> None:
        menu_list = await MenuCRUD(self.auth).get_list()
        total_ids = []

        if data.status == 0:
            id_map = get_parent_id_map(model_list=menu_list)
            for menu_id in data.ids:
                enable_ids = get_parent_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            id_map = get_child_id_map(model_list=menu_list)
            for menu_id in data.ids:
                disable_ids = get_child_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await MenuCRUD(self.auth).set(ids=total_ids, status=data.status)
