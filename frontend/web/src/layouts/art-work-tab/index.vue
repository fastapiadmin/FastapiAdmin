<!-- 三种模式与 art-design-pro 一致：tab-default / tab-card / tab-google（参考 art-design-pro/src/components/core/layouts/art-work-tab） -->
<template>
  <div
    v-if="showWorkTab"
    class="worktab-tags-shell box-border w-full select-none"
    :class="[
      /** 三种模式统一底边线；谷歌模式底边与标签贴合，默认/卡片需要与底边留出间距（避免重合） */
      'border-b border-[var(--art-card-border)]',
      tabStyle === 'tab-google' ? 'worktab-tags-shell--google pt-1 pb-0' : 'py-1',
    ]"
  >
    <div
      class="worktab-tags-bar flex items-stretch gap-0 w-full min-h-8"
      :class="chromeTabStrip ? 'worktab-tags-bar--google' : ''"
    >
      <button
        v-if="tabOverflow"
        type="button"
        class="worktab-bar-btn worktab-bar-cell worktab-bar-cell--sep-r"
        :title="t('worktab.scrollLeft')"
        @click="scrollTabs(SCROLL_STEP)"
      >
        <ArtSvgIcon icon="ri:arrow-left-double-line" class="text-lg text-current" />
      </button>

      <div
        class="worktab-scroll-wrap flex flex-1 min-w-0 items-center overflow-hidden"
        ref="scrollRef"
      >
        <ul
          class="float-left whitespace-nowrap !bg-transparent flex"
          :class="[chromeTabStrip ? 'pl-1' : '']"
          ref="tabsRef"
          :style="{
            transform: `translateX(${scrollState.translateX}px)`,
            transition: `${scrollState.transition}`,
          }"
        >
          <li
            class="worktab-tab art-card-xs inline-flex flex-cc h-8 mr-1.5 text-xs c-p hover:text-theme group"
            :class="[
              item.path === activeTab
                ? chromeTabStrip
                  ? 'activ-tab'
                  : 'activ-tab !text-theme'
                : chromeTabStrip
                  ? ''
                  : 'text-g-600 dark:text-g-800',
              isCardTabs ? 'worktab-tab--card' : '',
              chromeTabStrip ? 'google-tab relative !h-8 !leading-8 !border-none' : '',
            ]"
            :style="
              tabStyle === 'tab-google'
                ? {
                    padding: item.fixedTab ? '0 10px' : '0 8px 0 12px',
                    borderRadius: 'calc(var(--custom-radius) / 2.5 + 4px)',
                  }
                : {
                    padding: item.fixedTab ? '0 10px' : '0 8px 0 12px',
                    borderRadius: 'calc(var(--custom-radius) / 2.5 + 2px)',
                  }
            "
            v-for="(item, index) in list"
            :key="item.path"
            :ref="item.path"
            :id="`scroll-li-${index}`"
            @click="clickTab(item)"
            @click.middle.prevent="onMiddleClickClose(item)"
            @contextmenu.prevent="(e: MouseEvent) => showMenu(e, item.path)"
          >
            <button
              type="button"
              class="worktab-star focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--el-color-primary)] focus-visible:ring-offset-1 rounded"
              :class="{ 'worktab-star--on': isQuickLinkBookmarked(item) }"
              :title="
                isQuickLinkBookmarked(item) ? t('worktab.bookmarkRemove') : t('worktab.bookmarkAdd')
              "
              @click.prevent.stop="toggleQuickBookmark(item)"
            >
              <ArtSvgIcon
                :icon="isQuickLinkBookmarked(item) ? 'ri:star-fill' : 'ri:star-line'"
                class="text-sm"
              />
            </button>
            <ArtSvgIcon
              v-show="item.icon"
              :icon="item.icon"
              class="text-base mr-1 shrink-0 group-hover:text-theme"
              :class="[
                item.path === activeTab ? 'text-theme' : '',
                chromeTabStrip ? 'google-tab-route-icon' : 'text-g-600',
              ]"
            />
            {{ item.customTitle || formatMenuTitle(item.title) }}
            <ArtSvgIcon
              v-if="item.fixedTab"
              icon="ri:pushpin-2-fill"
              class="worktab-pin shrink-0 text-sm ml-0.5"
            />
            <span
              v-if="list.length > 1 && !item.fixedTab"
              class="worktab-close inline-flex flex-cc relative ml-0.5 rounded-full p-1 tad-200"
              @click.stop="closeWorktab('current', item.path)"
            >
              <ArtSvgIcon icon="ri:close-large-fill" class="text-[10px]" />
            </span>
            <div
              v-if="chromeTabStrip && showGoogleTabDivider(index)"
              class="worktab-google-divider"
              aria-hidden="true"
            />
          </li>
        </ul>
      </div>

      <!-- 竖线分格：用 scoped CSS 画线；divide-x 会被 .worktab-bar-btn { border:none } 盖掉 -->
      <div class="worktab-toolbar-end flex shrink-0 items-stretch" aria-label="tab-toolbar-actions">
        <button
          v-if="tabOverflow"
          type="button"
          class="worktab-bar-btn worktab-bar-cell"
          :title="t('worktab.scrollRight')"
          @click="scrollTabs(-SCROLL_STEP)"
        >
          <ArtSvgIcon icon="ri:arrow-right-double-line" class="text-lg text-current" />
        </button>

        <button
          type="button"
          class="worktab-bar-btn worktab-bar-cell"
          :title="t('navbar.refreshCache')"
          @click="handleRefreshCache"
        >
          <ArtSvgIcon icon="ri:loop-right-line" class="text-base text-current" />
        </button>

        <button
          type="button"
          class="worktab-bar-btn worktab-bar-cell"
          :title="t('worktab.menuMore')"
          @click="(e: MouseEvent) => showMenu(e, activeTab)"
        >
          <ArtSvgIcon icon="ri:apps-2-line" class="text-base text-current" />
        </button>
      </div>
    </div>

    <ArtMenuRight
      ref="menuRef"
      :menu-items="menuItems"
      :menu-width="140"
      :border-radius="10"
      @select="handleSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, nextTick, onUnmounted } from "vue";
import { LocationQueryRaw, useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";

import { ElMessage } from "element-plus";
import { refreshAppCaches } from "@stores";
import { useWorktabStore } from "@stores/modules/worktab.store";
import { useUserStore } from "@stores/modules/user.store";
import { formatMenuTitle } from "@utils/navigation";
import { useSettingsStore } from "@stores/modules/setting.store";
import { MenuItemType } from "@/components/Core/others/art-menu-right/index.vue";
import { useCommon } from "@/hooks/core/useCommon";
import { quickStartManager } from "@utils/common";
import { WorkTab } from "@/types";

defineOptions({ name: "ArtWorkTab" });

// 类型定义
interface ScrollState {
  translateX: number;
  transition: string;
}

interface TouchState {
  startX: number;
  currentX: number;
}

type TabCloseType = "current" | "left" | "right" | "other" | "all";

// 基础设置
const { t } = useI18n();
const store = useWorktabStore();
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const { currentRoute } = router;
const settingStore = useSettingsStore();
const { tabStyle, showWorkTab } = storeToRefs(settingStore);

/** tab-google：Chrome 顶栏标签（tab-default / tab-card 走原有样式） */
const chromeTabStrip = computed(() => tabStyle.value === "tab-google");
const isCardTabs = computed(() => tabStyle.value === "tab-card");

// DOM 引用
const scrollRef = ref<HTMLElement | null>(null);
const tabsRef = ref<HTMLElement | null>(null);
const menuRef = ref();

// 状态管理
const scrollState = ref<ScrollState>({
  translateX: 0,
  transition: "",
});

const touchState = ref<TouchState>({
  startX: 0,
  currentX: 0,
});

const clickedPath = ref("");

/** 标签总宽度超过可视区时才显示左右滚动按钮（与常见控制台一致） */
const tabOverflow = ref(false);

function measureTabOverflow(): void {
  requestAnimationFrame(() => {
    const wrap = scrollRef.value;
    const tabs = tabsRef.value;
    if (!wrap || !tabs) {
      tabOverflow.value = false;
      return;
    }
    tabOverflow.value = tabs.scrollWidth > wrap.clientWidth + 1;
  });
}

let tabOverflowResizeObserver: ResizeObserver | null = null;

function setupTabOverflowObserver(): void {
  teardownTabOverflowObserver();
  if (typeof ResizeObserver === "undefined") return;
  tabOverflowResizeObserver = new ResizeObserver(() => measureTabOverflow());
  if (scrollRef.value) tabOverflowResizeObserver.observe(scrollRef.value);
  if (tabsRef.value) tabOverflowResizeObserver.observe(tabsRef.value);
}

function teardownTabOverflowObserver(): void {
  tabOverflowResizeObserver?.disconnect();
  tabOverflowResizeObserver = null;
}

// 计算属性
const list = computed(() => store.opened);
const activeTab = computed(() => currentRoute.value.path);
const activeTabIndex = computed(() => list.value.findIndex((tab) => tab.path === activeTab.value));

// 右键菜单逻辑
const useContextMenu = () => {
  const getClickedTabInfo = () => {
    const clickedIndex = list.value.findIndex((tab) => tab.path === clickedPath.value);
    const currentTab = list.value[clickedIndex];

    return {
      clickedIndex,
      currentTab,
      isLastTab: clickedIndex === list.value.length - 1,
      isOneTab: list.value.length === 1,
      isCurrentTab: clickedPath.value === activeTab.value,
    };
  };

  // 检查标签页是否固定
  const checkTabsFixedStatus = (clickedIndex: number) => {
    const leftTabs = list.value.slice(0, clickedIndex);
    const rightTabs = list.value.slice(clickedIndex + 1);
    const otherTabs = list.value.filter((_, index) => index !== clickedIndex);

    return {
      areAllLeftTabsFixed: leftTabs.length > 0 && leftTabs.every((tab) => tab.fixedTab),
      areAllRightTabsFixed: rightTabs.length > 0 && rightTabs.every((tab) => tab.fixedTab),
      areAllOtherTabsFixed: otherTabs.length > 0 && otherTabs.every((tab) => tab.fixedTab),
      areAllTabsFixed: list.value.every((tab) => tab.fixedTab),
    };
  };

  // 右键菜单选项
  const menuItems = computed(() => {
    const { clickedIndex, currentTab, isLastTab, isOneTab, isCurrentTab } = getClickedTabInfo();
    const fixedStatus = checkTabsFixedStatus(clickedIndex);

    return [
      {
        key: "refresh",
        label: t("worktab.btn.refresh"),
        icon: "ri:refresh-line",
        disabled: !isCurrentTab,
      },
      {
        key: "fixed",
        label: currentTab?.fixedTab ? t("worktab.btn.unfixed") : t("worktab.btn.fixed"),
        icon: "ri:pushpin-2-line",
        disabled: false,
        showLine: true,
      },
      {
        key: "current",
        label: t("worktab.btn.closeCurrent"),
        icon: "ri:close-line",
        disabled: !!currentTab?.fixedTab,
      },
      {
        key: "left",
        label: t("worktab.btn.closeLeft"),
        icon: "ri:arrow-left-s-line",
        disabled: clickedIndex === 0 || fixedStatus.areAllLeftTabsFixed,
      },
      {
        key: "right",
        label: t("worktab.btn.closeRight"),
        icon: "ri:arrow-right-s-line",
        disabled: isLastTab || fixedStatus.areAllRightTabsFixed,
      },
      {
        key: "other",
        label: t("worktab.btn.closeOther"),
        icon: "ri:close-fill",
        disabled: isOneTab || fixedStatus.areAllOtherTabsFixed,
      },
      {
        key: "all",
        label: t("worktab.btn.closeAll"),
        icon: "ri:close-circle-line",
        disabled: isOneTab || fixedStatus.areAllTabsFixed,
      },
    ];
  });

  return { menuItems };
};

// 滚动逻辑
const useScrolling = () => {
  const setTransition = () => {
    scrollState.value.transition = "transform 0.5s cubic-bezier(0.15, 0, 0.15, 1)";
    setTimeout(() => {
      scrollState.value.transition = "";
    }, 250);
  };

  const getCurrentTabElement = (): HTMLElement | null => {
    return document.getElementById(`scroll-li-${activeTabIndex.value}`);
  };

  const calculateScrollPosition = () => {
    if (!scrollRef.value || !tabsRef.value) return;

    const scrollWidth = scrollRef.value.offsetWidth;
    const ulWidth = tabsRef.value.offsetWidth;
    const curTabEl = getCurrentTabElement();

    if (!curTabEl) return;

    const { offsetLeft, clientWidth } = curTabEl;
    const curTabRight = offsetLeft + clientWidth;
    const targetLeft = scrollWidth - curTabRight;

    return {
      scrollWidth,
      ulWidth,
      offsetLeft,
      clientWidth,
      curTabRight,
      targetLeft,
    };
  };

  const autoPositionTab = () => {
    const positions = calculateScrollPosition();
    if (!positions) return;

    const { scrollWidth, ulWidth, offsetLeft, curTabRight, targetLeft } = positions;

    if (
      (offsetLeft > Math.abs(scrollState.value.translateX) && curTabRight <= scrollWidth) ||
      (scrollState.value.translateX < targetLeft && targetLeft < 0)
    ) {
      return;
    }

    requestAnimationFrame(() => {
      if (curTabRight > scrollWidth) {
        scrollState.value.translateX = Math.max(targetLeft - 6, scrollWidth - ulWidth);
      } else if (offsetLeft < Math.abs(scrollState.value.translateX)) {
        scrollState.value.translateX = -offsetLeft;
      }
    });
  };

  const adjustPositionAfterClose = () => {
    const positions = calculateScrollPosition();
    if (!positions) return;

    const { scrollWidth, ulWidth, offsetLeft, clientWidth } = positions;
    const curTabLeft = offsetLeft + clientWidth;

    requestAnimationFrame(() => {
      scrollState.value.translateX = curTabLeft > scrollWidth ? scrollWidth - ulWidth : 0;
    });
  };

  return {
    setTransition,
    autoPositionTab,
    adjustPositionAfterClose,
  };
};

// 事件处理逻辑
const useEventHandlers = () => {
  const { setTransition, adjustPositionAfterClose } = useScrolling();

  const handleWheelScroll = (event: WheelEvent) => {
    if (!scrollRef.value || !tabsRef.value) return;

    event.preventDefault();

    if (tabsRef.value.offsetWidth <= scrollRef.value.offsetWidth) return;

    const xMax = 0;
    const xMin = scrollRef.value.offsetWidth - tabsRef.value.offsetWidth;
    const delta = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;

    scrollState.value.translateX = Math.min(
      Math.max(scrollState.value.translateX - delta, xMin),
      xMax
    );
  };

  const handleTouchStart = (event: TouchEvent) => {
    touchState.value.startX = event.touches[0].clientX;
  };

  const handleTouchMove = (event: TouchEvent) => {
    if (!scrollRef.value || !tabsRef.value) return;

    touchState.value.currentX = event.touches[0].clientX;
    const deltaX = touchState.value.currentX - touchState.value.startX;
    const xMin = scrollRef.value.offsetWidth - tabsRef.value.offsetWidth;

    scrollState.value.translateX = Math.min(
      Math.max(scrollState.value.translateX + deltaX, xMin),
      0
    );
    touchState.value.startX = touchState.value.currentX;
  };

  const handleTouchEnd = () => {
    setTransition();
  };

  const setupEventListeners = () => {
    if (tabsRef.value) {
      tabsRef.value.addEventListener("wheel", handleWheelScroll, { passive: false });
      tabsRef.value.addEventListener("touchstart", handleTouchStart, { passive: true });
      tabsRef.value.addEventListener("touchmove", handleTouchMove, { passive: true });
      tabsRef.value.addEventListener("touchend", handleTouchEnd, { passive: true });
    }
  };

  const cleanupEventListeners = () => {
    if (tabsRef.value) {
      tabsRef.value.removeEventListener("wheel", handleWheelScroll);
      tabsRef.value.removeEventListener("touchstart", handleTouchStart);
      tabsRef.value.removeEventListener("touchmove", handleTouchMove);
      tabsRef.value.removeEventListener("touchend", handleTouchEnd);
    }
  };

  return {
    setupEventListeners,
    cleanupEventListeners,
    adjustPositionAfterClose,
  };
};

// 标签页操作逻辑
const useTabOperations = (adjustPositionAfterClose: () => void) => {
  const clickTab = (item: WorkTab) => {
    router.push({
      path: item.path,
      query: item.query as LocationQueryRaw,
    });
  };

  const closeWorktab = (type: TabCloseType, tabPath: string) => {
    const path = typeof tabPath === "string" ? tabPath : route.path;

    const closeActions = {
      current: () => store.removeTab(path),
      left: () => store.removeLeft(path),
      right: () => store.removeRight(path),
      other: () => store.removeOthers(path),
      all: () => store.removeAll(),
    };

    closeActions[type]?.();

    setTimeout(() => {
      adjustPositionAfterClose();
    }, 100);
  };

  const showMenu = (e: MouseEvent, path?: string) => {
    clickedPath.value = path || "";
    menuRef.value?.show(e);
    e.preventDefault();
    e.stopPropagation();
  };

  const handleSelect = (item: MenuItemType) => {
    const { key } = item;

    if (key === "refresh") {
      useCommon().refresh();
      return;
    }

    if (key === "fixed") {
      useWorktabStore().toggleFixedTab(clickedPath.value);
      return;
    }

    const activeIndex = list.value.findIndex((tab) => tab.path === activeTab.value);
    const clickedIndex = list.value.findIndex((tab) => tab.path === clickedPath.value);

    const navigationRules = {
      left: activeIndex < clickedIndex,
      right: activeIndex > clickedIndex,
      other: true,
    } as const;

    const shouldNavigate = navigationRules[key as keyof typeof navigationRules];

    if (shouldNavigate) {
      const dest = list.value.find((tab) => tab.path === clickedPath.value);
      if (dest) {
        router.push({
          path: dest.path,
          query: dest.query as LocationQueryRaw,
        });
      } else {
        router.push(clickedPath.value);
      }
    }

    closeWorktab(key as TabCloseType, clickedPath.value);
  };

  return {
    clickTab,
    closeWorktab,
    showMenu,
    handleSelect,
  };
};

// 组合所有逻辑
const { menuItems } = useContextMenu();
const { setTransition, autoPositionTab } = useScrolling();
const { setupEventListeners, cleanupEventListeners, adjustPositionAfterClose } = useEventHandlers();
const { clickTab, closeWorktab, showMenu, handleSelect } =
  useTabOperations(adjustPositionAfterClose);

/** 标签横向滚动步长（px） */
const SCROLL_STEP = 200;

/**
 * Chrome 条竖线：固定区右侧必显；其余仅在「两侧都未选中」时显示（与 Vben 类控制台一致，避免贴激活标签显得碎）
 */
function showGoogleTabDivider(index: number): boolean {
  const tabs = list.value;
  if (index <= 0 || index >= tabs.length) return false;
  const prev = tabs[index - 1];
  const cur = tabs[index];
  if (prev.fixedTab && !cur.fixedTab) return true;
  if (prev.path === activeTab.value || cur.path === activeTab.value) return false;
  return true;
}

function scrollTabs(delta: number): void {
  if (!scrollRef.value || !tabsRef.value) return;
  const xMin = scrollRef.value.offsetWidth - tabsRef.value.offsetWidth;
  const xMax = 0;
  scrollState.value.translateX = Math.min(
    Math.max(scrollState.value.translateX + delta, xMin),
    xMax
  );
  setTransition();
}

const quickLinksRevision = ref(0);
function onQuickLinksChanged(): void {
  quickLinksRevision.value++;
}

function bookmarkHref(item: WorkTab): string {
  const q = item.query as LocationQueryRaw | undefined;
  if (!q || !Object.keys(q).length) return item.path;
  const sp = new URLSearchParams();
  Object.entries(q).forEach(([k, v]) => {
    if (v === null || v === undefined) return;
    if (Array.isArray(v)) v.forEach((x) => sp.append(k, String(x)));
    else sp.set(k, String(v));
  });
  const s = sp.toString();
  return s ? `${item.path}?${s}` : item.path;
}

function isQuickLinkBookmarked(item: WorkTab): boolean {
  void quickLinksRevision.value;
  return quickStartManager.isLinkExists(bookmarkHref(item));
}

function toggleQuickBookmark(item: WorkTab): void {
  const href = bookmarkHref(item);
  const title = item.customTitle || formatMenuTitle(item.title);
  try {
    if (quickStartManager.isLinkExists(href)) {
      quickStartManager.removeQuickLinkByHref(href);
      ElMessage.success(t("worktab.bookmarkRemoved"));
    } else {
      const link = quickStartManager.createQuickLinkFromRoute(
        { ...item, title, fullPath: href, path: item.path },
        title
      );
      link.href = href;
      if (quickStartManager.addQuickLink(link)) {
        ElMessage.success(t("worktab.bookmarkAdded"));
      }
    }
  } catch (e) {
    console.error(e);
    ElMessage.error(t("worktab.bookmarkFail"));
  }
}

function onMiddleClickClose(item: WorkTab): void {
  if (!item.fixedTab && list.value.length > 1) {
    closeWorktab("current", item.path);
  }
}

async function handleRefreshCache(): Promise<void> {
  try {
    await refreshAppCaches();
    useCommon().refresh();
    ElMessage.success(t("worktab.refreshCacheDone"));
  } catch (e) {
    console.error(e);
    ElMessage.error(t("worktab.refreshCacheFail"));
  }
}

// 生命周期
onMounted(() => {
  setupEventListeners();
  quickStartManager.addListener(onQuickLinksChanged);
  autoPositionTab();
  nextTick(() => {
    measureTabOverflow();
    setupTabOverflowObserver();
  });
  window.addEventListener("resize", measureTabOverflow);
});

onUnmounted(() => {
  cleanupEventListeners();
  quickStartManager.removeListener(onQuickLinksChanged);
  teardownTabOverflowObserver();
  window.removeEventListener("resize", measureTabOverflow);
});

// 监听器
watch(tabOverflow, (overflow) => {
  if (!overflow) {
    scrollState.value.translateX = 0;
  }
});

watch(list, () => nextTick(measureTabOverflow), { deep: true });

watch(
  () => currentRoute.value,
  () => {
    setTransition();
    autoPositionTab();
    nextTick(measureTabOverflow);
  }
);

watch(
  () => userStore.language,
  () => {
    scrollState.value.translateX = 0;
    nextTick(() => {
      autoPositionTab();
      measureTabOverflow();
    });
  }
);
</script>

<style scoped>
/* 工具条：底边与内容区分界；顶边由顶部栏 border-b 承担，避免与标签条顶边双线 */
.worktab-tags-shell {
  /* 外壳 padding（py-1 / pt-1 pb-0）会让内部分割线出现上下缝隙；用变量让分割线延伸到 padding 区 */
  --worktab-shell-pad-top: 4px;
  --worktab-shell-pad-bottom: 4px;
}

/* Google 标签模式：外壳 padding + 激活块 / 主题变量（与下方 Chrome 弧角样式共用） */
.worktab-tags-shell--google {
  --worktab-shell-pad-top: 4px;
  --worktab-shell-pad-bottom: 0px;
  --worktab-google-active-bg: var(--el-fill-color-light);
  --worktab-google-tab-muted: var(--el-text-color-regular);
}

.worktab-tags-bar {
  background: var(--el-fill-color-blank);

  /* 外壳已统一提供 border-b，避免不同模式出现双线/高度不一致 */
  border: none;
}

.worktab-toolbar-end {
  position: relative;
  align-self: stretch;

  /* 让工具按钮边框（分割线）撑满外壳高度 */
  margin-top: calc(var(--worktab-shell-pad-top) * -1);
  margin-bottom: calc(var(--worktab-shell-pad-bottom) * -1);
}

/* 工具区左侧分割线：拉满到标签栏高度 */
.worktab-toolbar-end::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 1px;
  content: "";
  background: var(--el-border-color-lighter);
}

.dark .worktab-toolbar-end::before {
  background: rgb(255 255 255 / 12%);
}

/* 工具区内部按钮分割线：拉满到标签栏高度 */
.worktab-toolbar-end .worktab-bar-cell {
  position: relative;

  /* 让 hover/active 背景也覆盖到外壳 padding 区域（与左侧按钮一致的手感） */
  padding-top: var(--worktab-shell-pad-top);
  padding-bottom: var(--worktab-shell-pad-bottom);
  margin-top: calc(var(--worktab-shell-pad-top) * -1);
  margin-bottom: calc(var(--worktab-shell-pad-bottom) * -1);
}

.worktab-toolbar-end .worktab-bar-cell + .worktab-bar-cell::before {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 1px;
  content: "";
  background: var(--el-border-color-lighter);
}

.dark .worktab-toolbar-end .worktab-bar-cell + .worktab-bar-cell::before {
  background: rgb(255 255 255 / 12%);
}

/*
 * 工具区：单格无四边描边；悬停 / 按下仅在当前格矩形内铺底
 */
.worktab-tags-bar .worktab-bar-btn {
  padding: 0;
  margin: 0;
  color: var(--el-text-color-regular);
  cursor: pointer;
  background: transparent;
  border: none;
  border-radius: 0;
  transition:
    color 0.15s ease,
    background-color 0.15s ease;
}

.worktab-tags-bar .worktab-bar-cell {
  box-sizing: border-box;
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  align-self: stretch;
  justify-content: center;
  min-width: 2rem;
  padding: 0 0.5rem;
}

.worktab-tags-bar .worktab-bar-cell--sep-r {
  /* 左侧按钮分割线同样撑满外壳高度 */
  margin-top: calc(var(--worktab-shell-pad-top) * -1);
  margin-bottom: calc(var(--worktab-shell-pad-bottom) * -1);
  border-right: 1px solid var(--el-border-color-lighter);
}

.worktab-tags-bar .worktab-bar-btn:hover {
  color: var(--el-color-primary);
  background-color: color-mix(in srgb, var(--el-color-primary) 10%, var(--el-fill-color-blank));
}

.worktab-tags-bar .worktab-bar-btn:active {
  background-color: color-mix(in srgb, var(--el-color-primary) 16%, var(--el-fill-color-blank));
}

.worktab-tags-bar .worktab-bar-btn:focus-visible {
  outline: none;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--el-color-primary) 45%, transparent);
}

.dark .worktab-tags-bar .worktab-bar-btn {
  color: rgb(255 255 255 / 72%);
}

.dark .worktab-tags-bar .worktab-bar-cell--sep-r {
  border-right-color: rgb(255 255 255 / 12%);
}

.dark .worktab-tags-bar .worktab-bar-btn:hover {
  color: var(--el-color-primary);
  background-color: rgb(255 255 255 / 8%);
}

.dark .worktab-tags-bar .worktab-bar-btn:active {
  background-color: rgb(255 255 255 / 12%);
}

.dark .worktab-tags-bar .worktab-bar-btn:focus-visible {
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--el-color-primary) 55%, transparent);
}

/* tab-card：胶囊 + 轻阴影（仅 .worktab-tab--card；Chrome 由 .google-tab 负责） */
.worktab-tab.worktab-tab--card {
  gap: 6px;
  background: color-mix(
    in srgb,
    var(--el-bg-color) 94%,
    var(--el-text-color-regular) 6%
  ) !important;
  border: 1px solid color-mix(in srgb, var(--art-card-border) 80%, transparent) !important;

  /* 卡片模式圆角不要半圆：与默认一致 */
  border-radius: calc(var(--custom-radius) / 2.5 + 2px) !important;
  box-shadow:
    0 1px 2px rgb(0 0 0 / 5%),
    inset 0 1px 0 rgb(255 255 255 / 45%);
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease,
    background 0.18s ease,
    transform 0.15s ease;
}

.dark .worktab-tab.worktab-tab--card {
  background: color-mix(
    in srgb,
    var(--el-bg-color-overlay) 92%,
    var(--el-text-color-regular) 8%
  ) !important;
  border-color: color-mix(in srgb, var(--art-card-border) 55%, transparent) !important;
  box-shadow: 0 1px 4px rgb(0 0 0 / 35%);
}

.worktab-tab.worktab-tab--card:hover {
  border-color: var(--el-border-color) !important;
  transform: translateY(-0.5px);
}

.worktab-tab.worktab-tab--card.activ-tab {
  background: color-mix(in srgb, var(--el-color-primary) 14%, var(--el-bg-color)) !important;
  border-color: color-mix(in srgb, var(--el-color-primary) 50%, transparent) !important;
  box-shadow:
    0 2px 14px color-mix(in srgb, var(--el-color-primary) 20%, transparent),
    inset 0 -1px 0 color-mix(in srgb, var(--el-color-primary) 28%, transparent);
}

/* 亮色：胶囊选中态与顶栏标签一致，用主题浅底 */
html:not(.dark) .worktab-tab.worktab-tab--card.activ-tab {
  background: var(--el-color-primary-light-9) !important;
  border-color: var(--el-color-primary-light-7) !important;
  box-shadow:
    0 2px 14px color-mix(in srgb, var(--el-color-primary) 18%, transparent),
    inset 0 -1px 0 color-mix(in srgb, var(--el-color-primary) 22%, transparent);
}

.worktab-star {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  padding: 2px;
  margin: 0 2px 0 0;
  color: var(--el-text-color-placeholder);
  cursor: pointer;
  background: transparent;
  border: none;
  border-radius: 6px;
  opacity: 0.45;
  transition:
    opacity 0.15s ease,
    color 0.15s ease,
    transform 0.15s ease;
}

.group:hover .worktab-star,
.worktab-star:hover {
  opacity: 1;
}

.worktab-star:hover {
  color: var(--el-color-primary);
  transform: scale(1.06);
}

.worktab-star--on {
  color: var(--el-color-primary);
  opacity: 1;
}

.worktab-close {
  color: var(--el-text-color-secondary);
  opacity: 0.28;
  transition:
    opacity 0.15s ease,
    background-color 0.15s ease,
    color 0.15s ease;
}

.group:hover .worktab-close,
.worktab-close:hover {
  opacity: 1;
}

.worktab-close:hover {
  color: var(--el-color-danger);
  background-color: color-mix(in srgb, var(--el-color-danger) 12%, transparent) !important;
}

/* 亮色：当前选中标签条为主题浅底（::before/::after 弧角共用同一变量） */
html:not(.dark) .worktab-tags-shell--google {
  --worktab-google-active-bg: var(--el-color-primary-light-9);
}

.dark .worktab-tags-shell--google {
  --worktab-google-active-bg: color-mix(in srgb, rgb(255 255 255) 15%, var(--el-bg-color) 85%);
}

.worktab-tags-shell--google .google-tab:not(.activ-tab) {
  color: var(--worktab-google-tab-muted) !important;
  background: transparent !important;
}

.worktab-tags-shell--google .google-tab:not(.activ-tab):hover {
  box-sizing: border-box;
  color: var(--el-text-color-primary) !important;
  background-color: color-mix(in srgb, var(--el-text-color-primary) 8%, transparent) !important;
  border-bottom: none !important;
  border-radius: 6px 6px 0 0 !important;
}

.worktab-tags-shell--google .google-tab-route-icon:not(.text-theme) {
  color: color-mix(in srgb, var(--worktab-google-tab-muted) 92%, transparent);
}

.worktab-tags-shell--google .google-tab.activ-tab {
  color: var(--theme-color) !important;
  background-color: var(--worktab-google-active-bg) !important;
  border-bottom: 0 !important;
  border-bottom-right-radius: 0 !important;
  border-bottom-left-radius: 0 !important;
}

.worktab-tags-shell--google .google-tab.activ-tab::before,
.worktab-tags-shell--google .google-tab.activ-tab::after {
  box-shadow: 0 0 0 30px var(--worktab-google-active-bg);
}

.worktab-google-divider {
  position: absolute;
  top: 50%;
  left: 0;
  width: 1px;
  height: 14px;
  pointer-events: none;
  background: color-mix(in srgb, var(--el-border-color) 72%, transparent);
  transform: translateY(-50%);
  transition: opacity 0.15s ease;
}

.dark .worktab-tags-shell--google .worktab-google-divider {
  background: rgb(255 255 255 / 14%);
}

/* 悬停当前标签：隐藏与本标签相邻的两条竖线（自身左缘 + 下一标签左缘） */
.worktab-tags-shell--google .google-tab:hover .worktab-google-divider {
  opacity: 0;
}

.worktab-tags-shell--google .google-tab:hover + .google-tab .worktab-google-divider {
  opacity: 0;
}

/* 当前选中标签：与悬停一致，不展示左右相邻竖线 */
.worktab-tags-shell--google .google-tab.activ-tab .worktab-google-divider {
  opacity: 0;
}

.worktab-tags-shell--google .google-tab.activ-tab + .google-tab .worktab-google-divider {
  opacity: 0;
}

/* 固定标签图钉（pushpin）：常用黄色，与路由菜单图标区分 */
.worktab-pin {
  color: #ca8a04 !important;
}

.dark .worktab-pin {
  color: #fbbf24 !important;
}

.worktab-tags-shell--google .worktab-pin {
  color: #ca8a04 !important;
}

.dark .worktab-tags-shell--google .worktab-pin {
  color: #fbbf24 !important;
}

.group:hover .worktab-pin {
  color: #a16207 !important;
}

.dark .group:hover .worktab-pin {
  color: #fcd34d !important;
}

.google-tab::before,
.google-tab::after {
  position: absolute;
  bottom: 0;
  width: 20px;
  height: 20px;
  content: "";
  border-radius: 50%;
  box-shadow: 0 0 0 30px transparent;
}

.google-tab::before {
  left: -20px;
  clip-path: inset(50% -10px 0 50%);
}

.google-tab::after {
  right: -20px;
  clip-path: inset(50% 50% 0 -10px);
}

@media only screen and (width <= 768px) {
  .box-border.flex.justify-between {
    padding-right: 0.625rem;
    padding-left: 0.625rem;
  }
}

@media only screen and (width <= 640px) {
  .box-border.flex.justify-between {
    padding-right: 0.9375rem;
    padding-left: 0.9375rem;
  }
}
</style>
