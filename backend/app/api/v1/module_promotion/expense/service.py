"""
费用报销 - 服务层
"""

import uuid
from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import ExpenseCRUD
from .model import ExpenseStatus
from .schema import (
    ExpenseOutSchema,
    ExpenseQuerySchema,
)


class ExpenseService:
    """
    费用报销服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID

        返回:
        - dict: 费用报销模型实例字典
        """
        obj = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该费用报销不存在")
        return ExpenseOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: ExpenseQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (ExpenseQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await ExpenseCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建费用报销

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的费用报销模型实例字典
        """
        expense_no = f"EX{uuid.uuid4().hex[:12].upper()}"
        data["expense_no"] = expense_no

        obj = await ExpenseCRUD(auth).create_crud(data=data)
        log.info(f"创建费用报销成功: {obj.id}")
        return ExpenseOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新费用报销

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的费用报销模型实例字典
        """
        existing = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该费用报销不存在")

        if existing.approval_status != ExpenseStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的报销可以编辑")

        obj = await ExpenseCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新费用报销成功: {id}")
        return ExpenseOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除费用报销

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID
        """
        existing = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该费用报销不存在")

        if existing.approval_status == ExpenseStatus.REIMBURSED.value:
            raise CustomException(msg="已报销的报销单无法删除")

        await ExpenseCRUD(auth).delete_crud(id=id)
        log.info(f"删除费用报销成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除费用报销

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 费用报销ID列表
        """
        await ExpenseCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除费用报销成功: {ids}")

    @classmethod
    async def approve_service(
        cls, auth: AuthSchema, id: int, approval_comment: str | None = None
    ) -> dict:
        """
        审批通过

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID
        - approval_comment (str | None): 审批意见

        返回:
        - dict: 更新后的费用报销模型实例字典
        """
        existing = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该费用报销不存在")

        if existing.approval_status != ExpenseStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的报销可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "approval_status": ExpenseStatus.APPROVED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await ExpenseCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批通过费用报销成功: {id}")
        return ExpenseOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        审批拒绝

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID
        - approval_comment (str): 审批意见

        返回:
        - dict: 更新后的费用报销模型实例字典
        """
        existing = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该费用报销不存在")

        if existing.approval_status != ExpenseStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的报销可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "approval_status": ExpenseStatus.REJECTED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await ExpenseCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批拒绝费用报销成功: {id}")
        return ExpenseOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reimburse_service(
        cls, auth: AuthSchema, id: int, reimbursement_account: str | None = None
    ) -> dict:
        """
        报销

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 费用报销ID
        - reimbursement_account (str | None): 报销账户

        返回:
        - dict: 更新后的费用报销模型实例字典
        """
        existing = await ExpenseCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该费用报销不存在")

        if existing.approval_status != ExpenseStatus.APPROVED.value:
            raise CustomException(msg="只有已批准的报销可以报销")

        update_data = {
            "approval_status": ExpenseStatus.REIMBURSED.value,
            "reimburse_time": datetime.now(),
            "reimbursement_account": reimbursement_account,
        }

        obj = await ExpenseCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"报销成功: {id}")
        return ExpenseOutSchema.model_validate(obj).model_dump()
