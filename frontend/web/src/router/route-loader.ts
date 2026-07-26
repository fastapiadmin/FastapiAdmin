/**
 * 动态路由加载管道
 *
 * 封装了从后端菜单配置到 Vue Router `addRoute` 的完整管道：
 *   ComponentLoader  (路径→组件)
 *   RouteTransformer (菜单→路由记录)
 *   RouteRegistry    (批量注册/注销)
 *
 * @module router/route-loader
 */
import type { Router } from "vue-router";
import type { AppRouteRecord } from "@/types/router";
import { h } from "vue";
import {
  IframeRouteManager,
  IframeView,
  NestedRouterParent,
  ROOT_LAYOUT_ROUTE_NAME,
  ROUTE_COMPONENT_LAYOUT,
  ROUTE_COMPONENT_NESTED_PARENT,
} from "./routes";

// ──────── ComponentLoader ────────

/** 页面组件映射表（eager 加载：src/views 及 layouts 下所有 .vue 文件） */
const pageComponents = import.meta.glob("/src/{views,layouts}/**/*.vue", { eager: true });

/**
 * 组件加载器
 *
 * 职责：把后端菜单里 `component` 字段的字符串路径 → Vue 组件。
 *
 * 后端存的是相对路径如 "system/user/index"，Loader 去 glob 表里匹配对应的 .vue 文件。
 */
export class ComponentLoader {
  /** 查找路径对应的 Vue 组件（后端路径 → glob 模块表） */
  load(path: string): any {
    if (!path) return { render: () => null };

    // 标准化路径：移除开头的 /
    const normalizedPath = path.startsWith("/") ? path.slice(1) : path;

    const lookupPaths = [`/src/views/${normalizedPath}`, `/src/views/${normalizedPath}.vue`];
    for (const p of lookupPaths) {
      const mod = pageComponents[p];
      if (mod) return (mod as any).default || mod;
    }
    // 兼容末尾多余的 /index
    const fallbackPath = normalizedPath.endsWith("/index")
      ? normalizedPath.slice(0, -6)
      : `${normalizedPath}/index`;
    const mod = pageComponents[`/src/views/${fallbackPath}.vue`];
    return mod ? (mod as any).default || mod : this.createErrorComponent(path);
  }

  /** Layout 框架组件 */
  loadLayout(): any {
    return (pageComponents["/src/layouts/index.vue"] as any)?.default;
  }

  /** IframeView 组件 */
  loadIframe(): any {
    return IframeView;
  }

  /** NestedRouterParent 占位组件 */
  loadNestedParent(): any {
    return NestedRouterParent;
  }

  /** 空组件（空白 div） */
  createEmptyComponent(): any {
    return { render: () => null };
  }

  /** 错误提示组件（后端配置了不存在的路径时显示） */
  private createErrorComponent(path: string): any {
    return {
      render() {
        return h(
          "div",
          { style: "padding: 40px; text-align: center; color: #999;" },
          `[路由警告] 找不到组件: /src/views/${path}.vue`
        );
      },
    };
  }
}

// ──────── Validation ────────

/**
 * 开发期菜单配置校验（仅开发环境，生产期直接跳过）
 *
 * 后端下发的菜单通常是完整的，这里只做开发期配置检查：
 * - name 重复 → warn
 * - 叶子节点没有 component → warn
 * - 子菜单错误使用 ROUTE_COMPONENT_LAYOUT → error
 */
function warnInvalidRouteConfig(routes: AppRouteRecord[], parentPath = ""): void {
  if (import.meta.env.PROD) return;
  const nameSet = new Set<string>();
  const check = (items: AppRouteRecord[], pPath = "") => {
    items.forEach((route) => {
      const fullPath = route.path ?? "";
      // 检查 name 重复
      if (route.name) {
        const n = String(route.name);
        if (nameSet.has(n)) console.warn(`[路由配置] name 重复: "${n}" (${fullPath})`);
        nameSet.add(n);
      }
      // 检查叶子节点缺少 component
      if (
        !route.component &&
        !route.meta?.link &&
        !route.meta?.isIframe &&
        !route.children?.length
      ) {
        console.warn(`[路由配置] 缺少 component: "${route.path}"`);
      }
      // 检查子菜单错误使用了 Layout
      if (pPath !== "" && route.component === ROUTE_COMPONENT_LAYOUT) {
        console.error(
          `[路由配置] 菜单 "${route.meta?.title || route.path}" 为 ${pPath} 子菜单，不能使用 ${ROUTE_COMPONENT_LAYOUT}`
        );
      }
      if (route.children?.length) check(route.children, fullPath);
    });
  };
  check(routes, parentPath);
}

// ──────── RouteTransformer ────────

/**
 * 菜单 → 路由记录转换器
 *
 * 职责：把后端下发的菜单（AppRouteRecord）→ Vue Router 认识的 RouteRecordRaw。
 * 需要处理的情况：
 *
 * 1. 一级叶子菜单（如 /user）→ 包一层 Layout，其下挂实际组件
 * 2. iframe 菜单    → 一级包 Layout，子级直接 IframeView
 * 3. 多级目录       → 父级用 NestedRouterParent 占位，子级挂实际组件
 * 4. 常规子菜单     → 直接绑定组件
 */
export class RouteTransformer {
  private loader: ComponentLoader;

  /**
   * @param loader 组件加载器
   * @param options.shellChild 是否生成壳层子路由格式（path 用 routerPath 处理）
   */
  constructor(
    loaderArg?: ComponentLoader,
    private options: { shellChild?: boolean } = {}
  ) {
    this.loader = loaderArg ?? new ComponentLoader();
  }

  /** 递归转换：一个菜单节点 → RouteRecordRaw */
  transform(route: AppRouteRecord, depth: number): Record<string, any> | null {
    const { path } = route;
    if (!path && !route.children?.length) return null;

    const isIframe = route.meta?.isIframe;

    // iframe：一级包 Layout，子级直接 IframeView
    if (isIframe) return this.handleIframeRoute(route, depth);
    // 一级叶子（path="/user"，无 children）：包 Layout
    if (this.isFirstLevelLeaf(route, depth)) return this.handleFirstLevelLeaf(route);
    // 常规路由
    return this.handleNormalRoute(route, depth);
  }

  /** 取 path 第一段，用于一级菜单去重 */
  pathFirstSegment(path: string): string {
    return path.replace(/^\//, "").split("/")[0] || path.replace(/^\//, "");
  }

  /** 标准化 path：一级加 /，壳层子路由维持相对路径 */
  private routerPath(path: string, depth: number): string {
    if (depth === 0 && !path.startsWith("/")) return `/${path}`;
    if (this.options.shellChild && depth >= 1) return path;
    return path;
  }

  /** 判断是否一级叶子菜单（depth=0，无 children，不是 iframe/外链） */
  private isFirstLevelLeaf(route: AppRouteRecord, depth: number): boolean {
    if (depth !== 0) return false;
    if (route.meta?.link || route.meta?.isIframe) return false;
    if (route.children?.length) return false;
    return true;
  }

  /** iframe 路由：一级 → 包 Layout + redirect 到 iframe 子路由；子级 → 直接 IframeView */
  private handleIframeRoute(route: AppRouteRecord, depth: number): Record<string, any> | null {
    if (depth === 0) {
      const firstSegment = this.pathFirstSegment(route.path);
      return {
        path: `/${firstSegment}`,
        name: route.name || firstSegment,
        component: this.loader.loadLayout(),
        meta: { title: route.meta?.title, icon: route.meta?.icon },
        redirect: route.path.startsWith("/") ? route.path : `/${route.path}`,
        children: [
          {
            path: route.path.replace(/^\//, ""),
            name: route.name,
            component: this.loader.loadIframe(),
            meta: route.meta,
          },
        ],
      };
    }
    return {
      path: route.path.replace(/^\//, ""),
      name: route.name,
      component: this.loader.loadIframe(),
      meta: route.meta,
    };
  }

  /** 一级叶子 → 包 Layout，其下挂实际组件 */
  private handleFirstLevelLeaf(route: AppRouteRecord): Record<string, any> {
    const firstSegment = this.pathFirstSegment(route.path);
    const fullMenuPath = route.path.startsWith("/") ? route.path : `/${route.path}`;
    return {
      path: `/${firstSegment}`,
      name: route.name || firstSegment,
      component: this.loader.loadLayout(),
      meta: { title: route.meta?.title, icon: route.meta?.icon },
      redirect: fullMenuPath,
      children: [
        {
          path: fullMenuPath.replace(/^\//, ""),
          name: `${String(route.name) || firstSegment}Child`,
          component: this.loader.load(route.component ? String(route.component) : ""),
          meta: route.meta,
        },
      ],
    };
  }

  /**
   * 常规路由处理
   *
   * - 无 children 或 children 都是叶子 → 直接绑定组件
   * - 有 children（多级目录）→ 父级用 NestedRouterParent 占位，递归处理子级
   */
  private handleNormalRoute(route: AppRouteRecord, depth: number): Record<string, any> | null {
    if (!route.children?.length) {
      return this.buildLeafRoute(route, depth);
    }

    const allLeaves = route.children.every((c) => !c.children?.length);
    if (allLeaves && !route.component) {
      return this.buildLeafRoute(route, depth);
    }

    // 多级目录：父级占位 + 递归子级
    const children = route.children
      .map((child) => this.transform(child, depth + 1))
      .filter(Boolean);

    return {
      path: this.routerPath(route.path, depth),
      name: route.name,
      redirect: children.length > 0 ? { name: children[0]?.name } : undefined,
      component:
        route.component &&
        ![ROUTE_COMPONENT_NESTED_PARENT, ROUTE_COMPONENT_LAYOUT].includes(String(route.component))
          ? this.loader.load(String(route.component))
          : NestedRouterParent,
      meta: route.meta,
      children,
    };
  }

  /** 叶子路由（直接绑定组件） */
  private buildLeafRoute(route: AppRouteRecord, depth: number): Record<string, any> | null {
    if (
      (!route.component ||
        route.component === ROUTE_COMPONENT_NESTED_PARENT ||
        route.component === ROUTE_COMPONENT_LAYOUT) &&
      route.meta?.link
    ) {
      return null;
    }
    return {
      path: this.routerPath(route.path, depth),
      name: route.name,
      component:
        route.component &&
        ![ROUTE_COMPONENT_NESTED_PARENT, ROUTE_COMPONENT_LAYOUT].includes(String(route.component))
          ? this.loader.load(String(route.component))
          : undefined,
      meta: route.meta,
    };
  }
}

// ──────── RouteRegistry ────────

/**
 * 批量路由注册器
 *
 * 职责：把 RouteTransformer 转换后的路由记录批量 `addRoute` 到 Router。
 * 支持卸载（unregister）和防重复注册。
 */
export class RouteRegistry {
  private router: Router;
  private componentLoader: ComponentLoader;
  private transformer: RouteTransformer;
  private removeRouteFns: (() => void)[] = [];
  private registered = false;

  constructor(router: Router) {
    this.router = router;
    this.componentLoader = new ComponentLoader();
    this.transformer = new RouteTransformer(this.componentLoader, { shellChild: true });
  }

  /** 批量注册动态路由 */
  register(menuList: AppRouteRecord[]): void {
    if (this.registered) {
      console.warn("[RouteRegistry] 路由已注册，跳过重复注册");
      return;
    }

    warnInvalidRouteConfig(menuList);

    this.registered = true;
    menuList.forEach((menu, index) => {
      const firstSegment = this.transformer.pathFirstSegment(menu.path);
      // 壳层路径不覆盖
      if (this.isShellSegment(firstSegment)) return;
      // 去重：已注册过该 path 第一段则跳过
      if (this.router.hasRoute(registrationName(menu, index).trim())) return;

      if (menu.meta?.isIframe) {
        IframeRouteManager.getInstance().add(menu);
      }

      const routeRecord = this.transformer.transform(menu, 0);
      if (routeRecord) {
        this.router.addRoute(ROOT_LAYOUT_ROUTE_NAME, routeRecord as any);
        // 收集清理函数
        this.removeRouteFns.push(() => {
          const name = routeRecord.name as string;
          if (name && this.router.hasRoute(name)) {
            this.router.removeRoute(name);
          }
        });
      }
    });
  }

  /** 卸载所有动态注册的路由 */
  unregister(): void {
    this.removeRouteFns.forEach((fn) => fn());
    this.removeRouteFns = [];
    this.registered = false;
    IframeRouteManager.getInstance().clear();
  }

  /** 是否已注册 */
  isRegistered(): boolean {
    return this.registered;
  }

  /** 获取清理函数列表（供 menuStore 保存） */
  getRemoveRouteFns(): (() => void)[] {
    return this.removeRouteFns;
  }

  /** 强制标记为已注册（动态路由恢复场景用） */
  markAsRegistered(): void {
    this.registered = true;
  }

  /** 判断 path 第一段是否是壳层路径 */
  private isShellSegment(segment: string): boolean {
    return ["home", "profile", "changelog", "dashboard"].includes(segment);
  }
}

/** 动态路由注册去重的 name */
function registrationName(route: AppRouteRecord, index: number): string {
  const prefix = route.name ? String(route.name) : `Dyn_${index}`;
  return `Dyn_${index}_${prefix}`;
}
