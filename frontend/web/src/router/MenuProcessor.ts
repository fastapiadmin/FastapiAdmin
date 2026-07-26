import type { UserInfo } from "@/api/module_system/user";
import type { MenuTable } from "@/api/module_system/menu";
import type { AppRouteRecord, RouteMeta } from "@/types/router";
import type { AppRouteRecordRaw } from "@utils";
import { useUserStore } from "@stores";
import { useAppMode } from "@/hooks/core/useAppMode";

import {
  HOME_MENU_META,
  DASHBOARD_PARENT_META,
  dashboardLayoutChildren,
  ROUTE_COMPONENT_LAYOUT,
  ROUTE_COMPONENT_NESTED_PARENT,
} from "./routes";
import { MenuTypeEnum } from "@/enums/system/menu.enum";

/**
 * 菜单 → `AppRouteRecord`：后端 `MenuTable`、前端内置路由、混合模式合并；供守卫注册动态路由。
 * `getMenuList` 依 `useAppMode` 分支；meta 对齐后端 keep_alive、目录占位组件。
 */

/** 前端模式并入菜单的内置路由（扩展点，默认空） */
export const builtinFrontendRoutes: AppRouteRecord[] = [];

function joinAbsolutePath(parentAbs: string, segmentPath: string): string {
  const seg = segmentPath.replace(/^\/+/, "");
  const base = parentAbs.replace(/\/$/, "");
  if (!seg) return base;
  return `${base}/${seg}`;
}

function toComponentImportPath(componentPath: string): string {
  const t = componentPath.trim().replace(/^\/+/, "");
  return t ? `/${t}` : "";
}

function mapMenuNode(item: MenuTable, depth = 0, parentAbsolutePath = ""): AppRouteRecord {
  const raw = (item.route_path ?? "").trim();
  // 直接在此计算标准化路径，消除 normalizeMenuNestedPaths + normalizeAppRouteChildPaths 两次遍历
  const path = raw.startsWith("/")
    ? raw
    : parentAbsolutePath
      ? joinAbsolutePath(parentAbsolutePath, raw)
      : `/${raw}`;

  const childrenRaw = item.children?.filter((c) => c.type !== MenuTypeEnum.BUTTON) ?? [];
  const children = childrenRaw.length
    ? childrenRaw.map((c) => mapMenuNode(c, depth + 1, path))
    : undefined;

  const name = item.route_name || undefined;
  const redirect = item.redirect?.trim() || undefined;

  const hasKids = !!(children && children.length > 0);
  const isDirectory = item.type === MenuTypeEnum.CATALOG;

  let component: string | undefined;
  if (isDirectory || (hasKids && !(item.component_path ?? "").trim())) {
    component = depth === 0 ? ROUTE_COMPONENT_LAYOUT : ROUTE_COMPONENT_NESTED_PARENT;
  } else if ((item.component_path ?? "").trim()) {
    component = toComponentImportPath(item.component_path!);
  }

  const meta: RouteMeta = {
    title: item.title ?? "",
    icon: item.icon || undefined,
    hidden: !!item.hidden,
    keepAlive: item.keep_alive ?? true,
    affix: !!item.affix,
    fixedTab: !!item.affix,
    alwaysShow: !!item.always_show,
    isHide: !!item.hidden,
    isHideTab: !!item.is_hide_tab,
    link: item.link || undefined,
    isIframe: !!item.is_iframe,
    activePath: item.active_path || undefined,
    showBadge: !!item.show_badge,
    showTextBadge: item.show_text_badge || undefined,
    scope: item.scope,
  };

  return {
    path,
    name,
    component,
    redirect,
    meta,
    children,
  };
}

function backendMenusToAppRoutes(menus: MenuTable[]): AppRouteRecord[] {
  const roots = menus.filter((m) => m.type !== MenuTypeEnum.BUTTON);
  return roots.map((m) => mapMenuNode(m, 0, ""));
}

export class MenuProcessor {
  async getMenuList(): Promise<AppRouteRecord[]> {
    const { isFrontendMode, isMixedMenuMode } = useAppMode();

    let menuList: AppRouteRecord[];
    if (isMixedMenuMode.value) {
      menuList = await this.processMixedMenu();
    } else if (isFrontendMode.value) {
      menuList = await this.processFrontendMenu();
    } else {
      menuList = await this.processBackendMenu();
    }

    // 统一过滤空菜单，避免各分支重复调用
    menuList = this.filterEmptyMenus(menuList);

    return this.normalizeMenuPaths(menuList);
  }

  private async processFrontendMenu(): Promise<AppRouteRecord[]> {
    const userStore = useUserStore();
    let menuList = [...builtinFrontendRoutes];

    if (!userStore.info?.is_superuser) {
      const roles = userStore.info?.roles;

      if (roles && roles.length > 0) {
        const roleCodes = this.extractRoleCodesFromUserRoles(roles);
        if (roleCodes.length > 0) {
          menuList = this.filterMenuByRoles(menuList, roleCodes);
        }
      }
    }

    return menuList;
  }

  private extractRoleCodesFromUserRoles(roles: NonNullable<UserInfo["roles"]>): string[] {
    const codes = new Set<string>();
    for (const role of roles) {
      const r = role as { code?: string; name?: string };
      const c = r.code?.trim();
      if (c) codes.add(c);
      const n = r.name?.trim();
      if (n && /^R_[A-Z0-9_]+$/i.test(n)) codes.add(n);
    }
    return Array.from(codes);
  }

  private async processMixedMenu(): Promise<AppRouteRecord[]> {
    let backend: AppRouteRecord[] = [];
    try {
      backend = await this.processBackendMenu();
    } catch (e) {
      console.warn("[MenuProcessor] mixed：后端菜单获取失败，本次仅挂载前端路由", e);
    }
    const frontend = await this.processFrontendMenu();
    const merged = mergeAppRouteRecords(backend, frontend);
    return merged;
  }

  /** 优先用用户信息里附带的 `menus`，与守卫拉用户信息顺序一致，避免重复打菜单树接口 */
  private async processBackendMenu(): Promise<AppRouteRecord[]> {
    const userStore = useUserStore();
    const fromUser = userStore.routeList;
    if (Array.isArray(fromUser) && fromUser.length > 0) {
      return backendMenusToAppRoutes(fromUser);
    }
    return [];
  }

  private filterMenuByRoles(menu: AppRouteRecord[], roleCodes: string[]): AppRouteRecord[] {
    return menu.reduce((acc: AppRouteRecord[], item) => {
      const itemRoles = item.meta?.roles;
      const hasPermission = !itemRoles || itemRoles.some((role) => roleCodes?.includes(role));

      if (hasPermission) {
        const filteredItem = { ...item };
        if (filteredItem.children?.length) {
          filteredItem.children = this.filterMenuByRoles(filteredItem.children, roleCodes);
        }
        acc.push(filteredItem);
      }

      return acc;
    }, []);
  }

  private filterEmptyMenus(menuList: AppRouteRecord[]): AppRouteRecord[] {
    return menuList
      .map((item) => {
        if (!item.children?.length) return item;
        return { ...item, children: this.filterEmptyMenus(item.children) };
      })
      .filter((item) => this.isMenuNodeVisible(item));
  }

  /** 菜单节点在侧栏中是否可见（有子菜单 / iframe / 外链 / 有实际组件） */
  private isMenuNodeVisible(item: AppRouteRecord): boolean {
    if (item.children?.length) return true;
    if (item.meta?.isIframe || item.meta?.link) return true;
    return !!(item.component && item.component !== "" && item.component !== ROUTE_COMPONENT_LAYOUT);
  }

  validateMenuList(menuList: AppRouteRecord[]): boolean {
    return Array.isArray(menuList) && menuList.length > 0;
  }

  private normalizeMenuPaths(menuList: AppRouteRecord[], parentPath = ""): AppRouteRecord[] {
    return menuList.map((item) => {
      const fullPath = this.buildFullPath(item.path || "", parentPath);

      const children = item.children?.length
        ? this.normalizeMenuPaths(item.children, fullPath)
        : item.children;

      const redirect = item.redirect || this.resolveDefaultRedirect(children);

      return {
        ...item,
        path: fullPath,
        redirect,
        children,
      };
    });
  }

  private resolveDefaultRedirect(children?: AppRouteRecord[]): string | undefined {
    if (!children?.length) {
      return undefined;
    }

    for (const child of children) {
      if (this.isNavigableRoute(child)) {
        return child.path;
      }

      const nestedRedirect = this.resolveDefaultRedirect(child.children);
      if (nestedRedirect) {
        return nestedRedirect;
      }
    }

    return undefined;
  }

  private isNavigableRoute(route: AppRouteRecord): boolean {
    return Boolean(
      route.path &&
      route.path !== "/" &&
      !route.meta?.link &&
      route.meta?.isIframe !== true &&
      route.component &&
      route.component !== ""
    );
  }

  private buildFullPath(path: string, parentPath: string): string {
    if (!path) return "";

    if (path.startsWith("http://") || path.startsWith("https://")) {
      return path;
    }

    if (path.startsWith("/")) {
      return path;
    }

    if (parentPath) {
      const cleanParent = parentPath.replace(/\/$/, "");
      const cleanChild = path.replace(/^\//, "");
      return `${cleanParent}/${cleanChild}`;
    }

    return `/${path}`;
  }
}

// ──────── 壳层路由补全 ────────

/** 从后端菜单中去掉组件和 redirect，供侧栏合并 */
function stripRouteRecordForShell(route: AppRouteRecordRaw): AppRouteRecord {
  const children = route.children?.map(stripRouteRecordForShell);
  return {
    path: route.path,
    name: route.name,
    meta: (route.meta ?? {}) as AppRouteRecord["meta"],
    ...(children?.length ? { children } : {}),
  } as AppRouteRecord;
}

function getDashboardMenuTreeForMerge(): AppRouteRecord {
  return {
    name: "Dashboard",
    path: "/dashboard",
    meta: DASHBOARD_PARENT_META,
    children: dashboardLayoutChildren.map(stripRouteRecordForShell),
  };
}

function normalizeMenuPath(path?: string): string {
  if (!path || !path.trim()) return "";
  const p = path.trim();
  return p.startsWith("/") ? p : `/${p}`;
}

function collectPathsAndNames(items: AppRouteRecord[], paths: Set<string>, names: Set<string>) {
  for (const r of items) {
    const np = normalizeMenuPath(r.path as string);
    if (np) paths.add(np);
    if (r.name) names.add(String(r.name));
    if (r.children?.length) collectPathsAndNames(r.children, paths, names);
  }
}

function dashboardRoutesToShellMenu(route: AppRouteRecord, parentAbs = ""): AppRouteRecord {
  const raw = route.path?.trim() ?? "";
  const fullPath =
    raw.startsWith("/") && raw !== "/"
      ? raw
      : parentAbs
        ? `${parentAbs.replace(/\/$/, "")}/${raw.replace(/^\/+/, "")}`
        : `/${raw.replace(/^\/+/, "")}`;
  const meta = { ...route.meta, shellRoute: true as const };
  const children = route.children?.map((c) => dashboardRoutesToShellMenu(c, fullPath));
  return { ...route, path: fullPath, meta, children, component: undefined, redirect: undefined };
}

/** 将壳层路由（/home、/dashboard）合并到菜单列表 */
export function mergeShellRoutesIntoMenu(menuList: AppRouteRecord[]): AppRouteRecord[] {
  const paths = new Set<string>();
  const names = new Set<string>();
  collectPathsAndNames(menuList, paths, names);

  const additions: AppRouteRecord[] = [];

  const tryPush = (item: AppRouteRecord) => {
    const p = normalizeMenuPath(item.path as string);
    const n = item.name ? String(item.name) : "";
    if (p && !paths.has(p) && (!n || !names.has(n))) {
      additions.push(item);
      if (p) paths.add(p);
      if (n) names.add(n);
      if (item.children?.length) collectPathsAndNames(item.children, paths, names);
    }
  };

  const mergeShellHomeMenu: AppRouteRecord = {
    path: "/home",
    name: "Home",
    meta: { ...HOME_MENU_META, shellRoute: true },
  };

  tryPush(mergeShellHomeMenu);
  if (!paths.has("/dashboard")) {
    tryPush(dashboardRoutesToShellMenu(getDashboardMenuTreeForMerge()));
  }

  if (additions.length === 0) return menuList;
  return [...additions, ...menuList];
}

/** 按 name 去重合并两套菜单记录 */
export function mergeAppRouteRecords(
  primary: AppRouteRecord[],
  secondary: AppRouteRecord[]
): AppRouteRecord[] {
  const usedNames = new Set<string>();

  const collectNames = (routes: AppRouteRecord[]) => {
    for (const r of routes) {
      if (r.name) usedNames.add(String(r.name));
      if (r.children?.length) collectNames(r.children);
    }
  };
  collectNames(primary);

  const pickFresh = (routes: AppRouteRecord[]): AppRouteRecord[] => {
    const out: AppRouteRecord[] = [];
    for (const r of routes) {
      const n = r.name ? String(r.name) : "";
      if (n && usedNames.has(n)) continue;
      const next: AppRouteRecord = { ...r };
      if (r.children?.length) next.children = pickFresh(r.children);
      if (n) usedNames.add(n);
      out.push(next);
    }
    return out;
  };

  return [...primary, ...pickFresh(secondary)];
}
