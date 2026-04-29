import { store, useTagsViewStore, usePermissionStoreHook, useDictStoreHook } from "@/store";

import AuthAPI, { type LoginFormData } from "@/api/module_system/auth";
import UserAPI, { type UserInfo } from "@/api/module_system/user";
import type { MenuTable } from "@/api/module_system/menu";
import { Auth } from "@/utils/auth";
import { ResultEnum } from "@/enums";
import { defineStore } from "pinia";
import { ref } from "vue";
import { ElNotification } from "element-plus";

export const useUserStore = defineStore("user", {
  state: () => ({
    basicInfo: {} as UserInfo,
    routeList: [] as MenuTable[],
    prems: [] as string[],
    hasGetRoute: false,

    // 记住我状态
    rememberMe: ref(Auth.getRememberMe()),
  }),

  getters: {
    getBasicInfo: (state) => state.basicInfo,
    getRouteList: (state) => state.routeList,
    getPerms: (state) => state.prems,
    getHasGetRoute: (state) => state.hasGetRoute,
  },

  actions: {
    // 获取用户信息
    async getUserInfo() {
      const response = await UserAPI.getCurrentUserInfo();
      const routers: MenuTable[] = response.data.data.menus || [];
      delete response.data.data.menus;
      this.basicInfo = { ...this.basicInfo, ...response.data.data };
      // 然后设置路由信息
      this.setRoute(routers);
    },

    // 设置用户信息
    setUserInfo(info: UserInfo) {
      this.basicInfo = info;
      // 设置用户信息后自动更新权限
      this.setPermissions([]);
    },

    // 设置路由
    setRoute(routers: MenuTable[]) {
      this.routeList = routers;
      this.hasGetRoute = true;
      // 设置路由后自动更新权限
      this.setPermissions(routers);
    },

    setPermissions(menus: MenuTable[]) {
      this.prems = []; // 先清空现有权限

      // 确保 basicInfo.roles 存在，避免空值错误
      if (!this.basicInfo.roles) {
        return;
      }

      // 合并所有角色的菜单列表，使用数组扁平化方法简化代码并过滤undefined
      const roleMenus = this.basicInfo.roles
        .filter((role) => role.menus && role.menus.length > 0)
        .flatMap((role) => role.menus)
        .filter((menu): menu is MenuTable => menu !== undefined);

      // 合并传入的菜单和角色菜单
      const allMenus = [...menus, ...roleMenus];

      const permissionSet = new Set<string>();
      const collect = (items: MenuTable[]) => {
        items.forEach((item) => {
          // 收集当前菜单的权限
          if (item.permission) {
            permissionSet.add(item.permission);
          }

          // 递归收集子菜单的权限，确保子菜单不包含undefined
          if (item.children && item.children.length > 0) {
            collect(item.children.filter((child): child is MenuTable => child !== undefined));
          }
        });
      };

      // 收集所有权限
      collect(allMenus);
      this.prems = Array.from(permissionSet);
    },
    setAvatar(avatar: string) {
      this.basicInfo = { ...this.basicInfo, avatar };
    },
    clearUserInfo() {
      this.basicInfo = {};
      this.routeList = [];
      this.hasGetRoute = false;
    },

    // 登录
    async login(LoginFormData: LoginFormData) {
      const response = await AuthAPI.login(LoginFormData);
      if (response.data.code === ResultEnum.SUCCESS) {
        ElNotification({
          title: "通知",
          message: response.data.msg,
          type: "success",
        });
      }
      this.rememberMe = LoginFormData.remember;
      Auth.setTokens(
        response.data.data.access_token,
        response.data.data.refresh_token,
        this.rememberMe
      );
    },

    // 登出
    async logout() {
      const response = await AuthAPI.logout({ token: Auth.getAccessToken() });
      if (response.data.code === ResultEnum.SUCCESS) {
        ElNotification({
          title: "通知",
          message: response.data.msg,
          type: "success",
        });
      }
      this.resetAllState();
    },

    // 重置所有状态
    resetAllState() {
      // 重置用户状态
      Auth.clearAuth();
      // 重置用户信息
      this.clearUserInfo();
      // 重置路由
      usePermissionStoreHook().resetRouter();
      // 清除标签视图
      useTagsViewStore().delAllViews();
      // 重置字典
      useDictStoreHook().clearDictData();

      return Promise.resolve();
    },

    // 刷新token
    refreshToken() {
      const refreshToken = Auth.getRefreshToken();

      if (!refreshToken) {
        return Promise.reject(new Error("没有有效的刷新令牌"));
      }

      return new Promise<void>((resolve, reject) => {
        AuthAPI.refreshToken({ refresh_token: refreshToken })
          .then((response) => {
            // 更新令牌，保持当前记住我状态
            Auth.setTokens(
              response.data.data.access_token,
              response.data.data.refresh_token,
              Auth.getRememberMe()
            );
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },

  persist: true,
});

/**
 * 在组件外部使用UserStore的钩子函数
 * @see https://pinia.vuejs.org/core-concepts/outside-component-usage.html
 */
export function useUserStoreHook() {
  return useUserStore(store);
}
