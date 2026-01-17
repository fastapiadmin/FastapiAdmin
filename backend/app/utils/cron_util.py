import re
from datetime import datetime


class CronUtil:
    """
    Cron表达式工具类
    """

    @classmethod
    def __valid_range(cls, search_str: str, start_range: int, end_range: int) -> bool:
        """
        校验范围表达式的合法性。

        参数:
        - search_str (str): 范围表达式。
        - start_range (int): 开始范围。
        - end_range (int): 结束范围。

        返回:
        - bool: 校验是否通过。
        """
        match = re.match(r"^(\d+)-(\d+)$", search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return start_range <= start < end <= end_range
        return False

    @classmethod
    def __valid_sum(
        cls,
        search_str: str,
        start_range_a: int,
        start_range_b: int,
        end_range_a: int,
        end_range_b: int,
        sum_range: int,
    ) -> bool:
        """
        校验和表达式的合法性。

        参数:
        - search_str (str): 和表达式。
        - start_range_a (int): 开始范围A。
        - start_range_b (int): 开始范围B。
        - end_range_a (int): 结束范围A。
        - end_range_b (int): 结束范围B。
        - sum_range (int): 总和范围。

        返回:
        - bool: 校验是否通过。
        """
        match = re.match(r"^(\d+)/(\d+)$", search_str)
        if match:
            start, end = int(match.group(1)), int(match.group(2))
            return (
                start_range_a <= start <= start_range_b
                and end_range_a <= end <= end_range_b
                and start + end <= sum_range
            )
        return False

    @classmethod
    def validate_second_or_minute(cls, second_or_minute: str) -> bool:
        """
        校验秒或分钟字段的合法性。

        参数:
        - second_or_minute (str): 秒或分钟值。

        返回:
        - bool: 校验是否通过。
        """
        return bool(
            second_or_minute == "*"
            or ("-" in second_or_minute and cls.__valid_range(second_or_minute, 0, 59))
            or ("/" in second_or_minute and cls.__valid_sum(second_or_minute, 0, 58, 1, 59, 59))
            or re.match(r"^(?:[0-5]?\d|59)(?:,[0-5]?\d|59)*$", second_or_minute)
        )

    @classmethod
    def validate_hour(cls, hour: str) -> bool:
        """
        校验小时字段的合法性。

        参数:
        - hour (str): 小时值。

        返回:
        - bool: 校验是否通过。
        """
        return bool(
            hour == "*"
            or ("-" in hour and cls.__valid_range(hour, 0, 23))
            or ("/" in hour and cls.__valid_sum(hour, 0, 22, 1, 23, 23))
            or re.match(r"^(?:0|[1-9]|1\d|2[0-3])(?:,(?:0|[1-9]|1\d|2[0-3]))*$", hour)
        )

    @classmethod
    def validate_day(cls, day: str) -> bool:
        """
        校验日期字段的合法性。

        参数:
        - day (str): 日值。

        返回:
        - bool: 校验是否通过。
        """
        return bool(
            day in ["*", "?", "L"]
            or ("-" in day and cls.__valid_range(day, 1, 31))
            or ("/" in day and cls.__valid_sum(day, 1, 30, 1, 30, 31))
            or ("W" in day and re.match(r"^(?:[1-9]|1\d|2\d|3[01])W$", day))
            or re.match(
                r"^(?:0|[1-9]|1\d|2[0-9]|3[0-1])(?:,(?:0|[1-9]|1\d|2[0-9]|3[0-1]))*$",
                day,
            )
        )

    @classmethod
    def validate_month(cls, month: str) -> bool:
        """
        校验月份字段的合法性。

        参数:
        - month (str): 月值。

        返回:
        - bool: 校验是否通过。
        """
        return bool(
            month == "*"
            or ("-" in month and cls.__valid_range(month, 1, 12))
            or ("/" in month and cls.__valid_sum(month, 1, 11, 1, 11, 12))
            or re.match(r"^(?:0|[1-9]|1[0-2])(?:,(?:0|[1-9]|1[0-2]))*$", month)
        )

    @classmethod
    def validate_week(cls, week: str) -> bool:
        """
        校验星期字段的合法性。

        参数:
        - week (str): 周值。

        返回:
        - bool: 校验是否通过。
        """
        return bool(
            week in ["*", "?"]
            or ("-" in week and cls.__valid_range(week, 1, 7))
            or ("#" in week and re.match(r"^[1-7]#[1-4]$", week))
            or ("L" in week and re.match(r"^[1-7]L$", week))
            or re.match(r"^[1-7](?:(,[1-7]))*$", week)
        )

    @classmethod
    def validate_year(cls, year: str) -> bool:
        """
        校验年份字段的合法性。

        参数:
        - year (str): 年值。

        返回:
        - bool: 校验是否通过。
        """
        current_year = int(datetime.now().year)
        future_years = [current_year + i for i in range(9)]
        return bool(
            year == "*"
            or ("-" in year and cls.__valid_range(year, current_year, 2099))
            or (
                "/" in year
                and cls.__valid_sum(year, current_year, 2098, 1, 2099 - current_year, 2099)
            )
            or ("#" in year and re.match(r"^[1-7]#[1-4]$", year))
            or ("L" in year and re.match(r"^[1-7]L$", year))
            or (
                (len(year) == 4 or "," in year)
                and all(
                    int(item) in future_years and current_year <= int(item) <= 2099
                    for item in year.split(",")
                )
            )
        )

    @classmethod
    def validate_cron_expression(cls, cron_expression: str) -> bool | None:
        """
        校验 Cron 表达式是否正确。

        参数:
        - cron_expression (str): Cron 表达式。

        返回:
        - bool | None: 校验是否通过。
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
