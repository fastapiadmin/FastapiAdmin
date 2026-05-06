"""
活动申请审批 - 服务层
"""

from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ActivityApplyCRUD
from .model import ApprovalStatus
from .schema import (
    ActivityApplyOutSchema,
    ActivityApplyQuerySchema,
)


class ActivityApplyService:
    """
    活动申请管理服务层

    职责：活动申请增删改查、审批流(通过/拒绝/取消)
    状态机：pending(待审批) -> approved(已批准) / rejected(已拒绝) / cancelled(已取消)
    约束：只有待审批状态可编辑/审批；已批准不可删除；只有待审批和已批准可取消
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID

        返回:
        - dict: 活动申请模型实例字典
        """
        obj = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该活动申请不存在")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def list_service(
        cls,
        auth: AuthSchema,
        search: ActivityApplyQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> list[dict]:
        """
        列表查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - search (ActivityApplyQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - list[dict]: 活动申请模型实例字典列表
        """
        search_dict = search.__dict__ if search else None
        obj_list = await ActivityApplyCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ActivityApplyOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ActivityApplyQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (ActivityApplyQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ActivityApplyCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建活动申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的活动申请模型实例字典
        """
        if data.get("activity_code"):
            existing = await ActivityApplyCRUD(auth).get_by_activity_code_crud(
                data["activity_code"]
            )
            if existing:
                raise CustomException(msg="活动编码已存在")

        obj = await ActivityApplyCRUD(auth).create_crud(data=data)
        log.info(f"创建活动申请成功: {obj.id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新活动申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的活动申请模型实例字典
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status != ApprovalStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的申请可以编辑")

        # 编码唯一性校验（仅编码变更时检查）

        if data.get("activity_code") and data["activity_code"] != existing.activity_code:
            code_existing = await ActivityApplyCRUD(auth).get_by_activity_code_crud(
                data["activity_code"]
            )
            if code_existing:
                raise CustomException(msg="活动编码已存在")

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新活动申请成功: {id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除活动申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        # 已批准的申请不可删除，防止审批后撤回
        if existing.approval_status == ApprovalStatus.APPROVED.value:
            raise CustomException(msg="已批准的申请无法删除")

        await ActivityApplyCRUD(auth).delete_crud(id=id)
        log.info(f"删除活动申请成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除活动申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 活动申请ID列表
        """
        for apply_id in ids:
            existing = await ActivityApplyCRUD(auth).get_by_id_crud(apply_id)
            if existing and existing.approval_status == ApprovalStatus.APPROVED.value:
                raise CustomException(msg=f"活动申请ID {apply_id} 已批准，无法删除")

        await ActivityApplyCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除活动申请成功: {ids}")

    @classmethod
    async def approve_service(
        cls, auth: AuthSchema, id: int, approval_comment: str | None = None
    ) -> dict:
        """
        审批通过

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID
        - approval_comment (str | None): 审批意见

        返回:
        - dict: 更新后的活动申请模型实例字典
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status != ApprovalStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的申请可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "approval_status": ApprovalStatus.APPROVED.value,
            "approval_comment": approval_comment,
            "approval_by": user_id,
            "approval_by_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批通过活动申请成功: {id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        审批拒绝

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID
        - approval_comment (str): 审批意见

        返回:
        - dict: 更新后的活动申请模型实例字典
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status != ApprovalStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的申请可以审批")

        # 拒绝时必须填写审批意见
        if not approval_comment:
            raise CustomException(msg="请填写审批意见")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "approval_status": ApprovalStatus.REJECTED.value,
            "approval_comment": approval_comment,
            "approval_by": user_id,
            "approval_by_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批拒绝活动申请成功: {id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def cancel_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        取消活动申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动申请ID

        返回:
        - dict: 更新后的活动申请模型实例字典
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status not in [
            ApprovalStatus.PENDING.value,
            ApprovalStatus.APPROVED.value,
        ]:
            raise CustomException(msg="当前状态无法取消")

        update_data = {
            "approval_status": ApprovalStatus.CANCELLED.value,
        }

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"取消活动申请成功: {id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()
