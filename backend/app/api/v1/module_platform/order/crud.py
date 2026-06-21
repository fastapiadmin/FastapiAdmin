"""订单与支付 CRUD"""

from typing import Any

from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import OrderModel, PaymentRecordModel, RefundModel
from .schema import (
    OrderCreateInternalSchema,
    OrderUpdateInternalSchema,
    PaymentRecordCreateSchema,
    RefundCreateSchema,
    RefundUpdateSchema,
)


class OrderCRUD(CRUDBase[OrderModel, OrderCreateInternalSchema, OrderUpdateInternalSchema]):
    """订单 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=OrderModel, auth=auth)

    async def get_by_order_no(self, order_no: str) -> OrderModel | None:
        return await self.get(order_no=order_no)

    async def query(
        self,
        *,
        tenant_id: int | None = None,
        status: int | None = None,
        order_type: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[OrderModel], int]:
        result = await self.page(
            search={"tenant_id": tenant_id, "status": status, "order_type": order_type},
            order_by=[{"created_time": "desc"}],
            offset=offset,
            limit=limit,
        )
        return result.items, result.total

    async def mark_refunded(self, order_id: int) -> None:
        from sqlalchemy import update as sa_update

        await self.db.execute(
            sa_update(OrderModel)
            .where(OrderModel.id == order_id)
            .where(OrderModel.is_deleted == False)  # noqa: E712
            .values(status=3)
        )


class PaymentRecordCRUD(CRUDBase[PaymentRecordModel, PaymentRecordCreateSchema, Any]):
    """支付记录 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=PaymentRecordModel, auth=auth)

    async def query(self, offset: int = 0, limit: int = 20) -> tuple[list[PaymentRecordModel], int]:
        result = await self.page(
            order_by=[{"created_time": "desc"}],
            offset=offset,
            limit=limit,
            search={},
        )
        return result.items, result.total


class RefundCRUD(CRUDBase[RefundModel, RefundCreateSchema, RefundUpdateSchema]):
    """退款 CRUD"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=RefundModel, auth=auth)

    async def get_by_order_id(self, order_id: int) -> RefundModel | None:
        return await self.get(order_id=order_id)

    async def query(self, status: int | None = None, offset: int = 0, limit: int = 20) -> tuple[list[RefundModel], int]:
        result = await self.page(
            search={"status": status},
            order_by=[{"created_time": "desc"}],
            offset=offset,
            limit=limit,
        )
        return result.items, result.total
