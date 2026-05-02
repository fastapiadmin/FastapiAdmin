import type { AppRouteRecordRaw } from "@/utils/navigation/router";

/**
 * 主框架布局：新版 art 体系（`src/layouts/index.vue` + `src/components/core/layouts/*`）。
 * 旧版 Left/Top/Mix 壳子仍在 `@/layouts/index.vue`，路由不再默认使用。
 */
export const Layout = () => import("@/layouts/index.vue");

/**
 * 静态路由配置（不需要权限就能访问的路由）
 *
 * 属性说明：
 * isHideTab: true 表示不在标签页中显示
 *
 * 注意事项：
 * 1、path、name 不要和动态路由冲突，否则会导致路由冲突无法访问
 * 2、静态路由不管是否登录都可以访问
 */
export const staticRoutes: AppRouteRecordRaw[] = [
  {
    path: "/welcome",
    name: "WelcomeStatic",
    component: () => import("@views/dashboard/console/index.vue"),
    meta: { title: "menus.dashboard.title" },
  },
  {
    path: "/redirect",
    meta: { hidden: true },
    component: Layout,
    children: [
      {
        path: "/redirect/:path(.*)",
        component: () => import("@/views/redirect/index.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    meta: { hidden: true, title: "menus.login.title" },
    component: () => import("@views/module_system/auth/login/index.vue"),
  },
  {
    path: "/401",
    name: "401",
    meta: { hidden: true, title: "401" },
    component: () => import("@/views/error/401.vue"),
  },
  {
    path: "/404",
    name: "404",
    meta: { hidden: true, title: "404" },
    component: () => import("@/views/error/404.vue"),
  },
  {
    path: "/500",
    name: "500",
    meta: { hidden: true, title: "500" },
    component: () => import("@/views/error/500.vue"),
  },
  {
    path: "/",
    name: "/",
    redirect: "/workbench",
    component: Layout,
    children: [
      /** 业务工作台（自建 workplace.vue） */
      {
        path: "workbench",
        name: "Workbench",
        component: () => import("@/views/dashboard/workplace.vue"),
        meta: {
          title: "menus.workbench.title",
          icon: "ri:layout-grid-line",
          affix: true,
          keepAlive: true,
        },
      },
      /** 数据门户（自建 index.vue，与模版 /dashboard/* 子页区分） */
      {
        path: "portal",
        name: "PortalHome",
        component: () => import("@/views/dashboard/index.vue"),
        meta: {
          title: "menus.portal.title",
          icon: "ri:presentation-line",
          keepAlive: true,
        },
      },
      /** 旧链接 /#/home 兼容，进入工作台 */
      {
        path: "home",
        redirect: "/workbench",
      },
      {
        path: "profile",
        name: "Profile",
        meta: { title: "个人中心", icon: "user", hidden: true },
        component: () => import("@/views/current/profile.vue"),
      },
    ],
  },
  {
    path: "/403",
    name: "Exception403",
    component: () => import("@views/exception/403/index.vue"),
    meta: { title: "403", isHideTab: true },
  },
  {
    path: "/outside",
    component: () => import("@/layouts/index.vue"),
    name: "Outside",
    meta: { title: "menus.outside.title" },
    children: [
      {
        path: "/outside/iframe/:path",
        name: "Iframe",
        component: () => import("@/views/outside/Iframe.vue"),
        meta: { title: "iframe" },
      },
    ],
  },
  // 通配 404 必须置于静态路由最后
  {
    path: "/:pathMatch(.*)*",
    name: "Exception404",
    component: () => import("@views/exception/404/index.vue"),
    meta: { title: "404", isHideTab: true },
  },
];
