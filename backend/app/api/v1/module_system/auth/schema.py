from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import JWTOutSchema


class CaptchaOutSchema(BaseModel):
    """验证码响应模型"""

    model_config = ConfigDict(from_attributes=True)

    enable: bool = Field(default=True, description="是否启用验证码")
    key: str = Field(..., min_length=1, description="验证码唯一标识")
    img_base: str = Field(default="", description="Base64编码的验证码图片（滑块模式为空字符串）")


class LoginOutSchema(JWTOutSchema):
    """登录响应"""

    user_info: dict[str, Any] = Field(default_factory=dict, description="用户信息")


class SliderCompleteSchema(BaseModel):
    """滑块验证完成请求"""

    captcha_key: str = Field(..., min_length=1, description="验证码唯一标识")


class SliderCompleteOutSchema(BaseModel):
    """滑块验证完成响应"""

    captcha_key: str = Field(..., description="验证码唯一标识")
    verified: bool = Field(default=True, description="是否验证通过")
