<!-- 布局内容 -->
<template>
  <div id="app-scroll-main" class="layout-content" :style="containerStyle">
    <div id="app-content-header">
      <!-- 节日滚动 -->
      <ArtFestivalTextScroll />

      <!-- 路由信息调试 -->
      <div
        v-if="isOpenRouteInfo === 'true'"
        class="px-2 py-1.5 mb-3 text-sm text-g-500 bg-g-200 border-full-d rounded-md"
      >
        router meta：{{ route.meta }}
      </div>
    </div>

    <RouterView v-if="isRefresh" v-slot="{ Component, route: router }" :style="contentStyle">
      <Transition :name="actualTransition" mode="out-in" appear>
        <div class="route-view-shell flex min-h-0 flex-1 flex-col">
          <KeepAlive :max="10" :exclude="keepAliveExclude">
            <component
              v-if="router.meta.keepAlive === true"
              class="art-page-view min-h-0 flex-1"
              :is="Component"
              :key="router.fullPath"
            />
          </KeepAlive>
          <component
            v-if="router.meta.keepAlive !== true"
            class="art-page-view min-h-0 flex-1"
            :is="Component"
            :key="router.fullPath"
          />
        </div>
      </Transition>
    </RouterView>

    <!-- 返回顶部：宽屏 #app-scroll-main；窄屏文档滚动 target 置空 -->
    <ElBacktop
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

// 标记是否是首次加载（浏览器刷新）
const isFirstLoad = ref(true);

const actualTransition = computed(() => {
  if (isFirstLoad.value) return "";
  return pageTransition.value;
});

const containerStyle = computed(
  (): CSSProperties => ({
    maxWidth: containerWidth.value,
    flex: "1",
    minHeight: "0",
    display: "flex",
    flexDirection: "column",
  })
);

/** 常规布局下由 `.layout-content` 承担纵向滚动，路由视图填满剩余高度 */
const contentStyle = computed((): CSSProperties => ({ flex: "1", minHeight: "0" }));

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
