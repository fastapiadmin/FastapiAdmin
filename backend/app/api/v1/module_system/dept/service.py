
from app.core.base_schema import AuthSchema, BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.common_util import (
    get_child_id_map,
    get_child_recursion,
    get_parent_id_map,
    get_parent_recursion,
)

from .crud import DeptCRUD
from .schema import (
    DeptCreateSchema,
    DeptOutSchema,
    DeptQueryParam,
    DeptTreeOutSchema,
    DeptUpdateSchema,
)


class DeptService:
    """
    部门管理服务

    提供部门 CRUD、树形结构查询、级联启/禁用、租户配额检查等业务能力。
    """

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth

    async def detail(self, id: int) -> DeptOutSchema:
        dept = await DeptCRUD(self.auth).get_or_404(id=id)
        dept_out = DeptOutSchema.model_validate(dept)
        if dept.parent_id:
            parent = await DeptCRUD(self.auth).get(id=dept.parent_id)
            if parent:
                dept_out.parent_name = parent.name
        return dept_out

    async def tree(
        self,
        search: DeptQueryParam | None = None,
        order_by: list[dict] | None = None,
    ) -> list[dict]:
        dept_list = await DeptCRUD(self.auth).tree_list(search=vars(search) if search else None, order_by=order_by)
        dept_dict_list = [DeptTreeOutSchema.model_validate(dept).model_dump() for dept in dept_list]
        return [d for d in dept_dict_list if d.get("parent_id") is None]

    async def create(self, data: DeptCreateSchema) -> DeptOutSchema:
        dept = await DeptCRUD(self.auth).get(name=data.name)
        if dept:
            raise CustomException(msg="创建失败，该数据已存在")
        obj = await DeptCRUD(self.auth).get(code=data.code)
        if obj:
            raise CustomException(msg="创建失败，编码已存在")

        # 检查租户配额
        from app.api.v1.module_platform.tenant.service import TenantService

        await TenantService(self.auth).check_quota(self.auth.tenant_id, "dept")

        dept = await DeptCRUD(self.auth).create(data=data)
        return DeptOutSchema.model_validate(dept)

    async def update(self, id: int, data: DeptUpdateSchema) -> DeptOutSchema:
        dept = await DeptCRUD(self.auth).get_or_404(id=id, msg="更新失败，该数据不存在")
        exist_dept = await DeptCRUD(self.auth).get(name=data.name)
        if exist_dept and exist_dept.id != id:
            raise CustomException(msg="更新失败，名称已存在")
        exist_code = await DeptCRUD(self.auth).get(code=data.code)
        if exist_code and exist_code.id != id:
            raise CustomException(msg="更新失败，编码已存在")

        dept = await DeptCRUD(self.auth).update(id=id, data=data)
        dept_out = DeptOutSchema.model_validate(dept)
        if dept_out.parent_id:
            parent = await DeptCRUD(self.auth).get(id=dept_out.parent_id)
            if parent:
                dept_out.parent_name = parent.name
        return dept_out

    async def delete(self, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg="删除失败，删除对象不能为空")

        # 获取所有部门列表，用于构建树形关系
        all_depts = await DeptCRUD(self.auth).get_list()

        # 构建子部门ID映射
        child_id_map = get_child_id_map(model_list=all_depts)

        for pid in ids:
            if pid in child_id_map and child_id_map[pid]:
                raise CustomException(msg="存在子部门，不允许删除父部门")

        await DeptCRUD(self.auth).delete(ids=ids)

    async def batch_set_available(self, data: BatchSetAvailable) -> None:
        dept_list = await DeptCRUD(self.auth).get_list()
        total_ids = []

        if data.status == 0:
            id_map = get_parent_id_map(model_list=dept_list)
            for dept_id in data.ids:
                enable_ids = get_parent_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            id_map = get_child_id_map(model_list=dept_list)
            for dept_id in data.ids:
                disable_ids = get_child_recursion(id=dept_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await DeptCRUD(self.auth).set(ids=total_ids, status=data.status)
