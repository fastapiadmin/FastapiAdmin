/**
 * 动态路由一站式：菜单 → 组件解析 → 挂到 RootLayout 下注册。
 *（老 web 里分散在 permission / transform 的职责，这里收进一个文件，少跳类、少找文件。）
 */
import { defineComponent, h, onMounted, ref } from "vue";
import type { RouteRecordRaw, Router } from "vue-router";
import { useRoute } from "vue-router";
import type { AppRouteRecord } from "@/types/router";
import {
  IframeRouteManager,
  NestedRouterParent,
  ROOT_LAYOUT_ROUTE_NAME,
  ROUTE_COMPONENT_LAYOUT,
  ROUTE_COMPONENT_NESTED_PARENT,
} from "./staticRoutes";

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export class RouteValidator {
  private warnedRoutes = new Set<string>();

  validate(routes: AppRouteRecord[]): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];
    this.checkDuplicates(routes, errors, warnings);
    this.checkComponents(routes, errors, warnings);
    this.checkNestedIndexComponent(routes);
    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  private checkDuplicates(
    routes: AppRouteRecord[],
    errors: string[],
    warnings: string[],
    parentPath = ""
  ): void {
    const routeNameMap = new Map<string, string>();
    const componentPathMap = new Map<string, string>();

    const checkRoutes = (items: AppRouteRecord[], pPath = "") => {
      items.forEach((route) => {
        const currentPath = route.path || "";
        const fullPath = this.resolvePath(pPath, currentPath);

        if (route.name) {
          const routeName = String(route.name);
          if (routeNameMap.has(routeName)) {
            warnings.push(`路由名称重复: "${routeName}" (${fullPath})`);
          } else {
            routeNameMap.set(routeName, fullPath);
          }
        }

        if (route.component && typeof route.component === "string") {
          const componentPath = route.component;
          if (componentPath !== ROUTE_COMPONENT_LAYOUT) {
            const componentKey = `${pPath}:${componentPath}`;
            if (componentPathMap.has(componentKey)) {
              warnings.push(`组件路径重复: "${componentPath}" (${fullPath})`);
            } else {
              componentPathMap.set(componentKey, fullPath);
            }
          }
        }

        if (route.children?.length) {
          checkRoutes(route.children, fullPath);
        }
      });
    };

    checkRoutes(routes, parentPath);
  }

  private checkComponents(
    routes: AppRouteRecord[],
    errors: string[],
    warnings: string[],
    parentPath = ""
  ): void {
    routes.forEach((route) => {
      const hasExternalLink = !!route.meta?.link?.trim();
      const hasChildren = Array.isArray(route.children) && route.children.length > 0;
      const routePath = route.path || "[未定义路径]";
      const isIframe = route.meta?.isIframe;

      if (route.component) {
        if (route.children?.length) {
          const fullPath = this.resolvePath(parentPath, route.path || "");
          this.checkComponents(route.children, errors, warnings, fullPath);
        }
        return;
      }

      if (parentPath === "" && !hasExternalLink && !isIframe) {
        errors.push(`一级菜单(${routePath}) 缺少 component，必须指向 ${ROUTE_COMPONENT_LAYOUT}`);
        return;
      }

      if (!hasExternalLink && !isIframe && !hasChildren) {
        errors.push(`路由(${routePath}) 缺少 component 配置`);
      }

      if (route.children?.length) {
        const fullPath = this.resolvePath(parentPath, route.path || "");
        this.checkComponents(route.children, errors, warnings, fullPath);
      }
    });
  }

  private checkNestedIndexComponent(routes: AppRouteRecord[], level = 1): void {
    routes.forEach((route) => {
      if (level > 1 && route.component === ROUTE_COMPONENT_LAYOUT) {
        this.logLayoutError(route, level);
      }
      if (route.children?.length) {
        this.checkNestedIndexComponent(route.children, level + 1);
      }
    });
  }

  private logLayoutError(route: AppRouteRecord, level: number): void {
    const routeName = String(route.name || route.path || "未知路由");
    const routeKey = `${routeName}_${route.path}`;
    if (this.warnedRoutes.has(routeKey)) return;
    this.warnedRoutes.add(routeKey);

    const menuTitle = route.meta?.title || routeName;
    const routePath = route.path || "/";

    console.error(
      `[路由配置错误] 菜单 "${menuTitle}" (name: ${routeName}, path: ${routePath}) 配置错误\n` +
        `  问题: ${level}级菜单不能使用 ${ROUTE_COMPONENT_LAYOUT} 作为 component\n` +
        `  说明: 只有一级菜单才能使用 ${ROUTE_COMPONENT_LAYOUT}，二级及以下菜单应该指向具体的组件路径\n` +
        `  当前配置: component: '${ROUTE_COMPONENT_LAYOUT}'\n` +
        `  应该改为: component: '/your/component/path' 或留空 ''（如果是目录菜单）`
    );
  }

  private resolvePath(parent: string, child: string): string {
    return [parent.replace(/\/$/, ""), child.replace(/^\//, "")].filter(Boolean).join("/");
  }
}

// ----------------------------------------------------------------------------- ComponentLoader
export class ComponentLoader {
  private modules: Record<string, () => Promise<any>>;

  constructor() {
    this.modules = import.meta.glob("../views/**/*.vue");
  }

  load(componentPath: string): () => Promise<any> {
    if (!componentPath) {
      return this.createEmptyComponent();
    }
    if (componentPath === ROUTE_COMPONENT_LAYOUT || componentPath === "/layouts/index") {
      return this.loadLayout();
    }
    if (componentPath === ROUTE_COMPONENT_NESTED_PARENT) {
      return this.loadNestedParent();
    }

    const normalized = componentPath.startsWith("/")
      ? componentPath
      : `/${componentPath.replace(/^\/+/, "")}`;
    const fullPath = `../views${normalized}.vue`;
    const fullPathWithIndex = `../views${normalized}/index.vue`;
    const module = this.modules[fullPath] || this.modules[fullPathWithIndex];

    if (!module) {
      console.error(
        `[ComponentLoader] 未找到组件: ${componentPath}，尝试过的路径: ${fullPath} 和 ${fullPathWithIndex}`
      );
      return this.createErrorComponent(componentPath);
    }
    return module;
  }

  loadLayout(): () => Promise<any> {
    return () => import("@/layouts/index.vue");
  }

  loadIframe(): () => Promise<any> {
    return () =>
      Promise.resolve(
        defineComponent({
          name: "IframeView",
          setup() {
            const route = useRoute();
            const isLoading = ref(true);
            const iframeUrl = ref("");
            const iframeRef = ref<HTMLIFrameElement | null>(null);

            onMounted(() => {
              const iframeRoute = IframeRouteManager.getInstance().findByPath(route.path);
              if (iframeRoute?.meta) {
                iframeUrl.value = (iframeRoute.meta as any).link || "";
              }
            });

            const handleIframeLoad = () => {
              isLoading.value = false;
            };

            return () =>
              h("div", { class: "box-border w-full h-full", "v-loading": isLoading.value }, [
                h("iframe", {
                  ref: iframeRef,
                  src: iframeUrl.value,
                  frameborder: "0",
                  class: "w-full h-full min-h-[calc(100vh-120px)] border-none",
                  onLoad: handleIframeLoad,
                }),
              ]);
          },
        })
      );
  }

  loadNestedParent(): () => Promise<any> {
    return () => Promise.resolve(NestedRouterParent);
  }

  private createEmptyComponent(): () => Promise<any> {
    return () =>
      Promise.resolve({
        render() {
          return h("div", {});
        },
      });
  }

  private createErrorComponent(componentPath: string): () => Promise<any> {
    return () =>
      Promise.resolve({
        render() {
          return h("div", { class: "route-error" }, `组件未找到: ${componentPath}`);
        },
      });
  }
}

// ----------------------------------------------------------------------------- RouteTransformer
interface ConvertedRoute extends Omit<RouteRecordRaw, "children"> {
  id?: number;
  children?: ConvertedRoute[];
  component?: RouteRecordRaw["component"] | (() => Promise<any>);
}

export class RouteTransformer {
  private componentLoader: ComponentLoader;
  private iframeManager: IframeRouteManager;
  private readonly shellChild: boolean;

  constructor(componentLoader: ComponentLoader, options?: { shellChild?: boolean }) {
    this.componentLoader = componentLoader;
    this.shellChild = options?.shellChild ?? false;
    this.iframeManager = IframeRouteManager.getInstance();
  }

  transform(route: AppRouteRecord, depth = 0, parentAbsPath = ""): ConvertedRoute {
    const absPath = (route.path || "").trim();
    const pathOut = this.routerPath(depth, parentAbsPath, absPath);
    const { component, children, ...routeConfig } = route;

    const converted: ConvertedRoute = { ...routeConfig, path: pathOut, component: undefined };

    if (route.meta.isIframe) {
      this.handleIframeRoute(converted, route, depth);
    } else if (this.isFirstLevelLeaf(route, depth)) {
      this.handleFirstLevelLeaf(converted, route, component as string);
    } else {
      this.handleNormalRoute(converted, component as string, depth);
    }

    converted.path = pathOut;

    if (children?.length) {
      converted.children = children.map((c) => this.transform(c, depth + 1, absPath));
    }

    return converted;
  }

  private routerPath(depth: number, parentAbsPath: string, absPath: string): string {
    const firstSeg = absPath.split("/").filter(Boolean)[0] ?? "";
    if (!this.shellChild) {
      if (depth === 0) {
        return firstSeg ? `/${firstSeg}` : "/";
      }
      return absPath;
    }
    if (depth === 0) {
      return firstSeg;
    }
    if (!parentAbsPath || !absPath) return absPath;
    const p = parentAbsPath.replace(/\/$/, "");
    if (absPath.startsWith(`${p}/`)) return absPath.slice(p.length + 1);
    return absPath.split("/").filter(Boolean).pop() ?? absPath;
  }

  private isFirstLevelLeaf(route: AppRouteRecord, depth: number): boolean {
    return depth === 0 && (!route.children || route.children.length === 0);
  }

  private handleIframeRoute(
    targetRoute: ConvertedRoute,
    sourceRoute: AppRouteRecord,
    depth: number
  ): void {
    if (depth === 0) {
      targetRoute.component = this.shellChild
        ? this.componentLoader.loadNestedParent()
        : this.componentLoader.loadLayout();
      targetRoute.name = "";
      const leafPath = this.shellChild ? "" : sourceRoute.path || "";
      targetRoute.children = [
        {
          ...sourceRoute,
          path: leafPath,
          component: this.componentLoader.loadIframe(),
        } as ConvertedRoute,
      ];
    } else {
      targetRoute.component = this.componentLoader.loadIframe();
    }
    this.iframeManager.add(sourceRoute);
  }

  private handleFirstLevelLeaf(
    converted: ConvertedRoute,
    route: AppRouteRecord,
    component: string | undefined
  ): void {
    converted.component = this.shellChild
      ? this.componentLoader.loadNestedParent()
      : this.componentLoader.loadLayout();
    converted.name = "";
    route.meta.isFirstLevel = true;
    const leafPath = this.shellChild ? "" : route.path || "";
    converted.children = [
      {
        ...route,
        path: leafPath,
        component: component ? this.componentLoader.load(component) : undefined,
      } as ConvertedRoute,
    ];
  }

  private handleNormalRoute(
    converted: ConvertedRoute,
    component: string | undefined,
    depth: number
  ): void {
    if (!component) return;
    if (this.shellChild && depth === 0 && component === ROUTE_COMPONENT_LAYOUT) {
      converted.component = this.componentLoader.loadNestedParent();
      return;
    }
    converted.component = this.componentLoader.load(component);
  }
}

// ----------------------------------------------------------------------------- RouteRegistry
/** 与静态壳层冲突的一级 path 段，后端动态挂载时跳过以免覆盖首页/仪表盘等 */
const RESERVED_SHELL_SEGMENTS = new Set(["home", "profile", "changelog", "dashboard"]);

function pathFirstSegment(path: string): string {
  return (
    path
      .trim()
      .replace(/^\/+|\/+$/g, "")
      .split("/")
      .filter(Boolean)[0] ?? ""
  );
}

function registrationName(route: AppRouteRecord, index: number): AppRouteRecord {
  const explicit = typeof route.name === "string" ? route.name.trim() : "";
  if (explicit) return route;
  const seg = pathFirstSegment(route.path || "") || "route";
  const safe = seg.replace(/[^\w]/g, "_");
  return { ...route, name: `Dyn_${index}_${safe}` };
}

function routeNameKey(route: AppRouteRecord): string {
  return typeof route.name === "string" ? route.name : String(route.name ?? "");
}

export class RouteRegistry {
  private router: Router;
  private componentLoader: ComponentLoader;
  private validator: RouteValidator;
  private transformer: RouteTransformer;
  private removeRouteFns: (() => void)[] = [];
  private registered = false;

  constructor(router: Router) {
    this.router = router;
    this.componentLoader = new ComponentLoader();
    this.validator = new RouteValidator();
    this.transformer = new RouteTransformer(this.componentLoader, { shellChild: true });
  }

  register(menuList: AppRouteRecord[]): void {
    if (this.registered) {
      console.warn("[RouteRegistry] 路由已注册，跳过重复注册");
      return;
    }

    const validationResult = this.validator.validate(menuList);
    if (!validationResult.valid) {
      throw new Error(`路由配置验证失败: ${validationResult.errors.join(", ")}`);
    }

    const removeRouteFns: (() => void)[] = [];

    menuList.forEach((route, index) => {
      const seg = pathFirstSegment(route.path || "");
      if (seg && RESERVED_SHELL_SEGMENTS.has(seg)) {
        return;
      }

      const namedRoute = registrationName(route, index);
      if (this.router.hasRoute(routeNameKey(namedRoute))) {
        return;
      }

      const routeConfig = this.transformer.transform(namedRoute);
      removeRouteFns.push(
        this.router.addRoute(ROOT_LAYOUT_ROUTE_NAME, routeConfig as RouteRecordRaw)
      );
    });

    this.removeRouteFns = removeRouteFns;
    this.registered = true;
  }

  unregister(): void {
    this.removeRouteFns.forEach((fn) => fn());
    this.removeRouteFns = [];
    this.registered = false;
  }

  isRegistered(): boolean {
    return this.registered;
  }

  getRemoveRouteFns(): (() => void)[] {
    return this.removeRouteFns;
  }

  markAsRegistered(): void {
    this.registered = true;
  }
}
