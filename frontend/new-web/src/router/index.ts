import type { App } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import { HOME_ROUTE_NAME, ROOT_LAYOUT_ROUTE_NAME, staticRoutes } from "./routes/staticRoutes";
import { setupBeforeEachGuard } from "./guards/beforeEach";
import { setupAfterEachGuard } from "./guards/afterEach";
import "@/utils/ui";

// 创建路由实例
export const router = createRouter({
  history: createWebHashHistory(),
  routes: staticRoutes, // 静态路由
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
