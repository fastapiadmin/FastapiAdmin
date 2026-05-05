/**
 * 身份验证工具类
 *
 * 集中管理所有与认证相关的功能，包括：
 * - 登录状态判断
 * - Token 的存取（支持记住我功能）
 * - 会话状态清理
 *
 * ## 存储策略
 *
 * 根据「记住我」状态选择存储位置：
 * - `rememberMe = true`: Token 存储在 localStorage，持久化保存
 * - `rememberMe = false`: Token 存储在 sessionStorage，会话结束后自动清除
 *
 * @module utils/auth
 */

/** 认证相关存储键名常量 */
const AUTH_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
  REMEMBER_ME: "remember_me",
} as const;

/**
 * 身份验证工具类
 * 提供静态方法管理 Token 和记住我状态
 */
export class Auth {
  /**
   * 判断用户是否已登录
   *
   * 通过检查是否存在有效的访问令牌来判断登录状态
   *
   * @returns {boolean} 是否已登录
   *
   * @example
   * ```typescript
   * if (Auth.isLoggedIn()) {
   *   console.log('用户已登录');
   * } else {
   *   console.log('用户未登录');
   * }
   * ```
   */
  static isLoggedIn(): boolean {
    return !!Auth.getAccessToken();
  }

  /**
   * 获取当前有效的访问令牌
   *
   * 根据「记住我」状态从适当的存储位置获取 Token
   *
   * @returns {string} 当前有效的访问令牌，若不存在则返回空字符串
   *
   * @example
   * ```typescript
   * const token = Auth.getAccessToken();
   * if (token) {
   *   // 使用 token 进行 API 请求
   * }
   * ```
   */
  static getAccessToken(): string {
    const isRememberMe = Auth.getRememberMe();
    return isRememberMe
      ? localStorage.getItem(AUTH_KEYS.ACCESS_TOKEN) || ""
      : sessionStorage.getItem(AUTH_KEYS.ACCESS_TOKEN) || "";
  }

  /**
   * 获取刷新令牌
   *
   * 根据「记住我」状态从适当的存储位置获取刷新令牌
   *
   * @returns {string} 当前有效的刷新令牌，若不存在则返回空字符串
   *
   * @example
   * ```typescript
   * const refreshToken = Auth.getRefreshToken();
   * if (refreshToken) {
   *   // 使用 refreshToken 刷新访问令牌
   * }
   * ```
   */
  static getRefreshToken(): string {
    const isRememberMe = Auth.getRememberMe();
    return isRememberMe
      ? localStorage.getItem(AUTH_KEYS.REFRESH_TOKEN) || ""
      : sessionStorage.getItem(AUTH_KEYS.REFRESH_TOKEN) || "";
  }

  /**
   * 设置访问令牌和刷新令牌
   *
   * 根据「记住我」状态决定存储位置，并同步清理另一存储位置的旧 Token
   *
   * @param {string} accessToken - 访问令牌
   * @param {string} refreshToken - 刷新令牌
   * @param {boolean} rememberMe - 是否记住我
   *
   * @example
   * ```typescript
   * // 用户选择记住登录状态
   * Auth.setTokens('access_token_value', 'refresh_token_value', true);
   *
   * // 用户不希望记住登录状态
   * Auth.setTokens('access_token_value', 'refresh_token_value', false);
   * ```
   */
  static setTokens(accessToken: string, refreshToken: string, rememberMe: boolean): void {
    localStorage.setItem(AUTH_KEYS.REMEMBER_ME, String(rememberMe));

    if (rememberMe) {
      localStorage.setItem(AUTH_KEYS.ACCESS_TOKEN, accessToken);
      localStorage.setItem(AUTH_KEYS.REFRESH_TOKEN, refreshToken);
    } else {
      sessionStorage.setItem(AUTH_KEYS.ACCESS_TOKEN, accessToken);
      sessionStorage.setItem(AUTH_KEYS.REFRESH_TOKEN, refreshToken);
      localStorage.removeItem(AUTH_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(AUTH_KEYS.REFRESH_TOKEN);
    }
  }

  /**
   * 清除所有身份验证相关的数据
   *
   * 同时清除 localStorage 和 sessionStorage 中的 Token
   *
   * @example
   * ```typescript
   * // 用户退出登录时调用
   * Auth.clearAuth();
   * ```
   */
  static clearAuth(): void {
    localStorage.removeItem(AUTH_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(AUTH_KEYS.REFRESH_TOKEN);
    sessionStorage.removeItem(AUTH_KEYS.ACCESS_TOKEN);
    sessionStorage.removeItem(AUTH_KEYS.REFRESH_TOKEN);
  }

  /**
   * 获取「记住我」状态
   *
   * 从 localStorage 中读取记住我设置
   *
   * @returns {boolean} 是否记住我
   *
   * @example
   * ```typescript
   * const rememberMe = Auth.getRememberMe();
   * console.log(`记住我状态: ${rememberMe}`);
   * ```
   */
  static getRememberMe(): boolean {
    return localStorage.getItem(AUTH_KEYS.REMEMBER_ME) === "true";
  }
}

export { AUTH_KEYS };
