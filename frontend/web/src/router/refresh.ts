/**
 * 路由刷新/重置工具函数
 *
 * guards.ts 和 store/index.ts 共享的路由操作模块。
 * router 实例由调用方作为参数传入，存储通过静态导入获取。
 *
 * @module router/refresh
 */
import type { Router } from "vue-router";
import { useMenuStore, useWorktabStore } from "@/store";
import { MenuProcessor } from "./MenuProcessor";
import { IframeRouteManager } from "./routes";

// ──────── 守卫状态 ────────
export const refreshState = {
  pendingLoading: false,
  routeInitFailed: false,
  dynamicRoutesRegistered: false,
};

export function resetRouteInitState(): void {
  refreshState.routeInitFailed = false;
  refreshState.dynamicRoutesRegistered = false;
}

// ──────── 路由操作 ────────

/** 异步清理已注册的动态路由和菜单 */
export async function resetDynamicRoutesSync(): Promise<void> {
  const menuStore = useMenuStore();
  const removeRouteFns = menuStore.removeRouteFns;
  removeRouteFns.forEach((fn: () => void) => fn());
  menuStore.menuList.length = 0;
  menuStore.removeRouteFns.length = 0;
  IframeRouteManager.getInstance().clear();
}

/** 重新拉菜单 + 重新注册（管理员手动刷新菜单时调用） */
export async function refreshMenuAndRoutes(router: Router): Promise<void> {
  await resetDynamicRoutesSync();
  const { RouteRegistry } = await import("./route-loader");
  const menuProcessor = new MenuProcessor();
  const menuList = await menuProcessor.getMenuList();
  // 更新侧栏菜单并注册动态路由
  useMenuStore().setMenuList(menuList);
  const routeRegistry = new RouteRegistry(router);
  routeRegistry.register(menuList);
  useMenuStore().addRemoveRouteFns(routeRegistry.getRemoveRouteFns());
  // 菜单变更后清理无效的持久化标签
  useWorktabStore().validateWorktabs(router);
}

/** 延迟重置（token 过期降级时使用 3000ms 等待过渡动画） */
export async function resetRouterState(delay: number = 0): Promise<void> {
  if (delay > 0) {
    await new Promise((resolve) => setTimeout(resolve, delay));
  }
  await resetDynamicRoutesSync();
}
