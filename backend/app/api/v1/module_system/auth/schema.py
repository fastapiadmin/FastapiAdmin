from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_system.user.model import UserModel


class AuthSchema(BaseModel):
    """权限认证模型"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: UserModel | None = Field(default=None, description="用户信息")
    check_data_scope: bool = Field(default=True, description="是否检查数据权限")
    db: AsyncSession = Field(description="数据库会话")


class JWTPayloadSchema(BaseModel):
    """JWT载荷模型"""

    sub: str = Field(..., description="用户登录信息")
    is_refresh: bool = Field(default=False, description="是否刷新token")
    exp: datetime | int = Field(..., description="过期时间")

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.sub or len(self.sub.strip()) == 0:
            raise ValueError("会话编号不能为空")
        return self


class JWTOutSchema(BaseModel):
    """JWT响应模型"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., min_length=1, description="访问token")
    refresh_token: str = Field(..., min_length=1, description="刷新token")
    token_type: str = Field(default="Bearer", description="token类型")
    expires_in: int = Field(..., gt=0, description="过期时间(秒)")


class RefreshTokenPayloadSchema(BaseModel):
    """刷新Token载荷模型"""

    refresh_token: str = Field(..., min_length=1, description="刷新token")


class LogoutPayloadSchema(BaseModel):
    """退出登录载荷模型"""

    token: str = Field(..., min_length=1, description="token")


class CaptchaOutSchema(BaseModel):
    """验证码响应模型"""

    model_config = ConfigDict(from_attributes=True)

    enable: bool = Field(default=True, description="是否启用验证码")
    key: str = Field(..., min_length=1, description="验证码唯一标识")
    img_base: str = Field(..., min_length=1, description="Base64编码的验证码图片")
