from functools import wraps
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.common.enums import RET, EnvironmentEnum
from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.logger import logger


def require_superadmin(func):
    """装饰器：仅超级管理员可调用 Service 方法。

    自动校验 ``self.auth.user.is_superuser`` 属性，非超管直接抛出 403。
    适用于实例方法（``Service(auth).xxx(...)``），由 ``self.auth`` 取认证上下文。

    用法:
        class XxxService:
            def __init__(self, auth: AuthSchema) -> None:
                self.auth = auth

            @require_superadmin
            async def create(self, data: ...) -> ...:
                ...
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.auth.user or not self.auth.user.is_superuser:
            raise CustomException(msg="仅平台管理员可操作")
        return await func(self, *args, **kwargs)

    return wrapper


class CustomException(Exception):
    def __init__(
        self,
        msg: str = RET.EXCEPTION.msg,
        code: int = RET.EXCEPTION.code,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        data: Any | None = None,
        success: bool = False,
    ) -> None:
        super().__init__(msg)
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def __str__(self) -> str:
        return self.msg


def handle_exception(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        logger.error(
            "[自定义异常] {} {} | code={} | msg={} | data={}",
            request.method,
            request.url.path,
            exc.code,
            exc.msg,
            exc.data,
        )
        # 生产环境不外泄 data（可能含 SQL 字段、约束名等内部细节）
        expose_data = exc.data if settings.ENVIRONMENT != EnvironmentEnum.PROD else None
        return ErrorResponse(msg=exc.msg, code=exc.code, status_code=exc.status_code, data=expose_data)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        logger.error(
            "[HTTP异常] {} {} | status_code={} | detail={}",
            request.method,
            request.url.path,
            exc.status_code,
            exc.detail,
        )
        return ErrorResponse(msg=exc.detail, status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        msg = errors[0].get("msg", str(errors[0])) if errors else "请求参数验证失败"
        if msg.startswith("Value error"):
            msg = msg[11:].lstrip(" ,")
        logger.error(
            "[参数验证异常] {} {} | errors={}",
            request.method,
            request.url.path,
            errors,
        )
        return ErrorResponse(msg=str(msg), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, data=errors)

    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
        logger.error(
            "[响应验证异常] {} {} | errors={}",
            request.method,
            request.url.path,
            exc.errors(),
        )
        return ErrorResponse(msg="服务器响应格式错误", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=exc.body)

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        exc_type = type(exc).__name__

        if isinstance(exc, IntegrityError):
            detail = str(exc.orig) if exc.orig else str(exc)
            expose_detail = detail if settings.ENVIRONMENT != EnvironmentEnum.PROD else None
            if "connect" in detail or "connection" in detail:
                return ErrorResponse(msg="数据库连接失败", status_code=status.HTTP_403_SERVICE_UNAVAILABLE, data=expose_detail)
            if "Duplicate entry" in detail:
                return ErrorResponse(msg="数据重复，请检查唯一字段", status_code=status.HTTP_409_CONFLICT, data=expose_detail)
            if "foreign key constraint" in detail:
                return ErrorResponse(msg="存在关联数据，无法删除", status_code=status.HTTP_409_CONFLICT, data=expose_detail)
            if "cannot be null" in detail:
                return ErrorResponse(msg="必填字段缺失", status_code=status.HTTP_409_CONFLICT, data=expose_detail)
            return ErrorResponse(msg="数据已存在或违反完整性约束", status_code=status.HTTP_409_CONFLICT, data=expose_detail)

        logger.error("[数据库异常] {} {} | type={} | detail={}", request.method, request.url.path, exc_type, exc)
        data = str(exc) if settings.ENVIRONMENT != EnvironmentEnum.PROD else None
        return ErrorResponse(msg=f"数据库操作失败: {exc_type}", status_code=status.HTTP_400_BAD_REQUEST, data=data)

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError) -> JSONResponse:
        logger.error("[值异常] {} {} | msg={}", request.method, request.url.path, exc)
        return ErrorResponse(msg=str(exc), status_code=status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        exc_type = type(exc).__name__
        logger.error(
            "[未捕获异常] {} {} | type={} | detail={}",
            request.method,
            request.url.path,
            exc_type,
            exc,
        )
        return ErrorResponse(msg="服务器内部错误", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
