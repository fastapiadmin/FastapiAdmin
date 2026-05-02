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

/**
 * 与 `staticRoutes` 里挂在 Layout 下的壳子页一致（路由已在 vue-router 注册，仅补侧边栏入口）。
 * meta.shellRoute 表示无动态 component 字段，由 SidebarSubmenu 放行可点击。
 */
const STATIC_SHELL_MENU_ENTRIES: AppRouteRecord[] = [
  {
    path: "/workbench",
    name: "Workbench",
    meta: {
      title: "menus.workbench.title",
      icon: "ri:layout-grid-line",
      affix: true,
      keepAlive: true,
      shellRoute: true,
    },
  },
  {
    path: "/portal",
    name: "PortalHome",
    meta: {
      title: "menus.portal.title",
      icon: "ri:presentation-line",
      keepAlive: true,
      shellRoute: true,
    },
  },
];

/**
 * 将静态壳层菜单合并进后端菜单树（避免动态菜单里缺少工作台 / 数据门户入口）。
 */
export function mergeShellRoutesIntoMenu(menuList: AppRouteRecord[]): AppRouteRecord[] {
  const paths = new Set<string>();
  const names = new Set<string>();
  collectPathsAndNames(menuList, paths, names);

  const additions = STATIC_SHELL_MENU_ENTRIES.filter((shell) => {
    const p = normalizeMenuPath(shell.path as string);
    const n = shell.name ? String(shell.name) : "";
    return p && !paths.has(p) && (!n || !names.has(n));
  });

  if (additions.length === 0) return menuList;
  return [...additions, ...menuList];
}
