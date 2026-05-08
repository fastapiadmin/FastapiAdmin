/**
 * 菜单处理器（含后端菜单 → AppRouteRecord 转换）
 *
 * @module router/MenuProcessor
 */
import type { AppRouteRecord, RouteMeta } from "@/types/router";
import type { UserInfo } from "@/api/module_system/user";
import type { MenuTable } from "@/api/module_system/menu";
import { useUserStore } from "@stores/modules/user.store";
import { useAppMode } from "@/hooks/core/useAppMode";
import MenuAPI from "@/api/module_system/menu";
import {
  mergeAppRouteRecords,
  ROUTE_COMPONENT_LAYOUT,
  ROUTE_COMPONENT_NESTED_PARENT,
} from "./staticRoutes";
import { formatMenuTitle } from "@utils";
import { MenuTypeEnum } from "@/enums/system/menu.enum";

/** 前端模式并入菜单的内置路由（扩展点，默认空） */
export const builtinFrontendRoutes: AppRouteRecord[] = [];

function normalizeMenuNestedPaths(items: MenuTable[], parentAbsolutePath?: string): MenuTable[] {
  return items.map((node) => {
    const raw = (node.route_path ?? "").trim();
    let routePath: string | null | undefined = node.route_path;
    if (parentAbsolutePath && raw && raw === parentAbsolutePath) {
      routePath = "";
    }
    const canonical = raw.startsWith("/") ? raw : parentAbsolutePath;
    const children = node.children?.length
      ? normalizeMenuNestedPaths(node.children, canonical)
      : undefined;
    return { ...node, route_path: routePath, children };
  });
}

function joinAbsolutePath(parentAbs: string, segmentPath: string): string {
  const seg = segmentPath.replace(/^\/+/, "");
  const base = parentAbs.replace(/\/$/, "");
  if (!seg) return base;
  return `${base}/${seg}`;
}

function normalizeAppRouteChildPaths(
  routes: AppRouteRecord[],
  parentAbsolutePath = ""
): AppRouteRecord[] {
  return routes.map((route) => {
    let path = (route.path ?? "").trim();

    if (/^https?:\/\//i.test(path)) {
      return {
        ...route,
        children: route.children?.length
          ? normalizeAppRouteChildPaths(route.children, parentAbsolutePath)
          : route.children,
      };
    }

    if (parentAbsolutePath && path.startsWith("/")) {
      const p = parentAbsolutePath.replace(/\/$/, "");
      if (path.startsWith(`${p}/`)) {
        path = path.slice(p.length + 1);
      } else if (path === p) {
        path = "";
      }
    }

    if (
      parentAbsolutePath &&
      path.startsWith("/") &&
      !/^https?:\/\//i.test(path) &&
      !path.startsWith("/outside/iframe/")
    ) {
      const segments = path.split("/").filter(Boolean);
      if (segments.length) path = segments[segments.length - 1]!;
    }

    const currentAbs = !parentAbsolutePath
      ? path.startsWith("/")
        ? path
        : path
          ? `/${path.replace(/^\/+/, "")}`
          : ""
      : joinAbsolutePath(parentAbsolutePath, path);

    const children = route.children?.length
      ? normalizeAppRouteChildPaths(route.children, currentAbs)
      : route.children;

    return { ...route, path, children };
  });
}

function toComponentImportPath(componentPath: string): string {
  const t = componentPath.trim().replace(/^\/+/, "");
  return t ? `/${t}` : "";
}

function mapMenuNode(item: MenuTable, depth = 0): AppRouteRecord {
  const childrenRaw = item.children?.filter((c) => c.type !== MenuTypeEnum.BUTTON) ?? [];
  const children = childrenRaw.length
    ? childrenRaw.map((c) => mapMenuNode(c, depth + 1))
    : undefined;

  const path = (item.route_path ?? "").trim();
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
    client: item.client,
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
  const normalized = normalizeMenuNestedPaths(roots);
  const mapped = normalized.map((m) => mapMenuNode(m, 0));
  return normalizeAppRouteChildPaths(mapped);
}

export class MenuProcessor {
  /**
   * 获取菜单数据
   */
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

    this.validateMenuPaths(menuList);

    return this.normalizeMenuPaths(menuList);
  }

  private async processFrontendMenu(): Promise<AppRouteRecord[]> {
    const userStore = useUserStore();
    let menuList = [...builtinFrontendRoutes];

    if (userStore.info?.is_superuser) {
      return this.filterEmptyMenus(menuList);
    }

    const roles = userStore.info?.roles;

    if (roles && roles.length > 0) {
      const roleCodes = this.extractRoleCodesFromUserRoles(roles);
      if (roleCodes.length > 0) {
        menuList = this.filterMenuByRoles(menuList, roleCodes);
      }
    }

    return this.filterEmptyMenus(menuList);
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
    return this.filterEmptyMenus(merged);
  }

  private async processBackendMenu(): Promise<AppRouteRecord[]> {
    const response = await MenuAPI.listMenu({ menu_client: "pc" });
    const list = response.data.data || [];
    const routes = backendMenusToAppRoutes(list);
    return this.filterEmptyMenus(routes);
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
        if (item.children && item.children.length > 0) {
          const filteredChildren = this.filterEmptyMenus(item.children);
          return {
            ...item,
            children: filteredChildren,
          };
        }
        return item;
      })
      .filter((item) => {
        if ("children" in item) {
          return true;
        }

        if (item.meta?.isIframe === true || item.meta?.link) {
          return true;
        }

        if (item.component && item.component !== "" && item.component !== ROUTE_COMPONENT_LAYOUT) {
          return true;
        }

        return false;
      });
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

  private validateMenuPaths(menuList: AppRouteRecord[], level = 1): void {
    menuList.forEach((route) => {
      if (!route.children?.length) return;

      const parentName = String(route.name || route.path || "未知路由");

      route.children.forEach((child) => {
        const childPath = child.path || "";

        if (this.isValidAbsolutePath(childPath)) return;

        if (childPath.startsWith("/")) {
          this.logPathError(child, childPath, parentName, level);
        }
      });

      this.validateMenuPaths(route.children, level + 1);
    });
  }

  private isValidAbsolutePath(path: string): boolean {
    return (
      path.startsWith("http://") ||
      path.startsWith("https://") ||
      path.startsWith("/outside/iframe/")
    );
  }

  private logPathError(
    route: AppRouteRecord,
    path: string,
    parentName: string,
    level: number
  ): void {
    const routeName = String(route.name || path || "未知路由");
    const menuTitle = route.meta?.title || routeName;
    const suggestedPath = path.split("/").pop() || path.slice(1);

    console.error(
      `[路由配置错误] 菜单 "${formatMenuTitle(menuTitle)}" (name: ${routeName}, path: ${path}) 配置错误\n` +
        `  位置: ${parentName} > ${routeName}\n` +
        `  问题: ${level + 1}级菜单的 path 不能以 / 开头\n` +
        `  当前配置: path: '${path}'\n` +
        `  应该改为: path: '${suggestedPath}'`
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
