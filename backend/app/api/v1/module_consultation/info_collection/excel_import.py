"""
全网抓取 Excel 导入
"""

import hashlib
import io
import re
from datetime import date
from typing import Any

import pandas as pd
from fastapi import UploadFile

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from app.core.logger import log

from .crud import InfoCollectionCRUD
from .model import InfoSource, InfoStatus

# Excel 表头（与业务上传模板一致，见全网抓取 Excel 标准表）
EXCEL_HEADER_MAP: dict[str, str] = {
    "序号": "excel_serial_no",
    "省份": "province",
    "指导单位": "guidance_unit",
    "承办单位": "organizer",
    "线路安排": "route_arrangement",
    "是否参加": "is_participating",
    "收费标准": "fee_description",
    "时间": "event_time_text",
    "地点": "address",
    "人员": "personnel",
    "邮寄材料地址": "mailing_address",
    "联系人及电话": "contact_info",
    "汇款账户": "remittance_account",
    "回执情况 (已回执√)": "receipt_status",
    "材料": "materials",
    "材料已领取": "materials_received",
    "备注": "remarks",
    "是否需要回执（具体时间）": "receipt_required_time",
}

EXCEL_HEADERS = list(EXCEL_HEADER_MAP.keys())

# 表头别名：兼容历史模板及 Excel 自动改写
HEADER_ALIASES: dict[str, list[str]] = {
    "excel_serial_no": ["序号"],
    "province": ["省份"],
    "guidance_unit": ["指导单位"],
    "organizer": ["承办单位"],
    "route_arrangement": ["线路安排"],
    "is_participating": ["是否参加"],
    "fee_description": ["收费标准"],
    "event_time_text": ["时间"],
    "address": ["地点"],
    "personnel": ["人员"],
    "mailing_address": ["邮寄材料地址"],
    "contact_info": ["联系人及电话"],
    "remittance_account": ["汇款账户"],
    "receipt_status": [
        "回执情况 (已回执√)",
        "回执情况(已回执√)",
        "回执情况（已回执√）",
        "回执情况 (已回执)",
        "回执情况",
    ],
    "materials": ["材料"],
    "materials_received": ["材料已领取"],
    "remarks": ["备注"],
    "receipt_required_time": [
        "是否需要回执（具体时间）",
        "是否需要回执(具体时间)",
        "是否需要回执",
    ],
}


def _normalize_header(name: str) -> str:
    """归一化表头便于匹配（去空白、统一括号与勾号）"""
    text = str(name).strip()
    text = text.replace("\u3000", "").replace(" ", "")
    text = text.replace("（", "(").replace("）", ")")
    text = text.replace("√", "").replace("✓", "").replace("✔", "")
    return text


def _build_column_rename_map(columns: list) -> dict[str, str]:
    """
    将上传文件列名映射为内部字段名。
    优先精确匹配标准表头，再按归一化名称匹配别名。
    """
    rename: dict[str, str] = {}
    normalized_file_cols = {_normalize_header(c): c for c in columns}

    for canonical, field in EXCEL_HEADER_MAP.items():
        if canonical in columns:
            rename[canonical] = field
            continue
        norm_canonical = _normalize_header(canonical)
        if norm_canonical in normalized_file_cols:
            rename[normalized_file_cols[norm_canonical]] = field
            continue
        for alias in HEADER_ALIASES.get(field, [canonical]):
            if alias in columns:
                rename[alias] = field
                break
            norm_alias = _normalize_header(alias)
            if norm_alias in normalized_file_cols:
                rename[normalized_file_cols[norm_alias]] = field
                break

    return rename


def _find_header_row(df_raw: pd.DataFrame) -> int | None:
    """业务表可能在首行之前有多行标题，自动定位含「序号」「省份」的表头行"""
    for idx in range(min(30, len(df_raw))):
        row_vals = [_normalize_header(v) for v in df_raw.iloc[idx].tolist() if pd.notna(v)]
        row_set = set(row_vals)
        if "序号" in row_set and "省份" in row_set and "承办单位" in row_set:
            return idx
    return None


def _load_dataframe(contents: bytes) -> pd.DataFrame:
    raw = pd.read_excel(io.BytesIO(contents), header=None)
    if raw.empty:
        return raw

    header_row = _find_header_row(raw)
    if header_row is not None:
        headers = [
            str(v).strip() if pd.notna(v) else f"未命名列{i}"
            for i, v in enumerate(raw.iloc[header_row].tolist())
        ]
        df = raw.iloc[header_row + 1 :].copy()
        df.columns = headers
        df = df.reset_index(drop=True)
    else:
        df = pd.read_excel(io.BytesIO(contents))

    # 去掉全空列
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    return df


def _validate_required_columns(rename_map: dict[str, str]) -> None:
    required_fields = {"organizer", "province"}
    mapped = set(rename_map.values())
    missing_fields = required_fields - mapped
    if missing_fields:
        labels = {
            "organizer": "承办单位",
            "province": "省份",
        }
        raise CustomException(
            msg=f"导入文件缺少必要的列: {', '.join(labels[f] for f in missing_fields)}"
        )


def _cell_str(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text or None


def _truncate(value: str | None, max_len: int) -> str | None:
    if not value:
        return value
    return value[:max_len]


def _format_import_error(exc: Exception) -> str:
    msg = str(exc)
    if "Data too long" in msg:
        return "字段内容超过数据库长度限制"
    if "closed transaction" in msg:
        return "事务已中断，请重试导入"
    if "创建失败:" in msg:
        return msg.split("创建失败:", 1)[-1].strip()[:200]
    if "列表查询失败:" in msg:
        return msg.split("列表查询失败:", 1)[-1].strip()[:200]
    return msg[:200]


def parse_event_dates(text: str | None) -> tuple[date, date | None]:
    """解析如「6月25-28日」的时间原文为日期"""
    if not text:
        return date.today(), None

    year = date.today().year
    range_match = re.search(r"(\d{1,2})月(\d{1,2})-(\d{1,2})日?", text)
    if range_match:
        month = int(range_match.group(1))
        day_start = int(range_match.group(2))
        day_end = int(range_match.group(3))
        return date(year, month, day_start), date(year, month, day_end)

    single_match = re.search(r"(\d{1,2})月(\d{1,2})日?", text)
    if single_match:
        month = int(single_match.group(1))
        day = int(single_match.group(2))
        return date(year, month, day), None

    return date.today(), None


def build_title(
    province: str | None,
    route_arrangement: str | None,
    organizer: str,
) -> str:
    parts = [p for p in (province, route_arrangement, organizer) if p]
    title = "-".join(parts) if parts else organizer
    return title[:200]


def build_external_id(
    province: str | None,
    organizer: str,
    route_arrangement: str | None,
    event_time_text: str | None,
    excel_serial_no: str | None,
) -> str:
    raw = "|".join([
        province or "",
        organizer,
        route_arrangement or "",
        event_time_text or "",
        excel_serial_no or "",
    ])
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _resolve_organizer(row: pd.Series) -> str:
    """承办单位为空时用指导单位/省份兜底，避免写入空字符串"""
    organizer = _cell_str(row.get("organizer"))
    if organizer and len(organizer) >= 2:
        return organizer
    for fallback in (
        _cell_str(row.get("guidance_unit")),
        _cell_str(row.get("province")),
    ):
        if fallback and len(fallback) >= 2:
            return fallback
    if organizer:
        return organizer
    raise ValueError("承办单位不能为空（可填写指导单位或省份作为补充）")


def row_to_create_data(row: pd.Series) -> dict[str, Any]:
    organizer = _resolve_organizer(row)
    province = _cell_str(row.get("province"))
    route_arrangement = _cell_str(row.get("route_arrangement"))
    event_time_text = _cell_str(row.get("event_time_text"))
    start_date, end_date = parse_event_dates(event_time_text)
    excel_serial_no = _cell_str(row.get("excel_serial_no"))

    title = build_title(province, route_arrangement, organizer)
    if len(title) < 2:
        title = organizer
    external_id = build_external_id(
        province, organizer, route_arrangement, event_time_text, excel_serial_no
    )

    search_keywords = " ".join(
        filter(
            None,
            [title, organizer, province or "", route_arrangement or "", event_time_text or ""],
        )
    )

    return {
        "title": _truncate(title, 200) or organizer[:200],
        "organizer": _truncate(organizer, 200) or organizer[:200],
        "province": _truncate(province, 50),
        "guidance_unit": _cell_str(row.get("guidance_unit")),
        "route_arrangement": route_arrangement,
        "is_participating": _cell_str(row.get("is_participating")),
        "fee_description": _cell_str(row.get("fee_description")),
        "event_time_text": event_time_text,
        "start_date": start_date,
        "end_date": end_date,
        "address": _cell_str(row.get("address")),
        "personnel": _cell_str(row.get("personnel")),
        "mailing_address": _cell_str(row.get("mailing_address")),
        "contact_info": _cell_str(row.get("contact_info")),
        "remittance_account": _cell_str(row.get("remittance_account")),
        "receipt_status": _cell_str(row.get("receipt_status")),
        "materials": _cell_str(row.get("materials")),
        "materials_received": _cell_str(row.get("materials_received")),
        "remarks": _cell_str(row.get("remarks")),
        "receipt_required_time": _cell_str(row.get("receipt_required_time")),
        "excel_serial_no": _truncate(excel_serial_no, 20),
        "source_type": InfoSource.CRAWLER.value,
        "status": InfoStatus.PENDING.value,
        "external_id": external_id,
        "search_keywords": search_keywords[:500],
    }


async def import_excel_file(auth: AuthSchema, file: UploadFile) -> dict[str, Any]:
    """解析 Excel 并批量写入咨询会信息（source_type=crawler）"""
    crawl_auth = AuthSchema(db=auth.db, check_data_scope=False)

    try:
        contents = await file.read()
        await file.close()
        df = _load_dataframe(contents)
    except CustomException:
        raise
    except Exception as e:
        log.error(f"读取 Excel 失败: {e}", exc_info=True)
        raise CustomException(msg=f"读取 Excel 失败: {e!s}") from e

    if df.empty:
        raise CustomException(msg="导入文件为空")

    rename_map = _build_column_rename_map(list(df.columns))
    _validate_required_columns(rename_map)
    df = df.rename(columns=rename_map)

    mapped_fields = set(rename_map.values())

    total_rows = 0
    total_saved = 0
    total_skipped = 0
    errors: list[str] = []

    for index, row in df.iterrows():
        row_no = int(index) + 2 if isinstance(index, int) else total_rows + 2
        if all(
            _cell_str(row.get(col)) is None for col in mapped_fields if col != "excel_serial_no"
        ):
            continue

        total_rows += 1
        try:
            async with auth.db.begin_nested():
                create_data = row_to_create_data(row)
                external_id = create_data.get("external_id")
                if external_id:
                    existing = await InfoCollectionCRUD(crawl_auth).list_crud(
                        search={"external_id": ("eq", external_id)}
                    )
                    if existing:
                        total_skipped += 1
                        continue

                await InfoCollectionCRUD(crawl_auth).create_crud(create_data)
                total_saved += 1
        except ValueError as e:
            errors.append(f"第{row_no}行: {e}")
        except Exception as e:
            errors.append(f"第{row_no}行: {_format_import_error(e)}")

    log.info(
        f"Excel 导入完成: 有效行 {total_rows}, 保存 {total_saved}, 跳过 {total_skipped}, "
        f"失败 {len(errors)}"
    )
    return {
        "total_rows": total_rows,
        "total_saved": total_saved,
        "total_skipped": total_skipped,
        "total_failed": len(errors),
        "errors": errors[:50],
    }


def get_import_template_bytes() -> bytes:
    from app.utils.excel_util import ExcelUtil

    return ExcelUtil.get_excel_template(
        header_list=EXCEL_HEADERS,
        selector_header_list=[],
        option_list=[],
    )
