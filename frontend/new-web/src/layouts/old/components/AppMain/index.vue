<template>
  <section class="app-main" :style="{ height: appMainHeight }">
    <router-view>
      <template #default="{ Component, route }">
        <transition :name="transitionName" mode="out-in">
          <keep-alive :include="cachedViews">
            <component :is="Component" :key="route.path" />
          </keep-alive>
        </transition>
      </template>
    </router-view>

    <!-- 返回顶部按钮 -->
    <el-backtop target=".app-main">
      <div class="i-svg:backtop w-6 h-6" />
    </el-backtop>
  </section>
</template>

<script setup lang="ts">
import { useSettingsStore, useTagsViewStore } from "@/store";
import variables from "@/styles/variables.module.scss";
import { computed } from "vue";

const settingsStore = useSettingsStore();
// 页面切换动画名称
const transitionName = computed(() => {
  return settingsStore.pageSwitchingAnimation ?? "";
});
// 缓存页面集合
const cachedViews = computed(() => useTagsViewStore().cachedViews);
const appMainHeight = computed(() => {
  if (settingsStore.showTagsView) {
    return `calc(100vh - ${variables["navbar-height"]} - ${variables["tags-view-height"]})`;
  } else {
    return `calc(100vh - ${variables["navbar-height"]})`;
  }
});
</script>

<style lang="scss" scoped>
.app-main {
  position: relative;
  overflow-y: auto;
  background-color: var(--el-bg-color-page);

  /* 布局切换动画优化 */

  /* fade */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease-in-out;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  /* fade-slide - 优化后的平滑切换，增大位移 */
  .fade-slide-leave-active,
  .fade-slide-enter-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .fade-slide-enter-from {
    opacity: 0;
    transform: translateX(-60px);
  }

  .fade-slide-leave-to {
    opacity: 0;
    transform: translateX(60px);
  }

  /* fade-scale */
  .fade-scale-leave-active,
  .fade-scale-enter-active {
    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .fade-scale-enter-from {
    opacity: 0;
    transform: scale(1.2);
  }

  .fade-scale-leave-to {
    opacity: 0;
    transform: scale(0.8);
  }

  /* slide-left-right - 左右滑动切换 */
  .slide-left-right-leave-active,
  .slide-left-right-enter-active {
    position: absolute;
    width: 100%;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .slide-left-right-enter-from {
    opacity: 0;
    transform: translateX(100%);
  }

  .slide-left-right-leave-to {
    opacity: 0;
    transform: translateX(-100%);
  }

  /* zoom-in-out - 缩放进出 */
  .zoom-in-out-leave-active,
  .zoom-in-out-enter-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .zoom-in-out-enter-from {
    opacity: 0;
    transform: scale(0.8);
  }

  .zoom-in-out-leave-to {
    opacity: 0;
    transform: scale(1.2);
  }

  /* slide-up-down - 上下滑动 */
  .slide-up-down-leave-active,
  .slide-up-down-enter-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .slide-up-down-enter-from {
    opacity: 0;
    transform: translateY(40px);
  }

  .slide-up-down-leave-to {
    opacity: 0;
    transform: translateY(-40px);
  }

  /* bounce - 弹性效果 */
  .bounce-leave-active,
  .bounce-enter-active {
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }

  .bounce-enter-from {
    opacity: 0;
    transform: scale(0.3);
  }

  .bounce-leave-to {
    opacity: 0;
    transform: scale(0.3);
  }
}
</style>
