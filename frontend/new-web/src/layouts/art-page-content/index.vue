<!-- 布局内容 -->
<template>
  <div
    id="app-scroll-main"
    class="layout-content"
    :class="{ 'overflow-auto': isFullPage }"
    :style="containerStyle"
  >
    <div id="app-content-header">
      <!-- 节日滚动 -->
      <ArtFestivalTextScroll v-if="!isFullPage" />

      <!-- 路由信息调试 -->
      <div
        v-if="isOpenRouteInfo === 'true'"
        class="px-2 py-1.5 mb-3 text-sm text-g-500 bg-g-200 border-full-d rounded-md"
      >
        router meta：{{ route.meta }}
      </div>
    </div>

    <RouterView v-if="isRefresh" v-slot="{ Component, route: router }" :style="contentStyle">
      <!-- 缓存路由动画 -->
      <Transition :name="showTransitionMask ? '' : actualTransition" mode="out-in" appear>
        <KeepAlive :max="10" :exclude="keepAliveExclude">
          <component
            class="art-page-view"
            :is="Component"
            :key="router.path"
            v-if="router.meta.keepAlive"
          />
        </KeepAlive>
      </Transition>

      <!-- 非缓存路由动画 -->
      <Transition :name="showTransitionMask ? '' : actualTransition" mode="out-in" appear>
        <component
          class="art-page-view"
          :is="Component"
          :key="router.path"
          v-if="!router.meta.keepAlive"
        />
      </Transition>
    </RouterView>

    <!-- 全屏页面切换过渡遮罩（用于提升页面切换视觉体验） -->
    <Teleport to="body">
      <div
        v-show="showTransitionMask"
        class="fixed top-0 left-0 z-[2000] w-screen h-screen pointer-events-none bg-box"
      />
    </Teleport>

    <!-- 返回顶部：宽屏 #app-scroll-main；窄屏文档滚动 target 置空 -->
    <ElBacktop
      v-if="!isFullPage"
      :key="backtopTargetKey"
      :target="backtopScrollTarget"
      :right="28"
      :bottom="28"
      class="z-[90]"
    >
      <ArtSvgIcon icon="ri:arrow-up-circle-line" class="text-2xl text-g-600" />
    </ElBacktop>
  </div>
</template>
<script setup lang="ts">
import type { CSSProperties } from "vue";
import { useMediaQuery } from "@vueuse/core";
import { useRoute } from "vue-router";
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import { useAutoLayoutHeight } from "@/hooks/core/useLayoutHeight";
import { useSettingsStore } from "@/store/modules/setting.store";
import { useWorktabStore } from "@/store/modules/worktab.store";

defineOptions({ name: "ArtPageContent" });

const route = useRoute();
const isNarrowViewport = useMediaQuery("(max-width: 800px)");
const backtopScrollTarget = computed(() => (isNarrowViewport.value ? "" : "#app-scroll-main"));
const backtopTargetKey = computed(() => (isNarrowViewport.value ? "win" : "main"));

useAutoLayoutHeight();
const { pageTransition, containerWidth, refresh } = storeToRefs(useSettingsStore());
const { keepAliveExclude } = storeToRefs(useWorktabStore());

const isRefresh = shallowRef(true);
const isOpenRouteInfo = import.meta.env.VITE_OPEN_ROUTE_INFO;
const showTransitionMask = ref(false);

// 标记是否是首次加载（浏览器刷新）
const isFirstLoad = ref(true);

// 检查当前路由是否需要使用无基础布局模式
const isFullPage = computed(() => route.matched.some((r) => r.meta?.isFullPage));
const prevIsFullPage = ref(isFullPage.value);

// 切换动画名称：首次加载、从全屏返回时不使用动画
const actualTransition = computed(() => {
  if (isFirstLoad.value) return "";
  if (prevIsFullPage.value && !isFullPage.value) return "";
  return pageTransition.value;
});

// 监听全屏状态变化，显示过渡遮罩
watch(isFullPage, (val, oldVal) => {
  if (val !== oldVal) {
    showTransitionMask.value = true;
    // 延迟隐藏遮罩，给足时间让页面完成切换
    setTimeout(() => {
      showTransitionMask.value = false;
    }, 50);
  }

  nextTick(() => {
    prevIsFullPage.value = val;
  });
});

const containerStyle = computed(
  (): CSSProperties =>
    isFullPage.value
      ? {
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100vh",
          zIndex: 2500,
          background: "var(--default-bg-color)",
        }
      : {
          maxWidth: containerWidth.value,
          flex: "1",
          minHeight: "0",
          display: "flex",
          flexDirection: "column",
        }
);

/** 常规布局下由 `.layout-content` 承担纵向滚动，路由视图填满剩余高度 */
const contentStyle = computed(
  (): CSSProperties =>
    isFullPage.value
      ? { flex: "1", minHeight: "0", display: "flex", flexDirection: "column" }
      : { flex: "1", minHeight: "0" }
);

const reload = () => {
  isRefresh.value = false;
  nextTick(() => {
    isRefresh.value = true;
  });
};

watch(refresh, reload, { flush: "post" });

// 组件挂载后标记首次加载完成
onMounted(() => {
  // 延迟一帧，确保首次渲染完成
  nextTick(() => {
    isFirstLoad.value = false;
  });
});
</script>
