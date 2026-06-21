from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import JWTOutSchema


class CaptchaOutSchema(BaseModel):
    """验证码响应模型"""

    model_config = ConfigDict(from_attributes=True)

    enable: bool = Field(default=True, description="是否启用验证码")
    key: str = Field(..., min_length=1, description="验证码唯一标识")
    img_base: str = Field(..., min_length=1, description="Base64编码的验证码图片")


class AutoLoginUserSchema(BaseModel):
    """免登录用户信息模型"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    name: str = Field(..., description="用户姓名")
    avatar: str | None = Field(default=None, description="头像")


class AutoLoginTokenSchema(BaseModel):
    """免登录Token响应模型"""

    model_config = ConfigDict(from_attributes=True)

    token: str = Field(..., description="免登录Token")
    user: AutoLoginUserSchema = Field(..., description="用户信息")


class TenantOptionSchema(BaseModel):
    """租户选项（用于登录后选择租户）"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="租户ID")
    name: str = Field(..., description="租户名称")
    code: str = Field(..., description="租户编码")


class SelectTenantSchema(BaseModel):
    """选择租户请求"""

    tenant_id: int = Field(..., gt=0, description="租户ID")


class SelectTenantOutSchema(BaseModel):
    """选择租户响应"""

    model_config = ConfigDict(from_attributes=True)

    access_token: str = Field(..., description="访问token（含租户上下文）")
    token_type: str = Field(default="Bearer", description="token类型（RFC 6750）")
    expires_in: int = Field(..., gt=0, description="过期时间(秒)")


class LoginWithTenantsSchema(JWTOutSchema):
    """登录响应（含租户列表）"""

    tenants: list[TenantOptionSchema] = Field(default_factory=list, description="可选租户列表")
    user_info: dict = Field(default_factory=dict, description="用户信息")


class TenantRegisterSchema(BaseModel):
    """租户自助注册请求"""

    username: str = Field(..., min_length=3, max_length=32, description="登录账号")
    password: str = Field(..., min_length=6, max_length=128, description="登录密码")
    email: str = Field(..., max_length=128, description="邮箱（用于接收通知）")
    tenant_name: str | None = Field(default=None, max_length=100, description="企业/团队名称（可选，默认：{用户名}的租户）")


class TenantRegisterOutSchema(BaseModel):
    """租户自助注册响应"""

    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="账号")
    tenant_id: int = Field(..., description="租户ID")
    tenant_name: str = Field(..., description="租户名称")
    tenant_code: str = Field(..., description="租户编码")
    package: str | None = Field(default=None, description="开通套餐")
    trial_end: str = Field(..., description="试用到期日")
    message: str = Field(default="注册成功", description="提示信息")


class ForgotPasswordSchema(BaseModel):
    """忘记密码：提交邮箱，接收重置邮件"""

    email: str = Field(..., max_length=128, description="注册时使用的邮箱")


class ResetPasswordWithTokenSchema(BaseModel):
    """通过邮件链接重置密码"""

    token: str = Field(..., min_length=1, description="密码重置令牌")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码")
