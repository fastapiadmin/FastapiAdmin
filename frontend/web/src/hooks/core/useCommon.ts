/**
 * 通用页面能力：首页路径、触发整页刷新（settings）、主滚动容器滚动。
 */

import { computed } from "vue";
import { useMenuStore, useSettingsStore } from "@stores";

export function useCommon() {
  const menuStore = useMenuStore();
  const settingStore = useSettingsStore();

  const homePath = computed(() => menuStore.getHomePath());

  /** 触发 `ArtPageContent` 级重建（与布局 settings 联动） */
  const refresh = () => {
    settingStore.reload();
  };

  /** 主内容区滚动容器（顶栏、标签页固定，仅此处纵向滚动） */
  const getMainScrollEl = (): HTMLElement | null =>
    document.getElementById("app-scroll-main") ?? document.getElementById("app-main");

  const scrollToTop = () => {
    const scrollContainer = getMainScrollEl();
    if (scrollContainer) {
      scrollContainer.scrollTop = 0;
    }
  };

  const smoothScrollToTop = () => {
    const scrollContainer = getMainScrollEl();
    if (scrollContainer) {
      scrollContainer.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }
  };

  const scrollTo = (top: number, smooth: boolean = false) => {
    const scrollContainer = getMainScrollEl();
    if (scrollContainer) {
      scrollContainer.scrollTo({
        top,
        behavior: smooth ? "smooth" : "auto",
      });
    }
  };

  return {
    homePath,
    refresh,
    scrollTo,
    scrollToTop,
    smoothScrollToTop,
  };
}
