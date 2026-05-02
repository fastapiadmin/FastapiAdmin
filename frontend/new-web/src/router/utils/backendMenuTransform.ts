/**
 * 将后端 `/system/menu/tree` 返回的 MenuTable 转为前端动态路由 AppRouteRecord。
 * 字段对照：route_path→path、route_name→name、component_path→component、目录补 Layout。
 */
import type { MenuTable } from "@/api/module_system/menu";
import type { AppRouteRecord, RouteMeta } from "@/types/router";
import { RoutesAlias } from "@/router/routesAlias";

/**
 * 后端常把「模块目录」与「其下功能菜单」写成同一绝对 route_path。
 * Vue Router 嵌套子路由应使用空 path 挂到父 path 下。
 */
export function normalizeMenuNestedPaths(
  items: MenuTable[],
  parentAbsolutePath?: string
): MenuTable[] {
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

/**
 * 后端常把子菜单 path 存成完整绝对路径（如 `/system/menu`）。
 * Vue Router 嵌套子路由必须为相对段（如 `menu`），否则 validateMenuPaths 会报错。
 */
export function normalizeAppRouteChildPaths(
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

    // 父子 route_path 分叉时（如父 `/task/workflow-mgr` 与子 `/task/workflow/definition`）无法用父前缀裁剪；
    // 取末段作为嵌套相对 path，与 validateMenuPaths 建议一致。
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
  const childrenRaw = item.children?.filter((c) => c.type !== 3) ?? [];
  const children = childrenRaw.length
    ? childrenRaw.map((c) => mapMenuNode(c, depth + 1))
    : undefined;

  const path = (item.route_path ?? "").trim();
  const name = item.route_name || undefined;
  const redirect = item.redirect?.trim() || undefined;

  const hasKids = !!(children && children.length > 0);
  const isDirectory = item.type === 1;

  let component: string | undefined;
  if (isDirectory || (hasKids && !(item.component_path ?? "").trim())) {
    component = depth === 0 ? RoutesAlias.Layout : RoutesAlias.NestedRouterParent;
  } else if ((item.component_path ?? "").trim()) {
    component = toComponentImportPath(item.component_path!);
  }

  const meta: RouteMeta = {
    title: item.title ?? "",
    /** 与 IconSelect / MenuRouteIcon 约定一致，不做字符串改写 */
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

/**
 * 过滤按钮(type=3)，再递归映射为 AppRouteRecord
 */
export function backendMenusToAppRoutes(menus: MenuTable[]): AppRouteRecord[] {
  const roots = menus.filter((m) => m.type !== 3);
  const normalized = normalizeMenuNestedPaths(roots);
  const mapped = normalized.map((m) => mapMenuNode(m, 0));
  return normalizeAppRouteChildPaths(mapped);
}
