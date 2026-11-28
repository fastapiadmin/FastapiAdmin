"""定时任务内置处理器的元数据定义。

处理器仍然必须是 handlers 包内定义的普通 Python 函数；这里只描述它在后台
如何展示、需要哪些参数。前端不再接收任意 Python 代码块，而是选择处理器并
填写参数。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class HandlerParam:
    """一个处理器参数的展示与校验信息。"""

    name: str
    label: str
    type: str = "string"  # string | int | float | bool | json
    required: bool = False
    default: Any = None
    description: str = ""
    minimum: int | float | None = None
    maximum: int | float | None = None


@dataclass(frozen=True)
class HandlerSpec:
    """一个内置处理器的完整描述。"""

    key: str
    label: str
    description: str
    params: tuple[HandlerParam, ...] = field(default_factory=tuple)


__all__ = ["HandlerParam", "HandlerSpec"]
