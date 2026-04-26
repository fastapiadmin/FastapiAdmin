from collections.abc import Sequence
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_crud import CRUDBase

from .model import TenantModel
from .schema import TenantCreateSchema, TenantOutSchema, TenantUpdateSchema


class TenantCRUD(CRUDBase[TenantModel, TenantCreateSchema, TenantUpdateSchema]):
    """租户数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth
        super().__init__(model=TenantModel, auth=auth)

    async def get_by_id_crud(
        self, id: int, preload: list[str | Any] | None = None
    ) -> TenantModel | None:
        return await self.get(id=id, preload=preload)

    async def get_list_crud(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[TenantModel]:
        return await self.list(search=search, order_by=order_by, preload=preload)

    async def page_crud(
        self,
        offset: int,
        limit: int,
        order_by: list[dict[str, str]] | None,
        search: dict | None = None,
        out_schema: type[TenantOutSchema] | None = None,
        preload: list[str | Any] | None = None,
    ) -> dict:
        return await self.page(
            offset=offset,
            limit=limit,
            order_by=order_by or [{"id": "asc"}],
            search=search or {},
            out_schema=out_schema or TenantOutSchema,
            preload=preload or [],
        )

    async def create_crud(self, data: TenantCreateSchema) -> TenantModel | None:
        return await self.create(data=data)

    async def update_crud(self, id: int, data: TenantUpdateSchema) -> TenantModel | None:
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: list[int]) -> None:
        await self.delete(ids=ids)

    async def set_available_crud(self, ids: list[int], status: str) -> None:
        await self.set(ids=ids, status=status)
