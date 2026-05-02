import { RoutesAlias } from "@/router/routesAlias";
import { AppRouteRecord } from "@/types/router";

/**
 * 模版仪表盘（演示 console / analysis / ecommerce）
 * 与后端 sys_menu 的「仪表盘」区分：独立 name / path，混合模式下才不会被去重掉
 */
export const dashboardRoutes: AppRouteRecord = {
  name: "DashboardDemo",
  path: "/dashboard-demo",
  component: RoutesAlias.Layout,
  redirect: "/dashboard-demo/console",
  meta: {
    title: "menus.dashboard.demoTitle",
    icon: "ri:pie-chart-line",
  },
  children: [
    {
      path: "console",
      name: "DashboardDemoConsole",
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
      name: "DashboardDemoAnalysis",
      component: "/dashboard/analysis",
      meta: {
        title: "menus.dashboard.analysis",
        icon: "ri:align-item-bottom-line",
        keepAlive: false,
      },
    },
    {
      path: "ecommerce",
      name: "DashboardDemoEcommerce",
      component: "/dashboard/ecommerce",
      meta: {
        title: "menus.dashboard.ecommerce",
        icon: "ri:bar-chart-box-line",
        keepAlive: false,
      },
    },
  ],
};
