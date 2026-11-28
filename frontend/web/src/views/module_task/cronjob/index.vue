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
</style>
