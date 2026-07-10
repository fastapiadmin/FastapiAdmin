import { request } from "@utils";

const API_PATH = "/system/auth";

/** 方案提供方 */
export type OAuthProvider = "wechat" | "qq" | "github" | "gitee" | "feishu";

const AuthAPI = {
  /**
   * 登录
   * @param body 登录参数
   * @returns 登录响应
   */
  login(body: LoginFormData) {
    return request<ApiResponse<LoginResult>>({
      url: `${API_PATH}/login`,
      method: "post",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      data: body,
    });
  },

  refreshToken(body: RefreshToekenBody) {
    return request<ApiResponse<JWTOut>>({
      url: `${API_PATH}/token/refresh`,
      method: "post",
      data: body,
    });
  },

  getCaptcha() {
    return request<ApiResponse<CaptchaInfo>>({
      url: `${API_PATH}/captcha/get`,
      method: "get",
    });
  },

  logout(body: LogoutBody) {
    return request<ApiResponse>({
      url: `${API_PATH}/logout`,
      method: "post",
      data: body,
    });
  },

  /** 获取当前用户的可选租户列表 */
  getTenants() {
    return request<ApiResponse<TenantOption[]>>({
      url: `${API_PATH}/tenants`,
      method: "get",
    });
  },

  /** 选择租户，返回含 tenant_id 的新 JWT */
  selectTenant(tenantId: number) {
    return request<ApiResponse<SelectTenantResult>>({
      url: `${API_PATH}/select-tenant`,
      method: "post",
      data: { tenant_id: tenantId },
    });
  },
  /** 租户自助注册（PRD §4.5） */
  tenantRegister(body: TenantRegisterForm) {
    return request<ApiResponse<TenantRegisterResult>>({
      url: `${API_PATH}/tenant/register`,
      method: "post",
      data: body,
    });
  },
};

export default AuthAPI;

export interface TenantRegisterForm {
  username: string;
  password: string;
  email: string;
  tenant_name?: string;
}

export interface TenantRegisterResult {
  user_id: number;
  username: string;
  tenant_id: number;
  tenant_name: string;
  tenant_code: string;
  package: string | null;
  trial_end: string;
  message: string;
}

// ─── Auth 类型定义 ───

/** 登录表单 */
export interface LoginFormData {
  username: string;
  password: string;
  captcha?: string;
  captcha_key?: string;
  remember?: boolean;
  login_type?: string;
}

/** JWT 响应 (JWTOutSchema) */
export interface JWTOut {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

/** 登录成功返回 */
export interface LoginResult extends JWTOut {
  tenants?: TenantOption[];
}

/** 刷新 Token 请求体 */
export interface RefreshToekenBody {
  refresh_token: string;
}

/** 退出登录请求体 */
export interface LogoutBody {
  token: string;
}

/** 租户选项 */
export interface TenantOption {
  id: number;
  name: string;
  code: string;
}

/** 选择租户返回 (SelectTenantOutSchema) */
export interface SelectTenantResult {
  access_token: string;
  token_type: string;
  expires_in: number;
}

/** 验证码信息 */
export interface CaptchaInfo {
  enable: boolean;
  key: string;
  img_base: string;
}
