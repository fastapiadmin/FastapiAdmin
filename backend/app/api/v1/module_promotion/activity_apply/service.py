"""
活动申请审批 - 服务层
"""

from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from ..approval_record.crud import ApprovalRecordCRUD
from .crud import ActivityApplyCRUD
from .model import ApprovalStatus
from .schema import (
    ActivityApplyOutSchema,
    ActivityApplyQuerySchema,
)

# 允许审批的状态集合（含 pending 兼容旧数据）
_APPROVABLE_STATUSES = {
    ApprovalStatus.PENDING.value,
    ApprovalStatus.PENDING_LEVEL1.value,
    ApprovalStatus.PENDING_LEVEL2.value,
}

# 允许编辑的状态集合
_EDITABLE_STATUSES = {
    ApprovalStatus.PENDING.value,
    ApprovalStatus.PENDING_LEVEL1.value,
}


class ActivityApplyService:
    """
    活动申请管理服务层

    职责：活动申请增删改查、多级审批流(一级通过/二级通过/拒绝/取消)
    状态机：pending_level1 -> pending_level2 -> approved / rejected / cancelled
    兼容：旧数据 "pending" 等同于 "pending_level1"
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
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
        """列表查询"""
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
        """分页查询"""
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

        初始状态设为 PENDING_LEVEL1，当前审批级别为1
        """
        if data.get("activity_code"):
            existing = await ActivityApplyCRUD(auth).get_by_activity_code_crud(
                data["activity_code"]
            )
            if existing:
                raise CustomException(msg="活动编码已存在")

        data.setdefault("approval_status", ApprovalStatus.PENDING_LEVEL1.value)
        data.setdefault("current_approval_level", 1)
        data.setdefault("total_approval_levels", 2)

        obj = await ActivityApplyCRUD(auth).create_crud(data=data)
        log.info(f"创建活动申请成功: {obj.id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新活动申请

        只有 pending 或 pending_level1 状态（即一级审批前）才允许编辑
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status not in _EDITABLE_STATUSES:
            raise CustomException(msg="只有待审批状态的申请可以编辑")

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
        """删除活动申请"""
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status == ApprovalStatus.APPROVED.value:
            raise CustomException(msg="已批准的申请无法删除")

        await ActivityApplyCRUD(auth).delete_crud(id=id)
        log.info(f"删除活动申请成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """批量删除活动申请"""
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
        审批通过（多级）

        一级审批通过 -> 进入二级审批(pending_level2)
        二级审批通过 -> 最终批准(approved)
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status not in _APPROVABLE_STATUSES:
            raise CustomException(msg="当前状态无法审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None
        now = datetime.now()

        # 判断当前处于哪个审批级别
        status = existing.approval_status
        if status in (ApprovalStatus.PENDING.value, ApprovalStatus.PENDING_LEVEL1.value):
            # 一级审批通过
            update_data = {
                "current_approval_level": 2,
                "approval_status": ApprovalStatus.PENDING_LEVEL2.value,
                "level1_approved_by": user_id,
                "level1_approved_by_name": user_name,
                "level1_approval_time": now,
                "level1_approval_comment": approval_comment,
            }
            record_data = {
                "activity_apply_id": id,
                "approval_level": 1,
                "approval_action": "approved",
                "approver_id": user_id,
                "approver_name": user_name,
                "approval_comment": approval_comment,
                "approval_time": now,
            }
        elif status == ApprovalStatus.PENDING_LEVEL2.value:
            # 二级审批通过（最终批准）
            update_data = {
                "current_approval_level": 2,
                "approval_status": ApprovalStatus.APPROVED.value,
                "approval_by": user_id,
                "approval_time": now,
                "approval_comment": approval_comment,
                "level2_approved_by": user_id,
                "level2_approved_by_name": user_name,
                "level2_approval_time": now,
                "level2_approval_comment": approval_comment,
            }
            record_data = {
                "activity_apply_id": id,
                "approval_level": 2,
                "approval_action": "approved",
                "approver_id": user_id,
                "approver_name": user_name,
                "approval_comment": approval_comment,
                "approval_time": now,
            }
        else:
            raise CustomException(msg="当前状态无法审批")

        # 写入审批记录
        await ApprovalRecordCRUD(auth).create_crud(data=record_data)

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批通过活动申请成功: {id}, 级别: {record_data['approval_level']}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        审批拒绝（可在任意待审批级别拒绝）
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        if existing.approval_status not in _APPROVABLE_STATUSES:
            raise CustomException(msg="当前状态无法审批")

        if not approval_comment:
            raise CustomException(msg="请填写审批意见")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None
        now = datetime.now()

        # 判断当前审批级别
        status = existing.approval_status
        current_level = existing.current_approval_level or 1

        update_data = {
            "approval_status": ApprovalStatus.REJECTED.value,
            "approval_by": user_id,
            "approval_time": now,
            "approval_comment": approval_comment,
        }

        # 写入对应级别的审批字段
        if current_level == 1 or status in (
            ApprovalStatus.PENDING.value,
            ApprovalStatus.PENDING_LEVEL1.value,
        ):
            update_data.update({
                "level1_approved_by": user_id,
                "level1_approved_by_name": user_name,
                "level1_approval_time": now,
                "level1_approval_comment": approval_comment,
            })
            reject_level = 1
        else:
            update_data.update({
                "level2_approved_by": user_id,
                "level2_approved_by_name": user_name,
                "level2_approval_time": now,
                "level2_approval_comment": approval_comment,
            })
            reject_level = 2

        # 写入审批记录
        await ApprovalRecordCRUD(auth).create_crud(
            data={
                "activity_apply_id": id,
                "approval_level": reject_level,
                "approval_action": "rejected",
                "approver_id": user_id,
                "approver_name": user_name,
                "approval_comment": approval_comment,
                "approval_time": now,
            }
        )

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批拒绝活动申请成功: {id}, 级别: {reject_level}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def cancel_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        取消活动申请

        允许从 pending/pending_level1/pending_level2/approved 取消
        """
        existing = await ActivityApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动申请不存在")

        cancellable_statuses = {
            ApprovalStatus.PENDING.value,
            ApprovalStatus.PENDING_LEVEL1.value,
            ApprovalStatus.PENDING_LEVEL2.value,
            ApprovalStatus.APPROVED.value,
        }

        if existing.approval_status not in cancellable_statuses:
            raise CustomException(msg="当前状态无法取消")

        update_data = {
            "approval_status": ApprovalStatus.CANCELLED.value,
        }

        obj = await ActivityApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"取消活动申请成功: {id}")
        return ActivityApplyOutSchema.model_validate(obj).model_dump()
