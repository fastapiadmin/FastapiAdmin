# -*- coding: utf-8 -*-

from typing import Any
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import select, and_
from app.api.v1.module_system.user.model import UserModel
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.auth.schema import AuthSchema
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
    
    def __init__(self, model: Any, auth: AuthSchema):
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
        构造权限过滤表达式，返回None表示不限制。
        """
        # 如果不需要检查数据权限,则不限制
        if not self.auth.user:
            return None
        
        # 如果检查数据权限为False,则不限制
        if not self.auth.check_data_scope:
            return None

        # 如果模型没有创建人creator_id字段,则不限制
        if not hasattr(self.model, "creator_id"):
            return None
        
        # 超级管理员可以查看所有数据
        if self.auth.user.is_superuser:
            return None
            
        # 如果用户没有部门或角色,则只能查看自己的数据
        if not getattr(self.auth.user, "dept_id", None) or not getattr(self.auth.user, "roles", None):
            creator_id_attr = getattr(self.model, "creator_id", None)
            if creator_id_attr is not None:
                return creator_id_attr == self.auth.user.id
            return None
        
        # 获取用户所有角色的权限范围
        data_scopes = set()
        dept_ids = set()
        roles = getattr(self.auth.user, "roles", []) or []
        
        for role in roles:
            # 角色的部门集合
            if hasattr(role, 'depts') and role.depts:
                for dept in role.depts:
                    dept_ids.add(dept.id)
            data_scopes.add(role.data_scope)
        
        # 如果有全部数据权限，直接返回
        if self.DATA_SCOPE_ALL in data_scopes:
            # 全部数据权限
            return None

        # 如果有自定义数据权限且部门ID存在，优先处理
        if self.DATA_SCOPE_CUSTOM in data_scopes and dept_ids:
            # 自定义数据权限
            creator_rel = getattr(self.model, "creator", None)
            if hasattr(UserModel, 'dept_id') and creator_rel is not None:
                return creator_rel.has(getattr(UserModel, 'dept_id').in_(list(dept_ids)))
            else:
                creator_id_attr = getattr(self.model, "creator_id", None)
                if creator_id_attr is not None:
                    return creator_id_attr == self.auth.user.id
                return None

        # 处理其他数据权限范围
        dept_id_val = getattr(self.auth.user, "dept_id", None)
        
        if self.DATA_SCOPE_SELF in data_scopes:
            # 仅本人数据
            creator_id_attr = getattr(self.model, "creator_id", None)
            if creator_id_attr is not None:
                return creator_id_attr == self.auth.user.id
            return None

        if self.DATA_SCOPE_DEPT in data_scopes and dept_id_val is not None:
            # 本部门数据
            dept_ids.add(dept_id_val)
            
        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes and dept_id_val is not None:
            # 本部门及以下数据（查询所有部门并递归）
            dept_sql = select(DeptModel)
            dept_result = await self.auth.db.execute(dept_sql)
            dept_objs = dept_result.scalars().all()
            id_map = get_child_id_map(dept_objs)
            dept_child_ids = get_child_recursion(id=dept_id_val, id_map=id_map)
            dept_ids.add(dept_id_val)  # 包含本部门
            for child_id in dept_child_ids:
                dept_ids.add(child_id)

        # 处理2、3汇总的数据权限
        if (self.DATA_SCOPE_DEPT in data_scopes or self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes) and dept_ids:
            # 使用关系creator进行筛选（若存在），否则回退到仅本人数据
            creator_rel = getattr(self.model, "creator", None)
            if hasattr(UserModel, 'dept_id') and creator_rel is not None and dept_ids:
                return creator_rel.has(getattr(UserModel, 'dept_id').in_(list(dept_ids)))
            else:
                creator_id_attr = getattr(self.model, "creator_id", None)
                if creator_id_attr is not None:
                    return creator_id_attr == self.auth.user.id
                return None

        # 默认情况下，只能查看自己的数据
        creator_id_attr = getattr(self.model, "creator_id", None)
        if creator_id_attr is not None:
            return creator_id_attr == self.auth.user.id
        return None