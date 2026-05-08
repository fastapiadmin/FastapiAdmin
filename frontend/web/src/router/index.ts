import type { App } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME, staticRoutes } from "./staticRoutes";
import { setupBeforeEachGuard } from "./beforeEach";
import { setupAfterEachGuard } from "./afterEach";
import "@utils/ui";

/**
 * 路由分层：`staticRoutes` 一次性注册（登录页、首页、仪表盘、异常页等）；
 * 业务菜单来自后端或壳层合并后再由守卫动态 `addRoute`。
 */
export const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes,
  // 刷新时，滚动条位置还原
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

// 初始化路由
export function initRouter(app: App<Element>): void {
  setupBeforeEachGuard(router); // 路由前置守卫
  setupAfterEachGuard(router); // 路由后置守卫
  app.use(router);
}

// 主页路径；须与 `staticRoutes` 中首页子路由一致（当前为 `/home`）
export const HOME_PAGE_PATH = "/home";

export { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME };

/** 供 `@/router` 一处导入的运行时模块 */
export { RouteRegistry, ComponentLoader, RouteTransformer, RouteValidator } from "./dynamicRoutes";
export type { ValidationResult } from "./dynamicRoutes";
export { IframeRouteManager } from "./staticRoutes";
export { MenuProcessor, builtinFrontendRoutes } from "./MenuProcessor";
export { RoutePermissionValidator } from "./beforeEach";
