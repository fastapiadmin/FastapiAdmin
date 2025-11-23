# -*- coding: utf-8 -*-

from typing import TypeVar, Generic
from sqlalchemy.orm import Session, Query
from app.api.v1.module_system.user.model import UserModel
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.role.model import RoleModel


T = TypeVar('T')


class PermissionMixin(Generic[T]):
    """
    数据权限混入类
    
    为业务模型提供数据权限过滤功能，支持五种权限类型：
    1. 仅本人数据权限 - 只能查看自己创建的数据
    2. 本部门数据权限 - 只能查看同部门的数据
    3. 本部门及以下数据权限 - 可以查看本部门及所有子部门的数据
    4. 全部数据权限 - 可以查看所有数据
    5. 自定义数据权限 - 通过role_dept_relation表定义可访问的部门列表
    
    所有需要数据权限控制的业务模型都应该继承此混入类
    """
    
    @classmethod
    def get_data_permission_query(cls: type[T], db: Session, user_id: int, tenant_id: int | None = None, customer_id: int | None = None) -> Query:
        """
        获取数据权限过滤后的查询对象
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            tenant_id: 租户ID（可选）
            customer_id: 客户ID（可选）
            
        Returns:
            过滤后的查询对象
        """
        # 获取用户信息
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            # 返回空查询
            return db.query(cls).filter(~cls.id.in_([]))
        
        # 构建基础查询
        query = db.query(cls)
        
        # 应用租户和客户数据隔离
        if hasattr(cls, 'tenant_id'):
            if tenant_id is not None:
                query = query.filter(getattr(cls, 'tenant_id') == tenant_id)
            elif user.tenant_id is not None:
                query = query.filter(getattr(cls, 'tenant_id') == user.tenant_id)
        
        if hasattr(cls, 'customer_id'):
            if customer_id is not None:
                query = query.filter(getattr(cls, 'customer_id') == customer_id)
            elif user.user_type == 3 and user.customer_id is not None:
                query = query.filter(getattr(cls, 'customer_id') == user.customer_id)
        
        # 获取用户的角色数据权限范围
        user_roles = db.query(RoleModel).join(UserModel.roles).filter(UserModel.id == user_id).all()
        
        # 如果用户没有角色，默认只有本人权限
        if not user_roles:
            if hasattr(cls, 'created_id'):
                return query.filter(getattr(cls, 'created_id') == user_id)
            return query.filter(~cls.id.in_([]))
        
        # 确定用户的数据权限范围（取最大权限）
        data_scopes = []
        for role in user_roles:
            if role.data_scope:
                data_scopes.append(role.data_scope)
        
        # 构建权限过滤条件
        if '4' in data_scopes:  # 全部数据权限
            return query
        elif '3' in data_scopes and hasattr(user, 'dept_id') and user.dept_id:  # 本部门及以下数据权限
            return cls._filter_department_and_children(query, user.dept_id, db)
        elif '2' in data_scopes and hasattr(user, 'dept_id') and user.dept_id:  # 本部门数据权限
            return cls._filter_department(query, user.dept_id, db)
        elif '5' in data_scopes:  # 自定义数据权限
            return cls._filter_custom_departments(query, user_id, db)
        else:  # 仅本人数据权限（默认）
            if hasattr(cls, 'created_id'):
                return query.filter(getattr(cls, 'created_id') == user_id)
            return query.filter(~cls.id.in_([]))
    
    @classmethod
    def _filter_department(cls, query: Query, dept_id: Union[int, None], db: Session) -> Query:
        """
        过滤本部门数据
        
        Args:
            query: 原始查询
            dept_id: 部门ID
            db: 数据库会话
            
        Returns:
            过滤后的查询
        """
        if not dept_id:
            return query.filter(~cls.id.in_([]))  # 没有部门时返回空查询
        
        # 如果模型有dept_id字段，直接按部门ID过滤
        if hasattr(cls, 'dept_id'):
            return query.filter(getattr(cls, 'dept_id') == dept_id)
        
        # 如果模型有created_id字段，按创建者过滤
        if hasattr(cls, 'created_id'):
            # 查询该部门的所有用户ID
            dept_user_ids = (
                db.query(UserModel.id)
                .filter(UserModel.dept_id == dept_id)
                .all()
            )
            user_ids = [user.id for user in dept_user_ids]
            if user_ids:
                return query.filter(getattr(cls, 'created_id').in_(user_ids))
        
        return query.filter(~cls.id.in_([]))
    
    @classmethod
    def _filter_department_and_children(cls, query: Query, dept_id: Union[int, None], db: Session) -> Query:
        """
        过滤本部门及所有子部门数据
        
        Args:
            query: 原始查询
            dept_id: 部门ID
            db: 数据库会话
            
        Returns:
            过滤后的查询
        """
        if not dept_id:
            return query.filter(~cls.id.in_([]))  # 没有部门时返回空查询
        
        # 递归获取所有子部门ID
        def get_all_children_dept_ids(parent_id: int) -> list[int]:
            result = [parent_id]
            children = db.query(DeptModel.id).filter(DeptModel.parent_id == parent_id).all()
            for child in children:
                result.extend(get_all_children_dept_ids(child.id))
            return result
        
        all_dept_ids = get_all_children_dept_ids(dept_id)
        
        # 如果模型有dept_id字段，直接按部门ID过滤
        if hasattr(cls, 'dept_id'):
            return query.filter(getattr(cls, 'dept_id').in_(all_dept_ids))
        
        # 如果模型有created_id字段，按创建者过滤
        if hasattr(cls, 'created_id'):
            # 获取这些部门的所有用户ID
            dept_users = (
                db.query(UserModel.id)
                .filter(UserModel.dept_id.in_(all_dept_ids))
                .all()
            )
            user_ids = [user.id for user in dept_users]
            if user_ids:
                return query.filter(getattr(cls, 'created_id').in_(user_ids))
        
        return query.filter(~cls.id.in_([]))
    
    @classmethod
    def _filter_custom_departments(cls, query: Query, user_id: int, db: Session) -> Query:
        """
        过滤自定义部门数据
        
        Args:
            query: 原始查询
            user_id: 用户ID
            db: 数据库会话
            
        Returns:
            过滤后的查询
        """
        # 获取用户角色
        user_roles = db.query(RoleModel).join(UserModel.roles).filter(UserModel.id == user_id).all()
        
        # 收集所有可访问的部门ID
        accessible_dept_ids: set[int] = set()
        for role in user_roles:
            if role.data_scope == '5' and role.depts:
                accessible_dept_ids.update([dept.id for dept in role.depts])
        
        if not accessible_dept_ids:
            # 如果没有自定义部门权限，默认返回本人权限
            if hasattr(cls, 'created_id'):
                return query.filter(getattr(cls, 'created_id') == user_id)
            return query.filter(~cls.id.in_([]))
        
        # 如果模型有dept_id字段，直接按部门ID过滤
        if hasattr(cls, 'dept_id'):
            return query.filter(getattr(cls, 'dept_id').in_(accessible_dept_ids))
        
        # 如果模型有created_id字段，按创建者过滤
        if hasattr(cls, 'created_id'):
            # 获取这些部门的所有用户ID
            dept_users = (
                db.query(UserModel.id)
                .filter(UserModel.dept_id.in_(accessible_dept_ids))
                .all()
            )
            user_ids = [user.id for user in dept_users]
            if user_ids:
                return query.filter(getattr(cls, 'created_id').in_(user_ids))
        
        # 默认返回本人权限
        if hasattr(cls, 'created_id'):
            return query.filter(getattr(cls, 'created_id') == user_id)
        
        return query.filter(~cls.id.in_([]))
    
    @classmethod
    def has_permission_to_access(cls: Type[T], db: Session, user_id: int, record_id: int) -> bool:
        """
        检查用户是否有权限访问特定记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            record_id: 记录ID
            
        Returns:
            是否有权限访问
        """
        # 获取用户信息
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return False
        
        # 获取记录
        record = db.query(cls).filter(cls.id == record_id).first()
        if not record:
            return False
        
        # 检查租户和客户权限
        if hasattr(record, 'tenant_id') and getattr(record, 'tenant_id') is not None and hasattr(user, 'tenant_id') and user.tenant_id != getattr(record, 'tenant_id'):
            return False
        
        if hasattr(record, 'customer_id') and getattr(record, 'customer_id') is not None and hasattr(user, 'customer_id') and user.customer_id != getattr(record, 'customer_id'):
            return False
        
        # 获取用户角色的数据权限
        user_roles = db.query(RoleModel).join(UserModel.roles).filter(UserModel.id == user_id).all()
        data_scopes = [role.data_scope for role in user_roles if role.data_scope]
        
        # 全部数据权限
        if '4' in data_scopes:
            return True
        
        # 仅本人数据权限
        if hasattr(record, 'created_id') and getattr(record, 'created_id') == user_id:
            return True
        
        # 部门相关权限检查
        if not hasattr(user, 'dept_id') or not user.dept_id:
            return False
        
        # 本部门权限
        if '2' in data_scopes and hasattr(record, 'dept_id') and getattr(record, 'dept_id') == user.dept_id:
            return True
        
        # 本部门及以下权限
        if '3' in data_scopes and hasattr(record, 'dept_id'):
            # 检查记录的部门是否在用户部门的子树中
            def is_descendant(dept_id: int, ancestor_id: int) -> bool:
                dept = db.query(DeptModel).filter(DeptModel.id == dept_id).first()
                if not dept:
                    return False
                if dept.parent_id == ancestor_id:
                    return True
                if dept.parent_id:
                    return is_descendant(dept.parent_id, ancestor_id)
                return False
            
            record_dept_id = getattr(record, 'dept_id')
            if record_dept_id:
                return is_descendant(record_dept_id, user.dept_id)
        
        # 自定义数据权限
        if '5' in data_scopes and hasattr(record, 'dept_id'):
            # 收集所有可访问的部门ID
            accessible_dept_ids: set[int] = set()
            for role in user_roles:
                if role.data_scope == '5' and role.depts:
                    accessible_dept_ids.update([dept.id for dept in role.depts])
            
            record_dept_id = getattr(record, 'dept_id')
            if record_dept_id in accessible_dept_ids:
                return True
        
        return False