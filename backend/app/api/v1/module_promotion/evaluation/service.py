"""
表彰评优 - 服务层
"""
import json
import uuid
from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import EvaluationCRUD
from .model import EvaluationStatus, PromotionEvaluationModel
from .schema import (
    EvaluationOutSchema,
    EvaluationQuerySchema,
)


class EvaluationService:
    """
    表彰评优服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID

        返回:
        - dict: 表彰评优模型实例字典
        """
        obj = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该表彰记录不存在")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: EvaluationQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (EvaluationQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await EvaluationCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的表彰评优模型实例字典
        """
        evaluation_no = f"EV{uuid.uuid4().hex[:12].upper()}"
        data["evaluation_no"] = evaluation_no

        if "evidence_urls" in data and isinstance(data["evidence_urls"], list):
            data["evidence_urls"] = json.dumps(data["evidence_urls"])
        if "evidence_names" in data and isinstance(data["evidence_names"], list):
            data["evidence_names"] = json.dumps(data["evidence_names"])

        obj = await EvaluationCRUD(auth).create_crud(data=data)
        log.info(f"创建表彰评优成功: {obj.id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的表彰评优模型实例字典
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status not in [EvaluationStatus.DRAFT.value, EvaluationStatus.REJECTED.value]:
            raise CustomException(msg="只有草稿或已拒绝状态的记录可以编辑")

        if "evidence_urls" in data and isinstance(data["evidence_urls"], list):
            data["evidence_urls"] = json.dumps(data["evidence_urls"])
        if "evidence_names" in data and isinstance(data["evidence_names"], list):
            data["evidence_names"] = json.dumps(data["evidence_names"])

        obj = await EvaluationCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新表彰评优成功: {id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status == EvaluationStatus.APPROVED.value:
            raise CustomException(msg="已批准的记录无法删除")

        await EvaluationCRUD(auth).delete_crud(id=id)
        log.info(f"删除表彰评优成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 表彰评优ID列表
        """
        await EvaluationCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除表彰评优成功: {ids}")

    @classmethod
    async def submit_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        提交表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID

        返回:
        - dict: 更新后的表彰评优模型实例字典
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status != EvaluationStatus.DRAFT.value:
            raise CustomException(msg="只有草稿状态的记录可以提交")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "evaluation_status": EvaluationStatus.SUBMITTED.value,
            "submit_time": datetime.now(),
            "submitter_id": user_id,
            "submitter_name": user_name,
        }

        obj = await EvaluationCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"提交表彰评优成功: {id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def review_service(cls, auth: AuthSchema, id: int, review_comment: str | None = None) -> dict:
        """
        审核表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID
        - review_comment (str | None): 审核意见

        返回:
        - dict: 更新后的表彰评优模型实例字典
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status != EvaluationStatus.SUBMITTED.value:
            raise CustomException(msg="只有已提交的记录可以审核")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "evaluation_status": EvaluationStatus.REVIEWING.value,
            "review_comment": review_comment,
            "reviewer_id": user_id,
            "reviewer_name": user_name,
            "review_time": datetime.now(),
        }

        obj = await EvaluationCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审核表彰评优成功: {id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def approve_service(cls, auth: AuthSchema, id: int, approval_comment: str | None = None, reward_type: str | None = None, reward_amount: float | None = None) -> dict:
        """
        批准表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID
        - approval_comment (str | None): 批准意见
        - reward_type (str | None): 奖励类型
        - reward_amount (float | None): 奖励金额

        返回:
        - dict: 更新后的表彰评优模型实例字典
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status not in [EvaluationStatus.SUBMITTED.value, EvaluationStatus.REVIEWING.value]:
            raise CustomException(msg="只有已提交或审核中的记录可以批准")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "evaluation_status": EvaluationStatus.APPROVED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        if reward_type is not None:
            update_data["reward_type"] = reward_type
        if reward_amount is not None:
            update_data["reward_amount"] = reward_amount

        obj = await EvaluationCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"批准表彰评优成功: {id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        拒绝表彰评优

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 表彰评优ID
        - approval_comment (str): 拒绝意见

        返回:
        - dict: 更新后的表彰评优模型实例字典
        """
        existing = await EvaluationCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该表彰记录不存在")

        if existing.evaluation_status not in [EvaluationStatus.SUBMITTED.value, EvaluationStatus.REVIEWING.value]:
            raise CustomException(msg="只有已提交或审核中的记录可以拒绝")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "evaluation_status": EvaluationStatus.REJECTED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await EvaluationCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"拒绝表彰评优成功: {id}")
        return cls._format_evaluation_output(obj)

    @classmethod
    def _format_evaluation_output(cls, obj: PromotionEvaluationModel) -> dict:
        """格式化表彰评优输出"""
        result = EvaluationOutSchema.model_validate(obj).model_dump()

        for field in ["evidence_urls", "evidence_names"]:
            if result.get(field) and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []

        return result
