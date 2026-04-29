<template>
  <div class="layout-wrapper">
    <component :is="currentLayoutComponent" />

    <!-- 设置面板 - 独立于布局组件 -->
    <Settings v-if="isShowSettings" />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useLayout } from "./composables/useLayout";
import LeftLayout from "./views/LeftLayout.vue";
import TopLayout from "./views/TopLayout.vue";
import MixLayout from "./views/MixLayout.vue";
import Settings from "./components/Settings/index.vue";
import { LayoutMode } from "@/enums/settings/layout.enum";

const { currentLayout, isShowSettings } = useLayout();

// 根据当前布局模式选择对应的组件
const currentLayoutComponent = computed(() => {
  switch (currentLayout.value) {
    case LayoutMode.TOP:
      return TopLayout;
    case LayoutMode.MIX:
      return MixLayout;
    case LayoutMode.LEFT:
    default:
      return LeftLayout;
  }
});
</script>

<style lang="scss" scoped>
.layout-wrapper {
  width: 100%;
  height: 100%;
}
</style>
