"""
审批记录 - 服务层
"""

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException

from .crud import ApprovalRecordCRUD
from .schema import ApprovalRecordOutSchema, ApprovalRecordQuerySchema


class ApprovalRecordService:
    """
    审批记录服务层

    职责：查询活动申请的审批记录列表
    """

    @classmethod
    async def list_by_apply_service(cls, auth: AuthSchema, activity_apply_id: int) -> list[dict]:
        """
        获取活动申请的所有审批记录

        参数:
        - auth (AuthSchema): 认证信息模型
        - activity_apply_id (int): 活动申请ID

        返回:
        - list[dict]: 审批记录列表
        """
        obj_list = await ApprovalRecordCRUD(auth).get_by_activity_apply_id_crud(
            activity_apply_id=activity_apply_id
        )
        return [ApprovalRecordOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ApprovalRecordQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """分页查询"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"approval_level": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ApprovalRecordCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ApprovalRecordCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该审批记录不存在")
        return ApprovalRecordOutSchema.model_validate(obj).model_dump()
