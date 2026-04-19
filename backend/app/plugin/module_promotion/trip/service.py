"""
行程报备 - 服务层
"""
import uuid
from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import TripCRUD
from .model import PromotionTripModel, TripStatus
from .schema import (
    TripCreateSchema,
    TripOutSchema,
    TripQuerySchema,
    TripUpdateSchema,
)


class TripService:
    """
    行程报备服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID

        返回:
        - dict: 行程报备模型实例字典
        """
        obj = await TripCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该行程报备不存在")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: TripQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (TripQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await TripCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建行程报备

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的行程报备模型实例字典
        """
        trip_no = f"T{uuid.uuid4().hex[:12].upper()}"
        data["trip_no"] = trip_no

        obj = await TripCRUD(auth).create_crud(data=data)
        log.info(f"创建行程报备成功: {obj.id}")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新行程报备

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的行程报备模型实例字典
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        obj = await TripCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新行程报备成功: {id}")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除行程报备

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        await TripCRUD(auth).delete_crud(id=id)
        log.info(f"删除行程报备成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除行程报备

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 行程报备ID列表
        """
        await TripCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除行程报备成功: {ids}")

    @classmethod
    async def start_trip_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        开始行程

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID

        返回:
        - dict: 更新后的行程报备模型实例字典
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        if existing.trip_status != TripStatus.PLANNED.value:
            raise CustomException(msg="只有计划中的行程可以开始")

        update_data = {"trip_status": TripStatus.IN_PROGRESS.value}
        obj = await TripCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"开始行程成功: {id}")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def complete_trip_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        完成行程

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID

        返回:
        - dict: 更新后的行程报备模型实例字典
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        if existing.trip_status != TripStatus.IN_PROGRESS.value:
            raise CustomException(msg="只有进行中的行程可以完成")

        update_data = {"trip_status": TripStatus.COMPLETED.value}
        obj = await TripCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"完成行程成功: {id}")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def cancel_trip_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        取消行程

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID

        返回:
        - dict: 更新后的行程报备模型实例字典
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        if existing.trip_status == TripStatus.COMPLETED.value:
            raise CustomException(msg="已完成的行程无法取消")

        update_data = {"trip_status": TripStatus.CANCELLED.value}
        obj = await TripCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"取消行程成功: {id}")
        return TripOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_location_service(cls, auth: AuthSchema, id: int, latitude: float, longitude: float, address: str | None = None) -> dict:
        """
        更新位置

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 行程报备ID
        - latitude (float): 纬度
        - longitude (float): 经度
        - address (str | None): 地址

        返回:
        - dict: 更新后的行程报备模型实例字典
        """
        existing = await TripCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该行程报备不存在")

        if not existing.enable_location_sharing:
            raise CustomException(msg="该行程未启用位置共享")

        update_data = {
            "last_location_time": datetime.now(),
            "last_latitude": latitude,
            "last_longitude": longitude,
            "last_location_address": address,
        }
        obj = await TripCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"更新位置成功: {id}")
        return TripOutSchema.model_validate(obj).model_dump()