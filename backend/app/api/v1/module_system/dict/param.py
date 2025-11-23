# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query

from app.core.validator import DateTimeStr


class DictTypeQueryParam:
    """字典类型查询参数"""

    def __init__(
            self,
            dict_name: Optional[str] = Query(None, description="字典名称"),
            dict_type: Optional[str] = Query(None, description="字典类型"),
            status: Optional[bool] = Query(None, description="状态（1正常 0停用）"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2025-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2025-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.dict_name = ("like", f"%{dict_name}%") if dict_name else None
        
        # 精确查询字段
        self.dict_type = dict_type
        self.status = status
        
        # 时间范围查询
        if start_time and end_time:
            self.created_at = ("between", (start_time, end_time))


class DictDataQueryParam:
    """字典数据查询参数"""

    def __init__(
            self,
            dict_label: Optional[str] = Query(None, description="字典标签"),
            dict_type: Optional[str] = Query(None, description="字典类型"),
            status: Optional[bool] = Query(None, description="状态（1正常 0停用）"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2025-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2025-12-31 23:59:59"),
    ) -> None:
        
        # 模糊查询字段
        self.dict_label = ("like", f"%{dict_label}%") if dict_label else None
        
        # 精确查询字段
        self.dict_type = dict_type
        self.status = status
        
        # 时间范围查询
        if start_time and end_time:
            self.created_at = ("between", (start_time, end_time))