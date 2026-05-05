import type { AppRouteRecord } from "@/types/router";

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

/** 静态路由 /home 不在后端菜单树中，补侧栏入口 */
const HOME_SHELL: AppRouteRecord = {
  path: "/home",
  name: "Home",
  meta: {
    title: "menus.home.title",
    icon: "ri:presentation-line",
    keepAlive: true,
    shellRoute: true,
  },
};

/** 与 `staticRoutes` 根 Layout 下 `/dashboard/*` 一致，仅侧栏用（无 component） */
const dashboardMenuSource: AppRouteRecord = {
  name: "Dashboard",
  path: "/dashboard",
  meta: {
    title: "menus.dashboard.title",
    icon: "ri:pie-chart-line",
    alwaysShow: true,
  },
  children: [
    {
      path: "workplace",
      name: "DashboardWorkplace",
      meta: {
        title: "menus.workplace.title",
        icon: "ri:layout-grid-line",
        keepAlive: true,
      },
    },
    {
      path: "console",
      name: "DashboardConsole",
      meta: {
        title: "menus.dashboard.console",
        icon: "ri:home-smile-2-line",
        keepAlive: false,
      },
    },
    {
      path: "analysis",
      name: "DashboardAnalysis",
      meta: {
        title: "menus.dashboard.analysis",
        icon: "ri:align-item-bottom-line",
        keepAlive: false,
      },
    },
    {
      path: "ecommerce",
      name: "DashboardEcommerce",
      meta: {
        title: "menus.dashboard.ecommerce",
        icon: "ri:bar-chart-box-line",
        keepAlive: false,
      },
    },
    {
      path: "map",
      name: "DashboardMap",
      meta: {
        title: "menus.dashboard.map",
        icon: "ri:map-pin-line",
        keepAlive: true,
      },
    },
    {
      path: "pricing",
      name: "DashboardPricing",
      meta: {
        title: "menus.dashboard.pricing",
        icon: "ri:money-cny-box-line",
        keepAlive: true,
      },
    },
  ],
};

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

  tryPush(HOME_SHELL);

  if (!paths.has("/dashboard")) {
    tryPush(dashboardRoutesToShellMenu(structuredClone(dashboardMenuSource)));
  }

  if (additions.length === 0) return menuList;
  return [...additions, ...menuList];
}
