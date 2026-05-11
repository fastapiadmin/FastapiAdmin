import type { App } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME, staticRoutes } from "./staticRoutes";
import { setupBeforeEachGuard } from "./beforeEach";
import { setupAfterEachGuard } from "./afterEach";
import "@utils/ui";

/**
 * 路由入口：`staticRoutes` 首屏注册；业务路由由 `beforeEach` 内 `RouteRegistry` 动态挂载。
 * `initRouter` 注册前置/后置守卫并 `app.use(router)`。
 */
export const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
});

export function initRouter(app: App<Element>): void {
  setupBeforeEachGuard(router);
  setupAfterEachGuard(router);
  app.use(router);
}

/** 须与 `staticRoutes` 首页子路由 path 一致 */
export const HOME_PAGE_PATH = "/home";

export { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME };

/** 动态路由注册与菜单转换（一般从 `@/router` 按需导入） */
export { RouteRegistry, ComponentLoader, RouteTransformer, RouteValidator } from "./dynamicRoutes";
export type { ValidationResult } from "./dynamicRoutes";
export { IframeRouteManager } from "./staticRoutes";
export { MenuProcessor, builtinFrontendRoutes } from "./MenuProcessor";
export { RoutePermissionValidator } from "./beforeEach";
