from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import InvoiceModel
from .schema import InvoiceCreateSchema, InvoiceUpdateSchema


class InvoiceCRUD(CRUDBase[InvoiceModel, InvoiceCreateSchema, InvoiceUpdateSchema]):
    """发票 CRUD —— 继承 CRUDBase 获得增删改查、软删除过滤、租户隔离、权限过滤"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化发票 CRUD

        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=InvoiceModel, auth=auth)

    async def get_by_order_id(self, order_id: int) -> InvoiceModel | None:
        """
        根据订单 ID 查询发票

        参数:
        - order_id (int): 订单 ID

        返回:
        - InvoiceModel | None: 发票对象，不存在返回 None
        """
        return await self.get(order_id=order_id)
