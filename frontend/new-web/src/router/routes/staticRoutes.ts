import type { AppRouteRecordRaw } from "@/utils/navigation";
import { defineComponent, h, onMounted, ref } from "vue";
import { RouterView, useRoute } from "vue-router";
import { IframeRouteManager } from "../core/IframeRouteManager";
import type { DashboardLeafSegment } from "./shellMenuDescriptors";
import {
  DASHBOARD_LEAF_DESCRIPTORS,
  DASHBOARD_PARENT_META,
  HOME_MENU_META,
} from "./shellMenuDescriptors";

/** 根 Layout 的 route.name；动态路由 `addRoute` 父级须与此一致 */
export const ROOT_LAYOUT_ROUTE_NAME = "RootLayout" as const;

/** 静态首页子路由 name（面包屑等） */
export const HOME_ROUTE_NAME = "Home" as const;

/** 目录占位：仅嵌一层 RouterView（与 ComponentLoader 中占位同源） */
export const NestedRouterParent = defineComponent({
  name: "NestedRouterParent",
  setup() {
    return () => h(RouterView);
  },
});

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

const dashboardLeafComponents: Record<DashboardLeafSegment, () => Promise<unknown>> = {
  workplace: () => import("@/views/dashboard/workplace/index.vue"),
  console: () => import("@/views/dashboard/console/index.vue"),
  analysis: () => import("@/views/dashboard/analysis/index.vue"),
  ecommerce: () => import("@/views/dashboard/ecommerce/index.vue"),
  map: () => import("@/views/dashboard/map/index.vue"),
  pricing: () => import("@/views/dashboard/pricing/index.vue"),
};

/** iframe 内跳页面：内联组件（无需 views/outside/Iframe.vue） */
const IframeView = defineComponent({
  name: "IframeView",
  setup() {
    const route = useRoute();
    const isLoading = ref(true);
    const iframeUrl = ref("");
    const iframeRef = ref<HTMLIFrameElement | null>(null);

    onMounted(() => {
      const iframeRoute = IframeRouteManager.getInstance().findByPath(route.path);
      if (iframeRoute?.meta) {
        iframeUrl.value = (iframeRoute.meta as any).link || "";
      }
    });

    const handleIframeLoad = () => {
      isLoading.value = false;
    };

    return () =>
      h("div", { class: "box-border w-full h-full", "v-loading": isLoading.value }, [
        h("iframe", {
          ref: iframeRef,
          src: iframeUrl.value,
          frameborder: "0",
          class: "w-full h-full min-h-[calc(100vh-120px)] border-none",
          onLoad: handleIframeLoad,
        }),
      ]);
  },
});

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
    name: ROOT_LAYOUT_ROUTE_NAME,
    redirect: "/home",
    component: Layout,
    children: [
      /** 首页（侧栏补入逻辑见 mergeShellMenus + shellMenuDescriptors） */
      {
        path: "home",
        name: HOME_ROUTE_NAME,
        component: () => import("@/views/dashboard/index.vue"),
        meta: HOME_MENU_META,
      },
      {
        path: "profile",
        name: "Profile",
        meta: { title: "个人中心", icon: "ri:user-line", hidden: true },
        component: () => import("@/views/current/profile.vue"),
      },
      /** 更新日志（mock 数据）：侧栏隐藏，由顶栏头像下拉进入（routeName 供 fastEnter 等使用） */
      {
        path: "changelog",
        name: "ChangeLog",
        meta: {
          title: "menus.changelog.title",
          icon: "ri:draft-line",
          hidden: true,
          keepAlive: true,
        },
        component: () => import("@/views/changelog/index.vue"),
      },
      /** 仪表盘：嵌套在根 Layout 下（叶子 meta 与 mergeShellMenus 同源：shellMenuDescriptors） */
      {
        path: "dashboard",
        name: "Dashboard",
        redirect: "/dashboard/workplace",
        component: NestedRouterParent,
        meta: DASHBOARD_PARENT_META,
        children: [
          ...DASHBOARD_LEAF_DESCRIPTORS.map((d) => ({
            path: d.segment,
            name: d.name,
            component: dashboardLeafComponents[d.segment],
            meta: d.meta,
          })),
          /** 文章演示（由 widgets 迁入 dashboard） */
          {
            path: "article",
            name: "DashboardArticle",
            component: NestedRouterParent,
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
                component: () => import("@/views/dashboard/article/list/index.vue"),
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
                component: () => import("@/views/dashboard/article/detail/index.vue"),
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
                component: () => import("@/views/dashboard/article/comment/index.vue"),
                meta: {
                  title: "menus.article.comment",
                  icon: "ri:mail-line",
                  keepAlive: true,
                },
              },
              {
                path: "publish",
                name: "ArticlePublish",
                component: () => import("@/views/dashboard/article/publish/index.vue"),
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
        component: IframeView,
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
