/**
 * 用户状态管理模块
 *
 * 提供用户相关的状态管理
 *
 * ## 主要功能
 *
 * - 用户登录状态管理
 * - 用户信息存储
 * - 访问令牌和刷新令牌管理
 * - 语言设置
 * - 搜索历史记录
 * - 锁屏状态和密码管理
 * - 登出清理逻辑
 * - Token刷新
 * - 记住我功能
 *
 * ## 使用场景
 *
 * - 用户登录和认证
 * - 权限验证
 * - 个人信息展示
 * - 多语言切换
 * - 锁屏功能
 * - 搜索历史管理
 * - 路由权限控制
 *
 * ## 持久化
 *
 * - 使用 localStorage 存储
 * - 存储键：sys-v{version}-user
 * - 登出时自动清理
 *
 * @module store/modules/user.store
 * @author FastapiAdmin Team
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { LanguageEnum } from "@/enums/appEnum";
import { router } from "@/router";
import { useSettingsStore } from "./setting.store";
import { useWorktabStore } from "./worktab.store";
import { useMenuStore } from "./menu.store";
import { AppRouteRecord } from "@/types/router";
import { setPageTitle } from "@/utils/navigation/router";
import { resetRouterState } from "@/router/guards/beforeEach";
import { StorageConfig } from "@/utils/storage/storage-config";
import AuthAPI from "@/api/module_system/auth";
import UserAPI from "@/api/module_system/user";
import type { MenuTable } from "@/api/module_system/menu";
import { Auth } from "@/utils/auth";
import { ResultEnum } from "@/enums/api/result.enum";
import { ElNotification } from "element-plus";
import { store, useTagsViewStore, usePermissionStore, useDictStore } from "@/store";
import type { UserInfo } from "@/api/module_system/user";

/** {@link useUserStore} 的 `logout` 可选参数 */
export interface LogoutOptions {
  /**
   * 为 false 时仅清理状态，不跳转登录（由调用方自行 next/router，如锁屏页 replace）
   * @default true
   */
  navigate?: boolean;
}

/**
 * 用户状态管理
 * 管理用户登录状态、个人信息、语言设置、搜索历史、锁屏状态等
 */
export const useUserStore = defineStore(
  "userStore",
  () => {
    // 语言设置
    const language = ref(LanguageEnum.ZH);
    // 登录状态
    const isLogin = ref(false);
    // 锁屏状态
    const isLock = ref(false);
    // 锁屏密码
    const lockPassword = ref("");
    // 用户信息
    const info = ref<Partial<UserInfo>>({});
    // 搜索历史记录
    const searchHistory = ref<AppRouteRecord[]>([]);
    // 访问令牌
    const accessToken = ref("");
    // 刷新令牌
    const refreshToken = ref("");
    // 路由列表
    const routeList = ref<MenuTable[]>([]);
    // 权限列表
    const prems = ref<string[]>([]);
    // 是否已获取路由
    const hasGetRoute = ref(false);
    // 记住我状态
    const rememberMe = ref(Auth.getRememberMe());
    // 计算属性：基础用户信息（兼容 web 原有结构）
    const basicInfo = computed(() => info.value as any);
    // 计算属性：获取设置状态
    const getSettingState = computed(() => useSettingsStore().$state);
    // 计算属性：获取工作台状态
    const getWorktabState = computed(() => useWorktabStore().$state);
    // 计算属性：获取基础信息（兼容 web 项目）
    const getBasicInfo = computed(() => info.value as any);
    // 计算属性：获取路由列表
    const getRouteList = computed(() => routeList.value);
    // 计算属性：获取权限列表
    const getPerms = computed(() => prems.value);
    // 计算属性：是否已获取路由
    const getHasGetRoute = computed(() => hasGetRoute.value);

    /**
     * 设置用户信息
     * @param newInfo 新的用户信息
     */
    const setUserInfo = (newInfo: UserInfo | UserInfo) => {
      info.value = newInfo;
      // 设置用户信息后自动更新权限
      setPermissions([]);
    };

    /**
     * 设置登录状态
     * @param status 登录状态
     */
    const setLoginStatus = (status: boolean) => {
      isLogin.value = status;
    };

    /**
     * 设置语言
     * @param lang 语言枚举值
     */
    const setLanguage = (lang: LanguageEnum) => {
      setPageTitle(router.currentRoute.value);
      language.value = lang;
    };

    /**
     * 设置搜索历史
     * @param list 搜索历史列表
     */
    const setSearchHistory = (list: AppRouteRecord[]) => {
      searchHistory.value = list;
    };

    /**
     * 设置锁屏状态
     * @param status 锁屏状态
     */
    const setLockStatus = (status: boolean) => {
      isLock.value = status;
    };

    /**
     * 设置锁屏密码
     * @param password 锁屏密码
     */
    const setLockPassword = (password: string) => {
      lockPassword.value = password;
    };

    /**
     * 设置令牌
     * @param newAccessToken 访问令牌
     * @param newRefreshToken 刷新令牌（可选）
     */
    const setToken = (newAccessToken: string, newRefreshToken?: string) => {
      accessToken.value = newAccessToken;
      if (newRefreshToken) {
        refreshToken.value = newRefreshToken;
      }
    };

    /**
     * 检查并清理工作台标签页
     * 如果不是同一用户登录，清空工作台标签页
     * 应在登录成功后调用
     */
    const checkAndClearWorktabs = () => {
      const lastUserId = localStorage.getItem(StorageConfig.LAST_USER_ID_KEY);
      const currentUserId = (info.value as any).id || (info.value as any).user_id;

      // 无法获取当前用户 ID，跳过检查
      if (!currentUserId) return;

      // 首次登录或缓存已清除，保留现有标签页
      if (!lastUserId) {
        return;
      }

      // 不同用户登录，清空工作台标签页
      if (String(currentUserId) !== lastUserId) {
        const worktabStore = useWorktabStore();
        worktabStore.opened = [];
        worktabStore.keepAliveExclude = [];
      }

      // 清除临时存储
      localStorage.removeItem(StorageConfig.LAST_USER_ID_KEY);
    };

    /**
     * 获取用户信息
     */
    async function getUserInfo() {
      try {
        const response = await UserAPI.getCurrentUserInfo();
        const data = response.data.data;
        const menus: MenuTable[] = data?.menus || [];
        delete data?.menus;
        info.value = { ...info.value, ...data } as Partial<UserInfo>;
        setRoute(menus);
      } catch (error) {
        console.error("获取用户信息失败:", error);
        throw error;
      }
    }

    /**
     * 设置头像
     */
    function setAvatar(avatar: string) {
      info.value = { ...info.value, avatar };
    }

    /**
     * 设置路由
     */
    function setRoute(routers: MenuTable[]) {
      routeList.value = routers;
      hasGetRoute.value = true;
      setPermissions(routers);
    }

    /**
     * 设置权限
     */
    function setPermissions(menus: MenuTable[]) {
      prems.value = [];
      if (!info.value.roles) return;

      const roleMenus = info.value.roles
        .filter((role) => role.menus && role.menus.length > 0)
        .flatMap((role) => role.menus)
        .filter((menu): menu is MenuTable => menu !== undefined);

      const allMenus = [...menus, ...roleMenus];

      const permissionSet = new Set<string>();
      const collect = (items: MenuTable[]) => {
        items.forEach((item) => {
          if (item.permission) {
            permissionSet.add(item.permission);
          }
          if (item.children && item.children.length > 0) {
            collect(item.children.filter((child): child is MenuTable => child !== undefined));
          }
        });
      };

      collect(allMenus);
      prems.value = Array.from(permissionSet);
    }

    /**
     * 登录
     */
    async function login(loginForm: any) {
      const response = await AuthAPI.login(loginForm);
      const data = response.data.data;
      if (response.data.code === ResultEnum.SUCCESS) {
        ElNotification({
          title: "通知",
          message: response.data.msg,
          type: "success",
        });
      }
      rememberMe.value = loginForm.remember;
      Auth.setTokens(data.access_token, data.refresh_token, rememberMe.value);
      setToken(data.access_token, data.refresh_token);
      setLoginStatus(true);
      await getUserInfo();
    }

    /**
     * 登出：有 token 时请求后端；统一清理状态；默认跳转登录页并带 redirect
     */
    async function logout(options?: LogoutOptions) {
      const shouldNavigate = options?.navigate !== false;

      const currentUserId = (info.value as any).id || (info.value as any).user_id;
      if (currentUserId) {
        localStorage.setItem(StorageConfig.LAST_USER_ID_KEY, String(currentUserId));
      }

      let apiError: unknown;
      const token = Auth.getAccessToken();
      if (token) {
        try {
          const response = await AuthAPI.logout({ token });
          if (response.data.code === ResultEnum.SUCCESS) {
            ElNotification({
              title: "通知",
              message: response.data.msg,
              type: "success",
            });
          }
        } catch (e) {
          apiError = e;
        }
      }

      resetAllState();
      sessionStorage.removeItem("iframeRoutes");
      useMenuStore().setHomePath("");
      // 与 RouteRegistry 并行：立即清理 permissionStore 中的动态路由标记与实例，避免仅依赖延迟 reset 时侧栏/守卫状态不一致
      usePermissionStore(store).resetRouter();
      resetRouterState(500);

      if (shouldNavigate) {
        const currentRoute = router.currentRoute.value;
        const redirect = currentRoute.path !== "/login" ? currentRoute.fullPath : undefined;
        await router.push({
          name: "Login",
          query: redirect ? { redirect } : undefined,
        });
      }

      if (apiError) {
        throw apiError;
      }
    }

    /**
     * 重置所有状态
     */
    function resetAllState() {
      Auth.clearAuth();
      info.value = {};
      routeList.value = [];
      hasGetRoute.value = false;
      isLogin.value = false;
      isLock.value = false;
      lockPassword.value = "";
      accessToken.value = "";
      refreshToken.value = "";
      prems.value = [];
    }

    /**
     * 清空用户信息
     */
    function clearUserInfo() {
      info.value = {};
      routeList.value = [];
      hasGetRoute.value = false;
    }

    /**
     * 刷新token
     */
    function refreshTokenFn() {
      const currentRefreshToken = Auth.getRefreshToken();

      if (!currentRefreshToken) {
        return Promise.reject(new Error("没有有效的刷新令牌"));
      }

      return new Promise<void>((resolve, reject) => {
        AuthAPI.refreshToken({ refresh_token: currentRefreshToken })
          .then((response: any) => {
            const data = response.data.data;
            // 更新令牌，保持当前记住我状态
            Auth.setTokens(data.access_token, data.refresh_token, Auth.getRememberMe());
            setToken(data.access_token, data.refresh_token);
            resolve();
          })
          .catch((error: any) => {
            reject(error);
          });
      });
    }

    /**
     * 完全重置所有状态（包括路由、标签页、字典等）
     */
    function fullResetAllState() {
      // 重置用户状态
      Auth.clearAuth();
      // 重置用户信息
      clearUserInfo();
      // 重置路由
      usePermissionStore(store).resetRouter();
      // 清除标签视图
      useTagsViewStore().delAllViews();
      // 重置字典
      useDictStore(store).clearDictData();

      return Promise.resolve();
    }

    return {
      language,
      isLogin,
      isLock,
      lockPassword,
      info,
      searchHistory,
      accessToken,
      routeList,
      prems,
      hasGetRoute,
      rememberMe,
      getUserInfo,
      getSettingState,
      getWorktabState,
      basicInfo,
      getBasicInfo,
      getRouteList,
      getPerms,
      getHasGetRoute,
      setUserInfo,
      setLoginStatus,
      setLanguage,
      setSearchHistory,
      setLockStatus,
      setLockPassword,
      setToken,
      setAvatar,
      setRoute,
      setPermissions,
      login,
      logout,
      checkAndClearWorktabs,
      clearUserInfo,
      refreshTokenFn,
      resetAllState,
      fullResetAllState,
    };
  },
  {
    persist: {
      key: "user",
      storage: localStorage,
    },
  }
);

export function useUserStoreHook() {
  return useUserStore(store);
}
