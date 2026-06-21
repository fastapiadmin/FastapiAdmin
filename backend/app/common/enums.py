from enum import Enum, unique


@unique
class EnvironmentEnum(str, Enum):
    """应用运行环境（开发 / 生产）。"""

    DEV = "dev"
    PROD = "prod"


@unique
class BusinessType(Enum):
    """
    业务操作类型

    OTHER: 其它
    INSERT: 新增
    UPDATE: 修改
    DELETE: 删除
    GRANT: 授权
    EXPORT: 导出
    IMPORT: 导入
    FORCE: 强退
    GENCODE: 生成代码
    CLEAN: 清空数据
    """

    OTHER = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3
    GRANT = 4
    EXPORT = 5
    IMPORT = 6
    FORCE = 7
    GENCODE = 8
    CLEAN = 9


@unique
class RedisInitKeyConfig(Enum):
    """系统内置Redis键名枚举"""

    ACCESS_TOKEN = {"key": "access_token", "remark": "登录令牌信息"}
    REFRESH_TOKEN = {"key": "refresh_token", "remark": "刷新令牌信息"}
    USER_SESSION = {"key": "user_session", "remark": "用户会话信息"}
    CAPTCHA_CODES = {"key": "captcha_codes", "remark": "图片验证码"}
    SYSTEM_CONFIG = {"key": "system_config", "remark": "系统配置"}
    TENANT_CONFIG = {"key": "tenant_config", "remark": "租户配置"}
    SYSTEM_DICT = {"key": "system_dict", "remark": "数据字典"}
    APSCHEDULER_LOCK_KEY = {
        "key": "scheduler_job_lock",
        "remark": "定时任务初始化锁",
    }

    @property
    def key(self) -> str:
        """
        获取 Redis 键名。

        返回:
        - str: 键名字符串。
        """
        return self.value.get("key", "")

    @property
    def remark(self) -> str:
        """
        获取 Redis 键说明。

        返回:
        - str: 说明文案。
        """
        return self.value.get("remark", "")


class McpType(Enum):
    """Mcp 服务器类型"""

    stdio = 0
    sse = 1


class McpLLMProvider(Enum):
    """MCP 大语言模型供应商"""

    openai = "openai"
    deepseek = "deepseek"
    anthropic = "anthropic"
    gemini = "gemini"
    qwen = "qwen"


@unique
class QueueEnum(str, Enum):
    """队列枚举"""

    none = "None"
    not_none = "not None"
    date = "date"
    month = "month"
    like = "like"
    eq = "eq" or "=="
    in_ = "in"
    between = "between"
    ne = "!=" or "ne"
    gt = ">" or "gt"
    ge = ">=" or "ge"
    lt = "<" or "lt"
    le = "<=" or "le"


class PermissionFilterStrategy(str, Enum):
    """
    权限过滤策略枚举

    每个策略对应一种过滤实现，模型通过 ``__permission_strategy__`` 选择。
    注意：``DATA_SCOPE`` 是 dispatcher（基于 ``data_scope`` 字段再分发到
    5 个具体的 data_scope 子策略），其余是具体策略。
    """

    DATA_SCOPE = "data_scope"  # 数据范围权限分发器（默认）
    MENU_AUTH = "menu_auth"  # 菜单授权（用于 MenuModel，按角色-菜单绑定过滤）
    DEPT_RELATION = "dept_relation"  # 部门关联（用于 DeptModel、RoleModel，按所属部门过滤）
    OWN = "own"  # 仅本人数据
    USER_BINDING = "user_binding"  # 用户绑定角色（用于 RoleModel，仅显示当前用户绑定的角色）


@unique
class OrderTypeEnum(str, Enum):
    """订单类型"""

    NEW = "new"
    RENEW = "renew"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    PLUGIN = "plugin"


@unique
class InvoiceTypeEnum(str, Enum):
    """发票类型"""

    VAT_NORMAL = "vat_normal"
    VAT_SPECIAL = "vat_special"


@unique
class TicketTypeEnum(str, Enum):
    """工单类型"""

    SUGGESTION = "suggestion"
    BUG = "bug"
    OPTIMIZE = "optimize"
    OTHER = "other"
