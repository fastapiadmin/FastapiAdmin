import { request } from "@utils";

const API_PATH = "/system/auth";

/** 方案提供方 */
export type OAuthProvider = "wechat" | "qq" | "github" | "gitee";

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

  refreshToken(refreshToken: string) {
    return request<ApiResponse<JWTOut>>({
      url: `${API_PATH}/token/refresh`,
      method: "post",
      data: { refresh_token: refreshToken },
    });
  },

  getCaptcha() {
    return request<ApiResponse<CaptchaInfo>>({
      url: `${API_PATH}/captcha/get`,
      method: "get",
    });
  },

  logout(body: string) {
    return request<ApiResponse>({
      url: `${API_PATH}/logout`,
      method: "post",
      data: body,
    });
  },

  /** 滑块验证完成后端标记 */
  sliderComplete(captchaKey: string) {
    return request<ApiResponse<{ captcha_key: string; verified: boolean }>>({
      url: `${API_PATH}/captcha/slider/complete`,
      method: "post",
      data: { captcha_key: captchaKey },
    });
  },
};

export default AuthAPI;

// ─── Auth 类型定义 ───

/** 登录表单 */
export interface LoginFormData {
  username: string;
  password: string;
  captcha_key?: string;
  captcha?: string;
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
export type LoginResult = JWTOut;

/** 验证码信息 */
export interface CaptchaInfo {
  enable: boolean;
  key: string;
  img_base: string;
}
