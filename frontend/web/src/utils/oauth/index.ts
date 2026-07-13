import type { OAuthProvider } from "@/api/module_system/auth";

/**
 * 跳转浏览器至后端 OAuth 入口，授权完成后回到 `redirect_uri`（当前站点登录页）。
 *
 * 前端为 Hash 路由并带有部署 base（如 `/web/`），登录页真实地址是
 * `<origin><base>#/login`。后端会把 token 以 query 形式拼在 redirect_uri 之后，
 * 必须落在 `#` 之后，vue-router 的 `route.query` 才能读到。
 */
export function startOAuthLogin(provider: OAuthProvider): void {
  const apiBase = (import.meta.env.VITE_APP_BASE_API || "/api/v1").replace(/\/$/, "");
  const rawBase = import.meta.env.BASE_URL || "/";
  const appBase = rawBase.endsWith("/") ? rawBase : `${rawBase}/`;
  const redirectUri = `${window.location.origin}${appBase}#/login`;
  const url = `${apiBase}/system/auth/oauth/${provider}/login?redirect_uri=${encodeURIComponent(redirectUri)}`;
  window.location.href = url;
}
