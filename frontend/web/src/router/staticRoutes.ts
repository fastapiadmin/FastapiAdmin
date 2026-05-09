import type { AppRouteRecordRaw } from "@utils/navigation";
import type { AppRouteRecord, RouteMeta } from "@/types/router";
import { defineComponent, h, onMounted, ref } from "vue";
import type { RouteRecordRaw } from "vue-router";
import { RouterView, useRoute } from "vue-router";

/** 首页 / 仪表盘父级 meta（侧栏、静态子路由共用） */
export const HOME_MENU_META: RouteMeta = {
  title: "menus.home.title",
  icon: "ri:presentation-line",
  keepAlive: true,
};

export const DASHBOARD_PARENT_META: RouteMeta = {
  title: "menus.dashboard.title",
  icon: "ri:pie-chart-line",
  alwaysShow: true,
};

/** iframe 路由注册表（与动态路由、守卫共用） */
export class IframeRouteManager {
  private static instance: IframeRouteManager;
  private iframeRoutes: AppRouteRecord[] = [];

  private constructor() {}

  static getInstance(): IframeRouteManager {
    if (!IframeRouteManager.instance) {
      IframeRouteManager.instance = new IframeRouteManager();
    }
    return IframeRouteManager.instance;
  }

  add(route: AppRouteRecord): void {
    if (!this.iframeRoutes.find((r) => r.path === route.path)) {
      this.iframeRoutes.push(route);
    }
  }

  getAll(): AppRouteRecord[] {
    return this.iframeRoutes;
  }

  findByPath(path: string): AppRouteRecord | undefined {
    return this.iframeRoutes.find((route) => route.path === path);
  }

  clear(): void {
    this.iframeRoutes = [];
  }

  save(): void {
    if (this.iframeRoutes.length > 0) {
      sessionStorage.setItem("iframeRoutes", JSON.stringify(this.iframeRoutes));
    }
  }

  load(): void {
    try {
      const data = sessionStorage.getItem("iframeRoutes");
      if (data) {
        this.iframeRoutes = JSON.parse(data);
      }
    } catch (error) {
      console.error("[IframeRouteManager] 加载 iframe 路由失败:", error);
      this.iframeRoutes = [];
    }
  }
}

/** 根 Layout 的 route.name；动态路由 `addRoute` 父级须与此一致 */
export const ROOT_LAYOUT_ROUTE_NAME = "RootLayout" as const;

/** 静态首页子路由 name（面包屑等） */
export const HOME_ROUTE_NAME = "Home" as const;

/** 目录占位：仅嵌一层 RouterView（与 ComponentLoader 中占位同源） */
export const NestedRouterParent = defineComponent({
  name: "NestedRouterParent",
  setup() {
    return () => h(RouterView);
  },
});

/** 后端菜单 / 动态路由里 `component` 占位（与 ComponentLoader 约定一致） */
export const ROUTE_COMPONENT_LAYOUT = "/index/index";

/** 多级目录父级占位（`views/nested/router-view-parent`） */
export const ROUTE_COMPONENT_NESTED_PARENT = "/nested/router-view-parent";

/** 登录页备用 path（与静态 `/login` 并存，守卫与白名单用） */
export const ROUTE_PATH_LOGIN_ALT = "/auth/login";

/**
 * 主框架布局：新版 art 体系（`src/layouts/index.vue` + `src/layouts/art-*` 组件）。
 * 旧版 Left/Top/Mix 壳子仍在 `@/layouts/index.vue`，路由不再默认使用。
 */
export const Layout = () => import("@/layouts/index.vue");

/** iframe 内跳页面：内联组件（无需 views/outside/Iframe.vue） */
const IframeView = defineComponent({
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
});

/**
 * `/dashboard` 下静态子路由（唯一数据源）。
 * 下方壳层菜单合并函数由此剥离 `component` 生成侧栏补全菜单。
 */
export const dashboardLayoutChildren: AppRouteRecordRaw[] = [
  {
    path: "workplace",
    name: "DashboardWorkplace",
    component: () => import("@views/dashboard/workplace/index.vue"),
    meta: {
      title: "menus.workplace.title",
      icon: "ri:layout-grid-line",
      keepAlive: true,
    },
  },
  {
    path: "console",
    name: "DashboardConsole",
    component: () => import("@views/dashboard/console/index.vue"),
    meta: {
      title: "menus.dashboard.console",
      icon: "ri:home-smile-2-line",
      keepAlive: false,
      fixedTab: true,
    },
  },
  {
    path: "analysis",
    name: "DashboardAnalysis",
    component: () => import("@views/dashboard/analysis/index.vue"),
    meta: {
      title: "menus.dashboard.analysis",
      icon: "ri:align-item-bottom-line",
      keepAlive: false,
    },
  },
  {
    path: "ecommerce",
    name: "DashboardEcommerce",
    component: () => import("@views/dashboard/ecommerce/index.vue"),
    meta: {
      title: "menus.dashboard.ecommerce",
      icon: "ri:bar-chart-box-line",
      keepAlive: false,
    },
  },
  {
    path: "map",
    name: "DashboardMap",
    component: () => import("@views/dashboard/map/index.vue"),
    meta: {
      title: "menus.dashboard.map",
      icon: "ri:map-pin-line",
      keepAlive: true,
    },
  },
  {
    path: "pricing",
    name: "DashboardPricing",
    component: () => import("@views/dashboard/pricing/index.vue"),
    meta: {
      title: "menus.dashboard.pricing",
      icon: "ri:money-cny-box-line",
      keepAlive: true,
    },
  },
  {
    path: "article",
    name: "DashboardArticle",
    component: NestedRouterParent,
    meta: {
      title: "menus.article.title",
      icon: "ri:book-2-line",
      alwaysShow: true,
      roles: ["R_SUPER", "R_ADMIN"],
    },
    children: [
      {
        path: "article-list",
        name: "ArticleList",
        component: () => import("@views/dashboard/article/list/index.vue"),
        meta: {
          title: "menus.article.articleList",
          icon: "ri:article-line",
          keepAlive: true,
          authList: [
            { title: "新增", authMark: "add" },
            { title: "编辑", authMark: "edit" },
          ],
        },
      },
    ],
  },
  {
    path: "tutorial",
    name: "DashboardTutorial",
    component: () => import("@views/dashboard/tutorial/index.vue"),
    meta: {
      title: "menus.dashboard.tutorial",
      icon: "ri:movie-2-line",
      keepAlive: true,
    },
  },
];

// -----------------------------------------------------------------------------
// 静态壳层菜单：后端未下发 /home、/dashboard 时补全侧栏；混合模式路由按 name 去重合并

export const mergeShellHomeMenu: AppRouteRecord = {
  path: "/home",
  name: "Home",
  meta: { ...HOME_MENU_META, shellRoute: true },
};

/** 去掉组件与 redirect，供侧栏合并（菜单节点不需要懒加载引用） */
function stripRouteRecordForShell(route: RouteRecordRaw): AppRouteRecord {
  const children = route.children?.map(stripRouteRecordForShell);
  return {
    path: route.path,
    name: route.name,
    meta: (route.meta ?? {}) as AppRouteRecord["meta"],
    ...(children?.length ? { children } : {}),
  } as AppRouteRecord;
}

export function getDashboardMenuTreeForMerge(): AppRouteRecord {
  return {
    name: "Dashboard",
    path: "/dashboard",
    meta: DASHBOARD_PARENT_META,
    children: dashboardLayoutChildren.map(stripRouteRecordForShell),
  };
}

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
      if (r.children?.length) {
        next.children = pickFresh(r.children);
      }
      if (n) usedNames.add(n);
      out.push(next);
    }
    return out;
  };

  return [...primary, ...pickFresh(secondary)];
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
  return {
    ...route,
    path: fullPath,
    meta,
    children,
    component: undefined,
    redirect: undefined,
  };
}

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
      if (item.children?.length) {
        collectPathsAndNames(item.children, paths, names);
      }
    }
  };

  tryPush(mergeShellHomeMenu);

  if (!paths.has("/dashboard")) {
    tryPush(dashboardRoutesToShellMenu(structuredClone(getDashboardMenuTreeForMerge())));
  }

  if (additions.length === 0) return menuList;
  return [...additions, ...menuList];
}

/**
 * 静态路由配置（不需要权限就能访问的路由）
 *
 * 属性说明：
 * isHideTab: true 表示不在标签页中显示
 *
 * 注意事项：
 * 1、path、name 不要和动态路由冲突，否则会导致路由冲突无法访问
 * 2、静态路由不管是否登录都可以访问
 */
export const staticRoutes: AppRouteRecordRaw[] = [
  {
    path: "/redirect",
    meta: { hidden: true },
    component: Layout,
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@views/redirect/index.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    meta: { hidden: true, isHideTab: true, title: "menus.login.title" },
    component: () => import("@views/module_system/auth/login/index.vue"),
  },
  /** 无 Layout 全屏异常页；守卫与白名单跳转使用（勿再在 RootLayout 下重复挂载同组件） */
  {
    path: "/401",
    name: "401",
    meta: { hidden: true, title: "401" },
    component: () => import("@views/exception/401/index.vue"),
  },
  {
    path: "/403",
    name: "403",
    component: () => import("@views/exception/403/index.vue"),
    meta: { hidden: true, title: "403" },
  },
  {
    path: "/404",
    name: "404",
    meta: { hidden: true, title: "404" },
    component: () => import("@views/exception/404/index.vue"),
  },
  {
    path: "/500",
    name: "500",
    meta: { hidden: true, title: "500" },
    component: () => import("@views/exception/500/index.vue"),
  },
  {
    path: "/",
    name: ROOT_LAYOUT_ROUTE_NAME,
    redirect: "/home",
    component: Layout,
    children: [
      /** 首页（侧栏补入逻辑见同文件 `mergeShellRoutesIntoMenu`） */
      {
        path: "home",
        name: HOME_ROUTE_NAME,
        component: () => import("@views/dashboard/index.vue"),
        meta: HOME_MENU_META,
      },
      {
        path: "profile",
        name: "Profile",
        meta: { title: "个人中心", icon: "ri:user-line", hidden: true },
        component: () => import("@views/current/profile.vue"),
      },
      /** 更新日志（mock 数据）：侧栏隐藏，由顶栏头像下拉进入（routeName 供 fastEnter 等使用） */
      {
        path: "changelog",
        name: "ChangeLog",
        meta: {
          title: "menus.changelog.title",
          icon: "ri:draft-line",
          hidden: true,
          keepAlive: true,
        },
        component: () => import("@views/changelog/index.vue"),
      },
      /** 仪表盘子路由定义见同文件导出的 `dashboardLayoutChildren` */
      {
        path: "dashboard",
        name: "Dashboard",
        redirect: "/dashboard/workplace",
        component: NestedRouterParent,
        meta: DASHBOARD_PARENT_META,
        children: dashboardLayoutChildren,
      },
    ],
  },
  {
    path: "/outside",
    component: () => import("@/layouts/index.vue"),
    name: "Outside",
    meta: { title: "menus.outside.title" },
    children: [
      {
        path: "/outside/iframe/:path",
        name: "Iframe",
        component: IframeView,
        meta: { title: "iframe" },
      },
    ],
  },
  // 通配 404 必须置于静态路由最后（name 勿与上方 `/404` 重复，否则按名跳转不稳定）
  {
    path: "/:pathMatch(.*)*",
    name: "CatchAll404",
    component: () => import("@views/exception/404/index.vue"),
    meta: { hidden: true, title: "404" },
  },
];
