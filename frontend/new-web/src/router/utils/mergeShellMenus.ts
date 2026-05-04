import type { AppRouteRecord } from "@/types/router";
import { dashboardRoutes } from "@/router/modules/dashboard";

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
    tryPush(dashboardRoutesToShellMenu(structuredClone(dashboardRoutes)));
  }

  if (additions.length === 0) return menuList;
  return [...additions, ...menuList];
}
