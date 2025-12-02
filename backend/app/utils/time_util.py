# -*- coding: utf-8 -*-

import re
from datetime import datetime
from typing import Any

class TimeUtil:
    """
    时间格式化工具类
    """
    
    DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    @classmethod
    def object_format_datetime(cls, obj: Any) -> Any:
        """
        格式化对象中的 datetime 属性为默认字符串格式。
        
        参数:
        - obj (Any): 输入对象。
        
        返回:
        - Any: 格式化后的对象。
        """
        for attr in dir(obj):
            if not attr.startswith('_'):  # 跳过私有属性
                value = getattr(obj, attr)
                if isinstance(value, datetime):
                    setattr(obj, attr, value.strftime(cls.DEFAULT_DATETIME_FORMAT))
        return obj

    @classmethod
    def list_format_datetime(cls, lst: list[Any]) -> list[Any]:
        """
        格式化列表内每个对象的 datetime 属性。
        
        参数:
        - lst (List[Any]): 对象列表。
        
        返回:
        - list[Any]: 格式化后的对象列表。
        """
        return [cls.object_format_datetime(obj) for obj in lst]

    @classmethod
    def format_datetime_dict_list(cls, dicts: list[dict]) -> list[dict]:
        """
        递归格式化字典列表中的 datetime 值为默认字符串格式。
        
        参数:
        - dicts (list[dict]): 字典列表。
        
        返回:
        - list[dict]: 格式化后的字典列表。
        """
        def _format_value(value: Any) -> Any:
            if isinstance(value, dict):
                return {k: _format_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [_format_value(item) for item in value]
            elif isinstance(value, datetime):
                return value.strftime(cls.DEFAULT_DATETIME_FORMAT)
            return value
            
        return [_format_value(item) for item in dicts]

    @classmethod
    def __valid_range(cls, search_str: str, start_range: int, end_range: int) -> bool:
        """
        校验范围字符串是否合法。
        
        参数:
        - search_str (str): 范围字符串（例如："1-5"）。
        - start_range (int): 允许的最小范围值。
        - end_range (int): 允许的最大范围值。
        
        返回:
        - bool: 校验是否通过。
        """
        match = re.match(r'^(\d+)-(\d+)$', search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return start_range <= start < end <= end_range
        return False

    @classmethod
    def __valid_sum(cls, search_str: str, start_range_a: int, start_range_b: int, end_range_a: int, end_range_b: int, sum_range: int) -> bool:
        """
        校验和字符串是否合法。
        
        参数:
        - search_str (str): 和字符串（例如："1/5"）。
        - start_range_a (int): 允许的最小范围值A。
        - start_range_b (int): 允许的最大范围值A。
        - end_range_a (int): 允许的最小范围值B。
        - end_range_b (int): 允许的最大范围值B。
        - sum_range (int): 允许的最大和值。
        
        返回:
        - bool: 校验是否通过。
        """
        match = re.match(r'^(\d+)/(\d+)$', search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return (
                start_range_a <= start <= start_range_b
                and end_range_a <= end <= end_range_b
                and start + end <= sum_range
            )
        return False

    @classmethod
    def validate_second_or_minute(cls, second_or_minute: str):
        """
        校验秒或分钟字段的合法性。

        参数:
        - second_or_minute (str): 秒或分钟值。

        返回:
        - bool: 校验是否通过。
        """
        if (
            second_or_minute == '*'
            or ('-' in second_or_minute and cls.__valid_range(second_or_minute, 0, 59))
            or ('/' in second_or_minute and cls.__valid_sum(second_or_minute, 0, 58, 1, 59, 59))
            or re.match(r'^(?:[0-5]?\d|59)(?:,[0-5]?\d|59)*$', second_or_minute)
        ):
            return True
        return False

    @classmethod
    def validate_hour(cls, hour: str):
        """
        校验小时字段的合法性。

        参数:
        - hour (str): 小时值。

        返回:
        - bool: 校验是否通过。
        """
        if (
            hour == '*'
            or ('-' in hour and cls.__valid_range(hour, 0, 23))
            or ('/' in hour and cls.__valid_sum(hour, 0, 22, 1, 23, 23))
            or re.match(r'^(?:0|[1-9]|1\d|2[0-3])(?:,(?:0|[1-9]|1\d|2[0-3]))*$', hour)
        ):
            return True
        return False

    @classmethod
    def validate_day(cls, day: str):
        """
        校验日期字段的合法性。

        参数:
        - day (str): 日值。

        返回:
        - bool: 校验是否通过。
        """
        if (
            day in ['*', '?', 'L']
            or ('-' in day and cls.__valid_range(day, 1, 31))
            or ('/' in day and cls.__valid_sum(day, 1, 30, 1, 30, 31))
            or ('W' in day and re.match(r'^(?:[1-9]|1\d|2\d|3[01])W$', day))
            or re.match(r'^(?:0|[1-9]|1\d|2[0-9]|3[0-1])(?:,(?:0|[1-9]|1\d|2[0-9]|3[0-1]))*$', day)
        ):
            return True
        return False

    @classmethod
    def validate_month(cls, month: str):
        """
        校验月份字段的合法性。

        参数:
        - month (str): 月值。

        返回:
        - bool: 校验是否通过。
        """
        if (
            month == '*'
            or ('-' in month and cls.__valid_range(month, 1, 12))
            or ('/' in month and cls.__valid_sum(month, 1, 11, 1, 11, 12))
            or re.match(r'^(?:0|[1-9]|1[0-2])(?:,(?:0|[1-9]|1[0-2]))*$', month)
        ):
            return True
        return False

    @classmethod
    def validate_week(cls, week: str):
        """
        校验星期字段的合法性。

        参数:
        - week (str): 周值。

        返回:
        - bool: 校验是否通过。
        """
        if (
            week in ['*', '?']
            or ('-' in week and cls.__valid_range(week, 1, 7))
            or ('#' in week and re.match(r'^[1-7]#[1-4]$', week))
            or ('L' in week and re.match(r'^[1-7]L$', week))
            or re.match(r'^[1-7](?:(,[1-7]))*$', week)
        ):
            return True
        return False

    @classmethod
    def validate_year(cls, year: str):
        """
        校验年份字段的合法性。

        参数:
        - year (str): 年值。

        返回:
        - bool: 校验是否通过。
        """
        current_year = int(datetime.now().year)
        future_years = [current_year + i for i in range(9)]
        if (
            year == '*'
            or ('-' in year and cls.__valid_range(year, current_year, 2099))
            or ('/' in year and cls.__valid_sum(year, current_year, 2098, 1, 2099 - current_year, 2099))
            or ('#' in year and re.match(r'^[1-7]#[1-4]$', year))
            or ('L' in year and re.match(r'^[1-7]L$', year))
            or (
                (len(year) == 4 or ',' in year)
                and all(int(item) in future_years and current_year <= int(item) <= 2099 for item in year.split(','))
            )
        ):
            return True
        return False

    @classmethod
    def validate_cron_expression(cls, cron_expression: str):
        """
        校验 Cron 表达式是否正确。
        * * * * * *
        | | | | | |
        | | | | | +--- 星期（0-7，0和7都表示星期日）
        | | | | +----- 月份（1-12）
        | | | +------- 日期（1-31）
        | | +--------- 小时（0-23）
        | +----------- 分钟（0-59）
        +------------- 秒（0-59），部分环境不支持秒字段。

        参数:
        - cron_expression (str): Cron 表达式。

        返回:
        - bool: 校验是否通过。
        """
        values = cron_expression.split()
        if len(values) != 6 and len(values) != 7:
            return False
        second_validation = cls.validate_second_or_minute(values[0])
        minute_validation = cls.validate_second_or_minute(values[1])
        hour_validation = cls.validate_hour(values[2])
        day_validation = cls.validate_day(values[3])
        month_validation = cls.validate_month(values[4])
        week_validation = cls.validate_week(values[5])
        validation = (
            second_validation
            and minute_validation
            and hour_validation
            and day_validation
            and month_validation
            and week_validation
        )
        if len(values) == 6:
            return validation
        if len(values) == 7:
            year_validation = cls.validate_year(values[6])
            return validation and year_validation
