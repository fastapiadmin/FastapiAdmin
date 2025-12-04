import type { RouteRecordRaw } from "vue-router";
import router, { constantRoutes } from "@/router";
import { store, useUserStore } from "@/store";
import { MenuTable } from "@/api/module_system/menu";

const modules = import.meta.glob("../../views/**/**.vue");
const Layout = () => import("@/layouts/index.vue");

export interface Meta {
  /** 【目录】只有一个子路由是否始终显示 */
  alwaysShow?: boolean;
  /** 是否隐藏(true-是 false-否) */
  hidden?: boolean;
  /** ICON */
  icon?: string;
  /** 【菜单】是否开启页面缓存 */
  keepAlive?: boolean;
  /** 路由title */
  title?: string;
  /** 排序 */
  order?: number;
  /** 参数 */
  params?: { key: string; value: string }[];
  /** 是否固定路由 */
  affix?: boolean;
}

// 修改 component 类型，使其能接受动态导入函数
export interface RouteVO {
  /** 子路由列表 */
  children: RouteVO[];
  /** 组件路径或组件导入函数 */
  component?: string | (() => Promise<Component>);
  /** 路由属性 */
  meta?: Meta;
  /** 路由名称 */
  name?: string;
  /** 路由路径 */
  path?: string;
  /** 跳转链接 */
  redirect?: string;
}

export const generator = (routers: MenuTable[]): RouteVO[] => {
  return routers.map((item) => {
    const currentRouter: RouteVO = {
      children: [],
      path: item.route_path,
      name: item.route_name,
      component: item.component_path,
      redirect: item.redirect,
      meta: {
        title: item.title,
        icon: item.icon || undefined,
        keepAlive: item.keep_alive,
        hidden: item.hidden,
        order: item.order,
        alwaysShow: item.always_show,
        params: item.params,
        affix: item.affix,
      },
    };
    if (item.children && item.children.length > 0) {
      currentRouter.children = item.children ? generator(item.children) : [];
    }
    return currentRouter;
  });
};

export const usePermissionStore = defineStore("permission", () => {
  // 存储所有路由，包括静态路由和动态路由
  const routes = ref<RouteRecordRaw[]>([]);
  // 混合模式左侧菜单路由
  const mixLayoutSideMenus = ref<RouteRecordRaw[]>([]);
  // 路由是否加载完成
  const isRouteGenerated = ref(false);

  /**
   * 获取后台动态路由数据，解析并注册到全局路由
   *
   * @returns Promise<RouteRecordRaw[]> 解析后的动态路由列表
   */
  async function generateRoutes(): Promise<RouteRecordRaw[]> {
    try {
      const userStore = useUserStore();
      // 确保获取用户信息和路由列表
      if (!userStore.hasGetRoute) {
        await userStore.getUserInfo();
      }

      const data = generator(userStore.routeList);

      // 解析动态路由
      const dynamicRoutes = transformRoutes(data);

      routes.value = [...constantRoutes, ...dynamicRoutes];

      isRouteGenerated.value = true;

      return dynamicRoutes;
    } catch (error: any) {
      // 即使失败也要设置状态，避免无限重试
      isRouteGenerated.value = false;
      throw error;
    }
  }

  /**
   * 根据父菜单路径设置侧边菜单
   *
   * @param parentPath 父菜单的路径，用于查找对应的菜单项
   */
  const setMixLayoutSideMenus = (parentPath: string) => {
    const parentMenu = routes.value.find((item) => item.path === parentPath);
    mixLayoutSideMenus.value = parentMenu?.children || [];
  };

  /**
   * 重置路由
   */
  const resetRouter = () => {
    // 创建常量路由名称集合，用于O(1)时间复杂度的查找
    const constantRouteNames = new Set(constantRoutes.map((route) => route.name).filter(Boolean));

    // 从 router 实例中移除动态路由
    routes.value.forEach((route) => {
      if (route.name && !constantRouteNames.has(route.name)) {
        router.removeRoute(route.name);
      }
    });

    // 重置所有状态
    routes.value = [...constantRoutes];
    mixLayoutSideMenus.value = [];
    isRouteGenerated.value = false;
  };

  return {
    routes,
    mixLayoutSideMenus,
    isRouteGenerated,
    generateRoutes,
    setMixLayoutSideMenus,
    resetRouter,
  };
});

/**
 * 转换后端路由数据为Vue Router配置
 * 处理组件路径映射和Layout层级嵌套
 */
const transformRoutes = (routes: RouteVO[], isTopLevel: boolean = true): RouteRecordRaw[] => {
  return routes.map((route) => {
    // 创建路由对象，保留所有路由属性
    const normalizedRoute = { ...route } as RouteRecordRaw;

    // 处理组件路径映射
    // normalizedRoute.component = !normalizedRoute.component
    //   ? Layout
    //   : modules[`../../views/${normalizedRoute.component}.vue`] ||
    //     modules["../../views/error/404.vue"];

    // 关键优化：
    // 1. 顶级路由（一级目录）使用Layout组件，确保菜单和navbar能正常显示
    // 2. 二级及以上的父路由不使用Layout组件，只作为路由容器，避免Layout嵌套
    // 3. 叶子路由使用实际组件
    // 4. 递归处理子路由，实现无限层级菜单
    if (normalizedRoute.children && normalizedRoute.children.length > 0) {
      // normalizedRoute.children = transformRoutes(route.children);
    
      // 非叶子路由
      if (isTopLevel) {
        // 顶级路由（一级目录），使用Layout组件
        normalizedRoute.component = Layout;
      } else {
        // 二级及以上的父路由，不使用Layout组件，只作为路由容器
        normalizedRoute.component = undefined;
      }
      // 递归处理子路由，标记为非顶级路由
      normalizedRoute.children = transformRoutes(route.children, false);
    } else {
      // 叶子路由，使用实际组件
      normalizedRoute.component = normalizedRoute.component
        ? modules[`../../views/${normalizedRoute.component}.vue`] ||
          modules["../../views/error/404.vue"]
        : modules["../../views/error/404.vue"];
    }

    return normalizedRoute;
  });
};

/**
 * 导出此hook函数用于在非组件环境(如其他store、工具函数等)中获取权限store实例
 *
 * 在组件中可直接使用usePermissionStore()，但在组件外部需要传入store实例
 * 此函数简化了这个过程，避免每次都手动传入store参数
 */
export function usePermissionStoreHook() {
  return usePermissionStore(store);
}
