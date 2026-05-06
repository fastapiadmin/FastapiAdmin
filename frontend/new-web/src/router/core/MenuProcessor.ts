/**
 * 菜单处理器
 *
 * 负责菜单数据的获取、过滤和处理
 *
 * @module router/core/MenuProcessor
 * @author FastapiAdmin Team
 */

import type { AppRouteRecord } from "@/types/router";
import type { UserInfo } from "@/api/module_system/user";
import { useUserStore } from "@/store/modules/user.store";
import { useAppMode } from "@/hooks/core/useAppMode";
import MenuAPI from "@/api/module_system/menu";
import { asyncRoutes } from "../routes/asyncRoutes";
import { ROUTE_COMPONENT_LAYOUT } from "../routes/staticRoutes";
import { backendMenusToAppRoutes } from "../utils/backendMenuTransform";
import { mergeAppRouteRecords } from "../utils/mergeAppRouteRecords";
import { formatMenuTitle } from "@/utils";

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

    // 在规范化路径之前，验证原始路径配置
    this.validateMenuPaths(menuList);

    // 规范化路径（将相对路径转换为完整路径）
    return this.normalizeMenuPaths(menuList);
  }

  /**
   * 处理前端控制模式的菜单
   */
  private async processFrontendMenu(): Promise<AppRouteRecord[]> {
    const userStore = useUserStore();
    let menuList = [...asyncRoutes];

    // 超管不做前端 meta.roles 过滤，避免与接口未返回 code 或编码不一致时整棵模板路由被误删
    if (userStore.info?.is_superuser) {
      return this.filterEmptyMenus(menuList);
    }

    const roles = userStore.info?.roles;

    // 根据角色过滤菜单（仅当能解析出角色标识时才过滤；否则勿用空数组误杀全部 meta.roles）
    if (roles && roles.length > 0) {
      const roleCodes = this.extractRoleCodesFromUserRoles(roles);
      if (roleCodes.length > 0) {
        menuList = this.filterMenuByRoles(menuList, roleCodes);
      }
    }

    return this.filterEmptyMenus(menuList);
  }

  /**
   * 从用户信息中的角色解析与路由 meta.roles 对齐的标识（code，以及形如 R_XXX 的 name）
   */
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

  /**
   * 混合模式：后端菜单 + 前端 asyncRoutes（按路由 name 去重，后端优先）
   */
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

  /**
   * 处理后端控制模式的菜单
   */
  private async processBackendMenu(): Promise<AppRouteRecord[]> {
    const response = await MenuAPI.listMenu({ menu_client: "pc" });
    const list = response.data.data || [];
    const routes = backendMenusToAppRoutes(list);
    return this.filterEmptyMenus(routes);
  }

  /**
   * 根据角色过滤菜单
   */
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

  /**
   * 递归过滤空菜单项
   */
  private filterEmptyMenus(menuList: AppRouteRecord[]): AppRouteRecord[] {
    return menuList
      .map((item) => {
        // 如果有子菜单，先递归过滤子菜单
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
        // 如果定义了 children 属性（即使是空数组），说明这是一个目录菜单，应该保留
        if ("children" in item) {
          return true;
        }

        // 如果有外链或 iframe，保留
        if (item.meta?.isIframe === true || item.meta?.link) {
          return true;
        }

        // 如果有有效的 component，保留
        if (item.component && item.component !== "" && item.component !== ROUTE_COMPONENT_LAYOUT) {
          return true;
        }

        // 其他情况过滤掉
        return false;
      });
  }

  /**
   * 验证菜单列表是否有效
   */
  validateMenuList(menuList: AppRouteRecord[]): boolean {
    return Array.isArray(menuList) && menuList.length > 0;
  }

  /**
   * 规范化菜单路径
   * 将相对路径转换为完整路径，确保菜单跳转正确
   */
  private normalizeMenuPaths(menuList: AppRouteRecord[], parentPath = ""): AppRouteRecord[] {
    return menuList.map((item) => {
      // 构建完整路径
      const fullPath = this.buildFullPath(item.path || "", parentPath);

      // 递归处理子菜单
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

  /**
   * 为目录型菜单推导默认跳转地址
   */
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

  /**
   * 判断子路由是否可以作为默认落点
   */
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

  /**
   * 验证菜单路径配置
   * 检测非一级菜单是否错误使用了 / 开头的路径
   */
  /**
   * 验证菜单路径配置
   * 检测非一级菜单是否错误使用了 / 开头的路径
   */
  private validateMenuPaths(menuList: AppRouteRecord[], level = 1): void {
    menuList.forEach((route) => {
      if (!route.children?.length) return;

      const parentName = String(route.name || route.path || "未知路由");

      route.children.forEach((child) => {
        const childPath = child.path || "";

        // 跳过合法的绝对路径：外部链接和 iframe 路由
        if (this.isValidAbsolutePath(childPath)) return;

        // 检测非法的绝对路径
        if (childPath.startsWith("/")) {
          this.logPathError(child, childPath, parentName, level);
        }
      });

      // 递归检查更深层级的子路由
      this.validateMenuPaths(route.children, level + 1);
    });
  }

  /**
   * 判断是否为合法的绝对路径
   */
  private isValidAbsolutePath(path: string): boolean {
    return (
      path.startsWith("http://") ||
      path.startsWith("https://") ||
      path.startsWith("/outside/iframe/")
    );
  }

  /**
   * 输出路径配置错误日志
   */
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

  /**
   * 构建完整路径
   */
  private buildFullPath(path: string, parentPath: string): string {
    if (!path) return "";

    // 外部链接直接返回
    if (path.startsWith("http://") || path.startsWith("https://")) {
      return path;
    }

    // 如果已经是绝对路径，直接返回
    if (path.startsWith("/")) {
      return path;
    }

    // 拼接父路径和当前路径
    if (parentPath) {
      // 移除父路径末尾的斜杠，移除子路径开头的斜杠，然后拼接
      const cleanParent = parentPath.replace(/\/$/, "");
      const cleanChild = path.replace(/^\//, "");
      return `${cleanParent}/${cleanChild}`;
    }

    // 没有父路径，添加前导斜杠
    return `/${path}`;
  }
}
