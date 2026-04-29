import request from "@/utils/request";

const API_PATH = "/system/auth";

const AuthAPI = {
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
    return request<ApiResponse<LoginResult>>({
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

  /** 获取免登录用户列表 */
  getAutoLoginUsers() {
    return request<ApiResponse<AutoLoginUser[]>>({
      url: `${API_PATH}/auto-login/users`,
      method: "get",
    });
  },

  /** 获取免登录Token */
  getAutoLoginToken(userId: number) {
    return request<ApiResponse<AutoLoginToken>>({
      url: `${API_PATH}/auto-login/token`,
      method: "post",
      params: { user_id: userId },
    });
  },

  /** 免登录 */
  autoLogin(token: string) {
    return request<ApiResponse<LoginResult>>({
      url: `${API_PATH}/auto-login`,
      method: "post",
      params: { token },
    });
  },
};

export default AuthAPI;

/** 登录表单数据 */
export interface LoginFormData {
  username: string;
  password: string;
  captcha_key: string;
  captcha: string;
  remember: boolean;
  login_type: string;
}

// 刷新令牌
export interface RefreshToekenBody {
  refresh_token: string;
}

/** 登录响应 */
export interface LoginResult {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

/** 验证码信息 */
export interface CaptchaInfo {
  enable: boolean;
  key: string;
  img_base: string;
}

/** 退出登录操作 */
export interface LogoutBody {
  token: string;
}

/** 免登录用户信息 */
export interface AutoLoginUser {
  id: number;
  username: string;
  name: string;
  avatar: string | null;
}

/** 免登录Token响应 */
export interface AutoLoginToken {
  token: string;
  user: AutoLoginUser;
}
