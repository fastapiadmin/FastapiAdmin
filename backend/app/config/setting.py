# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

from app.common.enums import EnvironmentEnum
from app.config.path_conf import BASE_DIR, ENV_DIR


class Settings(BaseSettings):
    """系统配置类"""
    model_config = SettingsConfigDict(
        env_file=ENV_DIR / f".env.{os.getenv('ENVIRONMENT')}",
        env_file_encoding="utf-8",
        extra='ignore',
        case_sensitive=True, # 区分大小写
    )

    # ================================================= #
    # ******************* 项目环境 ****************** #
    # ================================================= #
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV

    # ================================================= #
    # ******************* 服务器配置 ****************** #
    # ================================================= #
    SERVER_HOST: str = '0.0.0.0'        # 允许访问的IP地址
    SERVER_PORT: int = 8001             # 服务端口

    # ================================================= #
    # ******************* API文档配置 ****************** #
    # ================================================= #
    DEBUG: bool = True            # 调试模式
    TITLE: str = "🎉 FastapiAdmin 🎉 -dev"  # 文档标题
    VERSION: str = '0.1.0'        # 版本号
    DESCRIPTION: str = "该项目是一个基于python的web服务框架，基于fastapi和sqlalchemy实现。"  # 文档描述
    SUMMARY: str = "接口汇总"      # 文档概述
    DOCS_URL: str = "/docs"      # Swagger UI路径
    REDOC_URL: str = "/redoc"    # ReDoc路径
    ROOT_PATH: str = "/api/v1"   # API路由前缀

    # ================================================= #
    # ******************** 跨域配置 ******************** #
    # ================================================= #
    CORS_ORIGIN_ENABLE: bool = True    # 是否启用跨域
    # ALLOW_ORIGINS: List[str] = ["*"]   # 允许的域名列表
    ALLOW_ORIGINS: List[str] = [
        'http://127.0.0.1:8001',
        'http://localhost:5180',
    ]   # 允许的域名列表
    ALLOW_METHODS: List[str] = ["*"]   # 允许的HTTP方法
    ALLOW_HEADERS: List[str] = ["*"]   # 允许的请求头
    ALLOW_CREDENTIALS: bool = True     # 是否允许携带cookie
    CORS_EXPOSE_HEADERS: list[str] = ['X-Request-ID']

    # ================================================= #
    # ******************* 登录认证配置 ****************** #
    # ================================================= #
    SECRET_KEY: str = "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=krylxcjq75vzps$"  # JWT密钥
    ALGORITHM: str = "HS256"                                                # JWT算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24 * 1                     # access_token过期时间(秒)1 天
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 60 * 24 * 7                    # refresh_token过期时间(秒)7 天
    TOKEN_TYPE: str = "bearer"                                              # token类型
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [                               # JWT / RBAC 路由白名单
        'api/v1/auth/login',
    ]

    # ================================================= #
    # ******************** 数据库配置 ******************* #
    # ================================================= #
    SQL_DB_ENABLE: bool = True                             # 是否启用数据库
    DATABASE_ECHO: bool | Literal['debug'] = False         # 是否显示SQL日志
    ECHO_POOL: bool | Literal['debug'] = False             # 是否显示连接池日志
    POOL_SIZE: int = 10                                    # 连接池大小
    MAX_OVERFLOW: int = 20                                 # 最大溢出连接数
    POOL_TIMEOUT: int = 30                                 # 连接超时时间(秒)
    POOL_RECYCLE: int = 1800                               # 连接回收时间(秒)
    POOL_USE_LIFO: bool = True                             # 是否使用LIFO连接池
    POOL_PRE_PING: bool = True                             # 是否开启连接预检
    FUTURE: bool = True                                    # 是否使用SQLAlchemy 2.0特性
    AUTOCOMMIT: bool = False                               # 是否自动提交
    AUTOFETCH: bool = False                                # 是否自动刷新
    EXPIRE_ON_COMMIT: bool = False                         # 是否在提交时过期

    # 数据库类型
    DATABASE_TYPE: Literal['mysql', 'postgres'] = 'mysql'
    

    # MySQL/PostgreSQL数据库连接
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = 'root'
    DATABASE_PASSWORD: str = 'ServBay.dev'
    DATABASE_NAME: str = 'fastapiadmin'

    # ================================================= #
    # ******************** Redis配置 ******************* #
    # ================================================= #
    REDIS_ENABLE: bool = True  # 是否启用Redis
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB_NAME: int = 1
    REDIS_USER: str = ''
    REDIS_PASSWORD: str = ''

    # ================================================= #
    # ******************** 验证码配置 ******************* #
    # ================================================= #
    CAPTCHA_ENABLE: bool = True                              # 是否启用验证码
    CAPTCHA_EXPIRE_SECONDS: int = 60 * 1                     # 验证码过期时间(秒) 1分钟
    CAPTCHA_FONT_SIZE: int = 40                              # 字体大小
    CAPTCHA_FONT_PATH: str = 'static/assets/font/Arial.ttf'  # 字体路径

    # ================================================= #
    # ********************* 日志配置 ******************* #
    # ================================================= #
    OPERATION_LOG_RECORD: bool = True                                                               # 是否记录操作日志
    IGNORE_OPERATION_FUNCTION: List[str] = ["get_captcha_for_login"]                                # 忽略记录的函数
    OPERATION_RECORD_METHOD: List[str] = ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]      # 需要记录的请求方法

    # ================================================= #
    # ******************* Gzip压缩配置 ******************* #
    # ================================================= #
    GZIP_ENABLE: bool = True        # 是否启用Gzip
    GZIP_MIN_SIZE: int = 1000       # 最小压缩大小(字节)
    GZIP_COMPRESS_LEVEL: int = 9    # 压缩级别(1-9)

    # ================================================= #
    # ***************** 静态文件配置 ***************** #
    # ================================================= #
    STATIC_ENABLE: bool = True                            # 是否启用静态文件
    STATIC_URL: str = "/static"                           # 访问路由
    STATIC_DIR: str = "static"                            # 目录名
    STATIC_ROOT: Path = BASE_DIR.joinpath(STATIC_DIR)     # 绝对路径

    # ================================================= #
    # ***************** 动态文件配置 ***************** #
    # ================================================= #
    UPLOAD_FILE_PATH: Path = Path('static/upload')    # 上传目录
    UPLOAD_MACHINE: str = 'A'                         # 上传机器标识
    ALLOWED_EXTENSIONS: list[str] = [                 # 允许的文件类型
        '.gif', '.jpg', '.jpeg', '.png', '.ico', '.svg', '.xls', '.xlsx'
    ]
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 最大文件大小(10MB)

    # ================================================= #
    # ***************** Swagger配置 ***************** #
    # ================================================= #
    SWAGGER_CSS_URL: str = "static/swagger/swagger-ui/swagger-ui.css"
    SWAGGER_JS_URL: str = "static/swagger/swagger-ui/swagger-ui-bundle.js"
    REDOC_JS_URL: str = "static/swagger/redoc/bundles/redoc.standalone.js"
    FAVICON_URL: str = "static/swagger/favicon.png"

    # ================================================= #
    # ******************* AI大模型配置 ****************** #
    # ================================================= #
    OPENAI_BASE_URL: str = ''
    OPENAI_API_KEY: str = ''
    OPENAI_MODEL: str = ''

    # ================================================= #
    # ******************* 请求限制配置 ****************** #
    # ================================================= #
    REQUEST_LIMITER_REDIS_PREFIX: str = 'fastapiadmin:request_limiter:'

    # ================================================= #
    # ******************* 重构配置 ******************* #
    # ================================================= #
    @property
    def MIDDLEWARE_LIST(self) -> List[Optional[str]]:
        """获取项目根目录"""
        # 中间件列表
        MIDDLEWARES: List[Optional[str]] = [
            "app.core.middlewares.CustomCORSMiddleware" if self.CORS_ORIGIN_ENABLE else None,
            "app.core.middlewares.RequestLogMiddleware" if self.OPERATION_LOG_RECORD else None,
            "app.core.middlewares.CustomGZipMiddleware" if self.GZIP_ENABLE else None,
        ]
        return MIDDLEWARES

    @property
    def EVENT_LIST(self) -> List[Optional[str]]:
        """获取事件列表"""
        EVENTS: List[Optional[str]] = [
            "app.core.database.redis_connect" if self.REDIS_ENABLE else None,
        ]
        return EVENTS

    @property
    def ASYNC_DB_URI(self) -> str:
        """获取异步数据库连接"""
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+asyncmy://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
        elif self.DATABASE_TYPE == "postgres":
            return f"postgresql+asyncpg://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        else:
            raise ValueError(f"数据库驱动不支持: {self.DATABASE_TYPE}, 请选择 请选择 mysql、postgres")

    @property
    def DB_URI(self) -> str:
        """获取同步数据库连接"""
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+pymysql://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?charset=utf8mb4"
        elif self.DATABASE_TYPE == "postgres":
            return f"postgresql+psycopg2://{self.DATABASE_USER}:{quote_plus(self.DATABASE_PASSWORD)}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        else:
            raise ValueError(f"数据库驱动不支持: {self.DATABASE_TYPE}, 请选择 请选择 mysql、postgres")
    
    @property
    def REDIS_URI(self) -> str:
        """获取Redis连接"""
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_NAME}"
    
    @property
    def FASTAPI_CONFIG(self) -> dict[str, Any]:
        """获取FastAPI应用属性"""
        return {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "summary": self.SUMMARY,
            "docs_url": None,
            "redoc_url": None,
            "root_path": self.ROOT_PATH
        }
    

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()

settings = get_settings()
