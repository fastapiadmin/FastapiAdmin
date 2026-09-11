/**
 * 通用页面能力：首页路径、触发整页刷新（settings）、主滚动容器滚动。
 */

import { computed } from "vue";
import { useMenuStore, useSettingsStore } from "@stores";

/**
 * 主内容区滚动容器。
 *
 * 真正的滚动元素是 `#app-content`（`_layouts.scss` 里带 `overflow: auto`，
 * 靠 `flex: 1` + `min-height: 0` 被限制在视口剩余高度内）。
 * 注意 `#app-scroll-main`（`.layout-content`）只是限宽居中的包装层，
 * 自身没有 `overflow`，对它设 `scrollTop` 是空操作；
 * 这里不能改用 `.el-scrollbar__wrap` 之类的第三方类名定位——
 * 文档里第一个命中的是左侧菜单的滚动条。
 */
export const getMainScrollEl = (): HTMLElement | null =>
  document.getElementById("app-content") ?? document.getElementById("app-main");

export function useCommon() {
  const menuStore = useMenuStore();
  const settingStore = useSettingsStore();

  const homePath = computed(() => menuStore.getHomePath());

  /** 触发 `FaPageContent` 级重建（与布局 settings 联动） */
  const refresh = () => {
    settingStore.reload();
  };

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
