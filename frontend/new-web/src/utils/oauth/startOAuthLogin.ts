import type { OAuthProvider } from "@/api/module_system/auth";

/**
 * 跳转浏览器至后端 OAuth 入口，授权完成后回到 `redirect_uri`（通常为当前站点 /login）。
 */
export function startOAuthLogin(provider: OAuthProvider): void {
  const base = (import.meta.env.VITE_APP_BASE_API || "/api/v1").replace(/\/$/, "");
  const redirectUri = `${window.location.origin}/login`;
  const url = `${base}/system/auth/oauth/${provider}/login?redirect_uri=${encodeURIComponent(redirectUri)}`;
  window.location.href = url;
}
