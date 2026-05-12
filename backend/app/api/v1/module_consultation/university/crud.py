"""
高校信息管理 - 数据访问层
"""

from typing import Any

from sqlalchemy import Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import UniversityModel
from .schema import (
    UniversityCreateSchema,
    UniversityOutSchema,
    UniversityQuerySchema,
    UniversityUpdateSchema,
)


class UniversityCRUD:
    """高校信息 CRUD（独立 session，不依赖 CRUDBase 的 auth.db）"""

    @staticmethod
    def _build_query(search: UniversityQuerySchema) -> Select:
        """构建查询条件"""
        stmt = select(UniversityModel)

        if search.name:
            stmt = stmt.where(UniversityModel.name.contains(search.name))
        if search.code:
            stmt = stmt.where(UniversityModel.code.contains(search.code))
        if search.province:
            stmt = stmt.where(UniversityModel.province == search.province)
        if search.city:
            stmt = stmt.where(UniversityModel.city == search.city)
        if search.status:
            stmt = stmt.where(UniversityModel.status == search.status)

        return stmt

    @staticmethod
    def _order_clauses(
        order_by: list[dict[str, str]] | str | None,
    ) -> list[Any]:
        if order_by is None:
            return [desc(UniversityModel.id)]
        if isinstance(order_by, str):
            field = order_by.removeprefix("-")
            col = getattr(UniversityModel, field, None)
            if col is None:
                return [desc(UniversityModel.id)]
            if order_by.startswith("-"):
                return [desc(col)]
            return [asc(col)]
        clauses: list[Any] = []
        for item in order_by:
            for field, direction in item.items():
                col = getattr(UniversityModel, field, None)
                if col is None:
                    continue
                if str(direction).lower() == "desc":
                    clauses.append(desc(col))
                else:
                    clauses.append(asc(col))
        return clauses or [desc(UniversityModel.id)]

    async def get_by_id(self, session: AsyncSession, id: int) -> UniversityModel | None:
        """根据 ID 获取高校信息"""
        return await session.get(UniversityModel, id)

    async def get_list(
        self,
        session: AsyncSession,
        search: UniversityQuerySchema,
    ) -> list[UniversityModel]:
        """获取高校列表（不分页）"""
        stmt = self._build_query(search)
        stmt = stmt.order_by(desc(UniversityModel.id))
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_page(
        self,
        session: AsyncSession,
        page_no: int,
        page_size: int,
        search: UniversityQuerySchema,
        order_by: list[dict[str, str]] | str | None = None,
    ) -> dict[str, Any]:
        """分页获取高校列表"""
        stmt = self._build_query(search)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await session.execute(count_stmt)).scalar_one()

        stmt = stmt.order_by(*self._order_clauses(order_by))
        offset = (page_no - 1) * page_size
        result = await session.execute(stmt.offset(offset).limit(page_size))
        objs = list(result.scalars().all())

        return {
            "page_no": page_no,
            "page_size": page_size,
            "total": total,
            "has_next": offset + page_size < total,
            "items": [UniversityOutSchema.model_validate(o).model_dump() for o in objs],
        }

    async def create(
        self,
        session: AsyncSession,
        data: UniversityCreateSchema,
        user_id: int | None = None,
    ) -> UniversityModel:
        """创建高校信息"""
        raw = data.model_dump(exclude_unset=True, exclude_none=True)
        for key in ("id", "uuid", "created_time", "updated_time"):
            raw.pop(key, None)
        obj = UniversityModel(**raw)
        if user_id is not None:
            obj.created_id = user_id
            obj.updated_id = user_id
        session.add(obj)
        await session.flush()
        return obj

    async def update(
        self,
        session: AsyncSession,
        id: int,
        data: UniversityUpdateSchema,
        user_id: int | None = None,
    ) -> UniversityModel | None:
        """更新高校信息"""
        obj = await session.get(UniversityModel, id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        if user_id is not None:
            obj.updated_id = user_id
        return obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """删除高校信息"""
        obj = await session.get(UniversityModel, id)
        if not obj:
            return False
        await session.delete(obj)
        return True


university_crud = UniversityCRUD()
