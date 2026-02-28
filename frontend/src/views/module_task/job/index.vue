<template>
  <div class="app-container">
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <div class="status-content">
            <span>调度器任务列表</span>
            <div class="status-item">
              <span class="label">状态：</span>
              <el-tag :type="getSchedulerStatusType(schedulerStatus.status)" size="large">
                {{ schedulerStatus.status }}
              </el-tag>
            </div>
            <div class="status-item">
              <span class="label">运行中：</span>
              <el-tag :type="schedulerStatus.is_running ? 'success' : 'danger'" size="large">
                {{ schedulerStatus.is_running ? "是" : "否" }}
              </el-tag>
            </div>
            <div class="status-item">
              <span class="label">任务数量：</span>
              <el-tag type="info" size="large">{{ schedulerStatus.job_count }}</el-tag>
            </div>
          </div>
          <div class="status-actions">
            <el-button
              v-hasPerm="['module_task:job:scheduler']"
              type="success"
              icon="VideoPlay"
              :disabled="schedulerStatus.status !== '停止'"
              @click="handleStartScheduler"
            >
              启动
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:scheduler']"
              type="warning"
              icon="VideoPause"
              :disabled="schedulerStatus.status !== '运行中'"
              @click="handlePauseScheduler"
            >
              暂停
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:scheduler']"
              type="primary"
              icon="RefreshRight"
              :disabled="schedulerStatus.status !== '暂停'"
              @click="handleResumeScheduler"
            >
              恢复
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:scheduler']"
              type="danger"
              icon="SwitchButton"
              :disabled="schedulerStatus.status === '停止'"
              @click="handleShutdownScheduler"
            >
              关闭
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:task']"
              type="danger"
              icon="Delete"
              :disabled="schedulerStatus.job_count === 0"
              @click="handleClearAllJobs"
            >
              清空任务
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:task']"
              type="warning"
              icon="VideoPause"
              :disabled="selectedJobIds.length === 0"
              @click="handleBatchPauseJobs"
            >
              批量暂停
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:task']"
              type="primary"
              icon="VideoPlay"
              :disabled="selectedJobIds.length === 0"
              @click="handleBatchResumeJobs"
            >
              批量恢复
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:task']"
              type="danger"
              icon="Close"
              :disabled="selectedJobIds.length === 0"
              @click="handleBatchRemoveJobs"
            >
              批量移除
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:query']"
              type="info"
              icon="Monitor"
              @click="handleOpenConsole"
            >
              控制台
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:update']"
              type="warning"
              icon="Refresh"
              @click="handleRefresh"
            >
              刷新
            </el-button>
          </div>
          <div class="search-container">
            <el-form
              ref="queryFormRef"
              :model="queryFormData"
              :inline="true"
              label-suffix=":"
              @submit.prevent="handleQuery"
            >
              <el-form-item prop="name" label="任务名称">
                <el-input
                  v-model="queryFormData.name"
                  placeholder="请输入任务名称"
                  clearable
                  style="width: 150px"
                />
              </el-form-item>
              <el-form-item prop="status" label="任务状态">
                <el-select
                  v-model="queryFormData.status"
                  placeholder="请选择状态"
                  clearable
                  style="width: 150px"
                >
                  <el-option value="运行中" label="运行中" />
                  <el-option value="暂停" label="暂停" />
                  <el-option value="停止" label="停止" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" icon="search" native-type="submit">查询</el-button>
                <el-button icon="refresh" @click="handleResetQuery">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </template>

      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="schedulerJobs"
        class="data-table__content"
        highlight-current-row
        border
        stripe
        height="calc(100vh - 360px)"
        max-height="calc(100vh - 360px)"
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" align="center" min-width="55" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="任务ID" prop="id" min-width="80" show-overflow-tooltip />
        <el-table-column label="任务名称" prop="name" min-width="100" />
        <el-table-column label="状态" prop="status" min-width="80">
          <template #default="scope">
            <el-tag :type="getJobStatusType(scope.row.status)" size="small">
              {{ getJobStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="触发器" prop="trigger" min-width="200" show-overflow-tooltip>
          <template #default="scope">
            <el-tag v-if="scope.row.trigger.includes('cron')" type="primary" size="small">
              <el-icon><Clock /></el-icon>
              {{ formatTrigger(scope.row.trigger) }}
            </el-tag>
            <el-tag v-else-if="scope.row.trigger.includes('interval')" type="success" size="small">
              <el-icon><Timer /></el-icon>
              {{ formatTrigger(scope.row.trigger) }}
            </el-tag>
            <el-tag v-else-if="scope.row.trigger.includes('date')" type="warning" size="small">
              <el-icon><Calendar /></el-icon>
              {{ formatTrigger(scope.row.trigger) }}
            </el-tag>
            <el-tag v-else type="info" size="small">
              {{ formatTrigger(scope.row.trigger) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="下次执行时间"
          prop="next_run_time"
          min-width="140"
          show-overflow-tooltip
        >
          <template #default="scope">
            {{ scope.row.next_run_time || "-" }}
          </template>
        </el-table-column>

        <OperationColumn :list-data-length="schedulerJobs.length">
          <template #default="scope">
            <el-space class="flex">
              <el-button
                v-if="scope.row.status === '暂停'"
                v-hasPerm="['module_task:job:task']"
                type="primary"
                size="small"
                link
                icon="VideoPlay"
                @click="handleResumeJob(scope.row.id)"
              >
                恢复
              </el-button>
              <el-button
                v-if="scope.row.status === '运行中'"
                v-hasPerm="['module_task:job:task']"
                type="warning"
                size="small"
                link
                icon="VideoPause"
                @click="handlePauseJob(scope.row.id)"
              >
                暂停
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:task']"
                type="success"
                size="small"
                link
                icon="CaretRight"
                @click="handleRunJobNow(scope.row.id)"
              >
                执行
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:task']"
                type="danger"
                size="small"
                link
                icon="Close"
                @click="handleRemoveJob(scope.row.id)"
              >
                移除
              </el-button>
            </el-space>
          </template>
        </OperationColumn>
      </el-table>
    </el-card>

    <el-dialog v-model="consoleVisible" title="调度器控制台">
      <div class="terminal-wrapper">
        <Terminal name="scheduler-console" :show-header="false" theme="dark" />
      </div>
      <template #footer>
        <el-button @click="handleRefreshConsole">刷新</el-button>
        <el-button @click="handleClearConsole">清空</el-button>
        <el-button type="primary" @click="consoleVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Job",
  inheritAttrs: false,
});

import JobAPI, { SchedulerStatus, SchedulerJob } from "@/api/module_task/job";
import { onMounted } from "vue";
import { Terminal, TerminalApi } from "vue-web-terminal";
import OperationColumn from "@/components/OperationColumn/index.vue";

const loading = ref(false);

const queryFormRef = ref();

const queryFormData = ref({
  name: "",
  status: "",
});

const selectedJobIds = ref<string[]>([]);

const schedulerStatus = ref<SchedulerStatus>({
  status: "未知",
  is_running: false,
  job_count: 0,
});

const consoleVisible = ref(false);

const schedulerJobs = ref<SchedulerJob[]>([]);

function getSchedulerStatusType(status: string) {
  switch (status) {
    case "运行中":
      return "success";
    case "暂停":
      return "warning";
    case "停止":
      return "danger";
    default:
      return "info";
  }
}

function getJobStatusType(status: string) {
  switch (status) {
    case "运行中":
      return "success";
    case "暂停":
      return "warning";
    case "停止":
      return "danger";
    default:
      return "info";
  }
}

function getJobStatusLabel(status: string) {
  switch (status) {
    case "运行中":
      return "运行中";
    case "暂停":
      return "暂停";
    case "停止":
      return "停止";
    default:
      return status;
  }
}

function formatTrigger(trigger: string) {
  if (!trigger) {
    return "-";
  }

  if (trigger.includes("cron")) {
    const match = trigger.match(/cron\[([^\]]+)\]/);
    return match ? `Cron: ${match[1]}` : trigger;
  }

  if (trigger.includes("interval")) {
    const match = trigger.match(/interval\[([^\]]+)\]/);
    return match ? `Interval: ${match[1]}` : trigger;
  }

  if (trigger.includes("date")) {
    const match = trigger.match(/date\[([^\]]+)\]/);
    return match ? `Date: ${match[1]}` : trigger;
  }

  return trigger;
}

async function loadSchedulerStatus() {
  try {
    const response = await JobAPI.getSchedulerStatus();
    schedulerStatus.value = response.data.data;
  } catch (error: any) {
    console.error(error);
  }
}

async function loadSchedulerJobs() {
  loading.value = true;
  try {
    const response = await JobAPI.getSchedulerJobs();
    let jobs = response.data.data || [];

    if (queryFormData.value.name) {
      jobs = jobs.filter((job) => job.name.includes(queryFormData.value.name));
    }

    if (queryFormData.value.status) {
      jobs = jobs.filter((job) => job.status === queryFormData.value.status);
    }

    schedulerJobs.value = jobs;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function handleQuery() {
  loadSchedulerJobs();
}

function handleResetQuery() {
  queryFormData.value.name = "";
  queryFormData.value.status = "";
  loadSchedulerJobs();
}

function handleSelectionChange(selection: SchedulerJob[]) {
  selectedJobIds.value = selection.map((job) => job.id);
}

async function handleBatchPauseJobs() {
  if (selectedJobIds.value.length === 0) {
    return;
  }
  try {
    await ElMessageBox.confirm(
      `确定要批量暂停选中的 ${selectedJobIds.value.length} 个任务吗？`,
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    loading.value = true;
    await Promise.all(selectedJobIds.value.map((id) => JobAPI.pauseJob(id)));
    await handleRefresh();
    selectedJobIds.value = [];
  } catch (error: any) {
    if (error !== "cancel") {
      console.error(error);
    }
  } finally {
    loading.value = false;
  }
}

async function handleBatchResumeJobs() {
  if (selectedJobIds.value.length === 0) {
    return;
  }
  try {
    await ElMessageBox.confirm(
      `确定要批量恢复选中的 ${selectedJobIds.value.length} 个任务吗？`,
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    loading.value = true;
    await Promise.all(selectedJobIds.value.map((id) => JobAPI.resumeJob(id)));
    await handleRefresh();
    selectedJobIds.value = [];
  } catch (error: any) {
    if (error !== "cancel") {
      console.error(error);
    }
  } finally {
    loading.value = false;
  }
}

async function handleBatchRemoveJobs() {
  if (selectedJobIds.value.length === 0) {
    return;
  }
  try {
    await ElMessageBox.confirm(
      `确定要批量移除选中的 ${selectedJobIds.value.length} 个任务吗？`,
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    loading.value = true;
    await Promise.all(selectedJobIds.value.map((id) => JobAPI.removeJob(id)));
    await handleRefresh();
    selectedJobIds.value = [];
  } catch (error: any) {
    if (error !== "cancel") {
      console.error(error);
    }
  } finally {
    loading.value = false;
  }
}

async function handleRefresh() {
  await Promise.all([loadSchedulerStatus(), loadSchedulerJobs()]);
}

async function handleStartScheduler() {
  try {
    await JobAPI.startScheduler();
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handlePauseScheduler() {
  try {
    await JobAPI.pauseScheduler();
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeScheduler() {
  try {
    await JobAPI.resumeScheduler();
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleShutdownScheduler() {
  try {
    await ElMessageBox.confirm("确定要关闭调度器吗？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await JobAPI.shutdownScheduler();
    await handleRefresh();
  } catch (error: any) {
    if (error !== "cancel") {
      console.error(error);
    }
  }
}

async function handleClearAllJobs() {
  try {
    await ElMessageBox.confirm(
      "确定要清空所有任务吗？\n" +
        "此操作会将所有待执行任务的日志标记为已取消，不会删除历史执行记录。\n" +
        "如需删除所有执行记录，请使用执行记录的批量删除功能。",
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        dangerouslyUseHTMLString: false,
      }
    );
    await JobAPI.clearAllJobs();
    await handleRefresh();
  } catch (error: any) {
    if (error !== "cancel") {
      console.error(error);
    }
  }
}

async function handleOpenConsole() {
  consoleVisible.value = true;
  await handleRefreshConsole();
}

async function handleRefreshConsole() {
  try {
    const response = await JobAPI.getSchedulerConsole();
    const data = response.data.data || "暂无任务信息";
    TerminalApi.pushMessage("scheduler-console", {
      type: "normal",
      content: data,
    });
  } catch (error: any) {
    console.error(error);
    TerminalApi.pushMessage("scheduler-console", {
      type: "normal",
      class: "error",
      content: "获取控制台信息失败",
    });
  }
}

function handleClearConsole() {
  TerminalApi.clear("scheduler-console");
}

async function handlePauseJob(jobId: string) {
  try {
    await JobAPI.pauseJob(jobId);
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeJob(jobId: string) {
  try {
    await JobAPI.resumeJob(jobId);
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleRunJobNow(jobId: string) {
  try {
    await JobAPI.runJobNow(jobId);
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleRemoveJob(jobId: string) {
  ElMessageBox.confirm("确认移除该任务?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await JobAPI.removeJob(jobId);
        await handleRefresh();
      } catch (error: any) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

onMounted(async () => {
  await handleRefresh();
});
</script>

<style scoped>
.status-content {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
}

.status-item {
  display: flex;
  gap: 8px;
  align-items: center;
}

.status-item .label {
  font-weight: 500;
  color: #606266;
}

.status-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  margin-left: auto;
}

.terminal-wrapper {
  height: 500px;
  overflow: hidden;
  border-radius: 6px;
}
</style>
