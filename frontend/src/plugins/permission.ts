import type { NavigationGuardNext, RouteLocationNormalized, RouteRecordRaw } from "vue-router";
import NProgress from "@/utils/nprogress";
import { Auth } from "@/utils/auth";
import router from "@/router";
import { usePermissionStore, useUserStore } from "@/store";

export function setupPermission() {
  // 白名单路由
  const whiteList = ["/login"];

  router.beforeEach(async (to, from, next) => {
    NProgress.start();

    try {
      const isLoggedIn = Auth.isLoggedIn();

      if (isLoggedIn) {
        // 如果已登录但访问登录页，重定向到首页
        if (to.path === "/login") {
          next({ path: "/" });
          return;
        }

        // 处理已登录用户的路由访问
        await handleAuthenticatedUser(to, from, next);
      } else {
        // 检查是否开启了自动登录
        const autoLoginEnabled = import.meta.env.VITE_AUTO_LOGIN_ENABLED === 'true';
        const autoLoginUsername = import.meta.env.VITE_AUTO_LOGIN_USERNAME;
        const autoLoginPassword = import.meta.env.VITE_AUTO_LOGIN_PASSWORD;
        const autoLoginRemember = import.meta.env.VITE_AUTO_LOGIN_REMEMBER === 'true';
        

        if (autoLoginEnabled && autoLoginUsername && autoLoginPassword) {
          try {
            const userStore = useUserStore();
            await userStore.login({
              username: autoLoginUsername,
              password: autoLoginPassword,
              remember: autoLoginRemember,
              captcha_key: "",
              captcha: "",
              login_type: "password"
            });
            next({ ...to, replace: true });
            return;
          } catch (error) {
            console.error("Auto login failed！auto login need close captcha!:", error);
          }
        }
        // 未登录用户的处理
        if (whiteList.includes(to.path)) {
          next();
        } else {
          next(`/login?redirect=${encodeURIComponent(to.fullPath)}`);
          NProgress.done();
        }
      }
    } catch (error) {
      // 错误处理：重置状态并跳转登录
      console.error("Route guard error:", error);
      await useUserStore().resetAllState();
      next("/login");
      NProgress.done();
    }
  });

  // 后置守卫，确保进度条关闭
  router.afterEach(() => {
    NProgress.done();
  });
}

/**
 * 处理已登录用户的路由访问
 */
async function handleAuthenticatedUser(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) {
  const permissionStore = usePermissionStore();
  const userStore = useUserStore();

  try {
    // 检查路由是否已生成
    if (!permissionStore.isRouteGenerated) {
      if (!userStore.basicInfo?.roles?.length) {
        await userStore.getUserInfo();
      }

      const dynamicRoutes = await permissionStore.generateRoutes();
      // 添加路由到路由器
      dynamicRoutes.forEach((route: RouteRecordRaw) => {
        router.addRoute(route);
      });

      // 路由生成完成后，重新导航到目标路由
      next({ ...to, replace: true });
      return;
    }

    // 路由已加载，检查路由是否存在
    if (to.matched.length === 0) {
      next("/404");
      return;
    }

    // 动态设置页面标题
    const title = (to.params.title as string) || (to.query.title as string);
    if (title) {
      to.meta.title = title;
    }

    next();
  } catch (error) {
    console.error("❌ Route guard error:", error);
    await useUserStore().resetAllState();
    // 强制跳转到登录页
    next("/login");
    NProgress.done();
  }
  router.afterEach(() => {
    NProgress.done();
  });
}
