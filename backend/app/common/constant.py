from enum import Enum
from typing import Protocol

from app.config.setting import settings


class RET(Enum):
    """
    系统返回码枚举

    0~200: 成功状态码
    400~600: HTTP标准错误码
    4000+: 自定义业务错误码
    """

    # 成功状态码
    OK = (0, "成功")
    SUCCESS = (200, "操作成功")
    CREATED = (201, "创建成功")
    ACCEPTED = (202, "请求已接受")
    NO_CONTENT = (204, "操作成功,无返回数据")

    # HTTP标准错误码
    ERROR = (1, "请求错误")
    BAD_REQUEST = (400, "参数错误")
    UNAUTHORIZED = (401, "未授权")
    FORBIDDEN = (403, "访问受限")
    NOT_FOUND = (404, "资源不存在")
    BAD_METHOD = (405, "不支持的请求方法")
    NOT_ACCEPTABLE = (406, "不接受的请求")
    CONFLICT = (409, "资源冲突")
    GONE = (410, "资源已删除")
    PRECONDITION_FAILED = (412, "前提条件失败")
    UNSUPPORTED_MEDIA_TYPE = (415, "不支持的媒体类型")
    UNPROCESSABLE_ENTITY = (422, "无法处理的实体")
    TOO_MANY_REQUESTS = (429, "请求过于频繁")

    # 服务器错误码
    INTERNAL_SERVER_ERROR = (500, "服务器内部错误")
    NOT_IMPLEMENTED = (501, "功能未实现")
    BAD_GATEWAY = (502, "网关错误")
    SERVICE_UNAVAILABLE = (503, "服务不可用")
    GATEWAY_TIMEOUT = (504, "网关超时")
    HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP版本不支持")

    # 自定义业务错误码
    EXCEPTION = (-1, "系统异常")
    DATAEXIST = (4003, "数据已存在")
    DATAERR = (4004, "数据错误")
    PARAMERR = (4103, "参数错误")
    IOERR = (4302, "IO错误")
    SERVERERR = (4500, "服务错误")
    UNKOWNERR = (4501, "未知错误")
    TIMEOUT = (4502, "请求超时")
    RATE_LIMIT_EXCEEDED = (4503, "访问频率超限")

    # Token相关错误码
    INVALID_TOKEN = (4504, "无效令牌")
    EXPIRED_TOKEN = (4505, "令牌过期")

    # 认证授权错误码
    INVALID_CREDENTIALS = (4506, "无效凭证")
    INVALID_REQUEST = (4507, "无效请求")
    INVALID_FORMAT = (4508, "格式错误")
    INVALID_INPUT = (4509, "输入错误")
    INVALID_STATE = (4510, "状态错误")
    INVALID_OPERATION = (4511, "操作错误")
    INVALID_PERMISSION = (4512, "权限错误")
    INVALID_RESOURCE = (4513, "资源错误")
    INVALID_CONFIGURATION = (4514, "配置错误")

    # 会话安全错误码
    INVALID_SESSION = (4515, "会话错误")
    INVALID_LICENSE = (4516, "许可证错误")
    INVALID_CERTIFICATE = (4517, "证书错误")
    INVALID_SIGNATURE = (4518, "签名错误")
    INVALID_ENCRYPTION = (4519, "加密错误")
    INVALID_DECRYPTION = (4520, "解密错误")
    INVALID_COMPRESSION = (4521, "压缩错误")
    INVALID_DECOMPRESSION = (4522, "解压错误")

    # 权限相关错误码
    INVALID_AUTHENTICATION = (4523, "认证错误")
    INVALID_AUTHORIZATION = (4524, "授权错误")
    INVALID_ACCESS = (4525, "访问错误")
    INVALID_SECURITY = (4526, "安全错误")

    # 系统组件错误码
    INVALID_NETWORK = (4527, "网络错误")
    INVALID_DATABASE = (4528, "数据库错误")
    INVALID_CACHE = (4529, "缓存错误")
    INVALID_QUEUE = (4530, "队列错误")
    INVALID_LOCK = (4531, "锁错误")
    INVALID_TRANSACTION = (4532, "事务错误")
    INVALID_LOG = (4533, "日志错误")
    INVALID_MONITORING = (4534, "监控错误")
    INVALID_NOTIFICATION = (4535, "通知错误")

    # 任务调度错误码
    INVALID_SCHEDULING = (4536, "调度错误")
    INVALID_TASK = (4537, "任务错误")
    INVALID_JOB = (4538, "作业错误")
    INVALID_WORKFLOW = (4539, "工作流错误")

    # 开发相关错误码
    INVALID_SCRIPT = (4540, "脚本错误")
    INVALID_PLUGIN = (4541, "插件错误")
    INVALID_MODULE = (4542, "模块错误")
    INVALID_PACKAGE = (4543, "包错误")
    INVALID_CLASS = (4544, "类错误")
    INVALID_FUNCTION = (4545, "函数错误")
    INVALID_METHOD = (4546, "方法错误")
    INVALID_PROPERTY = (4547, "属性错误")
    INVALID_VARIABLE = (4548, "变量错误")
    INVALID_CONSTANT = (4549, "常量错误")
    INVALID_ENUM = (4550, "枚举错误")
    INVALID_INTERFACE = (4551, "接口错误")
    INVALID_PROTOCOL = (4552, "协议错误")

    # 服务相关错误码
    INVALID_SERVICE = (4553, "服务错误")
    INVALID_CLIENT = (4554, "客户端错误")
    INVALID_SERVER = (4555, "服务器错误")
    INVALID_SYSTEM = (4556, "系统错误")

    # 用户权限错误码
    INVALID_USER = (4557, "用户错误")
    INVALID_GROUP = (4558, "用户组错误")
    INVALID_ROLE = (4559, "角色错误")
    INVALID_PERMISSION_GROUP = (4560, "权限组错误")
    INVALID_PERMISSION_ROLE = (4561, "权限角色错误")
    INVALID_PERMISSION_USER = (4562, "权限用户错误")
    INVALID_PERMISSION_RESOURCE = (4563, "权限资源错误")
    INVALID_PERMISSION_ACTION = (4564, "权限操作错误")
    INVALID_PERMISSION_SCOPE = (4565, "权限范围错误")
    INVALID_PERMISSION_LEVEL = (4566, "权限级别错误")
    INVALID_PERMISSION_TYPE = (4567, "权限类型错误")
    INVALID_PERMISSION_STATUS = (4568, "权限状态错误")
    INVALID_PERMISSION_TIME = (4569, "权限时间错误")
    INVALID_PERMISSION_CONDITION = (4570, "权限条件错误")
    INVALID_PERMISSION_POLICY = (4571, "权限策略错误")
    INVALID_PERMISSION_RULE = (4572, "权限规则错误")
    INVALID_PERMISSION_EXCEPTION = (4573, "权限异常错误")
    INVALID_PERMISSION_VALIDATION = (4574, "权限验证错误")
    INVALID_PERMISSION_AUTHENTICATION = (4575, "权限认证错误")
    INVALID_PERMISSION_AUTHORIZATION = (4576, "权限授权错误")
    INVALID_PERMISSION_ACCESS = (4577, "权限访问错误")
    INVALID_PERMISSION_SECURITY = (4578, "权限安全错误")
    INVALID_PERMISSION_NETWORK = (4579, "权限网络错误")
    INVALID_PERMISSION_DATABASE = (4580, "权限数据库错误")
    INVALID_PERMISSION_CACHE = (4581, "权限缓存错误")
    INVALID_PERMISSION_QUEUE = (4582, "权限队列错误")
    INVALID_PERMISSION_LOCK = (4583, "权限锁错误")
    INVALID_PERMISSION_TRANSACTION = (4584, "权限事务错误")
    INVALID_PERMISSION_LOG = (4585, "权限日志错误")
    INVALID_PERMISSION_MONITORING = (4586, "权限监控错误")
    INVALID_PERMISSION_NOTIFICATION = (4587, "权限通知错误")
    INVALID_PERMISSION_SCHEDULING = (4588, "权限调度错误")
    INVALID_PERMISSION_TASK = (4589, "权限任务错误")
    INVALID_PERMISSION_JOB = (4590, "权限作业错误")
    INVALID_PERMISSION_WORKFLOW = (4591, "权限工作流错误")
    INVALID_PERMISSION_SCRIPT = (4592, "权限脚本错误")
    INVALID_PERMISSION_PLUGIN = (4593, "权限插件错误")
    INVALID_PERMISSION_MODULE = (4594, "权限模块错误")
    INVALID_PERMISSION_PACKAGE = (4595, "权限包错误")
    INVALID_PERMISSION_CLASS = (4596, "权限类错误")
    INVALID_PERMISSION_FUNCTION = (4597, "权限函数错误")
    INVALID_PERMISSION_METHOD = (4598, "权限方法错误")
    INVALID_PERMISSION_PROPERTY = (4599, "权限属性错误")
    INVALID_PERMISSION_VARIABLE = (4600, "权限变量错误")
    INVALID_PERMISSION_CONSTANT = (4601, "权限常量错误")
    INVALID_PERMISSION_ENUM = (4602, "权限枚举错误")
    INVALID_PERMISSION_INTERFACE = (4603, "权限接口错误")
    INVALID_PERMISSION_PROTOCOL = (4604, "权限协议错误")
    INVALID_PERMISSION_SERVICE = (4605, "权限服务错误")
    INVALID_PERMISSION_CLIENT = (4606, "权限客户端错误")
    INVALID_PERMISSION_SERVER = (4607, "权限服务器错误")
    INVALID_PERMISSION_SYSTEM = (4608, "权限系统错误")

    def __init__(self, code: int, msg: str) -> None:
        """
        初始化返回码。

        参数:
        - code (int): 错误码。
        - msg (str): 错误信息。

        返回:
        - None
        """
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        """获取错误码"""
        return self._code

    @property
    def msg(self) -> str:
        """获取错误信息"""
        return self._msg


class CommonConstant:
    """
    常用常量

    WWW: www主域名
    HTTP: http请求
    HTTPS: https请求
    LOOKUP_RMI: RMI远程方法调用
    LOOKUP_LDAP: LDAP远程方法调用
    LOOKUP_LDAPS: LDAPS远程方法调用
    YES: 是否为系统默认（是）
    NO: 是否为系统默认（否）
    DEPT_NORMAL: 部门正常状态
    DEPT_DISABLE: 部门停用状态
    UNIQUE: 校验是否唯一的返回标识（是）
    NOT_UNIQUE: 校验是否唯一的返回标识（否）
    """

    # 域名相关
    WWW = "www."
    HTTP = "http://"
    HTTPS = "https://"

    # 远程调用
    LOOKUP_RMI = "rmi:"
    LOOKUP_LDAP = "ldap:"
    LOOKUP_LDAPS = "ldaps:"

    # 系统标识
    YES = "Y"
    NO = "N"

    # 部门状态
    DEPT_NORMAL = "0"  # 正常
    DEPT_DISABLE = "1"  # 停用

    # 唯一性校验
    UNIQUE = True
    NOT_UNIQUE = False


class JobConstant:
    """
    定时任务常量

    JOB_ERROR_LIST: 定时任务禁止调用模块及违规字符串列表
    JOB_WHITE_LIST: 定时任务允许调用模块列表
    """

    JOB_ERROR_LIST = [
        "app",
        "config",
        "exceptions",
        "import ",
        "middlewares",
        "module_admin",
        "open(",
        "os.",
        "server",
        "sub_applications",
        "subprocess.",
        "sys.",
        "utils",
        "while ",
        "__import__",
        """,
        """,
        ",",
        "?",
        ":",
        ";",
        "/",
        "|",
        "+",
        "-",
        "=",
        "~",
        "!",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "<",
        ">",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        " ",
    ]
    JOB_WHITE_LIST = ["function_task"]


class MenuConstant:
    """
    菜单常量

    TYPE_DIR: 菜单类型（目录）
    TYPE_MENU: 菜单类型（菜单）
    TYPE_BUTTON: 菜单类型（按钮）
    YES_FRAME: 是否菜单外链（是）
    NO_FRAME: 是否菜单外链（否）
    LAYOUT: Layout组件标识
    PARENT_VIEW: ParentView组件标识
    INNER_LINK: InnerLink组件标识
    """

    TYPE_DIR = "M"
    TYPE_MENU = "C"
    TYPE_BUTTON = "F"
    YES_FRAME = 0
    NO_FRAME = 1
    LAYOUT = "Layout"
    PARENT_VIEW = "ParentView"
    INNER_LINK = "InnerLink"


class GenConstant:
    """
    代码生成常量

    COLUMNTYPE_STR: 数据库字符串类型
    COLUMNTYPE_TEXT: 数据库文本类型
    COLUMNTYPE_TIME: 数据库时间类型
    COLUMNTYPE_GEOMETRY: 数据库字空间类型
    COLUMNTYPE_NUMBER: 数据库数字类型
    COLUMNNAME_NOT_EDIT: 页面不需要编辑字段
    COLUMNNAME_NOT_LIST: 页面不需要显示的列表字段
    COLUMNNAME_NOT_QUERY: 页面不需要查询字段
    BASE_ENTITY: Entity基类字段
    TREE_ENTITY: Tree基类字段
    HTML_INPUT: 文本框
    HTML_TEXTAREA: 文本域
    HTML_SELECT: 下拉框
    HTML_RADIO: 单选框
    HTML_CHECKBOX: 复选框
    HTML_DATETIME: 日期控件
    HTML_IMAGE_UPLOAD: 图片上传控件
    HTML_FILE_UPLOAD: 文件上传控件
    HTML_EDITOR: 富文本控件
    TYPE_DECIMAL: 高精度计算类型
    TYPE_DATE: 时间类型
    QUERY_LIKE: 模糊查询
    QUERY_EQ: 相等查询
    REQUIRE: 需要
    DB_TO_SQLALCHEMY_TYPE_MAPPING: 数据库类型与sqlalchemy类型映射
    DB_TO_PYTHON_TYPE_MAPPING: 数据库类型与python类型映射
    """

    # 数据库字符串类型
    COLUMNTYPE_STR = (
        ["character varying", "varchar", "character", "char"]
        if settings.DATABASE_TYPE == "postgres"
        else ["char", "varchar", "nvarchar", "varchar2"]
    )

    # 数据库文本类型
    COLUMNTYPE_TEXT = (
        ["text", "citext"]
        if settings.DATABASE_TYPE == "postgres"
        else ["tinytext", "text", "mediumtext", "longtext"]
    )

    # 数据库时间类型
    COLUMNTYPE_TIME = (
        [
            "date",
            "time",
            "time with time zone",
            "time without time zone",
            "timestamp",
            "timestamp with time zone",
            "timestamp without time zone",
            "interval",
        ]
        if settings.DATABASE_TYPE == "postgres"
        else ["datetime", "time", "date", "timestamp"]
    )

    # 数据库字空间类型
    COLUMNTYPE_GEOMETRY = (
        ["point", "line", "lseg", "box", "path", "polygon", "circle"]
        if settings.DATABASE_TYPE == "postgres"
        else [
            "geometry",
            "point",
            "linestring",
            "polygon",
            "multipoint",
            "multilinestring",
            "multipolygon",
            "geometrycollection",
        ]
    )

    # 数据库数字类型
    COLUMNTYPE_NUMBER = [
        "tinyint",
        "smallint",
        "mediumint",
        "int",
        "number",
        "integer",
        "bit",
        "bigint",
        "float",
        "double",
        "decimal",
        "boolean",
        "bool",
    ]
    # 页面不需要显示的添加字段
    COLUMNNAME_NOT_ADD_SHOW = ["created_time", "updated_time"]

    # 页面不需要显示的编辑字段
    COLUMNNAME_NOT_EDIT_SHOW = ["uuid"]

    # 页面不需要编辑字段
    COLUMNNAME_NOT_EDIT = ["id", "uuid", "created_time", "updated_time"]

    # 页面不需要显示的列表字段
    COLUMNNAME_NOT_LIST = ["id", "uuid"]

    # 页面不需要查询字段
    COLUMNNAME_NOT_QUERY = ["id", "uuid", "description"]

    # Crud基类字段
    CRUD_COLUMN_NOT_EDIT = [
        "create_by",
        "description",
        "created_time",
        "updated_time",
    ]

    # 实体基类字段
    BASE_ENTITY = [
        "id",
        "uuid",
        "status",
        "description",
        "created_time",
        "updated_time",
        "created_id",
        "updated_id",
    ]

    # Tree基类字段
    TREE_ENTITY = [
        "parent_name",
        "parent_id",
        "order",
        "ancestors",
        "children",
    ]

    # 文本框
    HTML_INPUT = "input"

    # 文本域
    HTML_TEXTAREA = "textarea"

    # 下拉框
    HTML_SELECT = "select"

    # 单选框
    HTML_RADIO = "radio"

    # 复选框
    HTML_CHECKBOX = "checkbox"

    # 日期控件
    HTML_DATETIME = "datetime"

    # 图片上传控件
    HTML_IMAGE_UPLOAD = "imageUpload"

    # 文件上传控件
    HTML_FILE_UPLOAD = "fileUpload"

    # 富文本控件
    HTML_EDITOR = "editor"

    # 高精度计算类型
    TYPE_DECIMAL = "Decimal"

    # 时间类型
    TYPE_DATE = ["date", "time", "datetime"]

    # 模糊查询
    QUERY_LIKE = "LIKE"

    # 相等查询
    QUERY_EQ = "EQ"

    # 需要
    REQUIRE = True

    # 数据库类型与sqlalchemy类型映射
    DB_TO_SQLALCHEMY = (
        {
            "boolean": "Boolean",
            "smallint": "SmallInteger",
            "integer": "Integer",
            "int4": "Integer",
            "bigint": "BigInteger",
            "real": "Float",
            "double precision": "Float",
            "numeric": "Numeric",
            "character varying": "String",
            "varchar": "String",
            "character": "String",
            "text": "Text",
            "bytea": "LargeBinary",
            "date": "Date",
            "time": "Time",
            "time with time zone": "Time",
            "time without time zone": "Time",
            "timestamp": "DateTime",
            "timestamp with time zone": "DateTime",
            "timestamp without time zone": "DateTime",
            "interval": "Interval",
            "json": "JSON",
            "jsonb": "JSONB",
            "uuid": "Uuid",
            "inet": "INET",
            "cidr": "CIDR",
            "macaddr": "MACADDR",
            "point": "Geometry",
            "line": "Geometry",
            "lseg": "Geometry",
            "box": "Geometry",
            "path": "Geometry",
            "polygon": "Geometry",
            "circle": "Geometry",
            "bit": "Bit",
            "bit varying": "Bit",
            "tsvector": "TSVECTOR",
            "tsquery": "TSQUERY",
            "xml": "String",
            "array": "ARRAY",
            "composite": "JSON",
            "enum": "Enum",
            "range": "Range",
            "money": "Numeric",
            "pg_lsn": "BigInteger",
            "txid_snapshot": "String",
            "oid": "BigInteger",
            "regproc": "String",
            "regclass": "String",
            "regtype": "String",
            "regrole": "String",
            "regnamespace": "String",
            "int2vector": "ARRAY",
            "oidvector": "ARRAY",
            "pg_node_tree": "Text",
        }
        if settings.DATABASE_TYPE == "postgres"
        else {
            # 布尔类型
            "TINYINT": "Boolean",
            # 数值类型
            "SMALLINT": "SmallInteger",
            "MEDIUMINT": "Integer",
            "INT": "Integer",
            "INTEGER": "Integer",
            "BIGINT": "BigInteger",
            "FLOAT": "Float",
            "DOUBLE": "Float",
            "DECIMAL": "DECIMAL",
            "BIT": "Integer",
            "NUMERIC": "Numeric",
            # 日期和时间类型
            "DATE": "Date",
            "TIME": "Time",
            "DATETIME": "DateTime",
            "TIMESTAMP": "TIMESTAMP",
            "YEAR": "Integer",
            # 字符串类型
            "CHAR": "CHAR",
            "VARCHAR": "String",
            "TINYTEXT": "Text",
            "TEXT": "Text",
            "MEDIUMTEXT": "Text",
            "LONGTEXT": "Text",
            "BINARY": "BINARY",
            "VARBINARY": "VARBINARY",
            "TINYBLOB": "LargeBinary",
            "BLOB": "LargeBinary",
            "MEDIUMBLOB": "LargeBinary",
            "LONGBLOB": "LargeBinary",
            # 枚举和集合类型
            "ENUM": "Enum",
            "SET": "String",
            # JSON 类型
            "JSON": "JSON",
            # 空间数据类型（需要扩展支持，如 GeoAlchemy2）
            "GEOMETRY": "Geometry",  # 需要安装 geoalchemy2
            "POINT": "Geometry",
            "LINESTRING": "Geometry",
            "POLYGON": "Geometry",
            "MULTIPOINT": "Geometry",
            "MULTILINESTRING": "Geometry",
            "MULTIPOLYGON": "Geometry",
            "GEOMETRYCOLLECTION": "Geometry",
            # 其他类型
            "BOOL": "Boolean",
            "UUID": "String",
        }
    )

    # 数据库类型与python类型映射
    DB_TO_PYTHON = (
        {
            "boolean": "bool",
            "smallint": "int",
            "integer": "int",
            "int4": "int",
            "bigint": "int",
            "real": "float",
            "double precision": "float",
            "numeric": "Decimal",
            "character varying": "str",
            "varchar": "str",
            "character": "str",
            "text": "str",
            "bytea": "bytes",
            "date": "date",
            "time": "time",
            "time with time zone": "time",
            "time without time zone": "time",
            "timestamp": "datetime",
            "timestamp with time zone": "datetime",
            "timestamp without time zone": "datetime",
            "interval": "timedelta",
            "json": "dict",
            "jsonb": "dict",
            "uuid": "str",
            "inet": "str",
            "cidr": "str",
            "macaddr": "str",
            "point": "list",
            "line": "list",
            "lseg": "list",
            "box": "list",
            "path": "list",
            "polygon": "list",
            "circle": "list",
            "bit": "int",
            "bit varying": "int",
            "tsvector": "str",
            "tsquery": "str",
            "xml": "str",
            "array": "list",
            "composite": "dict",
            "enum": "str",
            "range": "list",
            "money": "Decimal",
            "pg_lsn": "int",
            "txid_snapshot": "str",
            "oid": "int",
            "regproc": "str",
            "regclass": "str",
            "regtype": "str",
            "regrole": "str",
            "regnamespace": "str",
            "int2vector": "list",
            "oidvector": "list",
            "pg_node_tree": "str",
        }
        if settings.DATABASE_TYPE == "postgres"
        else {
            # 布尔类型（特殊处理tinyint(1)）
            "TINYINT": "bool",
            # 数值类型
            "SMALLINT": "int",
            "MEDIUMINT": "int",
            "INT": "int",
            "INTEGER": "int",
            "BIGINT": "int",
            "FLOAT": "float",
            "DOUBLE": "float",
            "NUMERIC": "float",
            "DECIMAL": "Decimal",
            "BIT": "int",
            # 日期和时间类型
            "DATE": "datetime.date",
            "TIME": "datetime.time",
            "DATETIME": "datetime.datetime",
            "TIMESTAMP": "datetime.datetime",
            "YEAR": "int",
            "TINYINT UNSIGNED": "int",  # 无符号小整数类型
            # 布尔类型
            "BOOLEAN": "bool",
            "BOOL": "bool",  # 布尔类型，通常与 BOOLEAN 相同
            # UUID
            "UUID": "str",  # UUID 一般作为字符串
            # 字符串类型
            "CHAR": "str",
            "VARCHAR": "str",
            "TINYTEXT": "str",
            "TEXT": "str",
            "MEDIUMTEXT": "str",
            "LONGTEXT": "str",
            "BINARY": "bytes",
            "VARBINARY": "bytes",
            "TINYBLOB": "bytes",
            "BLOB": "bytes",
            "MEDIUMBLOB": "bytes",
            "LONGBLOB": "bytes",
            # 枚举和集合类型
            "ENUM": "str",
            "SET": "list",
            # JSON 类型
            "JSON": "dict",
            # 空间数据类型（通常需要特殊处理）
            "GEOMETRY": "bytes",  # 空间数据类型，通常存储为字节流
            "POINT": "bytes",  # 点数据类型
            "LINESTRING": "bytes",  # 线数据类型
            "POLYGON": "bytes",  # 多边形数据类型
            "MULTIPOINT": "bytes",  # 多点数据类型
            "MULTILINESTRING": "bytes",  # 多线数据类型
            "MULTIPOLYGON": "bytes",  # 多多边形数据类型
            "GEOMETRYCOLLECTION": "bytes",  # 几何集合类型
        }
    )


class TypedContextProtocol(Protocol):
    perf_time: float

    ip: str
    country: str | None
    region: str | None
    city: str | None

    user_agent: str
    os: str | None
    browser: str | None
    device: str | None

    permission: str | None


# if __name__ == "__main__":
#     print(RET.OK.msg)  # 输出: 成功
