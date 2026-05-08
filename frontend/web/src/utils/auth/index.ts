/** Auth utilities (web-style, flat module). */

const AUTH_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
  REMEMBER_ME: "remember_me",
} as const;

export class Auth {
  static isLoggedIn(): boolean {
    return !!Auth.getAccessToken();
  }

  static getAccessToken(): string {
    const isRememberMe = Auth.getRememberMe();
    return isRememberMe
      ? localStorage.getItem(AUTH_KEYS.ACCESS_TOKEN) || ""
      : sessionStorage.getItem(AUTH_KEYS.ACCESS_TOKEN) || "";
  }

  static getRefreshToken(): string {
    const isRememberMe = Auth.getRememberMe();
    return isRememberMe
      ? localStorage.getItem(AUTH_KEYS.REFRESH_TOKEN) || ""
      : sessionStorage.getItem(AUTH_KEYS.REFRESH_TOKEN) || "";
  }

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

  static clearAuth(): void {
    localStorage.removeItem(AUTH_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(AUTH_KEYS.REFRESH_TOKEN);
    sessionStorage.removeItem(AUTH_KEYS.ACCESS_TOKEN);
    sessionStorage.removeItem(AUTH_KEYS.REFRESH_TOKEN);
  }

  static getRememberMe(): boolean {
    return localStorage.getItem(AUTH_KEYS.REMEMBER_ME) === "true";
  }
}

export { AUTH_KEYS };

import { router } from "@/router";
import { useUserStore } from "@stores/modules/user.store";
import { ElMessage, ElNotification } from "element-plus";

/** 登录页跳转进行中，合并并发调用，避免重复通知与重复路由 */
let redirectToLoginInFlight: Promise<void> | null = null;

/**
 * 认证失效或需重新登录时跳转登录页：清空本地会话并带上 redirect。
 * 与 HTTP 拦截器、改密后重登等场景共用；并发只执行一次。
 */
export async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  if (redirectToLoginInFlight) return redirectToLoginInFlight;

  redirectToLoginInFlight = (async () => {
    try {
      ElNotification({
        title: "提示",
        message,
        type: "warning",
        duration: 3000,
      });

      await useUserStore().resetAllState();

      const currentPath = router.currentRoute.value.fullPath;
      await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
    } catch (error: any) {
      ElMessage.error(error?.message ?? String(error));
    } finally {
      redirectToLoginInFlight = null;
    }
  })();

  return redirectToLoginInFlight;
}
