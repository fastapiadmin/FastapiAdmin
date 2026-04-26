"""
行程方案管理 - 服务层
"""

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ItineraryCRUD
from .schema import (
    ItineraryCreateSchema,
    ItineraryOutSchema,
    ItineraryQuerySchema,
    ItineraryUpdateSchema,
)


class ItineraryService:
    """
    行程方案管理服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ItineraryQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await ItineraryCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ItineraryOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ItineraryQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ItineraryCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(
        cls, auth: AuthSchema, data: ItineraryCreateSchema
    ) -> dict:
        """创建"""
        create_data = data.model_dump(exclude_unset=True)
        obj = await ItineraryCRUD(auth).create_crud(create_data)
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: ItineraryUpdateSchema
    ) -> dict:
        """更新"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        update_data = data.model_dump(exclude_unset=True)
        obj = await ItineraryCRUD(auth).update_crud(id, update_data)
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        await ItineraryCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除"""
        await ItineraryCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def confirm_service(cls, auth: AuthSchema, id: int) -> dict:
        """确认行程方案"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).confirm_crud(id)
        log.info(f"确认行程方案 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def execute_service(cls, auth: AuthSchema, id: int) -> dict:
        """执行行程方案"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).execute_crud(id)
        log.info(f"执行行程方案 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def archive_service(cls, auth: AuthSchema, id: int) -> dict:
        """归档行程方案"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).archive_crud(id)
        log.info(f"归档行程方案 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def sync_calendar_service(cls, auth: AuthSchema, id: int) -> dict:
        """同步到日历"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).sync_calendar_crud(id)
        log.info(f"同步行程方案到日历 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def add_consultation_service(
        cls, auth: AuthSchema, id: int, consultation_id: int
    ) -> dict:
        """添加咨询会到行程"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")

        from app.api.v1.module_consultation.info_collection.crud import InfoCollectionCRUD
        consultation = await InfoCollectionCRUD(auth).get_by_id_crud(consultation_id)
        if not consultation:
            raise CustomException(msg="该咨询会不存在")

        consultation_detail = {
            "id": consultation.id,
            "title": consultation.title,
            "start_date": str(consultation.start_date) if consultation.start_date else None,
            "city": consultation.city,
            "address": consultation.address,
        }

        obj = await ItineraryCRUD(auth).add_consultation_crud(id, consultation_id, consultation_detail)
        log.info(f"添加咨询会 {consultation_id} 到行程 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def remove_consultation_service(
        cls, auth: AuthSchema, id: int, consultation_id: int
    ) -> dict:
        """从行程中移除咨询会"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).remove_consultation_crud(id, consultation_id)
        log.info(f"从行程 {id} 移除咨询会 {consultation_id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def optimize_route_service(cls, auth: AuthSchema, id: int) -> dict:
        """优化路线"""
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).optimize_route_crud(id)
        log.info(f"优化行程路线 {id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()
