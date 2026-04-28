"""
咨询会报名管理 - 服务层
"""

from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import RegistrationCRUD
from .schema import (
    RegistrationApproveSchema,
    RegistrationCreateSchema,
    RegistrationOutSchema,
    RegistrationPaySchema,
    RegistrationQuerySchema,
    RegistrationRejectSchema,
    RegistrationUpdateSchema,
)


class RegistrationService:
    """
    咨询会报名管理服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: RegistrationQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await RegistrationCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [RegistrationOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: RegistrationQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await RegistrationCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: RegistrationCreateSchema) -> dict:
        """创建报名"""
        create_data = data.model_dump(exclude_unset=True)

        existing = await RegistrationCRUD(auth).get_by_consultation_and_university(
            consultation_id=create_data["consultation_id"],
            university_id=create_data["university_id"],
        )
        if existing:
            raise CustomException(msg="该高校已报名此咨询会")

        obj = await RegistrationCRUD(auth).create_crud(create_data)
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(
        cls, auth: AuthSchema, id: int, data: RegistrationUpdateSchema
    ) -> dict:
        """更新报名"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        if obj.registration_status != "pending":
            raise CustomException(msg="只能修改待审核状态的报名")
        update_data = data.model_dump(exclude_unset=True)
        obj = await RegistrationCRUD(auth).update_crud(id, update_data)
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """删除"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        await RegistrationCRUD(auth).delete_crud(id)

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除"""
        await RegistrationCRUD(auth).batch_delete_crud(ids)

    @classmethod
    async def approve_service(
        cls, auth: AuthSchema, id: int, data: RegistrationApproveSchema
    ) -> dict:
        """审核通过"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        if obj.registration_status != "pending":
            raise CustomException(msg="只能审核待处理状态的报名")

        obj = await RegistrationCRUD(auth).approve_crud(
            id=id,
            booth_number=data.booth_number,
            booth_size=data.booth_size,
            booth_fee=data.booth_fee,
            comment=data.comment,
        )
        log.info(f"审核通过报名 {id}")

        # 自动创建行程待办项
        try:
            from app.api.v1.module_consultation.itinerary.service import ItineraryService

            await ItineraryService.create_auto_itinerary_service(auth=auth, registration_id=id)
            log.info(f"审核通过后自动创建行程待办项，报名ID: {id}")
        except Exception as e:
            log.warning(f"自动创建行程待办项失败: {e}")

        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reject_service(
        cls, auth: AuthSchema, id: int, data: RegistrationRejectSchema
    ) -> dict:
        """审核拒绝"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        if obj.registration_status != "pending":
            raise CustomException(msg="只能拒绝待处理状态的报名")

        obj = await RegistrationCRUD(auth).reject_crud(id=id, comment=data.comment)
        log.info(f"审核拒绝报名 {id}")
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def cancel_service(cls, auth: AuthSchema, id: int, reason: str | None = None) -> dict:
        """取消报名"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")

        obj = await RegistrationCRUD(auth).cancel_crud(id=id, reason=reason)
        log.info(f"取消报名 {id}")
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def confirm_payment_service(
        cls, auth: AuthSchema, id: int, data: RegistrationPaySchema
    ) -> dict:
        """确认支付"""
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")
        if obj.registration_status != "approved":
            raise CustomException(msg="只能确认已审核通过的报名支付")
        if obj.is_paid:
            raise CustomException(msg="该报名已确认支付")

        payment_time = datetime.strptime(data.payment_time, "%Y-%m-%d %H:%M:%S")
        obj = await RegistrationCRUD(auth).confirm_payment_crud(
            id=id, payment_time=payment_time, comment=data.comment
        )
        log.info(f"确认支付报名 {id}")
        return RegistrationOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def statistics_by_status_service(cls, auth: AuthSchema) -> dict:
        """按状态统计"""
        return await RegistrationCRUD(auth).statistics_by_status_crud()

    @classmethod
    async def statistics_by_consultation_service(
        cls, auth: AuthSchema, consultation_id: int
    ) -> dict:
        """统计某咨询会报名情况"""
        return await RegistrationCRUD(auth).statistics_by_consultation_crud(consultation_id)

    @classmethod
    async def one_click_register_service(cls, auth: AuthSchema, id: int) -> dict:
        """一键报名 - 发送回执邮件"""
        from app.api.v1.module_consultation.info_collection.crud import InfoCollectionCRUD
        from app.common.email_service import EmailService

        # 获取报名记录
        obj = await RegistrationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该报名记录不存在")

        if obj.registration_status != "approved":
            raise CustomException(msg="只能在审核通过后发送回执邮件")

        if obj.is_registered:
            raise CustomException(msg="该报名已完成一键报名，请勿重复操作")

        # 获取咨询会信息
        consultation = await InfoCollectionCRUD(auth).get_by_id_crud(obj.consultation_id)
        if not consultation:
            raise CustomException(msg="关联的咨询会信息不存在")

        # 获取报名接收邮箱
        registration_email = obj.registration_email or consultation.registration_email
        if not registration_email:
            raise CustomException(msg="报名接收邮箱不能为空，请在咨询会信息中维护报名邮箱")

        # 发送回执邮件
        consultation_date = str(consultation.start_date) if consultation.start_date else "待定"
        consultation_location = (
            consultation.address or f"{consultation.city or ''}{consultation.address or ''}"
        )

        email_result = await EmailService.sendRegistrationReceipt(
            to_email=registration_email,
            university_name=obj.university_name or "未知高校",
            consultation_title=consultation.title,
            consultation_date=consultation_date,
            consultation_location=consultation_location,
            booth_number=obj.booth_number,
            contact_person=obj.contact_person,
        )

        if not email_result.get("success"):
            raise CustomException(msg=f"邮件发送失败: {email_result.get('message')}")

        # 更新报名状态
        obj = await RegistrationCRUD(auth).update_registered_crud(
            id=id, registration_email=registration_email
        )
        log.info(f"一键报名成功，邮件已发送至 {registration_email}")

        return RegistrationOutSchema.model_validate(obj).model_dump()
