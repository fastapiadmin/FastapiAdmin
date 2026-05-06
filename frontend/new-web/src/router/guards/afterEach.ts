import { nextTick } from "vue";
import { useSettingsStore } from "@/store/modules/setting.store";
import { Router } from "vue-router";
import { NProgress } from "@/utils/ui";
import { useCommon } from "@/hooks/core/useCommon";
import { loadingService } from "@/utils/ui";
import { getPendingLoading, resetPendingLoading } from "./beforeEach";

/** 路由全局后置守卫 */
export function setupAfterEachGuard(router: Router) {
  const { scrollToTop } = useCommon();

  router.afterEach(() => {
    scrollToTop();

    // 关闭进度条
    const settingStore = useSettingsStore();
    if (settingStore.showNprogress) {
      NProgress.done();
      // 确保进度条完全移除，避免残影
      setTimeout(() => {
        NProgress.remove();
      }, 600);
    }

    // 关闭 loading 效果
    if (getPendingLoading()) {
      nextTick(() => {
        loadingService.hideLoading();
        resetPendingLoading();
      });
    }
  });
}
