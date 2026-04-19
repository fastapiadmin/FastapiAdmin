"""
物料管理 - 服务层
"""
import uuid
from datetime import datetime
from typing import Any

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import MaterialApplyCRUD, MaterialCRUD
from .model import ApplyStatus, MaterialStatus, PromotionMaterialApplyModel, PromotionMaterialModel
from .schema import (
    MaterialApplyCreateSchema,
    MaterialApplyOutSchema,
    MaterialApplyQuerySchema,
    MaterialApplyUpdateSchema,
    MaterialCreateSchema,
    MaterialOutSchema,
    MaterialQuerySchema,
    MaterialUpdateSchema,
)


class MaterialService:
    """
    物料管理服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料ID

        返回:
        - dict: 物料模型实例字典
        """
        obj = await MaterialCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该物料不存在")
        return MaterialOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: MaterialQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (MaterialQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await MaterialCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建物料

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的物料模型实例字典
        """
        obj = await MaterialCRUD(auth).create_crud(data=data)
        log.info(f"创建物料成功: {obj.id}")
        return MaterialOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: dict) -> dict:
        """
        更新物料

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料ID
        - data (dict): 更新数据

        返回:
        - dict: 更新后的物料模型实例字典
        """
        existing = await MaterialCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料不存在")

        obj = await MaterialCRUD(auth).update_crud(id=id, data=data)
        log.info(f"更新物料成功: {id}")
        return MaterialOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除物料

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料ID
        """
        existing = await MaterialCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料不存在")

        await MaterialCRUD(auth).delete_crud(id=id)
        log.info(f"删除物料成功: {id}")

    @classmethod
    async def batch_delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """
        批量删除物料

        参数:
        - auth (AuthSchema): 认证信息模型
        - ids (list[int]): 物料ID列表
        """
        await MaterialCRUD(auth).batch_delete_crud(ids=ids)
        log.info(f"批量删除物料成功: {ids}")

    @classmethod
    async def stock_change_service(cls, auth: AuthSchema, id: int, change_type: str, quantity: int) -> dict:
        """
        库存变动

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料ID
        - change_type (str): 变动类型(increase/decrease)
        - quantity (int): 变动数量

        返回:
        - dict: 更新后的物料模型实例字典
        """
        existing = await MaterialCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料不存在")

        if change_type == "increase":
            new_available = existing.available_stock + quantity
            new_total = existing.total_stock + quantity
        else:
            if existing.available_stock < quantity:
                raise CustomException(msg="可用库存不足")
            new_available = existing.available_stock - quantity
            new_total = existing.total_stock - quantity

        update_data = {
            "available_stock": new_available,
            "total_stock": new_total,
        }

        if new_available <= existing.low_stock_threshold:
            update_data["status"] = MaterialStatus.LOW_STOCK.value
        if new_available <= 0:
            update_data["status"] = MaterialStatus.OUT_OF_STOCK.value

        obj = await MaterialCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"库存变动成功: {id}, type={change_type}, quantity={quantity}")
        return MaterialOutSchema.model_validate(obj).model_dump()


class MaterialApplyService:
    """
    物料申请服务层
    """

    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> dict:
        """
        详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料申请ID

        返回:
        - dict: 物料申请模型实例字典
        """
        obj = await MaterialApplyCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该物料申请不存在")
        return MaterialApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: MaterialApplyQuerySchema | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        分页查询

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 页码
        - page_size (int): 每页数量
        - search (MaterialApplyQuerySchema | None): 查询参数
        - order_by (list[dict[str, str]] | None): 排序参数

        返回:
        - dict: 分页数据
        """
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{"display_order": "asc"}, {"id": "desc"}]
        offset = (page_no - 1) * page_size

        result = await MaterialApplyCRUD(auth).page_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict,
        )
        return result

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: dict) -> dict:
        """
        创建物料申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (dict): 创建数据

        返回:
        - dict: 创建的物料申请模型实例字典
        """
        apply_no = f"MA{uuid.uuid4().hex[:12].upper()}"
        data["apply_no"] = apply_no

        obj = await MaterialApplyCRUD(auth).create_crud(data=data)
        log.info(f"创建物料申请成功: {obj.id}")
        return MaterialApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def approve_service(cls, auth: AuthSchema, id: int, approved_quantity: int | None = None) -> dict:
        """
        审批通过

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料申请ID
        - approved_quantity (int | None): 批准数量

        返回:
        - dict: 更新后的物料申请模型实例字典
        """
        existing = await MaterialApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料申请不存在")

        if existing.apply_status != ApplyStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的申请可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "apply_status": ApplyStatus.APPROVED.value,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
            "approved_quantity": approved_quantity or existing.apply_quantity,
        }

        obj = await MaterialApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批通过物料申请成功: {id}")
        return MaterialApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def reject_service(cls, auth: AuthSchema, id: int, approval_comment: str) -> dict:
        """
        审批拒绝

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料申请ID
        - approval_comment (str): 审批意见

        返回:
        - dict: 更新后的物料申请模型实例字典
        """
        existing = await MaterialApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料申请不存在")

        if existing.apply_status != ApplyStatus.PENDING.value:
            raise CustomException(msg="只有待审批状态的申请可以审批")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        update_data = {
            "apply_status": ApplyStatus.REJECTED.value,
            "approval_comment": approval_comment,
            "approver_id": user_id,
            "approver_name": user_name,
            "approval_time": datetime.now(),
        }

        obj = await MaterialApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"审批拒绝物料申请成功: {id}")
        return MaterialApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def issue_service(cls, auth: AuthSchema, id: int, issued_quantity: int | None = None) -> dict:
        """
        发放物料

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料申请ID
        - issued_quantity (int | None): 发放数量

        返回:
        - dict: 更新后的物料申请模型实例字典
        """
        existing = await MaterialApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料申请不存在")

        if existing.apply_status != ApplyStatus.APPROVED.value:
            raise CustomException(msg="只有已批准的申请可以发放")

        user_id = auth.user.id if auth.user else None
        user_name = auth.user.name if auth.user else None

        issue_qty = issued_quantity or existing.approved_quantity or existing.apply_quantity

        update_data = {
            "apply_status": ApplyStatus.ISSUED.value,
            "issued_quantity": issue_qty,
            "issuer_id": user_id,
            "issuer_name": user_name,
            "issue_time": datetime.now(),
        }

        obj = await MaterialApplyCRUD(auth).update_crud(id=id, data=update_data)
        log.info(f"发放物料成功: {id}")
        return MaterialApplyOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_service(cls, auth: AuthSchema, id: int) -> None:
        """
        删除物料申请

        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 物料申请ID
        """
        existing = await MaterialApplyCRUD(auth).get_by_id_crud(id=id)
        if not existing:
            raise CustomException(msg="该物料申请不存在")

        await MaterialApplyCRUD(auth).delete_crud(id=id)
        log.info(f"删除物料申请成功: {id}")