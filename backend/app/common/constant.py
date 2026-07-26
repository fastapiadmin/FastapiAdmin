from app.config.setting import settings


class CommonConstant:
    """常用常量

    HTTP: http请求
    HTTPS: https请求
    YES: 是否为系统默认（是）
    NO: 是否为系统默认（否）
    UNIQUE: 校验是否唯一的返回标识（是）
    NOT_UNIQUE: 校验是否唯一的返回标识（否）
    """

    # 域名相关
    HTTP = "http://"
    HTTPS = "https://"

    # 系统标识
    YES = "Y"
    NO = "N"

    # 唯一性校验
    UNIQUE = True
    NOT_UNIQUE = False


class JobConstant:
    """定时任务常量

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
        "'\"",
        "''",
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


class GenConstant:
    """代码生成常量

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
    COLUMNTYPE_STR = ["character varying", "varchar", "character", "char"] if settings.DATABASE_TYPE == "postgres" else ["char", "varchar", "nvarchar", "varchar2"]

    # 数据库文本类型
    COLUMNTYPE_TEXT = ["text", "citext"] if settings.DATABASE_TYPE == "postgres" else ["tinytext", "text", "mediumtext", "longtext"]

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
            "decimal": "Numeric",
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
            # 布尔语义仅 tinyint(1)，其余 tinyint 在 get_sqlalchemy_type 中映射为 SmallInteger
            "TINYINT": "SmallInteger",
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
    DB_TO_PYTHON = {
        # MySQL 整数类型
        "tinyint": "int",
        "smallint": "int",
        "mediumint": "int",
        "int": "int",
        "integer": "int",
        "bigint": "int",
        # MySQL 浮点类型
        "float": "float",
        "double": "float",
        "decimal": "Decimal",
        "numeric": "Decimal",
        # MySQL 字符串类型
        "char": "str",
        "varchar": "str",
        "tinytext": "str",
        "text": "str",
        "mediumtext": "str",
        "longtext": "str",
        # MySQL 二进制类型
        "binary": "bytes",
        "varbinary": "bytes",
        "tinyblob": "bytes",
        "blob": "bytes",
        "mediumblob": "bytes",
        "longblob": "bytes",
        # MySQL 日期时间类型
        "date": "date",
        "time": "time",
        "datetime": "datetime",
        "timestamp": "datetime",
        "year": "int",
        # MySQL 其他类型
        "json": "dict",
        "enum": "str",
        "set": "str",
        "bit": "int",
        # MySQL 空间数据类型
        "geometry": "bytes",
        "linestring": "bytes",
        "multipoint": "bytes",
        "multilinestring": "bytes",
        "multipolygon": "bytes",
        "geometrycollection": "bytes",
        # PostgreSQL 整数类型
        "int2": "int",
        "int4": "int",
        "int8": "int",
        # PostgreSQL 浮点类型
        "real": "float",
        "double precision": "float",
        "float8": "float",
        # PostgreSQL 字符串类型
        "character": "str",
        "character varying": "str",
        "citext": "str",
        # PostgreSQL 二进制类型
        "bytea": "bytes",
        # PostgreSQL 日期时间类型
        "time with time zone": "time",
        "timetz": "time",
        "time without time zone": "time",
        "timestamptz": "datetime",
        "timestamp with time zone": "datetime",
        "timestamp without time zone": "datetime",
        "interval": "timedelta",
        # PostgreSQL 布尔类型
        "boolean": "bool",
        "bool": "bool",
        # PostgreSQL JSON类型
        "jsonb": "dict",
        # PostgreSQL 其他类型
        "uuid": "str",
        "inet": "str",
        "cidr": "str",
        "macaddr": "str",
        # PostgreSQL 几何类型
        "point": "list",
        "line": "list",
        "lseg": "list",
        "box": "list",
        "path": "list",
        "polygon": "list",
        "circle": "list",
        # PostgreSQL 位类型
        "bit varying": "int",
        "varbit": "int",
        # PostgreSQL 文本搜索类型
        "tsvector": "str",
        "tsquery": "str",
        # PostgreSQL XML类型
        "xml": "str",
        # PostgreSQL 数组类型
        "array": "list",
        # PostgreSQL 范围类型
        "range": "list",
        "int4range": "list",
        "int8range": "list",
        "tsrange": "list",
        "tstzrange": "list",
        "daterange": "list",
        # PostgreSQL 货币类型
        "money": "Decimal",
        # PostgreSQL 对象标识符类型
        "oid": "int",
        "regproc": "str",
        "regclass": "str",
        "regtype": "str",
        "regrole": "str",
        "regnamespace": "str",
        # PostgreSQL 向量类型
        "int2vector": "list",
        "oidvector": "list",
        # PostgreSQL 其他内部类型
        "pg_lsn": "int",
        "txid_snapshot": "str",
        "pg_node_tree": "str",
    }


# API 日期 / 时间 / 日期时间统一展示（validator、jsonable_response_content、文档约定一致）
DATE_DISPLAY_FMT = "%Y-%m-%d"
TIME_DISPLAY_FMT = "%H:%M:%S"
DATETIME_DISPLAY_FMT = "%Y-%m-%d %H:%M:%S"
