import type { AppRouteRecord } from "@/types/router";

/**
 * 合并两组路由菜单：先保留 primary（通常为后端菜单），再追加 secondary 中「路由 name 未出现过」的项。
 * Vue Router 要求 name 唯一，同名以前序为准。
 */
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
