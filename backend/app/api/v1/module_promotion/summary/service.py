"""
总结上传 - 服务层
"""
import json
import uuid
from datetime import datetime

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import SummaryCRUD
from .model import PromotionSummaryModel, SummaryStatus
from .schema import (
    SummaryOutSchema,
    SummaryQuerySchema,
)


class SummaryService:
    """
    总结上传服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结上传ID

        返回:
        - dict: 总结上传模型实例字典
        """
        obj = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该总结不存在")
        return cls._format_summary_output(obj)

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: SummaryQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (SummaryQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await SummaryCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建总结

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的总结模型实例字典
        """
        summary_no = f"SM{uuid.uuid4().hex[:12].upper()}"
        data["summary_no"] = summary_no

        if "attachment_urls" in data and isinstance(data["attachment_urls"], list):
            data["attachment_urls"] = json.dumps(data["attachment_urls"])
        if "attachment_names" in data and isinstance(data["attachment_names"], list):
            data["attachment_names"] = json.dumps(data["attachment_names"])

        obj = await SummaryCRUD(auth).create_crud(data=data)
        log.info(f"创建总结成功: {obj.id}")
        return cls._format_summary_output(obj)

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新总结

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的总结模型实例字典
        """
        existing = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该总结不存在")

        if existing.summary_status not in [SummaryStatus.DRAFT.value, SummaryStatus.REJECTED.value]:
            raise CustomException(msg="只有草稿或已拒绝状态的总结可以编辑")

        if "attachment_urls" in data and isinstance(data["attachment_urls"], list):
            data["attachment_urls"] = json.dumps(data["attachment_urls"])
        if "attachment_names" in data and isinstance(data["attachment_names"], list):
            data["attachment_names"] = json.dumps(data["attachment_names"])

        obj = await SummaryCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新总结成功: {id}")
        return cls._format_summary_output(obj)

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除总结

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结ID
        """
        existing = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该总结不存在")

        if existing.summary_status == SummaryStatus.APPROVED.value:
            raise CustomException(msg="已通过的总结无法删除")

        await SummaryCRUD(auth).delete_crud(id=id)
        log.info(f"删除总结成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除总结

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 总结ID列表
        """
        await SummaryCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除总结成功: {ids}")

    @classmethod
    async def submit_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        提交总结

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结ID

        返回:
        - dict: 更新后的总结模型实例字典
        """
        existing = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该总结不存在")

        if existing.summary_status != SummaryStatus.DRAFT.value:
            raise CustomException(msg="只有草稿状态的总结可以提交")

        update_data = {
            "summary_status": SummaryStatus.SUBMITTED.value,
            "submit_time": datetime.now(),
        }

        obj = await SummaryCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"提交总结成功: {id}")
        return cls._format_summary_output(obj)

    @classmethod
    async def approve_service(cls, auth: AuthSchema, id: int, approval_comment: str | None = None) -> dict:
        """
        审批通过

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结ID
        - approval_comment (str | None): 审批意见

        返回:
        - dict: 更新后的总结模型实例字典
        """
        existing = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该总结不存在")

        if existing.summary_status != SummaryStatus.SUBMITTED.value:
            raise CustomException(msg="只有已提交的总结可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "summary_status": SummaryStatus.APPROVED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await SummaryCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批通过总结成功: {id}")
        return cls._format_summary_output(obj)

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        审批拒绝

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 总结ID
        - approval_comment (str): 审批意见

        返回:
        - dict: 更新后的总结模型实例字典
        """
        existing = await SummaryCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该总结不存在")

        if existing.summary_status != SummaryStatus.SUBMITTED.value:
            raise CustomException(msg="只有已提交的总结可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "summary_status": SummaryStatus.REJECTED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await SummaryCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批拒绝总结成功: {id}")
        return cls._format_summary_output(obj)

    @classmethod
    def _format_summary_output(cls, obj: PromotionSummaryModel) -> dict:
        """格式化总结输出"""
        result = SummaryOutSchema.model_validate(obj).model_dump()

        for field in ["attachment_urls", "attachment_names"]:
            if result.get(field) and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except json.JSONDecodeError:
                    result[field] = []

        return result
