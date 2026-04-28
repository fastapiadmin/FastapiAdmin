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
    async def create_service(cls, auth: AuthSchema, data: ItineraryCreateSchema) -> dict:
        """创建"""
        create_data = data.model_dump(exclude_unset=True)
        obj = await ItineraryCRUD(auth).create_crud(create_data)
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: ItineraryUpdateSchema) -> dict:
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

        obj = await ItineraryCRUD(auth).add_consultation_crud(
            id, consultation_id, consultation_detail
        )
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

    @classmethod
    async def move_task_service(cls, auth: AuthSchema, id: int, board_column: str) -> dict:
        """移动任务到不同看板列"""
        if board_column not in ["todo", "doing", "done"]:
            raise CustomException(msg="看板列必须是 todo/doing/done 之一")
        obj = await ItineraryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程方案不存在")
        obj = await ItineraryCRUD(auth).move_task_crud(id, board_column)
        log.info(f"移动任务 {id} 到 {board_column}")
        return ItineraryOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def kanban_board_service(cls, auth: AuthSchema) -> dict:
        """获取看板视图"""
        all_items = await ItineraryCRUD(auth).list_crud(
            search={"status": "archived"}, order_by=[{"created_time": "desc"}]
        )
        non_archived = await ItineraryCRUD(auth).list_crud(order_by=[{"created_time": "desc"}])
        todo_list = [
            ItineraryOutSchema.model_validate(obj).model_dump()
            for obj in non_archived
            if obj.board_column == "todo" or not obj.board_column
        ]
        doing_list = [
            ItineraryOutSchema.model_validate(obj).model_dump()
            for obj in non_archived
            if obj.board_column == "doing"
        ]
        done_list = [
            ItineraryOutSchema.model_validate(obj).model_dump()
            for obj in non_archived
            if obj.board_column == "done"
        ]
        archived_list = [
            ItineraryOutSchema.model_validate(obj).model_dump()
            for obj in all_items
            if obj.board_column == "archived"
        ]
        return {
            "todo": todo_list,
            "doing": doing_list,
            "done": done_list,
            "archived": archived_list,
        }

    @classmethod
    async def calendar_board_service(
        cls,
        auth: AuthSchema,
        start_date_begin: str | None = None,
        start_date_end: str | None = None,
    ) -> dict:
        """获取日历视图（按日期分组）"""
        search = {}
        if start_date_begin:
            search["start_date"] = ("ge", start_date_begin)
        if start_date_end:
            search["start_date"] = ("le", start_date_end)
        all_items = await ItineraryCRUD(auth).list_crud(
            search=search if search else None, order_by=[{"start_date": "asc"}]
        )
        items = [ItineraryOutSchema.model_validate(obj).model_dump() for obj in all_items]
        calendar_dict = {}
        for item in items:
            date_key = item.get("start_date")
            if date_key:
                if date_key not in calendar_dict:
                    calendar_dict[date_key] = []
                calendar_dict[date_key].append(item)
        return {
            "dates": calendar_dict,
            "items": items,
        }

    @classmethod
    async def create_auto_itinerary_service(cls, auth: AuthSchema, registration_id: int) -> dict:
        """根据报名记录自动创建行程待办项"""
        from app.api.v1.module_consultation.info_collection.crud import InfoCollectionCRUD
        from app.api.v1.module_consultation.registration.crud import RegistrationCRUD

        registration = await RegistrationCRUD(auth).get_by_id_crud(registration_id)
        if not registration:
            raise CustomException(msg="该报名记录不存在")

        consultation = await InfoCollectionCRUD(auth).get_by_id_crud(registration.consultation_id)
        if not consultation:
            raise CustomException(msg="关联的咨询会不存在")

        create_data = {
            "consultation_id": consultation.id,
            "itinerary_name": f"{consultation.title} - {registration.university_name or '待分配'}",
            "start_date": consultation.start_date,
            "end_date": consultation.end_date or consultation.start_date,
            "destination_city": consultation.city,
            "board_column": "todo",
            "task_type": "auto_register",
            "auto_generated": True,
        }
        obj = await ItineraryCRUD(auth).create_auto_generated_crud(create_data)
        log.info(f"自动创建行程待办项 {obj.id}，关联报名 {registration_id}")
        return ItineraryOutSchema.model_validate(obj).model_dump()
