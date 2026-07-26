/**
 * useAuth - 权限验证管理
 *
 * 提供统一的权限验证功能。内部委托 checkPerm 进行核心权限判断，
 * 额外兼容路由 meta 短标识（authList）后端模式。
 * 仅由 v-hasPerm 指令内部使用。
 *
 * @module useAuth
 */
import { getCurrentInstance } from "vue";
import { useRoute } from "vue-router";
import { checkPerm } from "@/utils/checkPerm";
import type { AppRouteRecord } from "@/types/router";

type AuthItem = NonNullable<AppRouteRecord["meta"]["authList"]>[number];

export const useAuth = () => {
  // 有 setup 上下文时才获取路由（v-hasPerm 指令 mounted 钩子中无 setup 上下文）
  const route = getCurrentInstance() ? useRoute() : undefined;

  // 后端路由 meta 配置的权限列表（例如：[{ authMark: 'add' }]）
  const backendAuthList: AuthItem[] =
    route && Array.isArray(route.meta.authList) ? (route.meta.authList as AuthItem[]) : [];

  /**
   * 检查是否拥有某权限标识（供 v-hasPerm 指令使用）
   * @param auth 权限标识或权限标识数组（数组时任一匹配即放行）
   */
  const hasAuth = (auth: string | string[]): boolean => {
    if (!auth || (Array.isArray(auth) && auth.length === 0)) return true;

    const perms = Array.isArray(auth) ? auth : [auth];

    // 核心检查：superuser / ROLE_ROOT / 通配符 / prems
    if (perms.some((p) => checkPerm(p))) return true;

    // 后端模式：当前路由 meta 短标识
    return perms.some((p) => backendAuthList.some((item) => item?.authMark === p));
  };

  return {
    hasAuth,
  };
};
