<!-- 单个任务节点的最近执行记录 -->
<template>
  <ElDrawer
    :model-value="visible"
    :title="`执行记录 · ${jobName || '任务节点'}`"
    size="560px"
    @update:model-value="emit('update:visible', $event)"
  >
    <div class="log-drawer">
      <div class="log-drawer__toolbar">
        <span class="text-xs text-[var(--el-text-color-secondary)]">最近 20 条执行记录</span>
        <ElButton :icon="Refresh" size="small" :loading="loading" @click="loadLogs">刷新</ElButton>
      </div>
      <ElTable v-loading="loading" :data="logs" size="small" height="100%">
        <ElTableColumn prop="created_time" label="执行时间" width="158" />
        <ElTableColumn label="状态" width="86">
          <template #default="{ row }">
            <ElTag :type="statusType(row.status)" size="small" effect="light">
              {{ statusLabel(row.status) }}
            </ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn label="结果" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <span :class="row.error ? 'text-(--el-color-danger)' : ''">
              {{ row.error || row.result || "-" }}
            </span>
          </template>
        </ElTableColumn>
        <template #empty>
          <ElEmpty description="暂无执行记录" :image-size="72" />
        </template>
      </ElTable>
    </div>
  </ElDrawer>
</template>

<script setup lang="ts">
import { Refresh } from "@element-plus/icons-vue";
import JobAPI, { type JobLogTable } from "@/api/module_task/cronjob/job";

const props = defineProps<{ visible: boolean; jobName: string }>();
const emit = defineEmits<{
  "update:visible": [value: boolean];
}>();

const loading = ref(false);
const logs = ref<JobLogTable[]>([]);

function statusLabel(status?: number) {
  const labels = ["待执行", "执行中", "成功", "失败", "超时", "已取消"];
  return labels[status ?? -1] ?? "未知";
}

function statusType(status?: number) {
  if (status === 2) return "success";
  if (status === 3 || status === 4) return "danger";
  if (status === 1) return "warning";
  return "info";
}

async function loadLogs() {
  if (!props.jobName) {
    logs.value = [];
    return;
  }
  loading.value = true;
  try {
    const res = await JobAPI.getJobLogList({
      page_no: 1,
      page_size: 20,
      job_name: props.jobName,
    });
    logs.value = res.data.data?.items || [];
  } finally {
    loading.value = false;
  }
}

watch(
  () => [props.visible, props.jobName],
  ([visible]) => {
    if (visible) void loadLogs();
  },
  { immediate: true }
);
</script>

<style scoped lang="scss">
.log-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.log-drawer__toolbar {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
</style>
