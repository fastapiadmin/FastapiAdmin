"""
高校信息管理 - 业务逻辑层
"""

from typing import Any

from app.core.database import async_db_session

from .crud import university_crud
from .schema import (
    UniversityCreateSchema,
    UniversityOutSchema,
    UniversityQuerySchema,
    UniversitySimpleOutSchema,
    UniversityUpdateSchema,
)


class UniversityService:
    """高校信息服务类"""

    @staticmethod
    async def detail_service(id: int) -> dict[str, Any]:
        """获取高校详情"""
        async with async_db_session() as session:
            obj = await university_crud.get_by_id(session, id)
            if not obj:
                raise ValueError("高校信息不存在")
            return UniversityOutSchema.model_validate(obj).model_dump()

    @staticmethod
    async def page_service(
        page_no: int,
        page_size: int,
        search: UniversityQuerySchema,
        order_by: list[dict[str, str]] | str | None = None,
    ) -> dict[str, Any]:
        """分页获取高校列表"""
        async with async_db_session() as session:
            result = await university_crud.get_page(
                session=session,
                page_no=page_no,
                page_size=page_size,
                search=search,
                order_by=order_by,
            )
            return result

    @staticmethod
    async def list_service(
        search: UniversityQuerySchema,
    ) -> list[dict[str, Any]]:
        """获取高校列表（不分页，用于下拉选择）"""
        async with async_db_session() as session:
            objs = await university_crud.get_list(session, search)
            return [UniversitySimpleOutSchema.model_validate(obj).model_dump() for obj in objs]

    @staticmethod
    async def create_service(
        data: UniversityCreateSchema,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        """创建高校信息"""
        async with async_db_session() as session:
            obj = await university_crud.create(session, data, user_id)
            await session.commit()
            await session.refresh(obj)
            return UniversityOutSchema.model_validate(obj).model_dump()

    @staticmethod
    async def update_service(
        id: int,
        data: UniversityUpdateSchema,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        """更新高校信息"""
        async with async_db_session() as session:
            obj = await university_crud.update(session, id, data, user_id)
            if not obj:
                raise ValueError("高校信息不存在")
            await session.commit()
            await session.refresh(obj)
            return UniversityOutSchema.model_validate(obj).model_dump()

    @staticmethod
    async def delete_service(id: int) -> None:
        """删除高校信息"""
        async with async_db_session() as session:
            success = await university_crud.delete(session, id)
            if not success:
                raise ValueError("高校信息不存在")
            await session.commit()
