/**
 * 认证重定向工具模块
 *
 * 提供认证失效时的统一重定向处理功能
 *
 * ## 主要功能
 *
 * - 登录页跳转（自动带上 redirect 参数）
 * - 并发请求合并，避免重复跳转
 * - 会话状态清理
 *
 * @module utils/authRedirect
 */

import { router } from "@/router";
import { useUserStore } from "@/store/modules/user.store";
import { ElMessage, ElNotification } from "element-plus";

/**
 * 登录页跳转进行中标志
 *
 * 用于合并并发的登录跳转请求，避免重复通知与重复路由跳转
 */
let redirectToLoginInFlight: Promise<void> | null = null;

/**
 * 认证失效或需重新登录时跳转登录页
 *
 * 清空本地会话并带上 redirect 参数，支持并发调用合并
 *
 * @param {string} [message="请重新登录"] - 提示消息
 * @returns {Promise<void>} 跳转完成的 Promise
 *
 * @example
 * ```typescript
 * import { redirectToLogin } from '@/utils/authRedirect';
 *
 * // 在需要登录的地方调用
 * redirectToLogin('登录已过期，请重新登录');
 * ```
 */
export async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  // 如果已有跳转请求进行中，直接返回该请求的 Promise
  if (redirectToLoginInFlight) {
    return redirectToLoginInFlight;
  }

  // 创建新的跳转请求
  redirectToLoginInFlight = (async () => {
    try {
      // 显示提示通知
      ElNotification({
        title: "提示",
        message,
        type: "warning",
        duration: 3000,
      });

      // 重置用户状态
      await useUserStore().resetAllState();

      // 获取当前路径作为 redirect 参数
      const currentPath = router.currentRoute.value.fullPath;

      // 跳转到登录页
      await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
    } catch (error: any) {
      // 处理跳转过程中的错误
      ElMessage.error(error?.message ?? String(error));
    } finally {
      // 重置跳转进行中标志
      redirectToLoginInFlight = null;
    }
  })();

  return redirectToLoginInFlight;
}
