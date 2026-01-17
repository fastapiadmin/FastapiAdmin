from typing import Any

from sqlalchemy import select
from sqlalchemy.sql.elements import ColumnElement

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.user.model import UserModel
from app.utils.common_util import get_child_id_map, get_child_recursion


class Permission:
    """
    为业务模型提供数据权限过滤功能
    """

    # 数据权限常量定义，提高代码可读性
    DATA_SCOPE_SELF = 1  # 仅本人数据
    DATA_SCOPE_DEPT = 2  # 本部门数据
    DATA_SCOPE_DEPT_AND_CHILD = 3  # 本部门及以下数据
    DATA_SCOPE_ALL = 4  # 全部数据
    DATA_SCOPE_CUSTOM = 5  # 自定义数据

    def __init__(self, model: Any, auth: AuthSchema) -> None:
        """
        初始化权限过滤器实例

        Args:
            db: 数据库会话
            model: 数据模型类
            current_user: 当前用户对象
            auth: 认证信息对象
        """
        self.model = model
        self.auth = auth
        self.conditions: list[ColumnElement] = []  # 权限条件列表

    async def filter_query(self, query: Any) -> Any:
        """
        异步过滤查询对象

        Args:
            query: SQLAlchemy查询对象

        Returns:
            过滤后的查询对象
        """
        condition = await self.__permission_condition()
        return query.where(condition) if condition is not None else query

    async def __permission_condition(self) -> ColumnElement | None:
        """
        应用数据范围权限隔离
        基于角色的五种数据权限范围过滤
        支持五种权限类型：
        1. 仅本人数据权限 - 只能查看自己创建的数据
        2. 本部门数据权限 - 只能查看同部门的数据
        3. 本部门及以下数据权限 - 可以查看本部门及所有子部门的数据
        4. 全部数据权限 - 可以查看所有数据
        5. 自定义数据权限 - 通过role_dept_relation表定义可访问的部门列表

        权限处理原则：
        - 多个角色的权限取并集（最宽松原则）
        - 优先级：全部数据 > 部门权限（2、3、5的并集）> 仅本人
        - 构造权限过滤表达式，返回None表示不限制
        """
        # 如果不需要检查数据权限,则不限制
        if not self.auth.user:
            return None

        # 如果检查数据权限为False,则不限制
        if not self.auth.check_data_scope:
            return None

        # 如果模型没有创建人created_id字段,则不限制
        if not hasattr(self.model, "created_id"):
            return None

        # 超级管理员可以查看所有数据
        if self.auth.user.is_superuser:
            return None

        # 如果用户没有角色,则只能查看自己的数据
        roles = getattr(self.auth.user, "roles", []) or []
        if not roles:
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None

        # 获取用户所有角色的权限范围
        data_scopes = set()
        custom_dept_ids = set()  # 自定义权限（data_scope=5）关联的部门ID集合

        for role in roles:
            data_scopes.add(role.data_scope)
            # 收集自定义权限（data_scope=5）关联的部门ID
            if role.data_scope == self.DATA_SCOPE_CUSTOM and hasattr(role, "depts") and role.depts:
                custom_dept_ids.update(dept.id for dept in role.depts)

        # 权限优先级处理：全部数据权限最高优先级
        if self.DATA_SCOPE_ALL in data_scopes:
            return None

        # 收集所有可访问的部门ID（2、3、5权限的并集）
        accessible_dept_ids = set()
        user_dept_id = getattr(self.auth.user, "dept_id", None)

        # 处理自定义数据权限（5）
        if self.DATA_SCOPE_CUSTOM in data_scopes:
            accessible_dept_ids.update(custom_dept_ids)

        # 处理本部门数据权限（2）
        if self.DATA_SCOPE_DEPT in data_scopes and user_dept_id is not None:
            accessible_dept_ids.add(user_dept_id)

        # 处理本部门及以下数据权限（3）
        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes and user_dept_id is not None:
            try:
                # 查询所有部门并递归获取子部门
                dept_sql = select(DeptModel)
                dept_result = await self.auth.db.execute(dept_sql)
                dept_objs = dept_result.scalars().all()
                id_map = get_child_id_map(dept_objs)
                # get_child_recursion返回的结果已包含自身ID和所有子部门ID
                dept_with_children_ids = get_child_recursion(id=user_dept_id, id_map=id_map)
                accessible_dept_ids.update(dept_with_children_ids)
            except Exception:
                # 查询失败时降级到本部门
                accessible_dept_ids.add(user_dept_id)

        # 如果有部门权限（2、3、5任一），使用部门过滤
        if accessible_dept_ids:
            creator_rel = getattr(self.model, "created_by", None)
            # 优先使用关系过滤（性能更好）
            if creator_rel is not None and hasattr(UserModel, "dept_id"):
                return creator_rel.has(UserModel.dept_id.in_(list(accessible_dept_ids)))
            # 降级方案：如果模型没有created_by关系但有created_id，则只能查看自己的数据
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None

        # 处理仅本人数据权限（1）
        if self.DATA_SCOPE_SELF in data_scopes:
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None

        # 默认情况：如果用户有角色但没有任何有效权限范围，只能查看自己的数据
        created_id_attr = getattr(self.model, "created_id", None)
        if created_id_attr is not None:
            return created_id_attr == self.auth.user.id
        return None
