"""SQL 只读校验与敏感列脱敏（参照 FastHub 的 db_query，按本项目风格重写）。

为什么需要：SQL 控制台接收的是**人/AI 直接输入或生成的 SQL**，属于不受信输入。
首词是 select 不代表整句只读：
1. ``with x as (...) delete from ...`` —— 首词是 with，却在删数据；
2. ``select ... into outfile '/tmp/a'`` —— 首词是 select，却在写文件；
3. ``select 1; drop table t`` —— 首词是 select，第二句在写。

因此只读校验必须先剥注释、再判首词、再查写关键字/导出子句/延时函数，且只允许单条语句。
"""

import re
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
from decimal import Decimal
from typing import Any

from app.config.setting import settings
from app.core.exceptions import CustomException

# 允许的只读首词
READ_KEYWORDS: frozenset[str] = frozenset({"select", "show", "describe", "desc", "explain", "pragma", "with", "table", "values"})

# with 语句里可能夹带的写操作
_WRITE_WORDS = re.compile(r"\b(insert|update|delete|merge|replace|drop|alter|truncate|create|rename|grant|revoke)\b", re.IGNORECASE)
# select ... into outfile / dumpfile
_EXPORT_WORDS = re.compile(r"\binto\s+(outfile|dumpfile)\b", re.IGNORECASE)
# 延时函数：同步/长连接会被一条 sleep 钉死
_SLOW_WORDS = re.compile(r"\b(sleep|pg_sleep|benchmark)\s*\(", re.IGNORECASE)
_LINE_COMMENT = re.compile(r"--[^\n]*")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

# 敏感列（结果里命中即打码）
SENSITIVE_COLUMN = re.compile(r"(password|passwd|pwd|secret|token|api[_-]?key|private[_-]?key|credential|salt)", re.IGNORECASE)

MASK_TEXT = "••••••"


def strip_comments(sql: str) -> str:
    """剥掉行注释与块注释（避免用注释把写语句藏到第二行）。"""
    text = _BLOCK_COMMENT.sub(" ", sql or "")
    return _LINE_COMMENT.sub(" ", text).strip()


def is_read_only(sql: str) -> bool:
    """按首词粗判是否只读（只用于选择校验路径，真正的拦截见 assert_read_only）。"""
    text = strip_comments(sql).lstrip("(").strip().lower()
    head = text.split()[0] if text else ""
    return head in READ_KEYWORDS


def is_single_statement(sql: str) -> bool:
    """是否只包含一条语句（允许结尾一个分号）。"""
    text = strip_comments(sql)
    if text.endswith(";"):
        text = text[:-1].rstrip()
    return ";" not in text


def assert_read_only(sql: str) -> str:
    """校验只读并返回规整后的 SQL；不满足则抛 CustomException。"""
    text = strip_comments(sql)
    if not text:
        raise CustomException(msg="SQL 不能为空")
    if not is_single_statement(text):
        raise CustomException(msg="一次只能执行一条语句（检测到多个分号）")
    head = re.sub(r"^[(\s]+", "", text).split()[0].lower()
    if head not in READ_KEYWORDS:
        raise CustomException(msg="只支持查询语句（select / show / describe / explain / with）")
    if head == "with" and _WRITE_WORDS.search(text):
        raise CustomException(msg="该 with 语句里包含写操作，只读模式下不允许")
    if _EXPORT_WORDS.search(text):
        raise CustomException(msg="不支持 into outfile / dumpfile（导出请走专门的导出功能）")
    if _SLOW_WORDS.search(text):
        raise CustomException(msg="语句包含 sleep / benchmark 等延时函数，会长时间占用连接")
    if text.endswith(";"):
        text = text[:-1].rstrip()
    return text


def mask_rows(columns: list[str], rows: list[list[Any]]) -> tuple[list[list[Any]], list[str]]:
    """对命中敏感模式的列打码（返回新行与被脱敏列名）。"""
    masked_indexes = [index for index, name in enumerate(columns) if SENSITIVE_COLUMN.search(str(name))]
    if not masked_indexes:
        return rows, []
    masked_rows: list[list[Any]] = []
    for row in rows:
        new_row = list(row)
        for index in masked_indexes:
            if index < len(new_row) and new_row[index] is not None:
                new_row[index] = MASK_TEXT
        masked_rows.append(new_row)
    return masked_rows, [columns[index] for index in masked_indexes]


def to_jsonable(value: Any) -> Any:
    """把数据库返回值转成 JSON 可序列化形式（并限制单值长度）。"""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value[:2000] if isinstance(value, str) else value
    if isinstance(value, (datetime, date, time)):
        if isinstance(value, datetime) and value.tzinfo is not None:
            # 外部库返回 aware datetime（如 PostgreSQL timestamptz）时按服务器展示时区输出
            try:
                value = value.astimezone(ZoneInfo(settings.TIMEZONE))
            except Exception:
                pass
        return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", errors="backslashreplace")[:200]
    return str(value)[:500]
