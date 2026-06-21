import random
from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.utils.payment import create_payment_gateway

from .crud import OrderCRUD, PaymentRecordCRUD, RefundCRUD
from .model import OrderModel
from .schema import (
    OrderCreateInternalSchema,
    OrderCreateSchema,
    OrderOutSchema,
    OrderQueryParam,
    OrderStatusMessage,
    OrderUpdateInternalSchema,
    PaymentCreateOut,
    PaymentRecordCreateSchema,
    PaymentRecordOutSchema,
    PaymentStatusOut,
    RefundApplySchema,
    RefundCreateSchema,
    RefundOutSchema,
    RefundReviewSchema,
    RefundUpdateSchema,
)


def _generate_order_no() -> str:
    """生成订单号：YYYYMMDD + 6位随机数"""
    today = datetime.now().strftime("%Y%m%d")
    suffix = str(random.randint(100000, 999999))
    return f"{today}{suffix}"


def _generate_refund_no() -> str:
    """生成退款单号"""
    today = datetime.now().strftime("%Y%m%d")
    suffix = str(random.randint(100000, 999999))
    return f"RF{today}{suffix}"


class OrderService:
    """
    订单管理服务
    """

    @classmethod
    async def create_order(cls, auth: AuthSchema, data: OrderCreateSchema, amount: int | None = None) -> OrderOutSchema:
        """
        创建订单

        套餐订单：amount 从套餐价格自动计算
        插件订单：amount 从插件价格自动计算
        免费订单（amount=0）：自动激活

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (OrderCreateSchema): 订单创建模型
        - amount (int | None): 订单金额(分)，None 时自动计算

        返回:
        - OrderOutSchema: 新创建的订单详情
        """
        if amount is None:
            if data.order_type == "plugin":
                from app.api.v1.module_platform.plugin.model import PluginModel

                plugin = await auth.db.get(PluginModel, data.plugin_id)
                amount = plugin.price if plugin else 0
            else:
                from app.api.v1.module_platform.package.model import PackageModel

                pkg = await auth.db.get(PackageModel, data.package_id)
                amount = pkg.price if pkg else 0

        order = await OrderCRUD(auth).create(
            OrderCreateInternalSchema(
                order_no=_generate_order_no(),
                tenant_id=data.tenant_id,
                package_id=data.package_id,
                plugin_id=data.plugin_id,
                order_type=data.order_type,
                amount=amount,
                expire_time=datetime.now() + timedelta(minutes=15),
            )
        )

        # 免费订单自动激活
        if amount == 0:
            await OrderCRUD(auth).update(
                order.id,
                OrderUpdateInternalSchema(status=1, pay_method="free", pay_time=datetime.now()),
            )
            await PaymentService._activate_tenant_package(auth, order)
            await auth.db.refresh(order)

        return OrderOutSchema.model_validate(order)

    @classmethod
    async def get_detail(cls, auth: AuthSchema, order_id: int) -> OrderOutSchema | None:
        """
        订单详情

        参数:
        - auth (AuthSchema): 认证信息模型
        - order_id (int): 订单ID

        返回:
        - OrderOutSchema | None: 订单详情，不存在时返回 None
        """
        order = await OrderCRUD(auth).get_by_id(order_id)
        return OrderOutSchema.model_validate(order) if order else None

    @classmethod
    async def get_list(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: OrderQueryParam,
        order_by: list[dict[str, str]] | None = None,
    ) -> tuple[list, int]:
        """
        订单列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 当前页码
        - page_size (int): 每页数量
        - search (OrderQueryParam): 查询参数
        - order_by (list[dict] | None): 排序字段

        返回:
        - tuple[list, int]: (订单列表, 总数)
        """
        offset = (page_no - 1) * page_size
        rows, total = await OrderCRUD(auth).query(
            tenant_id=search.tenant_id,
            status=search.status,
            order_type=search.order_type,
            offset=offset,
            limit=page_size,
        )
        items = [OrderOutSchema.model_validate(r) for r in rows]
        return items, total

    @classmethod
    async def cancel_order(cls, auth: AuthSchema, order_id: int) -> OrderStatusMessage:
        """
        取消订单

        参数:
        - auth (AuthSchema): 认证信息模型
        - order_id (int): 订单ID

        返回:
        - OrderStatusMessage: 取消结果
        """
        crud = OrderCRUD(auth)
        order = await crud.get_by_id(order_id)
        if not order:
            raise CustomException(msg="该数据不存在")
        if order.status != 0:
            raise CustomException(msg="仅待支付订单可取消")
        await crud.update(order_id, OrderUpdateInternalSchema(status=2))
        return OrderStatusMessage(id=order.id, status=2, message="已取消")

    @classmethod
    async def check_payment_status(cls, auth: AuthSchema, order_id: int) -> PaymentStatusOut:
        """
        查询订单支付状态（供前端轮询用）

        参数:
        - auth (AuthSchema): 认证信息模型
        - order_id (int): 订单ID

        返回:
        - PaymentStatusOut: 支付状态信息
        """
        order = await OrderCRUD(auth).get_by_id(order_id)
        if not order:
            return PaymentStatusOut(exists=False)
        return PaymentStatusOut(
            exists=True,
            order_id=order.id,
            status=order.status,
            paid=order.status == 1,
            pay_method=order.pay_method,
            pay_time=order.pay_time.isoformat() if order.pay_time else None,
        )

    @staticmethod
    async def cancel_expired_orders() -> None:
        from sqlalchemy import update as sa_update

        from app.core.database import async_db_session

        now = datetime.now()
        async with async_db_session() as session:
            async with session.begin():
                result = await session.execute(
                    sa_update(OrderModel)
                    .where(OrderModel.status == 0)
                    .where(OrderModel.expire_time < now)
                    .where(OrderModel.is_deleted == False)  # noqa: E712
                    .values(status=2)
                )
            logger.info(f"超时订单取消: 已取消 {result.rowcount} 条订单")


class PaymentService:
    """
    支付管理服务
    """

    @classmethod
    async def create_payment(cls, auth: AuthSchema, order_id: int, method: str, notify_base_url: str) -> PaymentCreateOut:
        """
        创建支付（调用支付网关）

        参数:
        - auth (AuthSchema): 认证信息模型
        - order_id (int): 订单ID
        - method (str): 支付方式(alipay/wxpay)
        - notify_base_url (str): 回调基础URL

        返回:
        - PaymentCreateOut: 支付创建结果（支付URL/二维码）
        """
        from app.api.v1.module_platform.package.model import PackageModel

        order = await OrderCRUD(auth).get_by_id(order_id)
        if not order:
            raise CustomException(msg="该数据不存在")
        if order.status != 0:
            raise CustomException(msg="订单状态异常，无法支付")
        if order.amount <= 0:
            raise CustomException(msg="免费订单无需支付")

        if order.order_type == "plugin":
            from app.api.v1.module_platform.plugin.model import PluginModel

            plugin = await auth.db.get(PluginModel, order.plugin_id)
            subject = f"FastapiAdmin - 插件 {plugin.name}" if plugin else "FastapiAdmin 插件"
        else:
            pkg = await auth.db.get(PackageModel, order.package_id)
            subject = f"FastapiAdmin - {pkg.name}" if pkg else "FastapiAdmin 套餐"

        notify_url = f"{notify_base_url}/api/v1/platform/payment/callback/{method}" if method else ""

        gateway = create_payment_gateway(method)
        info = await gateway.create_payment(
            order_no=order.order_no,
            amount=order.amount,
            subject=subject,
            notify_url=notify_url,
        )
        return PaymentCreateOut(
            pay_url=info.pay_url,
            qr_code_url=info.qr_code_url,
            trade_no=info.trade_no,
            order_id=order.id,
            order_no=order.order_no,
            amount=order.amount,
        )

    @classmethod
    async def handle_callback(cls, auth: AuthSchema, method: str, callback_data: dict) -> dict:
        """
        处理支付回调

        参数:
        - auth (AuthSchema): 认证信息模型
        - method (str): 支付方式
        - callback_data (dict): 支付网关回调数据

        返回:
        - dict: 处理结果
        """
        gateway = create_payment_gateway(method)
        callback_result = await gateway.verify_callback(callback_data)

        if not callback_result.verified:
            logger.warning(f"支付回调验签失败: method={method} data={callback_data}")
            raise CustomException(msg="支付回调验签失败")

        order_no = callback_data.get("order_no") or callback_data.get("out_trade_no", "")
        o_crud = OrderCRUD(auth)
        order = None
        if order_no:
            order = await o_crud.get_by_order_no(order_no)
        elif callback_result.order_id:
            order = await o_crud.get_by_id(callback_result.order_id)

        if not order:
            raise CustomException(msg="该数据不存在")
        if order.status != 0:
            raise CustomException(msg="订单状态异常")
        if order.amount != callback_result.amount and callback_result.amount > 0:
            raise CustomException(msg="金额不一致")

        pid = order.package_id
        tid = order.tenant_id
        otype = order.order_type
        oid = order.id

        await o_crud.update(
            oid,
            OrderUpdateInternalSchema(status=1, pay_method=method, pay_time=datetime.now()),
        )

        await PaymentRecordCRUD(auth).create(
            PaymentRecordCreateSchema(
                order_id=oid,
                transaction_id=callback_result.transaction_id,
                pay_method=method,
                amount=callback_result.amount,
                raw_response=str(callback_result.raw) if callback_result.raw else None,
                pay_time=datetime.now(),
            )
        )

        order.package_id = pid
        order.tenant_id = tid
        order.order_type = otype
        await PaymentService._activate_tenant_package(auth, order)

        logger.info(f"支付回调处理完成: order_id={oid} method={method} tenant_id={tid} type={otype}")
        return {"order_id": oid, "status": 1, "message": "支付成功"}

    @classmethod
    async def _activate_tenant_package(cls, auth: AuthSchema, order: OrderModel) -> None:
        """
        支付成功后激活套餐

        参数:
        - auth (AuthSchema): 认证信息模型
        - order (OrderModel): 订单模型

        返回:
        - None
        """
        from app.api.v1.module_platform.package.model import PackageModel
        from app.api.v1.module_platform.tenant.model import TenantModel

        if order.order_type == "plugin":
            await PaymentService._activate_plugin(auth, order)
            return

        pkg = await auth.db.get(PackageModel, order.package_id)
        if not pkg:
            logger.warning(f"支付回调：套餐 {order.package_id} 不存在，跳过激活")
            return

        tenant = await auth.db.get(TenantModel, order.tenant_id)
        if not tenant:
            logger.warning(f"支付回调：租户 {order.tenant_id} 不存在，跳过激活")
            return

        now = datetime.now()
        period_months = order.period_count or 1
        duration = timedelta(days=30 * period_months)

        if order.order_type == "new":
            tenant.package_id = order.package_id
            tenant.start_time = now
            tenant.end_time = now + duration
            tenant.status = 0
            logger.info(f"租户[{tenant.name}]新开通 {pkg.name}，有效期至 {tenant.end_time}")

        elif order.order_type == "renew":
            base = tenant.end_time if tenant.end_time and tenant.end_time > now else now
            tenant.end_time = base + duration
            tenant.status = 0
            logger.info(f"租户[{tenant.name}]续费 {pkg.name}，续至 {tenant.end_time}")

        elif order.order_type in ("upgrade", "downgrade"):
            if order.order_type == "downgrade":
                await PaymentService._check_downgrade_quota(auth, order.tenant_id, pkg)
            tenant.package_id = order.package_id
            tenant.status = 0
            logger.info(f"租户[{tenant.name}]套餐变更 {'升级' if order.order_type == 'upgrade' else '降级'} → {pkg.name}")

        await auth.db.flush()

        if tenant.contact_email:
            await PaymentService._send_order_email(auth, order, pkg, tenant)

    @classmethod
    async def _activate_plugin(cls, auth: AuthSchema, order: OrderModel) -> None:
        """
        支付成功后标记插件为已购买

        参数:
        - auth (AuthSchema): 认证信息模型
        - order (OrderModel): 订单模型

        返回:
        - None
        """
        from app.api.v1.module_platform.plugin.model import PluginModel, TenantPluginModel

        plugin = await auth.db.get(PluginModel, order.plugin_id)
        if not plugin:
            logger.warning(f"支付回调：插件 {order.plugin_id} 不存在")
            return

        result = await auth.db.execute(
            select(TenantPluginModel)
            .where(
                TenantPluginModel.tenant_id == order.tenant_id,
                TenantPluginModel.plugin_id == order.plugin_id,
            )
            .limit(1)
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.purchased = "1"
        else:
            tp = TenantPluginModel(
                tenant_id=order.tenant_id,
                plugin_id=order.plugin_id,
                purchased="1",
                enabled="0",
                installed_time=datetime.now(),
            )
            auth.db.add(tp)

        await auth.db.flush()
        logger.info(f"租户[{order.tenant_id}]已购买插件[{plugin.name}]")

        from app.api.v1.module_platform.tenant.model import TenantModel

        tenant = await auth.db.get(TenantModel, order.tenant_id)
        if tenant and tenant.contact_email:
            await PaymentService._send_order_email(auth, order, plugin, tenant, order_type_label="购买")

    @classmethod
    async def _check_downgrade_quota(cls, auth: AuthSchema, tenant_id: int, new_pkg: object) -> None:
        """
        降级前检查：租户当前资源数是否超过新套餐限额

        参数:
        - auth (AuthSchema): 认证信息模型
        - tenant_id (int): 租户ID
        - new_pkg (object): 目标套餐

        返回:
        - None
        """
        from sqlalchemy import func, select

        from app.api.v1.module_system.dept.model import DeptModel
        from app.api.v1.module_system.role.model import RoleModel
        from app.api.v1.module_system.user.model import UserModel

        checks = {
            "用户": (UserModel, new_pkg.max_users),
            "角色": (RoleModel, new_pkg.max_roles),
            "部门": (DeptModel, new_pkg.max_depts),
        }

        for label, (model, limit) in checks.items():
            if limit <= 0:
                continue
            count_stmt = (
                select(func.count())
                .select_from(model)
                .where(
                    model.tenant_id == tenant_id,
                    model.is_deleted.is_(False),
                )
            )
            result = await auth.db.execute(count_stmt)
            current = result.scalar() or 0
            if current > limit:
                raise CustomException(msg=f"降级失败：当前租户已有 {current} 个{label}，超过目标套餐限额 {limit}")

    @classmethod
    async def _send_order_email(cls, auth: AuthSchema, order: OrderModel, product: object, tenant: object, order_type_label: str = "") -> None:
        """
        发送购买确认邮件（失败静默降级）

        参数:
        - order (OrderModel): 订单模型
        - product (object): 商品(套餐/插件)
        - tenant (object): 租户模型
        - order_type_label (str): 订单类型文案

        返回:
        - None
        """
        try:
            from app.api.v1.module_platform.email.service import EmailSendService

            if not order_type_label:
                order_type_labels = {
                    "new": "开通",
                    "renew": "续费",
                    "upgrade": "升级",
                    "downgrade": "降级",
                    "plugin": "购买",
                }
                order_type_label = order_type_labels.get(order.order_type, order.order_type)

            product_name = getattr(product, "name", "") if product else ""
            amount_str = f"{order.amount / 100:.2f}" if order.amount else "0.00"

            await EmailSendService(auth).send_by_template(
                to_email=tenant.contact_email,
                to_name=tenant.contact_name or tenant.name,
                template_code="order_confirmation",
                variables={
                    "tenant_name": tenant.name,
                    "order_no": order.order_no,
                    "package_name": product_name,
                    "order_type": order_type_label,
                    "amount": amount_str,
                },
                biz_type="order",
                tenant_id=tenant.id,
            )
        except Exception:
            pass  # 邮件发送失败不阻塞业务流程

    @classmethod
    async def get_records(cls, auth: AuthSchema, offset: int, limit: int) -> tuple[list, int]:
        """
        支付记录列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - offset (int): 偏移量
        - limit (int): 每页数量

        返回:
        - tuple[list, int]: (支付记录列表, 总数)
        """
        rows, total = await PaymentRecordCRUD(auth).query(offset, limit)
        items = [PaymentRecordOutSchema.model_validate(r) for r in rows]
        return items, total


class RefundService:
    """
    退款管理服务
    """

    @classmethod
    async def apply(cls, auth: AuthSchema, data: RefundApplySchema, order_id: int) -> RefundOutSchema:
        """
        申请退款

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (RefundApplySchema): 退款申请模型
        - order_id (int): 订单ID

        返回:
        - RefundOutSchema: 退款记录详情
        """
        o_crud = OrderCRUD(auth)
        order = await o_crud.get_by_id(order_id)
        if not order:
            raise CustomException(msg="该数据不存在")
        if order.status != 1:
            raise CustomException(msg="仅已支付订单可退款")
        if order.amount == 0:
            raise CustomException(msg="免费套餐不支持退款")
        if order.pay_time and (datetime.now() - order.pay_time).days > 7:
            raise CustomException(msg="已超过 7 天退款时限")
        existing = await RefundCRUD(auth).get_by_order_id(order_id)
        if existing:
            raise CustomException(msg="已存在退款申请")
        refund = await RefundCRUD(auth).create(
            RefundCreateSchema(
                order_id=order.id,
                refund_no=_generate_refund_no(),
                amount=order.amount,
                reason=data.reason,
            )
        )
        return RefundOutSchema.model_validate(refund)

    @classmethod
    async def get_list(cls, auth: AuthSchema, status: int | None, offset: int, limit: int) -> tuple[list, int]:
        """
        退款列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - status (int | None): 退款状态筛选
        - offset (int): 偏移量
        - limit (int): 每页数量

        返回:
        - tuple[list, int]: (退款列表, 总数)
        """
        rows, total = await RefundCRUD(auth).query(status, offset, limit)
        items = [RefundOutSchema.model_validate(r) for r in rows]
        return items, total

    @classmethod
    async def approve(cls, auth: AuthSchema, refund_id: int, reviewer_id: int, operator_name: str = "") -> OrderStatusMessage:
        """
        批准退款

        参数:
        - auth (AuthSchema): 认证信息模型
        - refund_id (int): 退款ID
        - reviewer_id (int): 审核人ID
        - operator_name (str): 操作人名称

        返回:
        - OrderStatusMessage: 审核结果
        """
        crud = RefundCRUD(auth)
        refund = await crud.get_by_id(refund_id)
        if not refund:
            raise CustomException(msg="该数据不存在")
        if refund.status != 1:
            raise CustomException(msg="仅申请中可审核")
        await crud.update(
            refund_id,
            RefundUpdateSchema(status=2, reviewer_id=reviewer_id, review_time=datetime.now()),
        )
        await OrderCRUD(auth).mark_refunded(refund.order_id)
        return OrderStatusMessage(id=refund.id, status=2, message="已批准退款")

    @classmethod
    async def reject(
        cls,
        auth: AuthSchema,
        refund_id: int,
        reviewer_id: int,
        data: RefundReviewSchema,
        operator_name: str = "",
    ) -> OrderStatusMessage:
        """
        驳回退款

        参数:
        - auth (AuthSchema): 认证信息模型
        - refund_id (int): 退款ID
        - reviewer_id (int): 审核人ID
        - data (RefundReviewSchema): 驳回原因
        - operator_name (str): 操作人名称

        返回:
        - OrderStatusMessage: 审核结果
        """
        crud = RefundCRUD(auth)
        refund = await crud.get_by_id(refund_id)
        if not refund:
            raise CustomException(msg="该数据不存在")
        if refund.status != 1:
            raise CustomException(msg="仅申请中可审核")
        await crud.update(
            refund_id,
            RefundUpdateSchema(
                status=3,
                reviewer_id=reviewer_id,
                review_time=datetime.now(),
                reject_reason=data.reject_reason,
            ),
        )
        return OrderStatusMessage(id=refund.id, status=3, message="已驳回")
