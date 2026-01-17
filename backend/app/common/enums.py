from enum import Enum, unique


@unique
class EnvironmentEnum(str, Enum):
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
    CAPTCHA_CODES = {"key": "captcha_codes", "remark": "图片验证码"}
    SYSTEM_CONFIG = {"key": "system_config", "remark": "系统配置"}
    SYSTEM_DICT = {"key": "system_dict", "remark": "数据字典"}
    APSCHEDULER_LOCK_KEY = {
        "key": "scheduler_job_lock",
        "remark": "定时任务初始化锁",
    }

    @property
    def key(self) -> str:
        """获取Redis键名"""
        return self.value.get("key", "")

    @property
    def remark(self) -> str:
        """获取Redis键名说明"""
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
