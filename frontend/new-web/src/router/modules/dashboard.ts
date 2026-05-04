import { RoutesAlias } from "@/router/routesAlias";
import type { AppRouteRecord } from "@/types/router";

/** 前端仪表盘（`/dashboard`）；与后端同 path/name 时 mergeAppRouteRecords 保留后端 */
export const dashboardRoutes: AppRouteRecord = {
  name: "Dashboard",
  path: "/dashboard",
  component: RoutesAlias.Layout,
  redirect: "/dashboard/workplace",
  meta: {
    title: "menus.dashboard.title",
    icon: "ri:pie-chart-line",
    alwaysShow: true,
  },
  children: [
    {
      path: "workplace",
      name: "DashboardWorkplace",
      component: "/dashboard/workplace",
      meta: {
        title: "menus.workplace.title",
        icon: "ri:layout-grid-line",
        keepAlive: true,
      },
    },
    {
      path: "console",
      name: "DashboardConsole",
      component: "/dashboard/console",
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
      component: "/dashboard/analysis",
      meta: {
        title: "menus.dashboard.analysis",
        icon: "ri:align-item-bottom-line",
        keepAlive: false,
      },
    },
    {
      path: "ecommerce",
      name: "DashboardEcommerce",
      component: "/dashboard/ecommerce",
      meta: {
        title: "menus.dashboard.ecommerce",
        icon: "ri:bar-chart-box-line",
        keepAlive: false,
      },
    },
  ],
};
