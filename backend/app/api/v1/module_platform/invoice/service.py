import json
import random
from datetime import date, datetime, timedelta

from app.api.v1.module_platform.order.crud import OrderCRUD
from app.core.base_schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import logger

from .crud import InvoiceCRUD
from .pdf_helper import _render_invoice_pdf, _render_oss_license_pdf
from .schema import (
    InvoiceApplySchema,
    InvoiceCreateSchema,
    InvoiceOutSchema,
    InvoiceQueryParam,
    InvoiceUpdateSchema,
    InvoiceVoidSchema,
)

_INVOICE_TYPE_LABEL = {
    "vat_normal": "电子普通发票",
    "vat_special": "增值税专用发票",
}


def _generate_invoice_no() -> str:
    """
    生成发票编号

    返回:
    - str: 形如 INV20250620123456 的发票编号
    """
    today = date.today().strftime("%Y%m%d")
    suffix = str(random.randint(100000, 999999))
    return f"INV{today}{suffix}"


class InvoiceTenantService:
    """租户端发票服务"""

    @classmethod
    async def apply(cls, auth: AuthSchema, data: InvoiceApplySchema, tenant_id: int) -> InvoiceOutSchema:
        """
        租户申请开票

        参数:
        - auth (AuthSchema): 认证信息模型
        - data (InvoiceApplySchema): 发票申请参数
        - tenant_id (int): 租户 ID

        返回:
        - InvoiceOutSchema: 发票信息
        """
        # 校验：专票必填字段
        if data.invoice_type == "vat_special":
            if not data.tax_no:
                raise CustomException(msg="增值税专用发票必须填写纳税人识别号")
            if not data.bank_info:
                raise CustomException(msg="增值税专用发票必须填写开户行及账号")
            if not data.address_info:
                raise CustomException(msg="增值税专用发票必须填写注册地址及电话")

        # 校验：订单存在且已支付
        order = await OrderCRUD(auth).get(id=data.order_id)
        if not order:
            raise CustomException(msg="订单不存在")
        if order.status != 1:
            raise CustomException(msg="仅已支付订单可申请开票")

        # 校验：30 天内
        if order.created_time and datetime.now() - order.created_time > timedelta(days=30):
            raise CustomException(msg="订单支付超过 30 天，不可申请开票")

        crud = InvoiceCRUD(auth)
        existing = await crud.get_by_order_id(data.order_id)
        if existing:
            raise CustomException(msg="该订单已申请过发票")

        tax_rate = 0  # 默认税率0%，未来可从套餐配置读取
        tax_amount = int(order.amount * tax_rate / 100)
        invoice = await crud.create(
            InvoiceCreateSchema(
                invoice_no=_generate_invoice_no(),
                order_id=data.order_id,
                tenant_id=tenant_id,
                invoice_type=data.invoice_type,
                title=data.title,
                tax_no=data.tax_no,
                bank_info=data.bank_info,
                address_info=data.address_info,
                amount=order.amount,
                tax_amount=tax_amount,
                description=data.description,
            )
        )
        logger.info(f"发票申请成功: invoice_no={invoice.invoice_no}, order_id={data.order_id}")
        return InvoiceOutSchema.model_validate(invoice)

    @classmethod
    async def list_my(
        cls,
        auth: AuthSchema,
        tenant_id: int,
        page_no: int,
        page_size: int,
        search: InvoiceQueryParam,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        租户查询自己的发票列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - tenant_id (int): 租户 ID
        - page_no (int): 当前页码
        - page_size (int): 每页数量
        - search (InvoiceQueryParam): 查询参数
        - order_by (list[dict] | None): 排序字段

        返回:
        - dict: 分页数据
        """
        _search: dict = {"tenant_id": tenant_id}
        if search.invoice_type:
            _search["invoice_type"] = search.invoice_type
        if search.status is not None:
            _search["status"] = search.status
        return await InvoiceCRUD(auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"created_time": "desc"}],
            search=_search,
            out_schema=InvoiceOutSchema,
        )


    @classmethod
    async def download(cls, auth: AuthSchema, invoice_id: int, tenant_id: int) -> str:
        crud = InvoiceCRUD(auth)
        invoice = await crud.get_or_404(id=invoice_id, msg="发票不存在")
        if hasattr(invoice, "tenant_id") and invoice.tenant_id != tenant_id:
            raise CustomException(msg="发票不存在")
        if invoice.status != 1 or not invoice.pdf_url:
            raise CustomException(msg="发票未开具或无PDF")
        return invoice.pdf_url

    @classmethod
    async def download_license(cls, auth: AuthSchema, invoice_id: int, tenant_id: int) -> str:
        crud = InvoiceCRUD(auth)
        invoice = await crud.get_or_404(id=invoice_id, msg="发票不存在")
        if hasattr(invoice, "tenant_id") and invoice.tenant_id != tenant_id:
            raise CustomException(msg="发票不存在")
        if not invoice.oss_license_pdf_url:
            raise CustomException(msg="开源授权函 PDF 不存在，请先开票")
        return invoice.oss_license_pdf_url


class InvoicePlatformService:
    """平台端发票服务"""

    @classmethod
    async def list_all(
        cls,
        auth: AuthSchema,
        page_no: int,
        page_size: int,
        search: InvoiceQueryParam,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        """
        平台查询全部发票列表

        参数:
        - auth (AuthSchema): 认证信息模型
        - page_no (int): 当前页码
        - page_size (int): 每页数量
        - search (InvoiceQueryParam): 查询参数
        - order_by (list[dict] | None): 排序字段

        返回:
        - dict: 分页数据
        """
        _search: dict = {}
        if search.invoice_type:
            _search["invoice_type"] = search.invoice_type
        if search.status is not None:
            _search["status"] = search.status
        if search.tenant_id:
            _search["tenant_id"] = search.tenant_id
        return await InvoiceCRUD(auth).page(
            offset=(page_no - 1) * page_size,
            limit=page_size,
            order_by=order_by or [{"created_time": "desc"}],
            search=_search,
            out_schema=InvoiceOutSchema,
        )

    @classmethod
    async def issue(
        cls,
        auth: AuthSchema,
        invoice_id: int,
        pdf_url: str,
        api_response: str,
        oss_license_pdf_url: str = "",
    ) -> InvoiceOutSchema:
        """
        平台开具发票

        参数:
        - auth (AuthSchema): 认证信息模型
        - invoice_id (int): 发票 ID
        - pdf_url (str): PDF 下载地址
        - api_response (str): 第三方 API 响应
        - oss_license_pdf_url (str): 授权函 PDF 地址（手动模式可空，自动模式自动渲染）

        返回:
        - InvoiceOutSchema: 发票信息
        """
        crud = InvoiceCRUD(auth)
        invoice = await crud.get(id=invoice_id)
        if not invoice:
            raise CustomException(msg="发票不存在")
        if invoice.status != 0:
            raise CustomException(msg="仅待开票状态可操作")

        # 调用开票服务：本地 WeasyPrint 渲染发票 PDF + 开源授权函 PDF（独立两个文件）
        try:
            pdf_url_result = _render_invoice_pdf(invoice)
            oss_license_pdf_url_result = _render_oss_license_pdf(invoice)
            api_response_result = json.dumps(
                {
                    "code": "SUCCESS",
                    "msg": "本地开票成功",
                    "invoice_no": invoice.invoice_no,
                    "engine": "weasyprint",
                },
                ensure_ascii=False,
            )
        except Exception as e:
            api_response_result = json.dumps(
                {
                    "code": "FAIL",
                    "msg": f"PDF 渲染失败: {e!s}",
                    "invoice_no": invoice.invoice_no,
                },
                ensure_ascii=False,
            )
            invoice = await crud.update(invoice_id, InvoiceUpdateSchema(status=2, api_response=api_response_result))
            logger.error(f"开票失败: invoice_no={invoice.invoice_no}, err={e!s}")
            raise CustomException(msg=f"开票失败: {e!s}") from e

        invoice = await crud.update(
            invoice_id,
            InvoiceUpdateSchema(
                status=1,
                pdf_url=pdf_url or pdf_url_result,
                oss_license_pdf_url=oss_license_pdf_url or oss_license_pdf_url_result,
                api_response=api_response or api_response_result,
            ),
        )
        logger.info(f"发票开具成功: invoice_no={invoice.invoice_no}")
        return InvoiceOutSchema.model_validate(invoice)

    @classmethod
    async def void(cls, auth: AuthSchema, invoice_id: int, data: InvoiceVoidSchema) -> InvoiceOutSchema:
        """
        平台作废发票

        参数:
        - auth (AuthSchema): 认证信息模型
        - invoice_id (int): 发票 ID
        - data (InvoiceVoidSchema): 作废参数（含作废原因）

        返回:
        - InvoiceOutSchema: 发票信息
        """
        crud = InvoiceCRUD(auth)
        invoice = await crud.get(id=invoice_id)
        if not invoice:
            raise CustomException(msg="发票不存在")
        if invoice.status != 1:
            code_text = {0: "待开票", 2: "开票失败", 3: "已作废"}.get(invoice.status, "未知")
            raise CustomException(msg=f"仅已开票状态可作废，当前状态: {code_text}")
        description = data.description or ""
        invoice = await crud.update(invoice_id, InvoiceUpdateSchema(status=3, description=description))
        logger.info(f"发票作废: invoice_no={invoice.invoice_no}")
        return InvoiceOutSchema.model_validate(invoice)
