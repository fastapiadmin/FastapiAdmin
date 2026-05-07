/**
 * 路由全局前置守卫模块
 *
 * 提供完整的路由导航守卫功能
 *
 * ## 主要功能
 *
 * - 登录状态验证和重定向
 * - 动态路由注册和权限控制
 * - 菜单数据获取和处理（前端/后端模式）
 * - 用户信息获取和缓存
 * - 页面标题设置
 * - 工作标签页管理
 * - 进度条和加载动画控制
 * - 静态路由识别和处理
 * - 错误处理和异常跳转
 *
 * ## 使用场景
 *
 * - 路由跳转前的权限验证
 * - 动态菜单加载和路由注册
 * - 用户登录状态管理
 * - 页面访问控制
 * - 路由级别的加载状态管理
 *
 * ## 工作流程
 *
 * 1. 检查登录状态，未登录跳转到登录页
 * 2. 首次访问时获取用户信息和菜单数据
 * 3. 根据权限动态注册路由
 * 4. 设置页面标题和工作标签页
 * 5. 处理根路径重定向到首页
 * 6. 未匹配路由跳转到 404 页面
 *
 * @module router/guards/beforeEach
 * @author FastapiAdmin Team
 */
import type { Router, RouteLocationNormalized, NavigationGuardNext } from "vue-router";
import { nextTick } from "vue";
import { NProgress } from "@/utils/ui";
import { useSettingsStore } from "@/store/modules/setting.store";
import { useUserStore } from "@/store/modules/user.store";
import { useMenuStore } from "@/store/modules/menu.store";
import { setWorktab } from "@/utils/navigation";
import { setPageTitle } from "@/utils/navigation";
import { ROUTE_PATH_LOGIN_ALT, staticRoutes } from "../routes/staticRoutes";
import { loadingService } from "@/utils/ui";
import { useCommon } from "@/hooks/core/useCommon";
import { useWorktabStore } from "@/store/modules/worktab.store";
import { UserAPI } from "@/api/module_system/user";
import { ApiStatus, isHttpError } from "@/utils/http";
import {
  RouteRegistry,
  MenuProcessor,
  IframeRouteManager,
  RoutePermissionValidator,
} from "../core";

// 路由注册器实例
let routeRegistry: RouteRegistry | null = null;

// 菜单处理器实例
const menuProcessor = new MenuProcessor();

// 跟踪是否需要关闭 loading
let pendingLoading = false;

// 路由初始化失败标记，防止死循环
// 一旦设置为 true，只有刷新页面或重新登录才能重置
let routeInitFailed = false;

// 路由初始化进行中标记，防止并发请求
let routeInitInProgress = false;

/**
 * 获取 pendingLoading 状态
 */
export function getPendingLoading(): boolean {
  return pendingLoading;
}

/**
 * 重置 pendingLoading 状态
 */
export function resetPendingLoading(): void {
  pendingLoading = false;
}

/**
 * 获取路由初始化失败状态
 */
export function getRouteInitFailed(): boolean {
  return routeInitFailed;
}

/**
 * 重置路由初始化状态（用于重新登录场景）
 */
export function resetRouteInitState(): void {
  routeInitFailed = false;
  routeInitInProgress = false;
}

/**
 * 设置路由全局前置守卫
 */
export function setupBeforeEachGuard(router: Router): void {
  // 初始化路由注册器
  routeRegistry = new RouteRegistry(router);

  router.beforeEach(
    async (
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      next: NavigationGuardNext
    ) => {
      try {
        await handleRouteGuard(to, from, next, router);
      } catch (error) {
        console.error("[RouteGuard] 路由守卫处理失败:", error);
        closeLoading();
        next({ name: "500" });
      }
    }
  );
}

/**
 * 关闭 loading 效果
 */
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

/**
 * 处理路由守卫逻辑
 */
async function handleRouteGuard(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext,
  router: Router
): Promise<void> {
  const settingStore = useSettingsStore();
  const userStore = useUserStore();

  // 启动进度条
  if (settingStore.showNprogress) {
    NProgress.start();
  }

  // 1. 检查登录状态
  if (!handleLoginStatus(to, userStore, next)) {
    return;
  }

  // 2. 检查路由初始化是否已失败（防止死循环）
  if (routeInitFailed) {
    // 已经失败过，直接放行到错误页面，不再重试
    if (to.matched.length > 0) {
      next();
    } else {
      // 未匹配到路由，跳转到 500 页面
      next({ name: "500", replace: true });
    }
    return;
  }

  // 3. 处理动态路由注册
  const menuStore = useMenuStore();
  /** 未注册动态路由，或菜单已被清空（登出延迟 reset 与再登录竞态下可能出现「已注册但 menuList 为空」） */
  const shouldInitRoutes =
    userStore.isLogin && (!routeRegistry?.isRegistered() || menuStore.menuList.length === 0);

  if (shouldInitRoutes) {
    // 防止并发请求（快速连续导航场景）
    if (routeInitInProgress) {
      // 正在初始化中，等待完成后重新导航
      next(false);
      return;
    }
    await handleDynamicRoutes(to, next, router);
    return;
  }

  // 4. 处理根路径重定向
  if (handleRootPathRedirect(to, next)) {
    return;
  }

  // 5. 处理已匹配的路由
  if (to.matched.length > 0) {
    applySafeTitleFromQuery(to);
    setWorktab(to);
    setPageTitle(to);
    next();
    return;
  }

  // 6. 未匹配到路由，跳转到 404
  next({ name: "404" });
}

/**
 * 处理登录状态
 * @returns true 表示可以继续，false 表示已处理跳转
 */
function handleLoginStatus(
  to: RouteLocationNormalized,
  userStore: ReturnType<typeof useUserStore>,
  next: NavigationGuardNext
): boolean {
  // 已登录 / 登录相关路由 / 明确配置的匿名白名单，放行。
  // 注意：不能使用「整条 staticRoutes 都算静态」——否则 `/`、`/` 重定向到的业务页也会被当成免登录，
  // 未登录用户会先被放过再跳首页（见 issue：打开站点先进首页而非登录页）。
  if (userStore.isLogin || isLoginRoute(to) || isAnonymousPublicPath(to.path)) {
    return true;
  }

  // 未登录且访问需要权限的页面，跳转到登录页并携带 redirect 参数
  userStore.resetAllState();
  next({
    name: "Login",
    query: { redirect: to.fullPath },
  });
  return false;
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
async function handleDynamicRoutes(
  to: RouteLocationNormalized,
  next: NavigationGuardNext,
  router: Router
): Promise<void> {
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
      next({
        path: to.path,
        query: to.query,
        hash: to.hash,
        replace: true,
      });
      return;
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
      // 无权限访问，跳转到首页
      closeLoading();

      // 输出警告信息
      console.warn(`[RouteGuard] 用户无权限访问路径: ${to.path}，已跳转到首页`);

      // 直接跳转到首页
      next({
        path: validatedPath,
        replace: true,
      });
    } else {
      // 有权限，正常导航
      next({
        path: to.path,
        query: to.query,
        hash: to.hash,
        replace: true,
      });
    }
  } catch (error) {
    console.error("[RouteGuard] 动态路由注册失败:", error);

    // 关闭 loading
    closeLoading();

    // 401 错误：axios 拦截器已处理退出登录，取消当前导航
    if (isUnauthorizedError(error)) {
      // 重置状态，允许重新登录后再次初始化
      routeInitInProgress = false;
      next(false);
      return;
    }

    // 标记初始化失败，防止死循环
    routeInitFailed = true;
    routeInitInProgress = false;

    // 输出详细错误信息，便于排查
    if (isHttpError(error)) {
      console.error(`[RouteGuard] 错误码: ${error.code}, 消息: ${error.message}`);
    }

    // 跳转到 500 页面，使用 replace 避免产生历史记录
    next({ name: "500", replace: true });
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
 * @returns true 表示已处理跳转，false 表示无需跳转
 */
function handleRootPathRedirect(to: RouteLocationNormalized, next: NavigationGuardNext): boolean {
  if (to.path !== "/") {
    return false;
  }

  const { homePath } = useCommon();
  if (homePath.value && homePath.value !== "/") {
    next({ path: homePath.value, replace: true });
    return true;
  }

  return false;
}

/**
 * 判断是否为未授权错误（401）
 */
function isUnauthorizedError(error: unknown): boolean {
  return isHttpError(error) && error.code === ApiStatus.unauthorized;
}
