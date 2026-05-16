/**
 * 路由后置守卫：滚动置顶、结束 NProgress、关闭 beforeEach 开启的全局 loading。
 */
import { nextTick } from "vue";
import { useSettingsStore } from "@stores";
import { Router } from "vue-router";
import { useCommon } from "@/hooks/core/useCommon";
import { NProgress, loadingService } from "@utils";

/** 防止重复注册 afterEach（与 beforeEach 同理） */
let afterEachGuardRegistered = false;

export async function setupAfterEachGuard(router: Router) {
  if (afterEachGuardRegistered) {
    if (import.meta.env.DEV) {
      console.warn("[Router] setupAfterEachGuard 已注册，跳过重复调用");
    }
    return;
  }
  afterEachGuardRegistered = true;

  const { scrollToTop } = useCommon();

  // 延迟加载 beforeEach 中导出的守卫状态函数，避免静态循环依赖
  const { getPendingLoading, resetPendingLoading } = await import("./beforeEach");

  router.afterEach(() => {
    scrollToTop();

    const settingStore = useSettingsStore();
    if (settingStore.showNprogress) {
      NProgress.done();
      setTimeout(() => {
        NProgress.remove();
      }, 600);
    }

    if (getPendingLoading()) {
      nextTick(() => {
        loadingService.hideLoading();
        resetPendingLoading();
      });
    }
  });
}
