<template>
  <div class="page-content mb-5" element-loading-text="加载中...">
    <FaMapChart />
  </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from "vue";

defineOptions({ name: "DashboardMap" });

/**
 * 异步加载地图组件
 * 减少初始加载体积
 */
const FaMapChart = defineAsyncComponent(() => import("@/components/charts/fa-map-chart/index.vue"));
</script>
