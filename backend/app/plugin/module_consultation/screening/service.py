"""
咨询会筛选匹配 - 服务层
"""
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ScreeningCRUD
from .model import ScreeningFilterModel
from .schema import (
    ScreeningFilterCreateSchema,
    ScreeningFilterOutSchema,
    ScreeningFilterQueryParam,
    ScreeningFilterUpdateSchema,
)


class ScreeningService:
    """
    咨询会筛选匹配服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ScreeningCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该筛选条件不存在")
        return ScreeningFilterOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ScreeningFilterQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await ScreeningCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ScreeningFilterOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ScreeningFilterQueryParam | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ScreeningCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(
        cls, auth: AuthSchema, data: ScreeningFilterCreateSchema
    ) -> dict:
        """创建"""
        create_data = data.model_dump(exclude_unset=True)
        obj = await ScreeningCRUD(auth).create_crud(create_data)
        return ScreeningFilterOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: ScreeningFilterUpdateSchema
    ) -> dict:
        """更新"""
        obj = await ScreeningCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该筛选条件不存在")
        update_data = data.model_dump(exclude_unset=True)
        obj = await ScreeningCRUD(auth).update_crud(id, update_data)
        return ScreeningFilterOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除"""
        obj = await ScreeningCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该筛选条件不存在")
        await ScreeningCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除"""
        await ScreeningCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def set_default_service(cls, auth: AuthSchema, id: int) -> dict:
        """设为默认"""
        obj = await ScreeningCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该筛选条件不存在")
        obj = await ScreeningCRUD(auth).set_default_crud(id)
        return ScreeningFilterOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def apply_filter_service(
        cls,
        auth: AuthSchema,
        filter_id: int,
        search: dict[str, Any] | None = None,
    ) -> list[dict]:
        """应用筛选条件"""
        log.info(f"应用筛选条件 {filter_id}")
        result = await ScreeningCRUD(auth).apply_filter_crud(filter_id, search)
        return result

    @classmethod
    async def get_default_filter_service(cls, auth: AuthSchema) -> dict | None:
        """获取默认筛选条件"""
        obj = await ScreeningCRUD(auth).get_default_crud()
        if obj:
            return ScreeningFilterOutSchema.model_validate(obj).model_dump()
        return None
