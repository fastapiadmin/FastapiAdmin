import type { AppRouteRecordRaw } from "@/utils/navigation";

/** 后端菜单 / 动态路由里 `component` 占位（与 ComponentLoader 约定一致） */
export const ROUTE_COMPONENT_LAYOUT = "/index/index";

/** 多级目录父级占位（`views/nested/router-view-parent`） */
export const ROUTE_COMPONENT_NESTED_PARENT = "/nested/router-view-parent";

/** 登录页备用 path（与静态 `/login` 并存，守卫与白名单用） */
export const ROUTE_PATH_LOGIN_ALT = "/auth/login";

/**
 * 主框架布局：新版 art 体系（`src/layouts/index.vue` + `src/layouts/art-*` 组件）。
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
    component: () => import("@/views/exception/401/index.vue"),
  },
  {
    path: "/403",
    name: "403",
    component: () => import("@views/exception/403/index.vue"),
    meta: { hidden: true, title: "403" },
  },
  {
    path: "/404",
    name: "404",
    meta: { hidden: true, title: "404" },
    component: () => import("@/views/exception/404/index.vue"),
  },
  {
    path: "/500",
    name: "500",
    meta: { hidden: true, title: "500" },
    component: () => import("@/views/exception/500/index.vue"),
  },
  {
    path: "/",
    name: "/",
    redirect: "/home",
    component: Layout,
    children: [
      /** 首页（壳层菜单见 mergeShellMenus）；仪表盘同挂在下方 `dashboard` 子树 */
      {
        path: "home",
        name: "Home",
        component: () => import("@/views/dashboard/index.vue"),
        meta: {
          title: "menus.home.title",
          icon: "ri:presentation-line",
          keepAlive: true,
        },
      },
      {
        path: "profile",
        name: "Profile",
        meta: { title: "个人中心", icon: "ri:user-line", hidden: true },
        component: () => import("@/views/current/profile.vue"),
      },
      /** 仪表盘：嵌套在根 Layout 下，与 `/home`、`/profile` 同级挂载 */
      {
        path: "dashboard",
        name: "Dashboard",
        redirect: "/dashboard/workplace",
        component: () => import("@/views/nested/router-view-parent/index.vue"),
        meta: {
          title: "menus.dashboard.title",
          icon: "ri:pie-chart-line",
          alwaysShow: true,
        },
        children: [
          {
            path: "workplace",
            name: "DashboardWorkplace",
            component: () => import("@/views/dashboard/workplace/index.vue"),
            meta: {
              title: "menus.workplace.title",
              icon: "ri:layout-grid-line",
              keepAlive: true,
            },
          },
          {
            path: "console",
            name: "DashboardConsole",
            component: () => import("@/views/dashboard/console/index.vue"),
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
            component: () => import("@/views/dashboard/analysis/index.vue"),
            meta: {
              title: "menus.dashboard.analysis",
              icon: "ri:align-item-bottom-line",
              keepAlive: false,
            },
          },
          {
            path: "ecommerce",
            name: "DashboardEcommerce",
            component: () => import("@/views/dashboard/ecommerce/index.vue"),
            meta: {
              title: "menus.dashboard.ecommerce",
              icon: "ri:bar-chart-box-line",
              keepAlive: false,
            },
          },
          {
            path: "map",
            name: "DashboardMap",
            component: () => import("@/views/dashboard/map/index.vue"),
            meta: {
              title: "menus.dashboard.map",
              icon: "ri:map-pin-line",
              keepAlive: true,
            },
          },
          {
            path: "pricing",
            name: "DashboardPricing",
            component: () => import("@/views/dashboard/pricing/index.vue"),
            meta: {
              title: "menus.dashboard.pricing",
              icon: "ri:money-cny-box-line",
              keepAlive: true,
            },
          },
        ],
      },
    ],
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
  // 通配 404 必须置于静态路由最后（name 勿与上方 `/404` 重复，否则按名跳转不稳定）
  {
    path: "/:pathMatch(.*)*",
    name: "CatchAll404",
    component: () => import("@views/exception/404/index.vue"),
    meta: { hidden: true, title: "404" },
  },
];
