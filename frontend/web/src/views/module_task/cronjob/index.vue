<!-- 定时任务：调度器监控与节点管理合并为同一页面 -->
<template>
  <div class="cronjob-page fa-full-height">
    <ElTabs v-model="activeTab" class="cronjob-tabs">
      <ElTabPane label="调度器监控" name="job">
        <JobPanel />
      </ElTabPane>
      <ElTabPane label="节点管理" name="node">
        <NodePanel />
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import JobPanel from "./job/index.vue";
import NodePanel from "./node/index.vue";

defineOptions({ name: "Cronjob" });

const route = useRoute();
const router = useRouter();
const activeTab = ref(route.query.tab === "node" ? "node" : "job");

watch(activeTab, (value) => {
  router.replace({ query: { ...route.query, tab: value } });
});
</script>

<style scoped lang="scss">
.cronjob-page {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.cronjob-tabs {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;

  :deep(.el-tabs__content) {
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  :deep(.el-tab-pane) {
    height: 100%;
    min-height: 0;
  }
}
</style>
