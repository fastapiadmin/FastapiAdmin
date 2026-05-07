// 权限文档：https://www.artd.pro/docs/zh/guide/in-depth/permission.html
import { AppRouteRecord } from "@/types/router";

/** 演示组件库分组（前端路由表；菜单模式下由权限过滤后挂载） */
const widgetsRoutes: AppRouteRecord = {
  path: "/widgets",
  name: "Widgets",
  component: "/index/index",
  meta: {
    title: "menus.widgets.title",
    icon: "ri:apps-2-add-line",
  },
  children: [
    {
      path: "icon",
      name: "Icon",
      component: "/widgets/icon",
      meta: {
        title: "menus.widgets.icon",
        icon: "ri:palette-line",
        keepAlive: true,
      },
    },
    {
      path: "image-crop",
      name: "ImageCrop",
      component: "/widgets/image-crop",
      meta: {
        title: "menus.widgets.imageCrop",
        icon: "ri:screenshot-line",
        keepAlive: true,
      },
    },
    {
      path: "video",
      name: "Video",
      component: "/widgets/video",
      meta: {
        title: "menus.widgets.video",
        icon: "ri:vidicon-line",
        keepAlive: true,
      },
    },
    {
      path: "qrcode",
      name: "Qrcode",
      component: "/widgets/qrcode",
      meta: {
        title: "menus.widgets.qrcode",
        icon: "ri:qr-code-line",
        keepAlive: true,
      },
    },
    {
      path: "drag",
      name: "Drag",
      component: "/widgets/drag",
      meta: {
        title: "menus.widgets.drag",
        icon: "ri:drag-move-fill",
        keepAlive: true,
      },
    },
    {
      path: "fireworks",
      name: "Fireworks",
      component: "/widgets/fireworks",
      meta: {
        title: "menus.widgets.fireworks",
        icon: "ri:magic-line",
        keepAlive: true,
        showTextBadge: "Hot",
      },
    },
  ],
};

/**
 * 「异常」路由分组（挂载在 /exception/*，走 Layout）。
 * 不在侧栏常驻展示（meta.isHide），仅供守卫 / 编程式跳转打开。
 * 与 `staticRoutes` 独立页区分：
 * - 全局短路径：`/403`、`/404`、`/500`（name 与静态路由一致）
 * - 本分组：`Exception403` / `Exception404` / `Exception500` → `/exception/403` 等
 */
const exceptionRoutes: AppRouteRecord = {
  path: "/exception",
  name: "Exception",
  component: "/index/index",
  meta: {
    title: "menus.exception.title",
    icon: "ri:error-warning-line",
    isHide: true,
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
        isHide: true,
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
        isHide: true,
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
        isHide: true,
      },
    },
  ],
};

/**
 * 前端内置路由表（与后端菜单合并或单独在前端模式下使用）。
 * 用于渲染菜单以及根据菜单权限动态加载路由。
 *
 * `/widgets/*` 演示：`widgetsRoutes` 内页面优先复用 `src/components/Core/**`；
 * 文章相关路由已迁至静态路由 `/dashboard/article/*`（见 `staticRoutes.ts` + `shellMenuDescriptors.ts`）。
 */
export const asyncRoutes: AppRouteRecord[] = [widgetsRoutes, exceptionRoutes];
