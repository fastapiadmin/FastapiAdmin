""""统一 CRUD 基类 — 同时支持有认证和无认证场景

- 当 `auth` 不为 None 时（Controller 注入）：自动处理租户隔离、数据权限过滤、审计字段填充
- 当 `auth` 为 None 时（后台任务/脚本）：纯数据操作，无权限/租户过滤

用法:
    # 带认证（Controller）
    class UserCRUD(CRUDBase[UserModel, UserCreateSchema, UserUpdateSchema]):
        def __init__(self, auth: AuthSchema) -> None:
            super().__init__(model=UserModel, auth=auth)

    # 无认证（后台任务）
    class OrderCRUD(CRUDBase[OrderModel, Any, Any]):
        def __init__(self, session: AsyncSession) -> None:
            super().__init__(model=OrderModel, session=session)
"""

from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, asc, delete, desc, false, func, literal_column, select, update
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import ColumnElement

from app.core.base_model import MappedBase
from app.core.base_schema import AuthSchema, PageResultSchema
from app.core.exceptions import CustomException
from app.core.permission import Permission

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


class CRUDBase[ModelType: MappedBase, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel]:
    """统一数据层基类 — 有认证时自动处理权限，无认证时纯数据操作"""

    def __init__(
        self,
        model: type[ModelType],
        auth: AuthSchema | None = None,
        session: AsyncSession | None = None,
    ) -> None:
        """
        初始化 CRUDBase。

        参数:
        - model: 数据模型类
        - auth: 认证信息（Controller 场景），为 None 时跳过所有权限/租户/审计逻辑
        - session: 数据库会话（后台任务场景），仅在 auth=None 时使用
        """
        self.model = model
        self.auth = auth
        self.db = session if session is not None else (auth.db if auth else None)
        if self.db is None:
            raise RuntimeError(
                "CRUDBase 未初始化数据库会话，请传入 auth 或 session 参数"
            )

    def _get_pk_col(self) -> ColumnElement:
        """获取模型主键列"""
        mapper = sa_inspect(self.model)
        pk_cols = list(getattr(mapper, "primary_key", []))
        if not pk_cols:
            raise CustomException(msg="模型缺少主键")
        if len(pk_cols) > 1:
            raise CustomException(msg="暂不支持复合主键操作")
        return pk_cols[0]

    @property
    def _supports_soft_delete(self) -> bool:
        """模型是否支持软删除"""
        return all(
            hasattr(self.model, attr) for attr in ("is_deleted", "deleted_time", "deleted_id")
        )

    def _soft_delete_values(self) -> dict[str, Any]:
        """软删除时需要更新的字段值"""
        data: dict[str, Any] = {"is_deleted": True, "deleted_time": datetime.now()}
        if self.auth and self.auth.user:
            data["deleted_id"] = self.auth.user.id
        return data

    async def _get_one(
        self, preload: list[str | Any] | None = None, **kwargs
    ) -> ModelType | None:
        """内部方法：在当前实例会话上执行单条查询（get / update 共用）

        参数:
        - preload: 预加载关系
        - **kwargs: 查询条件

        返回:
        - 对象实例或 None
        """
        conditions = await self.__build_conditions(**kwargs)
        sql = select(self.model).where(*conditions)
        for opt in self.__loader_options(preload):
            sql = sql.options(opt)
        sql = await self.__filter_permissions(sql)
        result: Result = await self.db.execute(sql)
        return result.scalars().first()

    async def get(self, preload: list[str | Any] | None = None, **kwargs) -> ModelType | None:
        """
        根据条件获取单个对象（复用请求级事务会话，保证读已写一致性）

        参数:
        - preload: 预加载关系
        - **kwargs: 查询条件

        返回:
        - 对象实例或 None
        """
        try:
            return await self._get_one(preload=preload, **kwargs)
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"获取查询失败: {e!s}")

    async def get_by_id(self, model_id: int) -> ModelType | None:
        """按主键查询"""
        return await self.get(id=model_id)

    async def get_or_404(
        self,
        id: int | None = None,
        msg: str = "该数据不存在",
        preload: list[str | Any] | None = None,
        out_schema: type[OutSchemaType] | None = None,
        **kwargs,
    ) -> ModelType | OutSchemaType:
        """
        按条件查询单条记录，不存在时抛出 404。

        参数:
        - id: 主键 ID（快捷方式，等价于 kwargs={"id": id}）。
        - msg: 不存在时的错误消息。
        - preload: 预加载关系列表。
        - out_schema: 输出 Schema，为 None 时返回 ORM 对象。
        - **kwargs: 其他查询条件（与 id 互斥）。

        返回:
        - ORM 对象或 Pydantic Schema 实例。

        异常:
        - CustomException: 记录不存在。
        """
        if id is not None:
            kwargs["id"] = id
        obj = await self.get(preload=preload, **kwargs)
        if not obj:
            raise CustomException(msg=msg)
        return out_schema.model_validate(obj) if out_schema else obj

    async def exists(self, **kwargs) -> bool:
        """
        检查是否存在符合条件的记录

        参数:
        - **kwargs: 查询条件

        返回:
        - 是否存在
        """
        return await self.get(**kwargs) is not None

    async def count(self, **kwargs) -> int:
        """
        统计符合条件的记录数（复用请求级事务会话）

        参数:
        - **kwargs: 查询条件，支持元组语法

        返回:
        - 记录数
        """
        try:
            conditions = await self.__build_conditions(**kwargs)
            count_sql = select(func.count()).select_from(self.model).where(*conditions)
            count_sql = await self.__filter_permissions(count_sql)
            result: Result = await self.db.execute(count_sql)
            return result.scalar() or 0
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"统计失败: {e!s}")

    async def get_list(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[ModelType]:
        """
        根据条件获取对象列表（复用请求级事务会话）

        参数:
        - search: 查询条件
        - order_by: 排序字段, 格式为 [{'id': 'asc'}, {'name': 'desc'}]
        - preload: 预加载关系

        返回:
        - 对象列表
        """
        try:
            conditions = await self.__build_conditions(**(search or {}))
            order = order_by or [{"id": "asc"}]
            sql = select(self.model).where(*conditions).order_by(*self._parse_order(order))
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            return result.scalars().all()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"列表查询失败: {e!s}")

    async def tree_list(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        children_attr: str | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[ModelType]:
        """
        获取树形结构数据列表（复用请求级事务会话）

        参数:
        - search: 查询条件
        - order_by: 排序字段
        - children_attr: 子节点属性名（None 时自动从模型 __tree_children_attr__ 推断）
        - preload: 额外预加载关系

        返回:
        - 树形结构数据列表
        """
        # 自动从模型推断 children_attr
        if children_attr is None:
            children_attr = getattr(self.model, "__tree_children_attr__", "children")
        try:
            conditions = await self.__build_conditions(**(search or {}))
            order = order_by or [{"id": "asc"}]
            sql = select(self.model).where(*conditions).order_by(*self._parse_order(order))

            final_preload = preload
            if preload is None and children_attr and hasattr(self.model, children_attr):
                model_defaults = getattr(self.model, "__loader_options__", [])
                final_preload = [*list(model_defaults), children_attr]

            for opt in self.__loader_options(final_preload):
                sql = sql.options(opt)

            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            return result.scalars().all()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"树形列表查询失败: {e!s}")

    async def page(
        self,
        offset: int,
        limit: int,
        order_by: list[dict[str, str]],
        search: dict,
        out_schema: type[OutSchemaType] | None = None,
        preload: list[str | Any] | None = None,
    ) -> PageResultSchema:
        """
        获取分页数据（复用请求级事务会话；count 与 data 共享同一会话）

        参数:
        - offset: 偏移量
        - limit: 每页数量
        - order_by: 排序字段
        - search: 查询条件
        - out_schema: 输出数据模型（None 时返回原始 ORM 对象）
        - preload: 预加载关系

        返回:
        - PageResultSchema: 分页结果
        """
        try:
            conditions = await self.__build_conditions(**(search or {}))
            order = order_by or [{"id": "asc"}]

            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            pk = pk_cols[0] if pk_cols else literal_column("1")

            data_sql = select(self.model).where(*conditions)
            for opt in self.__loader_options(preload):
                data_sql = data_sql.options(opt)
            data_sql = await self.__filter_permissions(data_sql)

            count_sql = select(func.count(pk)).select_from(self.model)
            where_clause = data_sql.whereclause
            if where_clause is not None:
                count_sql = count_sql.where(where_clause)

            total_result = await self.db.execute(count_sql)
            total = total_result.scalar() or 0

            result: Result = await self.db.execute(
                data_sql.order_by(*self._parse_order(order)).offset(offset).limit(limit)
            )
            objs = result.scalars().all()

            items = (
                [out_schema.model_validate(obj).model_dump() for obj in objs]
                if out_schema
                else list(objs)
            )

            return PageResultSchema(
                page_no=offset // limit + 1 if limit else 1,
                page_size=limit or 10,
                total=total,
                has_next=offset + limit < total,
                items=items,
            )
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"分页查询失败: {e!s}")

    async def create(self, data: CreateSchemaType) -> ModelType:
        """创建新对象（有认证时自动填充租户与审计字段）

        事务由 request 级 db_getter 统一管理，本方法不开启独立事务。

        参数:
        - data: 对象属性

        返回:
        - 新创建的对象实例
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump()
            obj = self.model(**obj_dict)

            if self.auth and self.auth.user:
                if hasattr(obj, "tenant_id"):
                    # 非超管始终使用当前租户；超管仅当未显式指定时自动填充
                    if not self.auth.user.is_superuser or getattr(obj, "tenant_id", None) is None:
                        setattr(obj, "tenant_id", self.auth.tenant_id or self.auth.user.tenant_id)
                if hasattr(obj, "created_id"):
                    setattr(obj, "created_id", self.auth.user.id)
                if hasattr(obj, "updated_id"):
                    setattr(obj, "updated_id", self.auth.user.id)

            self.db.add(obj)
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"创建失败: {e!s}")

    async def update(self, id: int, data: UpdateSchemaType) -> ModelType:
        """更新对象（有认证时检查租户归属 + 填充审计字段）

        事务由 request 级 db_getter 统一管理，本方法不开启独立事务。

        参数:
        - id: 对象 ID
        - data: 更新属性

        返回:
        - 更新后的对象实例
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True, exclude={"id"})
            model_defaults = getattr(self.model, "__loader_options__", [])
            obj = await self._get_one(id=id, preload=model_defaults)
            if not obj:
                raise CustomException(msg="更新对象不存在")

            # 租户权限检查（仅在有认证且非超管时）
            if self.auth and self.auth.user and not self.auth.user.is_superuser:
                if hasattr(obj, "tenant_id"):
                    obj_tid = getattr(obj, "tenant_id", None)
                    if obj_tid is not None and obj_tid != self.auth.user.tenant_id:
                        is_platform = getattr(self.model, "__platform_data_shared__", False)
                        if is_platform and obj_tid == 1:
                            raise CustomException(msg="平台数据仅管理员可修改")
                        raise CustomException(msg="无权修改其他租户的数据")

            # 审计字段
            if self.auth and self.auth.user and hasattr(obj, "updated_id"):
                setattr(obj, "updated_id", self.auth.user.id)

            for key, value in obj_dict.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"更新失败: {e!s}")

    async def delete(self, ids: list[int]) -> None:
        """软删除对象（有认证时填充删除人 + 租户隔离）"""
        try:
            pk = self._get_pk_col()

            if self._supports_soft_delete:
                sql = self._tenant_dml_where(
                    update(self.model).where(pk.in_(ids))
                ).values(**self._soft_delete_values())
                await self.db.execute(sql)
            else:
                sql = self._tenant_dml_where(
                    delete(self.model).where(pk.in_(ids))
                )
                await self.db.execute(sql)
            await self.db.flush()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"删除失败: {e!s}")

    async def clear(self) -> None:
        """软清空对象表（有认证时填充删除人 + 租户隔离）"""
        try:
            if self._supports_soft_delete:
                sql = self._tenant_dml_where(update(self.model)).values(**self._soft_delete_values())
                await self.db.execute(sql)
            else:
                sql = self._tenant_dml_where(delete(self.model))
                await self.db.execute(sql)
            await self.db.flush()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"清空失败: {e!s}")

    async def set(self, ids: list[int], **kwargs) -> None:
        """批量更新字段（带租户隔离）"""
        try:
            pk = self._get_pk_col()
            sql = self._tenant_dml_where(update(self.model)).where(pk.in_(ids)).values(**kwargs)
            await self.db.execute(sql)
            await self.db.flush()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"批量更新失败: {e!s}")

    async def restore(self, ids: list[int]) -> None:
        """恢复软删除对象（带租户隔离）"""
        try:
            if not self._supports_soft_delete:
                raise CustomException(msg="该模型不支持软删除，无法恢复")
            pk = self._get_pk_col()
            sql = self._tenant_dml_where(
                update(self.model).where(pk.in_(ids))
            ).values(is_deleted=False, deleted_time=None, deleted_id=None)
            await self.db.execute(sql)
            await self.db.flush()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"恢复失败: {e!s}")

    async def __filter_permissions(self, sql: Select) -> Select:
        """过滤数据权限（仅用于 Select）"""
        if not self.auth:
            return sql
        if getattr(self.model, "__platform_data_shared__", False):
            for condition in self._platform_shared_conditions():
                sql = sql.where(condition)
        filter_obj = Permission(model=self.model, auth=self.auth)
        return await filter_obj.filter_query(sql)

    def _platform_shared_conditions(self) -> list[ColumnElement]:
        if not self.auth or not self.auth.user:
            return []
        tid = self.auth.user.tenant_id
        if tid is not None and tid != 1:
            return [
                (getattr(self.model, "tenant_id") == tid)
                | (getattr(self.model, "tenant_id") == 1)
            ]
        return []

    def _tenant_dml_where(self, sql):
        """为 DML 语句注入 tenant_id 条件（不读平台数据）"""
        if self.auth and hasattr(self.model, "tenant_id") \
           and self.auth.user and not self.auth.user.is_superuser:
            tid = self.auth.tenant_id
            if tid is not None:
                return sql.where(getattr(self.model, "tenant_id") == tid)
        return sql

    async def __build_conditions(self, **kwargs) -> list[ColumnElement]:
        conditions: list[ColumnElement] = []

        if hasattr(self.model, "is_deleted"):
            conditions.append(getattr(self.model, "is_deleted") == False)  # noqa: E712

        if self.auth and hasattr(self.model, "tenant_id") \
           and not getattr(self.model, "__platform_data_shared__", False):
            if self.auth.user and not self.auth.user.is_superuser:
                tid = self.auth.tenant_id
                if tid is not None:
                    conditions.append(getattr(self.model, "tenant_id") == tid)

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
                    dt = datetime.strptime(val, "%Y-%m-%d")
                    conditions.append(attr >= dt)
                    conditions.append(attr < dt + timedelta(days=1))
                elif seq == "month" and val:
                    dt = datetime.strptime(val, "%Y-%m")
                    next_month = (
                        dt.replace(year=dt.year + 1, month=1)
                        if dt.month == 12
                        else dt.replace(month=dt.month + 1)
                    )
                    conditions.append(attr >= dt)
                    conditions.append(attr < next_month)
                elif seq == "like" and val:
                    conditions.append(attr.like(f"%{val}%"))
                elif seq == "in":
                    if val is None:
                        continue
                    if isinstance(val, (list, tuple, set)) and len(val) == 0:
                        conditions.append(false())
                    else:
                        conditions.append(attr.in_(val))
                elif seq == "between" and isinstance(val, (list, tuple)) and len(val) == 2:
                    conditions.append(attr.between(val[0], val[1]))
                elif seq in ("!=", "ne") and val is not None:
                    conditions.append(attr != val)
                elif seq in (">", "gt") and val is not None:
                    conditions.append(attr > val)
                elif seq in (">=", "ge") and val is not None:
                    conditions.append(attr >= val)
                elif seq in ("<", "lt") and val is not None:
                    conditions.append(attr < val)
                elif seq in ("<=", "le") and val is not None:
                    conditions.append(attr <= val)
                elif seq in ("eq", "==") and val is not None:
                    conditions.append(attr == val)
            else:
                conditions.append(attr == value)
        return conditions

    def _parse_order(
        self, order: list[dict[str, str]]
    ) -> list[ColumnElement]:
        """
        解析排序参数

        参数:
        - order: 排序字段列表, 格式为 [{'id': 'asc'}, {'name': 'desc'}]

        返回:
        - 排序表达式列表
        """
        columns: list[ColumnElement] = []
        for item in order:
            for field, direction in item.items():
                column = getattr(self.model, field)
                columns.append(desc(column) if direction.lower() == "desc" else asc(column))
        return columns

    def __loader_options(
        self, preload: list[str | Any] | None = None
    ) -> list[Any]:
        """
        构建预加载选项

        参数:
        - preload: 预加载关系，支持关系名字符串或 SQLAlchemy loader option

        返回:
        - 预加载选项列表
        """
        options: list[Any] = []
        model_loader_options = getattr(self.model, "__loader_options__", [])

        all_preloads: set[str | Any] = set(model_loader_options)
        if preload:
            for opt in preload:
                if isinstance(opt, str):
                    all_preloads.add(opt)
        elif preload == []:
            all_preloads = set()

        for opt in all_preloads:
            if isinstance(opt, str):
                if hasattr(self.model, opt):
                    options.append(selectinload(getattr(self.model, opt)))
            else:
                options.append(opt)

        return options
