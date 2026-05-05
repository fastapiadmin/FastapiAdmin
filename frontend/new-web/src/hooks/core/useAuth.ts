/**
 * useAuth - 权限验证管理
 *
 * 提供统一的权限验证功能，支持前端和后端两种权限模式。
 * 用于控制页面按钮、操作等功能的显示和访问权限。
 *
 * ## 主要功能
 *
 * 1. 权限检查 - 检查用户是否拥有指定的权限标识
 * 2. 双模式支持 - 自动适配前端模式和后端模式的权限验证
 * 3. 前端模式 - 从用户信息中获取按钮权限列表（如 ['add', 'edit', 'delete']）
 * 4. 后端模式 - 从路由 meta 配置中获取权限列表（如 [{ authMark: 'add' }]）
 *
 * ## 使用示例
 *
 * ```typescript
 * const { hasAuth } = useAuth()
 *
 * // 检查是否有新增权限
 * if (hasAuth('add')) {
 *   // 显示新增按钮
 * }
 *
 * // 在模板中使用
 * <el-button v-if="hasAuth('edit')">编辑</el-button>
 * <el-button v-if="hasAuth('delete')">删除</el-button>
 * ```
 *
 * @module useAuth
 * @author FastapiAdmin Team
 */

import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useUserStore } from "@/store/modules/user.store";
import { useAppMode } from "@/hooks/core/useAppMode";
import type { AppRouteRecord } from "@/types/router";
import { ROLE_ROOT } from "@/constants";

type AuthItem = NonNullable<AppRouteRecord["meta"]["authList"]>[number];

export const useAuth = () => {
  const route = useRoute();
  const userStore = useUserStore();
  const { isFrontendMode } = useAppMode();
  const { info } = storeToRefs(userStore);

  // 前端按钮权限（例如：['add', 'edit']）
  const frontendAuthList = info.value?.permissions ?? [];

  // 后端路由 meta 配置的权限列表（例如：[{ authMark: 'add' }]）
  const backendAuthList: AuthItem[] = Array.isArray(route.meta.authList)
    ? (route.meta.authList as AuthItem[])
    : [];

  /**
   * 检查是否拥有某权限标识（与 v-hasPerm / 表格内 ArtButtonMore 全码一致）
   * @param auth 权限标识（多为后端菜单 permission 全码，如 module_system:role:update）
   */
  const hasAuth = (auth: string): boolean => {
    if (!auth) return true;

    const userPrems = userStore.prems;
    const roles = userStore.basicInfo?.roles as { code?: string }[] | undefined;

    // 与 directives/permission hasPerm 一致：超级管理员、通配
    if (roles?.some((r) => r.code === ROLE_ROOT)) return true;
    if (userPrems.includes("*:*:*")) return true;

    /** 登录后由菜单树汇总的全局权限码（与 v-hasPerm 同源） */
    if (userPrems.includes(auth)) return true;

    // 前端模式：兼容 info.permissions
    if (isFrontendMode.value) {
      return frontendAuthList.includes(auth);
    }

    // 后端模式：当前路由 meta 短标识（与 v-auth 一致）
    return backendAuthList.some((item) => item?.authMark === auth);
  };

  return {
    hasAuth,
  };
};
