<!-- 定时任务：调度器状态 + 任务节点，单页管理 -->
<template>
  <div class="cronjob-page fa-full-height">
    <SchedulerBar @refresh="nodePanelRef?.refreshData()" />
    <NodePanel ref="nodePanelRef" class="cronjob-node" />
  </div>
</template>

<script setup lang="ts">
import SchedulerBar from "./components/SchedulerBar.vue";
import NodePanel from "./node/index.vue";

defineOptions({ name: "Cronjob" });

const nodePanelRef = ref<{ refreshData: () => Promise<void> }>();
</script>

<style scoped lang="scss">
.cronjob-page {
  min-height: 0;
  overflow: hidden;
}

.cronjob-node {
  flex: 1;
  min-height: 0;
}

@media (width <= 768px) {
  .cronjob-page :deep(.fa-table__mobile-cards) {
    font-size: 13px;
  }

  .cronjob-page :deep(.fa-table__mobile-cards .text-sm) {
    font-size: 13px;
  }

  .cronjob-page :deep(.fa-table__mobile-cards .text-xs) {
    font-size: 11px;
  }

  .cronjob-page :deep(.el-pagination) {
    font-size: 12px;
  }
}
</style>
