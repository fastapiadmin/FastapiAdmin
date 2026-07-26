import type { App } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME, staticRoutes } from "./routes";
import { setupAfterEachGuard, setupBeforeEachGuard } from "./guards";
import "@utils/ui";

/**
 * 路由入口：`staticRoutes` 首屏注册；业务路由由守卫内 `RouteRegistry` 动态挂载。
 * `initRouter` 注册前置/后置守卫并 `app.use(router)`。
 *
 * 选择 Hash 模式（createWebHashHistory）而非 History 模式的原因：
 * - 纯静态部署场景下无需服务端 URL 回落配置（NGINX try_files 等）
 * - 兼容 Electron 等非 HTTP 协议环境
 * - 开发环境 HMR 不受影响
 */
export const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

/** 注册守卫 + 挂载 router 到 Vue app（在 main.ts 调用） */
export async function initRouter(app: App<Element>): Promise<void> {
  setupBeforeEachGuard(router);
  setupAfterEachGuard(router);
  app.use(router);
}

/** 首页 path，供外部获取（须与静态路由首页子路由 path 一致） */
export const HOME_PAGE_PATH = "/home";

export { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME };

/** iframe 路由管理器 */
export { IframeRouteManager } from "./routes";
/** 菜单处理（获取、过滤、壳层补全） */
export { MenuProcessor, builtinFrontendRoutes } from "./MenuProcessor";
