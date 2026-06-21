"""
invoice/pdf_helper.py — 发票 PDF 渲染辅助

使用 WeasyPrint + Jinja2 渲染符合中国电子发票样式的 PDF。
对接百望云/票通等第三方平台后，可替换此模块的内部实现。
"""

import hashlib
from datetime import datetime

from app.config.path_conf import INVOICE_DIR, TEMPLATE_DIR
from app.utils.pdf_generator import amount_to_cn_uppercase, amount_to_yuan, generate_pdf_from_template

from .oss_licenses_helper import load_oss_licenses
from .schema import InvoiceOutSchema

_INVOICE_TYPE_LABEL = {
    "vat_normal": "电子普通发票",
    "vat_special": "增值税专用发票",
}


def _render_invoice_pdf(invoice: InvoiceOutSchema) -> str:
    """
    渲染并保存电子发票 PDF

    参数:
    - invoice (InvoiceOutSchema): 发票对象

    返回:
    - str: PDF 的相对 URL 路径（形如 /static/invoice/{tenant_id}/{invoice_no}.pdf）
    """
    amount_yuan = float(amount_to_yuan(invoice.amount))
    tax_yuan = float(amount_to_yuan(invoice.tax_amount))
    total_yuan = amount_yuan + tax_yuan

    check_code_seed = f"{invoice.invoice_no}|{invoice.amount}|{invoice.invoice_type}"
    check_code = hashlib.md5(check_code_seed.encode()).hexdigest()[:20].upper()

    variables = {
        "invoice_no": invoice.invoice_no,
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "invoice_type": invoice.invoice_type,
        "invoice_type_label": _INVOICE_TYPE_LABEL.get(invoice.invoice_type, "电子发票"),
        "buyer_name": invoice.title,
        "buyer_tax_no": invoice.tax_no or "-",
        "buyer_address_info": invoice.address_info or "-",
        "buyer_bank_info": invoice.bank_info or "-",
        "seller_name": "FastapiAdmin 平台",
        "seller_tax_no": "91310115MA1K00000X",
        "seller_address_info": "上海市浦东新区张江高科技园区",
        "seller_bank_info": "招商银行上海分行 1234 5678 9012 3456",
        "items": [
            {
                "name": "FastapiAdmin 企业服务",
                "spec": "SaaS 订阅",
                "unit": "套",
                "quantity": "1",
                "unit_price": amount_to_yuan(invoice.amount),
                "amount": amount_to_yuan(invoice.amount),
                "tax_rate": 0,
                "tax_amount": amount_to_yuan(invoice.tax_amount),
            }
        ],
        "amount_total_yuan": f"{total_yuan:.2f}",
        "amount_cn_uppercase": amount_to_cn_uppercase(total_yuan),
        "remarks": invoice.description or f"订单号: {invoice.order_id}",
        "check_code": f"{check_code[:4]} {check_code[4:8]} {check_code[8:12]} {check_code[12:16]} {check_code[16:20]}",
        "issuer_name": "系统开票",
        "receiver_name": "-",
        "reviewer_name": "-",
    }

    output_dir = INVOICE_DIR / str(invoice.tenant_id)
    output_path = output_dir / f"{invoice.invoice_no}.pdf"
    generate_pdf_from_template(
        template_name="invoice/invoice.jinja2",
        template_dir=TEMPLATE_DIR,
        variables=variables,
        output_path=output_path,
    )
    return f"/static/invoice/{invoice.tenant_id}/{invoice.invoice_no}.pdf"


def _render_oss_license_pdf(invoice: InvoiceOutSchema) -> str:
    """
    渲染并保存开源项目授权声明函 PDF（与发票 PDF 独立存储）

    参数:
    - invoice (InvoiceOutSchema): 发票对象（用于在授权函中展示关联发票号）

    返回:
    - str: PDF 的相对 URL 路径（形如 /static/invoice/{tenant_id}/{invoice_no}_license.pdf）
    """
    groups = load_oss_licenses()
    total_packages = sum(len(g["packages"]) for g in groups)

    variables = {
        "invoice_no": invoice.invoice_no,
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "product_version": "v1.0.0",
        "groups": groups,
        "total_packages": total_packages,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    output_dir = INVOICE_DIR / str(invoice.tenant_id)
    output_path = output_dir / f"{invoice.invoice_no}_license.pdf"
    generate_pdf_from_template(
        template_name="invoice/oss_license.jinja2",
        template_dir=TEMPLATE_DIR,
        variables=variables,
        output_path=output_path,
    )
    return f"/static/invoice/{invoice.tenant_id}/{invoice.invoice_no}_license.pdf"
