# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import TypeVar, Sequence, Generic, Dict, Any, List, Optional, Type, Union
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy import asc, func, select, delete, Select, desc, update, or_, and_
from sqlalchemy import inspect as sa_inspect

from app.core.base_model import MappedBase
from app.utils.common_util import get_child_id_map, get_child_recursion
from app.core.exceptions import CustomException
from app.common.request import PageResultSchema
from app.core.serialize import Serialize

from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.user.model import UserModel

ModelType = TypeVar("ModelType", bound=MappedBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """基础数据层"""

    def __init__(self, model: Type[ModelType], auth: AuthSchema) -> None:
        """
        初始化CRUDBase类
        
        参数:
        - model (Type[ModelType]): 数据模型类。
        - auth (AuthSchema): 认证信息。

        返回:
        - None
        """
        self.model = model
        self.auth = auth
        self.db = auth.db
        self.current_user = auth.user
    
    async def get(self, preload: Optional[List[Union[str, Any]]] = None, **kwargs) -> Optional[ModelType]:
        """
        根据条件获取单个对象
        
        参数:
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，支持关系名字符串或SQLAlchemy loader option
        - **kwargs: 查询条件
            
        返回:
        - Optional[ModelType]: 对象实例
            
        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**kwargs)
            sql = select(self.model).where(*conditions)
            # 应用可配置的预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            
            sql = await self.__filter_permissions(sql)

            result: Result = await self.db.execute(sql)
            obj = result.scalars().first()
            return obj
        except Exception as e:
            raise CustomException(msg=f"获取查询失败: {str(e)}")

    async def list(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, preload: Optional[List[Union[str, Any]]] = None) -> Sequence[ModelType]:
        """
        根据条件获取对象列表
        
        参数:
        - search (Optional[Dict]): 查询条件,格式为 {'id': value, 'name': value}
        - order_by (Optional[List[Dict[str, str]]]): 排序字段,格式为 [{'id': 'asc'}, {'name': 'desc'}]
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，支持关系名字符串或SQLAlchemy loader option
            
        返回:
        - Sequence[ModelType]: 对象列表
            
        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{'id': 'asc'}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))
            # 应用可配置的预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            return result.scalars().all()
        except Exception as e:
            raise CustomException(msg=f"列表查询失败: {str(e)}")

    async def tree_list(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None, children_attr: str = 'children', preload: Optional[List[Union[str, Any]]] = None) -> Sequence[ModelType]:
        """
        获取树形结构数据列表
        
        参数:
        - search (Optional[Dict]): 查询条件
        - order_by (Optional[List[Dict[str, str]]]): 排序字段
        - children_attr (str): 子节点属性名
        - preload (Optional[List[Union[str, Any]]]): 额外预加载关系，若为None则默认包含children_attr
            
        返回:
        - Sequence[ModelType]: 树形结构数据列表
            
        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{'id': 'asc'}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))
            
            # 处理预加载选项
            final_preload = preload
            # 如果没有提供preload且children_attr存在，则添加到预加载选项中
            if preload is None and children_attr and hasattr(self.model, children_attr):
                # 获取模型默认预加载选项
                model_defaults = getattr(self.model, "__loader_options__", [])
                # 将children_attr添加到默认预加载选项中
                final_preload = list(model_defaults) + [children_attr]
            
            # 应用预加载选项
            for opt in self.__loader_options(final_preload):
                sql = sql.options(opt)
            
            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            return result.scalars().all()
        except Exception as e:
            raise CustomException(msg=f"树形列表查询失败: {str(e)}")
    
    async def page(self, offset: int, limit: int, order_by: List[Dict[str, str]], search: Dict, out_schema: Type[OutSchemaType], preload: Optional[List[Union[str, Any]]] = None) -> Dict:
        """
        获取分页数据
        
        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (List[Dict[str, str]]): 排序字段
        - search (Dict): 查询条件
        - out_schema (Type[OutSchemaType]): 输出数据模型
        - preload (Optional[List[Union[str, Any]]]): 预加载关系
            
        返回:
        - Dict: 分页数据
            
        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{'id': 'asc'}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))
            # 应用预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            sql = await self.__filter_permissions(sql)

            # 获取总数
            count_sql = select(func.count()).select_from(self.model)
            if conditions:
                count_sql = count_sql.where(*conditions)
            count_sql = await self.__filter_permissions(count_sql)
            
            total_result = await self.db.execute(count_sql)
            total = total_result.scalar() or 0

            result: Result = await self.db.execute(sql.offset(offset).limit(limit))
            objs = result.scalars().all()

            data = PageResultSchema.model_construct(
                _fields_set={"items", "total", "page_no", "page_size", "has_next"},
                items=[out_schema.model_validate(obj).model_dump() for obj in objs],
                total=total,
                page_no=offset // limit + 1 if limit else 1,
                page_size=limit,
                has_next=offset + limit < total,
            ).model_dump()

            return data
        except Exception as e:
            raise CustomException(msg=f"分页查询失败: {str(e)}")
    
    async def create(self, data: Union[CreateSchemaType, Dict]) -> ModelType:
        """
        创建新对象
        
        参数:
        - data (Union[CreateSchemaType, Dict]): 对象属性
            
        返回:
        - ModelType: 新创建的对象实例
            
        异常:
        - CustomException: 创建失败时抛出异常
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump()
            obj = self.model(**obj_dict)
            
            # 设置创建人ID（存在该字段时）
            if hasattr(obj, "creator_id") and self.current_user:
                setattr(obj, "creator_id", self.current_user.id)
            
            self.db.add(obj)
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except Exception as e:
            raise CustomException(msg=f"创建失败: {str(e)}")

    async def update(self, id: int, data: Union[UpdateSchemaType, Dict]) -> ModelType:
        """
        更新对象
        
        参数:
        - id (int): 对象ID
        - data (Union[UpdateSchemaType, Dict]): 更新的属性及值
            
        返回:
        - ModelType: 更新后的对象实例
            
        异常:
        - CustomException: 更新失败时抛出异常
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True, exclude={"id"})
            obj = await self.get(id=id)
            if not obj:
                raise CustomException(msg="更新对象不存在")
            
            for key, value in obj_dict.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                    
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except Exception as e:
            raise CustomException(msg=f"更新失败: {str(e)}")

    async def delete(self, ids: List[int]) -> None:
        """
        删除对象
        
        参数:
        - ids (List[int]): 对象ID列表
            
        异常:
        - CustomException: 删除失败时抛出异常
        """
        try:
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if not pk_cols:
                raise CustomException(msg="模型缺少主键，无法删除")
            if len(pk_cols) > 1:
                raise CustomException(msg="暂不支持复合主键的批量删除")
            sql = delete(self.model).where(pk_cols[0].in_(ids))
            # 权限条件
            perm = await self.__permission_condition()
            if perm is not None:
                sql = sql.where(perm)
            await self.db.execute(sql)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"删除失败: {str(e)}")

    async def clear(self) -> None:
        """
        清空对象表
        
        异常:
        - CustomException: 清空失败时抛出异常
        """
        try:
            sql = delete(self.model)
            await self.db.execute(sql)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"清空失败: {str(e)}")

    async def set(self, ids: List[int], **kwargs) -> None:
        """
        批量更新对象
        
        参数:
        - ids (List[int]): 对象ID列表
        - **kwargs: 更新的属性及值
            
        异常:
        - CustomException: 更新失败时抛出异常
        """
        try:
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if not pk_cols:
                raise CustomException(msg="模型缺少主键，无法更新")
            if len(pk_cols) > 1:
                raise CustomException(msg="暂不支持复合主键的批量更新")
            sql = update(self.model).where(pk_cols[0].in_(ids)).values(**kwargs)
            # 权限条件
            perm = await self.__permission_condition()
            if perm is not None:
                sql = sql.where(perm)
            await self.db.execute(sql)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"批量更新失败: {str(e)}")

    async def __filter_permissions(self, sql: Select) -> Select:
        """
        过滤数据权限（仅用于Select）。
        """
        perm = await self.__permission_condition()
        if perm is None:
            return sql
        return sql.where(perm)

    async def __permission_condition(self) -> Optional[ColumnElement]:
        """
        构造权限过滤表达式，返回None表示不限制。
        """
        # 如果不需要检查数据权限,则不限制
        if not self.current_user or not self.auth.check_data_scope:
            return None

        # 如果模型没有创建人creator_id字段,则不限制
        if not hasattr(self.model, "creator_id"):
            return None
        
        # 超级管理员可以查看所有数据
        if getattr(self.current_user, "is_superuser", False):
            return None
            
        # 如果用户没有部门或角色,则只能查看自己的数据
        if not getattr(self.current_user, "dept_id", None) or not getattr(self.current_user, "roles", None):
            creator_id_attr = getattr(self.model, "creator_id", None)
            if creator_id_attr is not None:
                return creator_id_attr == self.current_user.id
            return None
        
        # 获取用户所有角色的权限范围
        data_scopes = set()
        dept_ids = set()
        roles = getattr(self.current_user, "roles", []) or []
        
        for role in roles:
            # 角色的部门集合
            if hasattr(role, 'depts') and role.depts:
                for dept in role.depts:
                    dept_ids.add(dept.id)
            data_scopes.add(role.data_scope)
        
        # 如果有全部数据权限，直接返回
        if 4 in data_scopes:
            # 全部数据权限
            return None

        # 如果有自定义数据权限且部门ID存在，优先处理
        if 5 in data_scopes and dept_ids:
            # 自定义数据权限
            creator_rel = getattr(self.model, "creator", None)
            if hasattr(UserModel, 'dept_id') and creator_rel is not None:
                return creator_rel.has(getattr(UserModel, 'dept_id').in_(list(dept_ids)))
            else:
                creator_id_attr = getattr(self.model, "creator_id", None)
                if creator_id_attr is not None:
                    return creator_id_attr == self.current_user.id
                return None

        # 处理其他数据权限范围
        dept_id_val = getattr(self.current_user, "dept_id", None)
        
        if 1 in data_scopes:
            # 仅本人数据
            creator_id_attr = getattr(self.model, "creator_id", None)
            if creator_id_attr is not None:
                return creator_id_attr == self.current_user.id
            return None

        if 2 in data_scopes and dept_id_val is not None:
            # 本部门数据
            dept_ids.add(dept_id_val)
            
        if 3 in data_scopes and dept_id_val is not None:
            # 本部门及以下数据（查询所有部门并递归）
            dept_sql = select(DeptModel)
            dept_result = await self.db.execute(dept_sql)
            dept_objs = dept_result.scalars().all()
            id_map = get_child_id_map(dept_objs)
            dept_child_ids = get_child_recursion(id=dept_id_val, id_map=id_map)
            dept_ids.add(dept_id_val)  # 包含本部门
            for child_id in dept_child_ids:
                dept_ids.add(child_id)

        # 处理2、3汇总的数据权限
        if (2 in data_scopes or 3 in data_scopes) and dept_ids:
            # 使用关系creator进行筛选（若存在），否则回退到仅本人数据
            creator_rel = getattr(self.model, "creator", None)
            if hasattr(UserModel, 'dept_id') and creator_rel is not None and dept_ids:
                return creator_rel.has(getattr(UserModel, 'dept_id').in_(list(dept_ids)))
            else:
                creator_id_attr = getattr(self.model, "creator_id", None)
                if creator_id_attr is not None:
                    return creator_id_attr == self.current_user.id
                return None

        # 默认情况下，只能查看自己的数据
        creator_id_attr = getattr(self.model, "creator_id", None)
        if creator_id_attr is not None:
            return creator_id_attr == self.current_user.id
        return None

    async def __build_conditions(self, **kwargs) -> List[ColumnElement]:
        """
        构建查询条件
        
        参数:
        - **kwargs: 查询参数
            
        返回:
        - List[ColumnElement]: SQL条件表达式列表
            
        异常:
        - CustomException: 查询参数不存在时抛出异常
        """
        conditions = []
        for key, value in kwargs.items():
            if value is None or value == "":
                continue

            attr = getattr(self.model, key)
            if isinstance(value, tuple):
                seq, val = value
                if seq == "None":
                    conditions.append(attr.is_(None))
                elif seq == "not None":
                    conditions.append(attr.isnot(None))
                elif seq == "date" and val:
                    conditions.append(func.date_format(attr, "%Y-%m-%d") == val)
                elif seq == "month" and val:
                    conditions.append(func.date_format(attr, "%Y-%m") == val)
                elif seq == "like" and val:
                    conditions.append(attr.like(f"%{val}%"))
                elif seq == "in" and val:
                    conditions.append(attr.in_(val))
                elif seq == "between" and isinstance(val, (list, tuple)) and len(val) == 2:
                    conditions.append(attr.between(val[0], val[1]))
                elif seq == "!=" and val:
                    conditions.append(attr != val)
                elif seq in [">", ">=", "<=", "=="] and val:
                    conditions.append(getattr(attr, seq.replace("==", "__eq__"))(val))
            else:
                conditions.append(attr == value)
        return conditions

    def __order_by(self, order_by: List[Dict[str, str]]) -> List[ColumnElement]:
        """
        获取排序字段
        
        参数:
        - order_by (List[Dict[str, str]]): 排序字段列表,格式为 [{'id': 'asc'}, {'name': 'desc'}]
            
        返回:
        - List[ColumnElement]: 排序字段列表
            
        异常:
        - CustomException: 排序字段不存在时抛出异常
        """
        columns = []
        for order in order_by:
            for field, direction in order.items():
                column = getattr(self.model, field)
                columns.append(desc(column) if direction.lower() == 'desc' else asc(column))
        return columns

    def __loader_options(self, preload: Optional[List[Union[str, Any]]] = None) -> List[Any]:
        """
        将预加载参数标准化为SQLAlchemy loader options。
        字符串会转换为selectinload(getattr(self.model, name))；loader option对象将原样返回。
        若模型定义了 __loader_options__，会作为默认预加载。
        """
        # 获取模型默认预加载选项
        model_defaults = getattr(self.model, "__loader_options__", [])
        
        # 确定最终使用的预加载选项
        final_preload = []
        if preload is None:
            # 如果未指定preload，使用模型默认选项
            final_preload = model_defaults
        elif preload == []:
            # 如果preload为空列表，表示不使用任何预加载
            final_preload = []
        else:
            # 如果指定了preload，使用指定的选项（完全替换默认选项）
            final_preload = preload
            
        # 转换为SQLAlchemy loader options并去重
        opts = []
        added_options = set()
        
        for item in final_preload:
            if isinstance(item, str):
                # 字符串类型的预加载选项
                if item not in added_options and hasattr(self.model, item):
                    opts.append(selectinload(getattr(self.model, item)))
                    added_options.add(item)
            else:
                # loader option对象
                item_str = str(item)
                if item_str not in added_options and item is not None:
                    opts.append(item)
                    added_options.add(item_str)
                    
        return opts
