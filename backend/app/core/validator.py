import re
from datetime import date, datetime, time
from typing import Annotated, Any

from pydantic import AfterValidator, PlainSerializer, WithJsonSchema

from app.common.constant import RET
from app.core.exceptions import CustomException

# 自定义日期时间字符串类型
DateTimeStr = Annotated[
    datetime,
    AfterValidator(lambda x: datetime_validator(x)),
    PlainSerializer(
        lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, datetime) else str(x),
        return_type=str,
    ),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

# 自定义日期字符串类型
DateStr = Annotated[
    date,
    PlainSerializer(
        lambda x: x.strftime("%Y-%m-%d") if isinstance(x, date) else str(x),
        return_type=str,
    ),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

# 自定义时间字符串类型
TimeStr = Annotated[
    time,
    PlainSerializer(
        lambda x: x.strftime("%H:%M:%S") if isinstance(x, time) else str(x),
        return_type=str,
    ),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

# 自定义手机号类型
Telephone = Annotated[
    str,
    AfterValidator(lambda x: mobile_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

# 自定义邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: email_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


def datetime_validator(value: str | datetime) -> datetime:
    """
    日期格式验证器。

    参数:
    - value (str | datetime): 日期值。

    返回:
    - datetime: 格式化后的日期。

    异常:
    - CustomException: 日期格式无效时抛出。
    """
    pattern = "%Y-%m-%d %H:%M:%S"
    try:
        if isinstance(value, str):
            return datetime.strptime(value, pattern)
        if isinstance(value, datetime):
            return value
    except Exception:
        raise CustomException(code=RET.ERROR.code, msg="无效的日期格式")


def email_validator(value: str) -> str:
    """
    邮箱地址验证器。

    参数:
    - value (str): 邮箱地址。

    返回:
    - str: 验证后的邮箱地址。

    异常:
    - CustomException: 邮箱格式无效时抛出。
    """
    if not value:
        raise CustomException(code=RET.ERROR.code, msg="邮箱地址不能为空")

    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(regex, value):
        raise CustomException(code=RET.ERROR.code, msg="邮箱地址格式不正确")

    return value


def mobile_validator(value: str | None) -> str | None:
    """
    手机号验证器。

    参数:
    - value (str | None): 手机号。

    返回:
    - str | None: 验证后的手机号。

    异常:
    - CustomException: 手机号格式无效时抛出。
    """
    if not value:
        return value

    if len(value) != 11 or not value.isdigit():
        raise CustomException(code=RET.ERROR.code, msg="手机号格式不正确")

    regex = r"^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$"

    if not re.match(regex, value):
        raise CustomException(code=RET.ERROR.code, msg="手机号格式不正确")

    return value


def code_validator(value: str | None) -> str | None:
    """
    编码验证器。

    参数:
    - value (str | None): 编码。

    返回:
    - str | None: 验证后的编码。

    异常:
    - CustomException: 编码格式无效时抛出。
    """
    if not value:
        return value
    v = value.strip()
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]{1,15}$", v):
        raise CustomException(
            code=RET.ERROR.code,
            msg="编码需字母开头，允许字母/数字/下划线，长度2-16",
        )
    return v


def menu_request_validator(data: Any) -> Any:
    """
    菜单请求数据验证器。

    参数:
    - data (Any): 请求数据。

    返回:
    - Any: 验证后的请求数据。

    异常:
    - CustomException: 请求数据无效时抛出。
    """
    menu_types = {1: "目录", 2: "功能", 3: "权限", 4: "外链"}

    if data.type not in menu_types:
        raise CustomException(
            code=RET.ERROR.code,
            msg=f"菜单类型必须为: {','.join(map(str, menu_types.keys()))}",
        )

    if data.type in [1, 2]:
        if not data.route_name:
            raise CustomException(code=RET.ERROR.code, msg="路由名称不能为空")
        if not data.route_path:
            raise CustomException(code=RET.ERROR.code, msg="路由路径不能为空")

    if data.type == 2 and not data.component_path:
        raise CustomException(code=RET.ERROR.code, msg="组件路径不能为空")

    return data


def role_permission_request_validator(data: Any) -> Any:
    """
    角色权限设置数据验证器。

    参数:
    - data (Any): 请求数据。

    返回:
    - Any: 验证后的请求数据。

    异常:
    - CustomException: 请求数据无效时抛出。
    """
    data_scopes = {
        1: "仅本人数据权限",
        2: "本部门数据权限",
        3: "本部门及以下数据权限",
        4: "全部数据权限",
        5: "自定义数据权限",
    }

    if data.data_scope not in data_scopes:
        raise CustomException(
            code=RET.ERROR.code,
            msg=f"数据权限范围必须为: {','.join(map(str, data_scopes.keys()))}",
        )

    if not data.role_ids:
        raise CustomException(code=RET.ERROR.code, msg="角色不能为空")

    return data
