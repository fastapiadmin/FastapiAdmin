<!-- 定时任务顶部：调度器状态与全局控制 -->
<template>
  <div class="scheduler-bar">
    <div class="scheduler-bar__status">
      <span class="scheduler-bar__caption">调度器</span>
      <ElTag :type="statusType" size="small" effect="dark">{{ statusLabel }}</ElTag>
      <span class="scheduler-bar__caption">运行中</span>
      <ElTag :type="status.is_running ? 'success' : 'info'" size="small" effect="dark">
        {{ status.is_running ? "是" : "否" }}
      </ElTag>
      <span class="scheduler-bar__caption">任务</span>
      <span class="scheduler-bar__count">{{ status.job_count }}</span>
    </div>

    <div class="scheduler-bar__actions">
      <ElButton
        v-hasPerm="['module_task:cronjob:job:scheduler']"
        type="primary"
        :icon="VideoPlay"
        :disabled="status.status !== '停止'"
        size="small"
        @click="handleStart"
      >
        启动
      </ElButton>
      <ElButton
        v-hasPerm="['module_task:cronjob:job:scheduler']"
        :icon="VideoPause"
        :disabled="status.status !== '运行中'"
        size="small"
        @click="handlePause"
      >
        暂停
      </ElButton>
      <ElButton
        v-hasPerm="['module_task:cronjob:job:scheduler']"
        :icon="RefreshRight"
        :disabled="status.status !== '暂停'"
        size="small"
        @click="handleResume"
      >
        恢复
      </ElButton>
      <ElButton
        v-hasPerm="['module_task:cronjob:job:scheduler']"
        type="danger"
        plain
        :icon="SwitchButton"
        :disabled="status.status === '停止'"
        size="small"
        @click="handleShutdown"
      >
        关闭
      </ElButton>
      <ElButton :icon="Refresh" size="small" :loading="loading" @click="loadStatus">刷新</ElButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Refresh, RefreshRight, SwitchButton, VideoPause, VideoPlay } from "@element-plus/icons-vue";
import JobAPI, { type SchedulerStatus } from "@/api/module_task/cronjob/job";
import { confirmDelete } from "@/hooks/core/useConfirm";

const emit = defineEmits<{ refresh: [] }>();

const loading = ref(false);
const status = ref<SchedulerStatus>({
  status: "停止",
  is_running: false,
  job_count: 0,
});

const statusLabel = computed(() => status.value.status || "未知");
const statusType = computed(() => {
  if (status.value.status === "运行中") return "success";
  if (status.value.status === "暂停") return "warning";
  return "info";
});

async function loadStatus() {
  loading.value = true;
  try {
    const res = await JobAPI.getSchedulerStatus();
    if (res.data.data) status.value = res.data.data;
  } finally {
    loading.value = false;
  }
}

async function runAction(action: () => Promise<unknown>) {
  try {
    await action();
    await loadStatus();
    emit("refresh");
  } catch {
    // 全局请求层已提示错误
  }
}

const handleStart = () => runAction(() => JobAPI.startScheduler());
const handlePause = () => runAction(() => JobAPI.pauseScheduler());
const handleResume = () => runAction(() => JobAPI.resumeScheduler());
const handleShutdown = async () => {
  try {
    await confirmDelete("确定要关闭调度器吗？关闭后所有定时任务将停止执行。");
    await runAction(() => JobAPI.shutdownScheduler());
  } catch {
    // 用户取消
  }
};

let statusTimer: number | undefined;

onMounted(() => {
  void loadStatus();
  statusTimer = window.setInterval(loadStatus, 30000);
});

onUnmounted(() => {
  if (statusTimer) window.clearInterval(statusTimer);
});
</script>

<style scoped lang="scss">
.scheduler-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 16px;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  padding: 12px 16px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--custom-radius);
}

.scheduler-bar__status {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  min-width: 0;
}

.scheduler-bar__caption {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.scheduler-bar__count {
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
  color: var(--el-color-warning);
}

.scheduler-bar__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
</style>
