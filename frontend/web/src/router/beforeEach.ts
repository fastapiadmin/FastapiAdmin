/**
 * 路由前置守卫 —— 导航生命周期中的核心编排器。
 *
 * ── 职责 ──
 * 1. 存储失效检测（storage 异常时登出）
 * 2. 登录态校验 & 未登录重定向
 * 3. 动态路由延迟注册（fetch 菜单 → addRoute → 保存）
 * 4. 根路径 `/` → 首页重定向
 * 5. 工作标签同步、页面标题设置
 * 6. 404 / 500 降级兜底
 *
 * ── 核心流程 ──
 * setupBeforeEachGuard() → 注册 `router.beforeEach`
 *   └─ handleRouteGuard()   ← 单一编排入口，按优先级顺序执行
 *        ├─ checkStorageInvalidated()
 *        ├─ handleLoginStatus()
 *        ├─ routeInitFailed 兜底
 *        ├─ handleDynamicRoutes()  ← 按需拉菜单 + addRoute
 *        ├─ handleRootPathRedirect()
 *        └─ setWorktab / setPageTitle / 404
 */
import type { AppRouteRecord } from "@/types/router";
import type { Router, RouteLocationNormalized } from "vue-router";
import { nextTick } from "vue";
import { useSettingsStore, useUserStore, useMenuStore, useWorktabStore } from "@stores";
import { IframeRouteManager, ROUTE_PATH_LOGIN_ALT, staticRoutes } from "./staticRoutes";
import { useCommon } from "@/hooks/core/useCommon";
import { UserAPI } from "@/api/module_system/user";
import {
  NProgress,
  setWorktab,
  setPageTitle,
  loadingService,
  ApiStatus,
  isHttpError,
  resetStorageInvalidated,
  checkStorageInvalidated,
} from "@utils";
import { RouteRegistry } from "./dynamicRoutes";
import { MenuProcessor } from "./MenuProcessor";

// --- 模块级单例与守卫状态 ---

/** 动态路由注册表（惰性创建，首次导航时生成） */
let routeRegistry: RouteRegistry | null = null;

/** 菜单数据处理器（不含注册逻辑，只做列表拉取 + 树形组装） */
const menuProcessor = new MenuProcessor();

/**
 * 全局 loading 开关 —— 动态路由初始化时由 beforeEach 开启，
 * afterEach 收到标志后关闭。
 */
let pendingLoading = false;

/**
 * 路由初始化失败标记 —— 动态路由拉取/注册抛出异常后置为 true，
 * 随后所有导航直接走 500 兜底，避免反复请求造成死循环。
 * `resetRouteInitState()` 可在重新登录后重置。
 */
let routeInitFailed = false;

/**
 * 路由初始化进行中标记 —— 防止并发导航下多次拉取菜单。
 * 第二次导航 `next(false)` 取消，由首次初始化完成后重新恢复。
 */
let routeInitInProgress = false;

export function getPendingLoading(): boolean {
  return pendingLoading;
}

export function resetPendingLoading(): void {
  pendingLoading = false;
}

export function getRouteInitFailed(): boolean {
  return routeInitFailed;
}

/** 重新登录等场景重置初始化标记 */
export function resetRouteInitState(): void {
  routeInitFailed = false;
  routeInitInProgress = false;
}

/** 防止 dev/HMR 或异常重复 init 导致多个 beforeEach 叠加（导航副作用与请求会成倍增长） */
let beforeEachGuardRegistered = false;

export function setupBeforeEachGuard(router: Router): void {
  if (beforeEachGuardRegistered) {
    if (import.meta.env.DEV) {
      console.warn("[Router] setupBeforeEachGuard 已注册，跳过重复调用");
    }
    return;
  }
  beforeEachGuardRegistered = true;

  routeRegistry = new RouteRegistry(router);

  router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
    try {
      return await handleRouteGuard(to, from, router);
    } catch (error) {
      console.error("[RouteGuard] 路由守卫处理失败:", error);
      closeLoading();
      return { name: "500" };
    }
  });
}

function closeLoading(): void {
  if (pendingLoading) {
    nextTick(() => {
      loadingService.hideLoading();
      pendingLoading = false;
    });
  }
}

/**
 * 若路由带有 query/params 传入的 title，写入 meta（净化防注入与过长字符串）
 */
function applySafeTitleFromQuery(to: RouteLocationNormalized): void {
  const rawTitle = (to.params.title as string) || (to.query.title as string);
  if (rawTitle && typeof rawTitle === "string") {
    const safe = rawTitle.replace(/[<>]/g, "").trim().slice(0, 64);
    if (safe) {
      to.meta.title = safe;
    }
  }
}

async function handleRouteGuard(
  to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  router: Router
) {
  // 顺序：登录 → 动态路由初始化失败兜底 → 动态路由注册 → 根路径 → 已匹配页 → 404
  const settingStore = useSettingsStore();
  const userStore = useUserStore();

  if (settingStore.showNprogress) {
    NProgress.start();
  }

  // 检查存储是否已失效（storage/index.ts 检测到异常时标记）
  if (checkStorageInvalidated()) {
    console.info("[RouteGuard] 检测到存储已失效，执行登出");
    await userStore.logout({ navigate: false });
    resetStorageInvalidated();
    return { name: "Login", replace: true };
  }

  const loginRedirect = handleLoginStatus(to, userStore);
  if (loginRedirect) return loginRedirect;

  if (routeInitFailed) {
    return to.matched.length > 0 ? true : { name: "500", replace: true };
  }

  const menuStore = useMenuStore();
  const shouldInitRoutes =
    userStore.isLogin && (!routeRegistry?.isRegistered() || menuStore.menuList.length === 0);

  if (shouldInitRoutes) {
    if (routeInitInProgress) return false;
    return await handleDynamicRoutes(to, router);
  }

  const rootRedirect = handleRootPathRedirect(to);
  if (rootRedirect) return rootRedirect;

  if (to.matched.length > 0) {
    applySafeTitleFromQuery(to);
    setWorktab(to);
    setPageTitle(to);
    return true;
  }

  return { name: "404" };
}

/** @returns undefined 继续守卫，或重定向到登录页的路由 */
function handleLoginStatus(
  to: RouteLocationNormalized,
  userStore: ReturnType<typeof useUserStore>
): Record<string, unknown> | undefined {
  if (userStore.isLogin) {
    if (isLoginRoute(to)) {
      return { path: "/", replace: true };
    }
    return undefined;
  }

  if (isLoginRoute(to) || isAnonymousPublicPath(to.path)) {
    return undefined;
  }

  userStore.resetAllState();
  return { name: "Login", query: { redirect: to.fullPath }, replace: true };
}

/** 登录页（项目里同时存在 `/login` 与 `/auth/login` 等多套入口） */
function isLoginRoute(to: RouteLocationNormalized): boolean {
  return to.path === "/login" || to.path === ROUTE_PATH_LOGIN_ALT || to.name === "Login";
}

/**
 * 无需登录即可访问的路径（登录页由 isLoginRoute 处理，此处为错误页、重定向等）。
 * 勿将挂载 Layout 的业务路由（如 `/home`、`/dashboard/*`、`/profile`）列入此处。
 */
function isAnonymousPublicPath(path: string): boolean {
  if (path.startsWith("/redirect")) return true;
  const allow = new Set(["/401", "/404", "/500", "/403"]);
  return allow.has(path);
}

/** 将父级绝对路径与相对子 path 拼成完整路径（用于识别如 `/` + `home` → `/home`） */
function resolveStaticChildFullPath(parentFullPath: string, segment: string): string {
  const seg = segment.replace(/^\/+/, "");
  if (!parentFullPath || parentFullPath === "/") {
    return `/${seg}`;
  }
  return `${parentFullPath.replace(/\/$/, "")}/${seg}`;
}

/**
 * 检查路由是否为静态路由
 */
function isStaticRoute(path: string): boolean {
  const checkRoute = (routes: any[], targetPath: string, parentFullPath = ""): boolean => {
    return routes.some((route) => {
      // 通配 404（pathMatch）不应视为免登录静态页；静态表里可能与 `/404` 同名，按 path 区分。
      if (route.path === "/:pathMatch(.*)*") {
        return false;
      }

      const routePath = route.path ?? "";
      const fullPath = routePath.startsWith("/")
        ? routePath
        : resolveStaticChildFullPath(parentFullPath, routePath);

      const pattern = fullPath.replace(/:[^/]+/g, "[^/]+").replace(/\*/g, ".*");
      const regex = new RegExp(`^${pattern}$`);

      if (regex.test(targetPath)) {
        return true;
      }
      if (route.children && route.children.length > 0) {
        return checkRoute(route.children, targetPath, fullPath);
      }
      return false;
    });
  };

  return checkRoute(staticRoutes, path);
}

/**
 * 动态路由仍标记为已注册但侧边菜单已被清空时，先卸下动态路由再拉菜单。
 * 典型场景：`logout` 中 `resetRouterState(500)` 延迟执行，用户在 500ms 内再次登录，
 * 守卫若仅判断 `isRegistered()` 会跳过拉菜单，侧栏空白。
 */
function repairDynamicRoutesIfMenuEmpty(): void {
  if (!routeRegistry?.isRegistered()) return;
  const ms = useMenuStore();
  if (ms.menuList.length > 0) return;
  routeRegistry.unregister();
  IframeRouteManager.getInstance().clear();
  ms.removeAllDynamicRoutes();
  resetRouteInitState();
}

/**
 * 处理动态路由注册
 */
async function handleDynamicRoutes(to: RouteLocationNormalized, router: Router) {
  repairDynamicRoutesIfMenuEmpty();

  // 标记初始化进行中
  routeInitInProgress = true;

  // 显示 loading
  pendingLoading = true;
  loadingService.showLoading();

  try {
    // 1. 获取用户信息
    await fetchUserInfo();

    // 2. 获取菜单数据
    const menuList = await menuProcessor.getMenuList();

    // 3. 验证菜单数据
    if (!menuProcessor.validateMenuList(menuList)) {
      throw new Error("获取菜单列表失败，请重新登录");
    }

    // 4. 注册动态路由
    routeRegistry?.register(menuList);

    // 5. 保存菜单数据到 store
    const menuStore = useMenuStore();
    menuStore.setMenuList(menuList);
    menuStore.addRemoveRouteFns(routeRegistry?.getRemoveRouteFns() || []);

    // 6. 保存 iframe 路由
    IframeRouteManager.getInstance().save();

    // 7. 验证工作标签页
    useWorktabStore().validateWorktabs(router);

    // 8. 静态路由不依赖菜单权限，初始化后直接恢复目标地址。
    if (isStaticRoute(to.path)) {
      routeInitInProgress = false;
      return {
        path: to.path,
        query: to.query,
        hash: to.hash,
        replace: true,
      };
    }

    // 8. 验证目标路径权限
    const { homePath } = useCommon();
    const { path: validatedPath, hasPermission } = RoutePermissionValidator.validatePath(
      to.path,
      menuList,
      homePath.value || "/"
    );

    // 初始化成功，重置进行中标记
    routeInitInProgress = false;

    // 9. 重新导航到目标路由
    if (!hasPermission) {
      closeLoading();
      console.warn(`[RouteGuard] 用户无权限访问路径: ${to.path}，已跳转到首页`);
      return { path: validatedPath, replace: true };
    }

    return { path: to.path, query: to.query, hash: to.hash, replace: true };
  } catch (error) {
    console.error("[RouteGuard] 动态路由注册失败:", error);
    closeLoading();

    // 401 错误：axios 拦截器已处理退出登录，取消当前导航
    if (isUnauthorizedError(error)) {
      routeInitInProgress = false;
      return false;
    }

    routeInitFailed = true;
    routeInitInProgress = false;

    if (isHttpError(error)) {
      console.error(`[RouteGuard] 错误码: ${error.code}, 消息: ${error.message}`);
    }

    return { name: "500", replace: true };
  }
}

/**
 * 获取用户信息
 */
async function fetchUserInfo(): Promise<void> {
  const userStore = useUserStore();
  const response = await UserAPI.getCurrentUserInfo();
  const data = response.data.data;
  userStore.setUserInfo(data);
  // 检查并清理工作台标签页（如果是不同用户登录）
  userStore.checkAndClearWorktabs();
}

/**
 * 立即卸下动态路由与菜单缓存（与 {@link resetRouterState} 回调一致，供刷新路由等同步场景）。
 */
export function resetDynamicRoutesSync(): void {
  routeRegistry?.unregister();
  IframeRouteManager.getInstance().clear();

  const menuStore = useMenuStore();
  menuStore.removeAllDynamicRoutes();
  menuStore.setMenuList([]);

  resetRouteInitState();
}

/**
 * 延迟重置路由相关状态（登出等场景避免与导航竞态）
 */
export function resetRouterState(delay: number): void {
  setTimeout(() => {
    resetDynamicRoutesSync();
  }, delay);
}

/**
 * 处理根路径重定向到首页
 * @returns 重定向路由或 false
 */
function handleRootPathRedirect(to: RouteLocationNormalized): Record<string, unknown> | false {
  if (to.path !== "/") return false;

  const { homePath } = useCommon();
  if (homePath.value && homePath.value !== "/") {
    return { path: homePath.value, replace: true };
  }

  return false;
}

/**
 * 判断是否为未授权错误（401）
 */
function isUnauthorizedError(error: unknown): boolean {
  return isHttpError(error) && error.code === ApiStatus.unauthorized;
}

/** 守卫内菜单路径权限校验（扁平菜单路径集合） */
export class RoutePermissionValidator {
  static hasPermission(targetPath: string, menuList: AppRouteRecord[]): boolean {
    if (targetPath === "/") {
      return true;
    }
    return this.matchRoute(targetPath, menuList);
  }

  static buildMenuPathSet(
    menuList: AppRouteRecord[],
    pathSet: Set<string> = new Set()
  ): Set<string> {
    if (!Array.isArray(menuList) || menuList.length === 0) {
      return pathSet;
    }

    for (const menuItem of menuList) {
      if (!menuItem.path) {
        continue;
      }

      const menuPath = menuItem.path.startsWith("/") ? menuItem.path : `/${menuItem.path}`;
      pathSet.add(menuPath);

      if (menuItem.children?.length) {
        this.buildMenuPathSet(menuItem.children, pathSet);
      }
    }

    return pathSet;
  }

  static checkPathPrefix(targetPath: string, pathSet: Set<string>): boolean {
    for (const menuPath of pathSet) {
      if (targetPath.startsWith(`${menuPath}/`)) {
        return true;
      }
    }
    return false;
  }

  static matchRoute(targetPath: string, routes: AppRouteRecord[]): boolean {
    if (!Array.isArray(routes) || routes.length === 0) {
      return false;
    }

    for (const route of routes) {
      if (!route.path) {
        continue;
      }

      const routePath = route.path.startsWith("/") ? route.path : `/${route.path}`;

      if (
        routePath === targetPath ||
        this.isDynamicRouteMatch(targetPath, routePath) ||
        targetPath.startsWith(`${routePath}/`)
      ) {
        return true;
      }

      if (route.children?.length && this.matchRoute(targetPath, route.children)) {
        return true;
      }
    }

    return false;
  }

  static isDynamicRouteMatch(targetPath: string, routePath: string): boolean {
    if (!routePath.includes(":")) {
      return false;
    }

    const pattern = routePath
      .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      .replace(/:([^/]+)/g, "[^/]+")
      .replace(/\\\*/g, ".*");

    return new RegExp(`^${pattern}$`).test(targetPath);
  }

  static validatePath(
    targetPath: string,
    menuList: AppRouteRecord[],
    homePath: string = "/"
  ): { path: string; hasPermission: boolean } {
    const hasPermission = this.hasPermission(targetPath, menuList);

    if (hasPermission) {
      return { path: targetPath, hasPermission: true };
    }

    return { path: homePath, hasPermission: false };
  }
}
