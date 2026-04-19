"""
活动打卡 - 服务层
"""
import json
import uuid
from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import CheckinCRUD
from .model import CheckinStatus, PromotionCheckinModel
from .schema import (
    CheckinCreateSchema,
    CheckinOutSchema,
    CheckinQuerySchema,
    CheckinUpdateSchema,
)


class CheckinService:
    """
    活动打卡服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动打卡ID

        返回:
        - dict: 活动打卡模型实例字典
        """
        obj = await CheckinCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该活动打卡不存在")
        return cls._format_checkin_output(obj)

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: CheckinQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (CheckinQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await CheckinCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建活动打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的活动打卡模型实例字典
        """
        checkin_no = f"CK{uuid.uuid4().hex[:12].upper()}"
        data["checkin_no"] = checkin_no

        if "checkin_images" in data and isinstance(data["checkin_images"], list):
            data["checkin_images"] = json.dumps(data["checkin_images"])

        obj = await CheckinCRUD(auth).create_crud(data=data)
        log.info(f"创建活动打卡成功: {obj.id}")
        return cls._format_checkin_output(obj)

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新活动打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动打卡ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的活动打卡模型实例字典
        """
        existing = await CheckinCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动打卡不存在")

        if "checkin_images" in data and isinstance(data["checkin_images"], list):
            data["checkin_images"] = json.dumps(data["checkin_images"])

        obj = await CheckinCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新活动打卡成功: {id}")
        return cls._format_checkin_output(obj)

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除活动打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动打卡ID
        """
        existing = await CheckinCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动打卡不存在")

        await CheckinCRUD(auth).delete_crud(id=id)
        log.info(f"删除活动打卡成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除活动打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 活动打卡ID列表
        """
        await CheckinCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除活动打卡成功: {ids}")

    @classmethod
    async def validate_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        验证打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动打卡ID

        返回:
        - dict: 更新后的活动打卡模型实例字典
        """
        existing = await CheckinCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动打卡不存在")

        if existing.checkin_status == CheckinStatus.VALIDATED.value:
            raise CustomException(msg="该打卡已验证")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "checkin_status": CheckinStatus.VALIDATED.value,
            "validated_by": user_id,
            "validated_by_name": user_name,
            "validated_time": datetime.now(),
        }

        obj = await CheckinCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"验证打卡成功: {id}")
        return cls._format_checkin_output(obj)

    @classmethod
    async def invalidate_service(cls, auth: AuthSchema, id: int, reason: str) -> dict:
        """
        无效打卡

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 活动打卡ID
        - reason (str): 无效原因

        返回:
        - dict: 更新后的活动打卡模型实例字典
        """
        existing = await CheckinCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该活动打卡不存在")

        if existing.checkin_status == CheckinStatus.INVALID.value:
            raise CustomException(msg="该打卡已无效")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "checkin_status": CheckinStatus.INVALID.value,
            "validated_by": user_id,
            "validated_by_name": user_name,
            "validated_time": datetime.now(),
            "remark": reason,
        }

        obj = await CheckinCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"无效打卡成功: {id}")
        return cls._format_checkin_output(obj)

    @classmethod
    def _format_checkin_output(cls, obj: PromotionCheckinModel) -> dict:
        """格式化打卡输出"""
        result = CheckinOutSchema.model_validate(obj).model_dump()
        if result.get("checkin_images") and isinstance(result["checkin_images"], str):
            try:
                result["checkin_images"] = json.loads(result["checkin_images"])
            except json.JSONDecodeError:
                result["checkin_images"] = []
        return result