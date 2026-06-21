"""
pdf_generator.py — PDF 生成工具

使用 WeasyPrint 将 HTML/CSS 渲染为 PDF。
当前用于电子发票 PDF 本地生成（对接百望云/票通后可平滑替换）。
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def render_html_template(
    template_name: str,
    template_dir: str | Path,
    variables: dict[str, Any],
) -> str:
    """
    渲染 Jinja2 HTML 模板文件

    参数:
    - template_name (str): 模板文件名（如 "invoice.html"）
    - template_dir (str | Path): 模板目录路径
    - variables (dict[str, Any]): 模板变量

    返回:
    - str: 渲染后的 HTML 字符串
    """
    env = Environment(loader=FileSystemLoader(str(template_dir)), undefined=StrictUndefined, autoescape=True)
    template = env.get_template(template_name)
    return template.render(**variables)


def html_to_pdf(html_str: str, css_str: str | None = None) -> bytes:
    """
    将 HTML 字符串转换为 PDF 字节流

    需要 weasyprint + 系统 libgobject（安装: brew install glib pango）。

    参数:
    - html_str (str): HTML 内容
    - css_str (str | None): 可选的内联 CSS 字符串

    返回:
    - bytes: PDF 字节流
    """
    from weasyprint import CSS, HTML

    html = HTML(string=html_str, base_url=".")
    if css_str:
        return html.write_pdf(stylesheets=[CSS(string=css_str)])
    return html.write_pdf()


def save_pdf(pdf_bytes: bytes, output_path: str | Path) -> Path:
    """
    将 PDF 字节流保存到文件

    参数:
    - pdf_bytes (bytes): PDF 内容
    - output_path (str | Path): 输出文件路径

    返回:
    - Path: 写入的文件路径
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    return output_path


def generate_pdf_from_template(
    template_name: str,
    template_dir: str | Path,
    variables: dict[str, Any],
    output_path: str | Path,
    css_str: str | None = None,
) -> Path:
    """
    一站式从模板生成 PDF 并保存

    参数:
    - template_name (str): 模板文件名
    - template_dir (str | Path): 模板目录
    - variables (dict[str, Any]): 模板变量
    - output_path (str | Path): 输出 PDF 路径
    - css_str (str | None): 可选的内联 CSS

    返回:
    - Path: 生成的 PDF 文件路径
    """
    html_str = render_html_template(template_name, template_dir, variables)
    pdf_bytes = html_to_pdf(html_str, css_str)
    return save_pdf(pdf_bytes, output_path)


def _int_to_cn(num: int) -> str:
    """
    整数部分转中文（不含"元"单位）

    例如 100 -> "壹佰", 1000001 -> "壹佰万零壹"
    """
    if num == 0:
        return ""

    digits = "零壹贰叁肆伍陆柒捌玖"
    int_units = ["仟", "佰", "拾", ""]
    big_units = ["", "万", "亿", "万亿"]

    groups: list[int] = []
    while num > 0:
        groups.insert(0, num % 10000)
        num //= 10000

    result = ""
    for gi, group in enumerate(groups):
        big_unit = big_units[len(groups) - 1 - gi]
        group_str = ""
        last_was_zero = True
        for i in range(4):
            d = (group // (10 ** (3 - i))) % 10
            if d == 0:
                if not last_was_zero:
                    group_str += "零"
                last_was_zero = True
            else:
                group_str += digits[d] + int_units[i]
                last_was_zero = False
        group_str = group_str.rstrip("零")
        if group_str:
            if result and result[-1] in ("万", "亿") and not group_str.startswith("零"):
                result += "零"
            result += group_str + big_unit
    return result.rstrip("零")


def amount_to_cn_uppercase(amount_yuan: float) -> str:
    """
    数字金额转中文大写（人民币）

    支持 0.01 ~ 99999999999.99 元

    规则:
    - 整数部分 + "元" + 小数部分 + "整"
    - 整数为 0 时不显示"零元"
    - 仅有分时（如 0.05 元）补"零"
    - 跨大单位（万/亿）需补"零"衔接
    """
    if amount_yuan < 0.01:
        return "零元整"

    digits = "零壹贰叁肆伍陆柒捌玖"

    yuan_int = int(amount_yuan)
    cents = round((amount_yuan - yuan_int) * 100)

    if yuan_int == 0 and cents == 0:
        return "零元整"

    int_part = _int_to_cn(yuan_int)
    int_str = int_part + "元" if int_part else ""

    decimal_part = ""
    if cents > 0:
        jiao = cents // 10
        fen = cents % 10
        if jiao > 0:
            decimal_part += digits[jiao] + "角"
        elif int_str or fen > 0:
            decimal_part = "零"
        if fen > 0:
            decimal_part += digits[fen] + "分"

    if cents == 0:
        result = int_str + "整"
    else:
        result = int_str + decimal_part
    return result or "零元整"


def amount_to_yuan(cents: int) -> str:
    """
    分转元字符串

    参数:
    - cents (int): 金额（分）

    返回:
    - str: 形如 "9999.99" 的金额字符串
    """
    return f"{cents / 100:.2f}"
