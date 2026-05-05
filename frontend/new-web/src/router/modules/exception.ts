import { AppRouteRecord } from "@/types/router";

/**
 * 「异常」菜单分组（挂载在 /exception/*，走 Layout）。
 * 与 `staticRoutes` 中独立页区分：
 * - 编程式跳转、守卫：`name` 为 `"403" | "404" | "500"`（对应 `/403`、`/404`、`/500`）
 * - 本模块子路由：`Exception403` / `Exception404` / `Exception500`（对应 `/exception/403` 等），勿与前者混用
 */
export const exceptionRoutes: AppRouteRecord = {
  path: "/exception",
  name: "Exception",
  component: "/index/index",
  meta: {
    title: "menus.exception.title",
    icon: "ri:error-warning-line",
  },
  children: [
    {
      path: "403",
      name: "Exception403",
      component: "/exception/403",
      meta: {
        title: "menus.exception.forbidden",
        keepAlive: true,
        isHideTab: true,
      },
    },
    {
      path: "404",
      name: "Exception404",
      component: "/exception/404",
      meta: {
        title: "menus.exception.notFound",
        keepAlive: true,
        isHideTab: true,
      },
    },
    {
      path: "500",
      name: "Exception500",
      component: "/exception/500",
      meta: {
        title: "menus.exception.serverError",
        keepAlive: true,
        isHideTab: true,
      },
    },
  ],
};
