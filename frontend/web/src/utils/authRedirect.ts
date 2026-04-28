import router from '@/router';
import { useUserStoreHook } from '@/store/modules/user.store';

/** 登录页跳转进行中，合并并发调用，避免重复通知与重复路由 */
let redirectToLoginInFlight: Promise<void> | null = null;

/**
 * 认证失效或需重新登录时跳转登录页：清空本地会话并带上 redirect。
 * 与 HTTP 拦截器、改密后重登等场景共用；并发只执行一次。
 */
export async function redirectToLogin(message: string = '请重新登录'): Promise<void> {
  if (redirectToLoginInFlight) {
    return redirectToLoginInFlight;
  }
  redirectToLoginInFlight = (async () => {
    try {
      ElNotification({
        title: '提示',
        message,
        type: 'warning',
        duration: 3000,
      });

      await useUserStoreHook().resetAllState();

      const currentPath = router.currentRoute.value.fullPath;
      await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
    } catch (error: any) {
      ElMessage.error(error?.message ?? String(error));
    } finally {
      redirectToLoginInFlight = null;
    }
  })();
  return redirectToLoginInFlight;
}
