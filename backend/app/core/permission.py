from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from app.core.base_schema import AuthSchema
from app.utils.common_util import get_child_id_map, get_child_recursion


class Permission:
    """为业务模型提供数据权限过滤功能"""

    # 数据权限常量定义，提高代码可读性
    DATA_SCOPE_SELF = 1  # 仅本人数据
    DATA_SCOPE_DEPT_AND_CHILD = 2  # 本部门及以下数据
    DATA_SCOPE_ALL = 3  # 全部数据

    def __init__(self, model: Any, auth: AuthSchema, db: AsyncSession) -> None:
        self.model = model
        self.auth = auth
        self.db = db

    async def filter_query(self, query: Any) -> Any:
        condition = await self._permission_condition()
        return query.where(condition) if condition is not None else query

    async def _permission_condition(self) -> ColumnElement | None:
        if not self.auth.user or not self.auth.user.id:
            return None

        if self.auth.user.is_superuser:
            return None

        return await self._filter_by_data_scope()

    async def _filter_by_data_scope(self) -> ColumnElement | None:
        from app.api.v1.module_system.role.model import RoleModel
        from app.api.v1.module_system.user.model import UserModel

        if not hasattr(self.model, "created_id"):
            return None

        stmt = select(RoleModel).join(
            RoleModel.users
        ).where(UserModel.id == self.auth.user.id)
        result = await self.db.execute(stmt)
        roles = result.scalars().all()

        if not roles:
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None and self.auth.user and self.auth.user.id:
                return created_id_attr == self.auth.user.id
            return None

        data_scopes = {role.data_scope for role in roles}

        if self.DATA_SCOPE_ALL in data_scopes:
            return None

        accessible_dept_ids = await self._get_accessible_dept_ids(data_scopes)

        if accessible_dept_ids:
            if self.model.__name__ == "UserModel" and hasattr(self.model, "dept_id"):
                dept_id_attr = getattr(self.model, "dept_id", None)
                if dept_id_attr is not None:
                    return dept_id_attr.in_(list(accessible_dept_ids))

            creator_rel = getattr(self.model, "created_by", None)
            if creator_rel is not None and hasattr(UserModel, "dept_id"):
                return creator_rel.has(UserModel.dept_id.in_(list(accessible_dept_ids)))

            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None and self.auth.user and self.auth.user.id:
                return created_id_attr == self.auth.user.id
            return None

        if self.DATA_SCOPE_SELF in data_scopes:
            if self.model.__name__ == "UserModel":
                id_attr = getattr(self.model, "id", None)
                if id_attr is not None and self.auth.user and self.auth.user.id:
                    return id_attr == self.auth.user.id
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None and self.auth.user and self.auth.user.id:
                return created_id_attr == self.auth.user.id
            return None

        created_id_attr = getattr(self.model, "created_id", None)
        if created_id_attr is not None and self.auth.user and self.auth.user.id:
            return created_id_attr == self.auth.user.id
        return None

    async def _get_accessible_dept_ids(self, data_scopes: set) -> set[int]:
        accessible_dept_ids = set()
        user_dept_id = getattr(self.auth.user, "dept_id", None)

        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes and user_dept_id is not None:
            try:
                from app.api.v1.module_system.dept.model import DeptModel

                dept_sql = select(DeptModel)
                dept_result = await self.db.execute(dept_sql)
                dept_objs = dept_result.scalars().all()
                id_map = get_child_id_map(dept_objs)
                dept_with_children_ids = get_child_recursion(id=user_dept_id, id_map=id_map)
                accessible_dept_ids.update(dept_with_children_ids)
            except Exception:
                accessible_dept_ids.add(user_dept_id)

        return accessible_dept_ids
