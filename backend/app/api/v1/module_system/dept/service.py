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

from .crud import DeptCRUD
from .schema import (
    DeptCreateSchema,
    DeptOutSchema,
    DeptQueryParam,
    DeptUpdateSchema,
)


class DeptService:
    """
    部门管理模块服务层
    """

    @classmethod
    async def get_dept_detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        获取部门详情。

        参数:
        - auth (AuthSchema): 认证对象。
        - id (int): 部门 ID。

        返回:
        - dict: 部门详情对象。
        """
        dept = await DeptCRUD(auth).get_by_id_crud(id=id)
        result = DeptOutSchema.model_validate(dept).model_dump()
        if dept and dept.parent_id:
            parent = await DeptCRUD(auth).get(id=dept.parent_id)
            if parent:
                result["parent_name"] = parent.name
        return result

    @classmethod
    async def get_dept_tree_service(
        cls,
        auth: AuthSchema,
        search: DeptQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
        """
        获取部门树形列表。

        参数:
        - auth (AuthSchema): 认证对象。
        - search (DeptQueryParam | None): 查询参数对象。
        - order_by (list[dict] | None): 排序参数。

        返回:
        - list[dict]: 部门树形列表对象。
        """
        # 使用树形结构查询，预加载children关系
        dept_list = await DeptCRUD(auth).get_tree_list_crud(
            search=search.__dict__, order_by=order_by
        )
        # 转换为字典列表
        dept_dict_list = [DeptOutSchema.model_validate(dept).model_dump() for dept in dept_list]
        # 使用traversal_to_tree构建树形结构
        return traversal_to_tree(dept_dict_list)

    @classmethod
    async def create_dept_service(cls, auth: AuthSchema, data: DeptCreateSchema) -> dict:
        """
        创建部门。

        参数:
        - auth (AuthSchema): 认证对象。
        - data (DeptCreateSchema): 部门创建对象。

        返回:
        - dict: 新创建的部门对象。

        异常:
        - CustomException: 当部门已存在时抛出。
        """
        dept = await DeptCRUD(auth).get(name=data.name)
        if dept:
            raise CustomException(msg="创建失败，该部门已存在")
        obj = await DeptCRUD(auth).get(code=data.code)
        if obj:
            raise CustomException(msg="创建失败，编码已存在")
        dept = await DeptCRUD(auth).create(data=data)
        return DeptOutSchema.model_validate(dept).model_dump()

    @classmethod
    async def update_dept_service(cls, auth: AuthSchema, id: int, data: DeptUpdateSchema) -> dict:
        """
        更新部门。

        参数:
        - auth (AuthSchema): 认证对象。
        - id (int): 部门 ID。
        - data (DeptUpdateSchema): 部门更新对象。

        返回:
        - dict: 更新后的部门对象。

        异常:
        - CustomException: 当部门不存在或名称重复时抛出。
        """
        dept = await DeptCRUD(auth).get_by_id_crud(id=id)
        if not dept:
            raise CustomException(msg="更新失败，该部门不存在")
        exist_dept = await DeptCRUD(auth).get(name=data.name)
        if exist_dept and exist_dept.id != id:
            raise CustomException(msg="更新失败，部门名称重复")
        dept = await DeptCRUD(auth).update(id=id, data=data)
        return DeptOutSchema.model_validate(dept).model_dump()

    @classmethod
    async def delete_dept_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        删除部门。

        参数:
        - auth (AuthSchema): 认证对象。
        - ids (List[int]): 部门 ID 列表。

        返回:
        - None

        异常:
        - CustomException: 当删除对象为空时抛出。
        """
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        # 获取所有部门列表，用于构建树形关系
        all_depts = await DeptCRUD(auth).get_list_crud()

        # 构建子部门ID映射
        child_id_map = get_child_id_map(model_list=all_depts)

        # 收集所有需要删除的部门ID，包括直接指定的ID和它们的所有子部门ID
        delete_ids_set = set()

        for id in ids:
            # 递归获取该ID的所有子部门ID
            all_descendants = get_child_recursion(id=id, id_map=child_id_map)
            delete_ids_set.update(all_descendants)

        # 将集合转换为列表
        delete_ids = list(delete_ids_set)

        # 执行批量删除操作
        await DeptCRUD(auth).delete(ids=delete_ids)

    @classmethod
    async def batch_set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量设置部门可用状态。

        参数:
        - auth (AuthSchema): 认证对象。
        - data (BatchSetAvailable): 批量设置可用状态对象。

        返回:
        - None
        """
        dept_list = await DeptCRUD(auth).get_list_crud()
        total_ids = []

        if data.status == "0":
            id_map = get_parent_id_map(model_list=dept_list)
            for dept_id in data.ids:
                enable_ids = get_parent_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            id_map = get_child_id_map(model_list=dept_list)
            for dept_id in data.ids:
                disable_ids = get_child_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await DeptCRUD(auth).set_available_crud(ids=total_ids, status=data.status)
