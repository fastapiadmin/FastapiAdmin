<template>
  <div class="app-container">
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <div class="status-content">
            <span>任务列表</span>
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
            <div class="status-actions">
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="success"
                icon="VideoPlay"
                :disabled="schedulerStatus.status !== '停止'"
                @click="handleStartScheduler"
              >
                启动
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="warning"
                icon="VideoPause"
                :disabled="schedulerStatus.status !== '运行中'"
                @click="handlePauseScheduler"
              >
                暂停
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="primary"
                icon="RefreshRight"
                :disabled="schedulerStatus.status !== '暂停'"
                @click="handleResumeScheduler"
              >
                恢复
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="danger"
                icon="SwitchButton"
                :disabled="schedulerStatus.status === '停止'"
                @click="handleShutdownScheduler"
              >
                关闭
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:delete']"
                type="danger"
                icon="Delete"
                :disabled="schedulerStatus.job_count === 0"
                @click="handleClearAllJobs"
              >
                清空任务
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
                @click="handleSyncJobs"
              >
                同步
              </el-button>
            </div>
          </div>
        </div>
      </template>

      <div class="search-container">
        <el-form
          ref="queryFormRef"
          :model="queryFormData"
          :inline="true"
          label-suffix=":"
          @submit.prevent="handleQuery"
        >
          <el-form-item prop="job_name" label="任务名称">
            <el-input v-model="queryFormData.job_name" placeholder="请输入任务名称" clearable />
          </el-form-item>
          <el-form-item prop="status" label="执行状态">
            <el-select
              v-model="queryFormData.status"
              placeholder="请选择状态"
              clearable
              style="width: 120px"
            >
              <el-option value="pending" label="待执行" />
              <el-option value="running" label="执行中" />
              <el-option value="success" label="成功" />
              <el-option value="failed" label="失败" />
              <el-option value="timeout" label="超时" />
              <el-option value="cancelled" label="已取消" />
            </el-select>
          </el-form-item>
          <el-form-item prop="trigger_type" label="触发方式">
            <el-select
              v-model="queryFormData.trigger_type"
              placeholder="请选择"
              clearable
              style="width: 120px"
            >
              <el-option value="cron" label="Cron表达式" />
              <el-option value="interval" label="时间间隔" />
              <el-option value="date" label="固定日期" />
              <el-option value="manual" label="一次性任务" />
            </el-select>
          </el-form-item>
          <el-form-item class="search-buttons">
            <el-button
              v-hasPerm="['module_task:job:query']"
              type="primary"
              icon="search"
              native-type="submit"
            >
              查询
            </el-button>
            <el-button
              v-hasPerm="['module_task:job:query']"
              icon="refresh"
              @click="handleResetQuery"
            >
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_task:job:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDeleteLog(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="dataTableRef"
        v-loading="logLoading"
        :data="logTableData"
        class="data-table__content"
        highlight-current-row
        border
        stripe
        height="450"
        max-height="450"
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" align="center" min-width="55" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="任务ID" prop="job_id" min-width="80" show-overflow-tooltip />
        <el-table-column label="任务名称" prop="job_name" min-width="140" />
        <el-table-column label="触发方式" prop="trigger_type" min-width="120">
          <template #default="scope">
            <el-tag size="small">{{ getTriggerTypeLabel(scope.row.trigger_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status" min-width="80">
          <template #default="scope">
            <el-tag :type="getLogStatusType(scope.row.status)" size="small">
              {{ getLogStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="下次执行时间"
          prop="next_run_time"
          min-width="300"
          show-overflow-tooltip
        />
        <el-table-column label="任务状态" prop="job_state" min-width="100">
          <template #default="scope">
            <el-button
              v-if="scope.row.job_state"
              type="primary"
              size="small"
              link
              icon="View"
              @click="handleViewJobState(scope.row.job_state)"
            >
              查看
            </el-button>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="执行结果" prop="result" min-width="150" show-overflow-tooltip />
        <el-table-column label="错误信息" prop="error" min-width="150" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_time" min-width="160" />
        <el-table-column label="更新时间" prop="updated_time" min-width="160" />

        <OperationColumn :list-data-length="logTableData.length">
          <template #default="scope">
            <el-space class="flex">
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="primary"
                size="small"
                link
                icon="VideoPlay"
                @click="handleResumeJob(scope.row.job_id)"
              >
                恢复
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="warning"
                size="small"
                link
                icon="VideoPause"
                @click="handlePauseJob(scope.row.job_id)"
              >
                暂停
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:update']"
                type="success"
                size="small"
                link
                icon="CaretRight"
                @click="handleRunJobNow(scope.row.job_id)"
              >
                执行
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:delete']"
                type="danger"
                size="small"
                link
                icon="Close"
                @click="handleRemoveJob(scope.row.job_id)"
              >
                移除
              </el-button>
              <el-button
                v-hasPerm="['module_task:job:delete']"
                type="danger"
                size="small"
                link
                icon="delete"
                @click="handleDeleteLog([scope.row.id])"
              >
                删除
              </el-button>
            </el-space>
          </template>
        </OperationColumn>
      </el-table>

      <template #footer>
        <pagination
          v-model:total="logTotal"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadLogData"
        />
      </template>
    </el-card>

    <el-dialog v-model="consoleVisible" title="调度器控制台" width="900px" top="5vh">
      <div class="terminal-wrapper">
        <Terminal name="scheduler-console" :show-header="false" theme="dark" />
      </div>
      <template #footer>
        <el-button @click="handleRefreshConsole">刷新</el-button>
        <el-button @click="handleClearConsole">清空</el-button>
        <el-button type="primary" @click="consoleVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="jobStateVisible" title="任务状态" width="800px">
      <JsonPretty :value="jobStateData" height="400px" />
      <template #footer>
        <el-button type="primary" @click="jobStateVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Job",
  inheritAttrs: false,
});

import JobAPI, { SchedulerStatus, JobLogTable, JobLogPageQuery } from "@/api/module_task/job";
import { onMounted } from "vue";
import { Terminal, TerminalApi } from "vue-web-terminal";
import OperationColumn from "@/components/OperationColumn/index.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";

const queryFormRef = ref();
const logTotal = ref(0);
const selectIds = ref<number[]>([]);
const logLoading = ref(false);

const schedulerStatus = ref<SchedulerStatus>({
  status: "未知",
  is_running: false,
  job_count: 0,
});

const consoleVisible = ref(false);

const jobStateVisible = ref(false);
const jobStateData = ref("");

const logTableData = ref<JobLogTable[]>([]);

const queryFormData = reactive<JobLogPageQuery>({
  page_no: 1,
  page_size: 10,
  job_id: undefined,
  job_name: undefined,
  status: undefined,
  trigger_type: undefined,
});

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

function getLogStatusType(status: string) {
  switch (status) {
    case "success":
      return "success";
    case "running":
      return "primary";
    case "pending":
      return "info";
    case "failed":
    case "timeout":
      return "danger";
    case "cancelled":
      return "warning";
    default:
      return "info";
  }
}

function getLogStatusLabel(status: string) {
  switch (status) {
    case "pending":
      return "待执行";
    case "running":
      return "执行中";
    case "success":
      return "成功";
    case "failed":
      return "失败";
    case "timeout":
      return "超时";
    case "cancelled":
      return "已取消";
    default:
      return status;
  }
}

function getTriggerTypeLabel(type: string | undefined) {
  switch (type) {
    case "cron":
      return "Cron表达式";
    case "interval":
      return "时间间隔";
    case "date":
      return "固定日期";
    case "manual":
      return "一次性任务";
    default:
      return type || "-";
  }
}

async function loadSchedulerStatus() {
  try {
    const response = await JobAPI.getSchedulerStatus();
    schedulerStatus.value = response.data.data;
  } catch (error: any) {
    console.error(error);
  }
}

async function loadLogData() {
  logLoading.value = true;
  try {
    const response = await JobAPI.getJobLogList(queryFormData);
    logTableData.value = response.data.data.items;
    logTotal.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    logLoading.value = false;
  }
}

async function handleRefresh() {
  await Promise.all([loadSchedulerStatus(), loadLogData()]);
}

async function handleQuery() {
  queryFormData.page_no = 1;
  loadLogData();
}

async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadLogData();
}

async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
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
    await ElMessageBox.confirm("确定要清空所有任务吗？此操作不可恢复！", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
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

async function handleSyncJobs() {
  try {
    await JobAPI.syncJobsToDb();
    await handleRefresh();
  } catch (error: any) {
    console.error(error);
  }
}

function handleViewJobState(jobState: string) {
  jobStateData.value = jobState;
  jobStateVisible.value = true;
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

async function handleDeleteLog(ids: number[]) {
  ElMessageBox.confirm("确认删除选中的记录?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await JobAPI.deleteJobLog(ids);
        handleResetQuery();
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
.status-card {
  margin-bottom: 16px;
}

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
  margin-left: auto;
}

.search-container {
  margin-bottom: 16px;
}

.data-table {
  margin-bottom: 16px;
}

.terminal-wrapper {
  height: 500px;
  overflow: hidden;
  border-radius: 6px;
}
</style>
