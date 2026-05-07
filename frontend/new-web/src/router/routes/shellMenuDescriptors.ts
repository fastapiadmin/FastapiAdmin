/**
 * 静态壳层「首页 / 仪表盘」菜单元数据单一来源。
 * - `staticRoutes` 据此挂载真实 component；
 * - `mergeShellMenus` 据此在后端未下发时补侧栏（无 component，含 shellRoute）。
 */
import type { AppRouteRecord, RouteMeta } from "@/types/router";

export const HOME_MENU_META: RouteMeta = {
  title: "menus.home.title",
  icon: "ri:presentation-line",
  keepAlive: true,
};

/** 后端菜单树无 `/home` 时并入侧栏（shellRoute 表示组件由静态路由提供） */
export const mergeShellHomeMenu: AppRouteRecord = {
  path: "/home",
  name: "Home",
  meta: { ...HOME_MENU_META, shellRoute: true },
};

export const DASHBOARD_PARENT_META: RouteMeta = {
  title: "menus.dashboard.title",
  icon: "ri:pie-chart-line",
  alwaysShow: true,
};

export type DashboardLeafSegment =
  | "workplace"
  | "console"
  | "analysis"
  | "ecommerce"
  | "map"
  | "pricing";

export interface DashboardLeafDescriptor {
  segment: DashboardLeafSegment;
  name: string;
  meta: RouteMeta;
}

/** 与根 Layout 下 `dashboard` 子路由 path/name/meta 一致（不含 component） */
export const DASHBOARD_LEAF_DESCRIPTORS: DashboardLeafDescriptor[] = [
  {
    segment: "workplace",
    name: "DashboardWorkplace",
    meta: {
      title: "menus.workplace.title",
      icon: "ri:layout-grid-line",
      keepAlive: true,
    },
  },
  {
    segment: "console",
    name: "DashboardConsole",
    meta: {
      title: "menus.dashboard.console",
      icon: "ri:home-smile-2-line",
      keepAlive: false,
      fixedTab: true,
    },
  },
  {
    segment: "analysis",
    name: "DashboardAnalysis",
    meta: {
      title: "menus.dashboard.analysis",
      icon: "ri:align-item-bottom-line",
      keepAlive: false,
    },
  },
  {
    segment: "ecommerce",
    name: "DashboardEcommerce",
    meta: {
      title: "menus.dashboard.ecommerce",
      icon: "ri:bar-chart-box-line",
      keepAlive: false,
    },
  },
  {
    segment: "map",
    name: "DashboardMap",
    meta: {
      title: "menus.dashboard.map",
      icon: "ri:map-pin-line",
      keepAlive: true,
    },
  },
  {
    segment: "pricing",
    name: "DashboardPricing",
    meta: {
      title: "menus.dashboard.pricing",
      icon: "ri:money-cny-box-line",
      keepAlive: true,
    },
  },
];

/** 供 mergeShellMenus 生成与静态路由一致的菜单树（再套 shellRoute / 绝对 path） */
export function getDashboardMenuTreeForMerge(): AppRouteRecord {
  return {
    name: "Dashboard",
    path: "/dashboard",
    meta: DASHBOARD_PARENT_META,
    children: [
      ...DASHBOARD_LEAF_DESCRIPTORS.map((d) => ({
        path: d.segment,
        name: d.name,
        meta: d.meta,
      })),
      {
        path: "article",
        name: "DashboardArticle",
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
          {
            path: "detail/:id",
            name: "ArticleDetail",
            meta: {
              title: "menus.article.articleDetail",
              isHide: true,
              keepAlive: true,
              activePath: "/dashboard/article/article-list",
            },
          },
          {
            path: "comment",
            name: "ArticleComment",
            meta: {
              title: "menus.article.comment",
              icon: "ri:mail-line",
              keepAlive: true,
            },
          },
          {
            path: "publish",
            name: "ArticlePublish",
            meta: {
              title: "menus.article.articlePublish",
              icon: "ri:telegram-2-line",
              keepAlive: true,
              authList: [{ title: "发布", authMark: "add" }],
            },
          },
        ],
      },
    ],
  };
}
