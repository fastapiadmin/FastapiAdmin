<template>
  <div class="app-container job-page">
    <CrudSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <CrudContent ref="contentRef" :content-config="contentConfig">
      <template #header>
        <div class="card-header">
          <div class="status-content">
            <span>调度器监控</span>
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
              <el-tag type="warning" size="large">{{ schedulerStatus.job_count }}</el-tag>
            </div>
            <div class="status-actions">
              <el-button
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="success"
                icon="VideoPlay"
                :disabled="schedulerStatus.status !== '停止'"
                @click="handleStartScheduler"
              >
                启动
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="warning"
                icon="VideoPause"
                :disabled="schedulerStatus.status !== '运行中'"
                @click="handlePauseScheduler"
              >
                暂停
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="primary"
                icon="RefreshRight"
                :disabled="schedulerStatus.status !== '暂停'"
                @click="handleResumeScheduler"
              >
                恢复
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="danger"
                icon="SwitchButton"
                :disabled="schedulerStatus.status === '停止'"
                @click="handleShutdownScheduler"
              >
                关闭
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:task']"
                type="danger"
                icon="Delete"
                :disabled="schedulerStatus.job_count === 0"
                @click="handleClearAllJobs"
              >
                清空任务
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:query']"
                type="info"
                icon="Monitor"
                @click="handleOpenConsole"
              >
                控制台
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="primary"
                icon="Refresh"
                @click="handleSyncJobs"
              >
                同步
              </el-button>
              <el-button
                v-hasPerm="['module_task:cronjob:job:update']"
                type="warning"
                icon="Refresh"
                @click="refreshMain"
              >
                刷新
              </el-button>
            </div>
          </div>
        </div>
      </template>

      <template #table="{ data, loading }">
        <div v-loading="loading" class="job-cards-container">
          <el-empty v-if="!data || data.length === 0" :image-size="80" description="暂无数据" />
          <el-row v-else :gutter="16">
            <el-col
              v-for="(job, index) in data"
              :key="job.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
              class="job-card-col"
            >
              <el-card class="job-card" shadow="hover">
                <template #header>
                  <div class="job-card-header">
                    <div class="job-card-title">
                      <span class="job-index">{{ index + 1 }}</span>
                      <span class="job-name" :title="job.name">{{ job.name }}</span>
                    </div>
                    <el-tag :type="getJobStatusType(job.status)" size="small">
                      {{ getJobStatusLabel(job.status) }}
                    </el-tag>
                  </div>
                </template>

                <div class="job-card-body">
                  <div class="job-info-item">
                    <span class="job-info-label">任务ID:</span>
                    <span class="job-info-value">{{ job.id }}</span>
                  </div>
                  <div class="job-info-item">
                    <span class="job-info-label">触发器:</span>
                    <el-tag
                      v-if="String(job.trigger ?? '').includes('cron')"
                      type="primary"
                      size="small"
                      class="job-trigger-tag"
                    >
                      <el-icon><Clock /></el-icon>
                      {{ formatTrigger(job.trigger) }}
                    </el-tag>
                    <el-tag
                      v-else-if="String(job.trigger ?? '').includes('interval')"
                      type="success"
                      size="small"
                      class="job-trigger-tag"
                    >
                      <el-icon><Timer /></el-icon>
                      {{ formatTrigger(job.trigger) }}
                    </el-tag>
                    <el-tag
                      v-else-if="String(job.trigger ?? '').includes('date')"
                      type="warning"
                      size="small"
                      class="job-trigger-tag"
                    >
                      <el-icon><Calendar /></el-icon>
                      {{ formatTrigger(job.trigger) }}
                    </el-tag>
                    <el-tag v-else type="info" size="small" class="job-trigger-tag">
                      {{ formatTrigger(job.trigger) }}
                    </el-tag>
                  </div>
                  <div class="job-info-item">
                    <span class="job-info-label">下次执行:</span>
                    <span class="job-info-value">{{ job.next_run_time || "无" }}</span>
                  </div>
                </div>

                <template #footer>
                  <div class="job-card-footer">
                    <el-button
                      v-if="job.status === '暂停中'"
                      v-hasPerm="['module_task:cronjob:job:task']"
                      type="primary"
                      size="small"
                      icon="VideoPlay"
                      @click="handleResumeJob(job.id)"
                    >
                      恢复
                    </el-button>
                    <el-button
                      v-if="job.status === '运行中'"
                      v-hasPerm="['module_task:cronjob:job:task']"
                      type="warning"
                      size="small"
                      icon="VideoPause"
                      @click="handlePauseJob(job.id)"
                    >
                      暂停
                    </el-button>
                    <el-button
                      v-if="job.status !== '已停止' && job.status !== '未知'"
                      v-hasPerm="['module_task:cronjob:job:task']"
                      type="success"
                      size="small"
                      icon="CaretRight"
                      @click="handleRunJobNow(job.id)"
                    >
                      调试
                    </el-button>
                    <el-button
                      v-if="job.status !== '未知'"
                      v-hasPerm="['module_task:cronjob:job:task']"
                      type="danger"
                      size="small"
                      icon="Close"
                      @click="handleRemoveJob(job.id)"
                    >
                      移除
                    </el-button>
                    <el-button
                      v-hasPerm="['module_task:cronjob:job:query']"
                      type="info"
                      size="small"
                      icon="List"
                      @click="handleOpenExecutionLogDrawer(job)"
                    >
                      记录
                    </el-button>
                  </div>
                </template>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </template>
    </CrudContent>

    <EnhancedDialog v-model="consoleVisible" title="调度器控制台" width="900px">
      <div class="terminal-wrapper">
        <Terminal name="scheduler-console" :show-header="false" theme="dark" />
      </div>
      <template #footer>
        <el-button @click="handleRefreshConsole">刷新</el-button>
        <el-button @click="handleClearConsole">清空</el-button>
        <el-button type="primary" @click="consoleVisible = false">关闭</el-button>
      </template>
    </EnhancedDialog>

    <EnhancedDrawer v-model="executionLogDrawerVisible" title="执行记录" direction="rtl" size="80%">
      <div class="execution-log-drawer">
        <CrudSearch
          ref="logSearchRef"
          :search-config="logSearchConfig"
          @query-click="handleLogQueryClick"
          @reset-click="handleLogResetClick"
        />
        <CrudContent ref="logContentRef" :content-config="logContentConfig">
          <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
            <div class="data-table__content">
              <el-table
                :ref="tableRef as any"
                v-loading="loading"
                :data="data"
                border
                stripe
                height="100%"
                @selection-change="onSelectionChange"
              >
                <template #empty>
                  <el-empty :image-size="80" description="暂无数据" />
                </template>
                <el-table-column type="selection" align="center" min-width="55" />
                <el-table-column type="index" fixed label="序号" min-width="60">
                  <template #default="scope">
                    {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column
                  label="任务ID"
                  prop="job_id"
                  min-width="80"
                  show-overflow-tooltip
                />
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
                  min-width="200"
                  show-overflow-tooltip
                />
                <el-table-column
                  label="执行结果"
                  prop="result"
                  min-width="100"
                  show-overflow-tooltip
                />
                <el-table-column
                  label="错误信息"
                  prop="error"
                  min-width="100"
                  show-overflow-tooltip
                />
                <el-table-column label="执行元数据" min-width="100">
                  <template #default="scope">
                    <el-button
                      v-if="scope.row.job_state"
                      type="primary"
                      size="small"
                      link
                      icon="View"
                      @click="handleViewJobState(scope.row)"
                    >
                      查看
                    </el-button>
                    <span v-else>-</span>
                  </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="created_time" min-width="160" />
                <el-table-column label="更新时间" prop="updated_time" min-width="160" />
                <el-table-column label="操作" min-width="80" fixed="right">
                  <template #default="scope">
                    <el-button
                      v-hasPerm="['module_task:cronjob:job:delete']"
                      type="danger"
                      size="small"
                      link
                      icon="delete"
                      @click="handleLogRowDelete(scope.row.id)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </template>
        </CrudContent>
      </div>
    </EnhancedDrawer>

    <EnhancedDialog v-model="jobStateVisible" title="执行元数据" width="800px">
      <JsonPretty :value="jobStateData" height="400px" />
      <template #footer>
        <el-button type="primary" @click="jobStateVisible = false">关闭</el-button>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Job",
  inheritAttrs: false,
});

import JobAPI, {
  SchedulerStatus,
  SchedulerJob,
  JobLogPageQuery,
  JobLogTable,
} from "@/api/module_task/cronjob/job";
import CrudSearch from "@/components/CURD/CrudSearch.vue";
import CrudContent from "@/components/CURD/CrudContent.vue";
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import EnhancedDrawer from "@/components/Core/overlays/EnhancedDrawer.vue";
import type { ISearchConfig, IContentConfig, IObject } from "@/components/Crud/types";
import { ref, reactive, nextTick } from "vue";
import { Terminal, TerminalApi } from "vue-web-terminal";
import JsonPretty from "@/components/JsonPretty/index.vue";
import { useCrudList } from "@/components/Crud/useCrudList";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
const refreshMain = refreshList;

const schedulerStatus = ref<SchedulerStatus>({
  status: "未知",
  is_running: false,
  job_count: 0,
});

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_task:cronjob:job",
  colon: true,
  isExpandable: false,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "name",
      label: "任务名称",
      type: "input",
      attrs: { placeholder: "请输入任务名称", clearable: true, style: { width: "150px" } },
    },
    {
      prop: "status",
      label: "任务状态",
      type: "select",
      options: [
        { label: "运行中", value: "运行中" },
        { label: "暂停", value: "暂停" },
        { label: "停止", value: "停止" },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "150px" } },
    },
  ],
});

const contentConfig = reactive<IContentConfig>({
  permPrefix: "module_task:cronjob:job",
  cols: [],
  hideColumnFilter: true,
  showToolbar: false,
  pagination: false,
  indexAction: async (params) => {
    try {
      const statusRes = await JobAPI.getSchedulerStatus();
      schedulerStatus.value = statusRes.data.data;
    } catch (error: unknown) {
      console.error(error);
    }
    const response = await JobAPI.getSchedulerJobs();
    const raw = response.data?.data;
    let jobs = Array.isArray(raw) ? raw : [];
    const p = params as { name?: string; status?: string };
    const name = typeof p.name === "string" ? p.name.trim() : "";
    if (name) jobs = jobs.filter((job) => job.name.includes(name));
    if (p.status) jobs = jobs.filter((job) => job.status === p.status);
    // pagination 为 false 时 CrudContent 将整段返回值赋给 pageData，必须为列表数组
    return jobs;
  },
});

const consoleVisible = ref(false);

const executionLogDrawerVisible = ref(false);
const currentLogJobId = ref<string | undefined>(undefined);
const logSearchRef = ref<InstanceType<typeof CrudSearch>>();
const logContentRef = ref<InstanceType<typeof CrudContent>>();
const jobStateVisible = ref(false);
const jobStateData = ref<any>(null);

const logSearchConfig = reactive<ISearchConfig>({
  permPrefix: "module_task:cronjob:job",
  colon: true,
  isExpandable: false,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "status",
      label: "执行状态",
      type: "select",
      options: [
        { label: "待执行", value: "pending" },
        { label: "执行中", value: "running" },
        { label: "成功", value: "success" },
        { label: "失败", value: "failed" },
        { label: "超时", value: "timeout" },
        { label: "已取消", value: "cancelled" },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "120px" } },
    },
    {
      prop: "trigger_type",
      label: "触发方式",
      type: "select",
      options: [
        { label: "Cron表达式", value: "cron" },
        { label: "时间间隔", value: "interval" },
        { label: "固定日期", value: "date" },
        { label: "一次性任务", value: "manual" },
      ],
      attrs: { placeholder: "请选择", clearable: true, style: { width: "120px" } },
    },
  ],
});

const logContentConfig = reactive<IContentConfig>({
  permPrefix: "module_task:cronjob:job",
  cols: [],
  hideColumnFilter: true,
  toolbar: ["delete"],
  defaultToolbar: ["refresh"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const jobId = currentLogJobId.value;
    if (!jobId) {
      return { total: 0, list: [] };
    }
    const p = params as JobLogPageQuery;
    const res = await JobAPI.getJobLogList({
      page_no: p.page_no ?? 1,
      page_size: p.page_size ?? 10,
      job_id: jobId,
      job_name: undefined,
      status: p.status,
      trigger_type: p.trigger_type,
    });
    const page = res.data.data;
    return {
      total: page?.total ?? 0,
      list: page?.items ?? [],
    };
  },
  deleteAction: (ids) =>
    JobAPI.deleteJobLog(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n))
    ),
  deleteConfirm: {
    title: "警告",
    message: "确认删除选中的执行记录？",
    type: "warning",
  },
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

function getJobStatusType(status: string) {
  switch (status) {
    case "运行中":
      return "success";
    case "暂停中":
      return "warning";
    case "已停止":
      return "danger";
    case "未知":
      return "info";
    default:
      return "info";
  }
}

function getJobStatusLabel(status: string) {
  switch (status) {
    case "运行中":
      return "运行中";
    case "暂停中":
      return "暂停中";
    case "已停止":
      return "已停止";
    case "未知":
      return "未知";
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
    if (match) {
      const params = match[1];
      // 提取关键参数
      const month = params.match(/month='([^']+)'/);
      const day = params.match(/day='([^']+)'/);
      const hour = params.match(/hour='([^']+)'/);
      const minute = params.match(/minute='([^']+)'/);
      const second = params.match(/second='([^']+)'/);
      const dayOfWeek = params.match(/day_of_week='([^']+)'/);

      // 构建简化的 cron 表达式
      const parts = [];
      if (second && second[1] !== "'*'") parts.push(`秒:${second[1]}`);
      if (minute && minute[1] !== "'*'") parts.push(`分:${minute[1]}`);
      if (hour && hour[1] !== "'*'") parts.push(`时:${hour[1]}`);
      if (day && day[1] !== "'*'") parts.push(`日:${day[1]}`);
      if (month && month[1] !== "'*'") parts.push(`月:${month[1]}`);
      if (dayOfWeek && dayOfWeek[1] !== "'*'") parts.push(`周:${dayOfWeek[1]}`);

      if (parts.length === 0) {
        return "Cron: 每分钟";
      }
      return `Cron: ${parts.join(" ")}`;
    }
    return trigger;
  }

  if (trigger.includes("interval")) {
    const match = trigger.match(/interval\[([^\]]+)\]/);
    return match ? `间隔时长: ${match[1]}` : trigger;
  }

  if (trigger.includes("date")) {
    const match = trigger.match(/date\[([^\]]+)\]/);
    return match ? `执行日期: ${match[1]}` : trigger;
  }

  return trigger;
}

async function handleSyncJobs() {
  try {
    await JobAPI.syncJobsToDb();
    await refreshMain();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleStartScheduler() {
  try {
    await JobAPI.startScheduler();
    await refreshMain();
  } catch (error: any) {
    console.error(error);
  }
}

async function handlePauseScheduler() {
  try {
    await JobAPI.pauseScheduler();
    await refreshMain();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeScheduler() {
  try {
    await JobAPI.resumeScheduler();
    await refreshMain();
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
    await refreshMain();
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
    await refreshMain();
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
    await refreshMain();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeJob(jobId: string) {
  try {
    await JobAPI.resumeJob(jobId);
    await refreshMain();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleRunJobNow(jobId: string) {
  try {
    await JobAPI.runJobNow(jobId);
    await refreshMain();
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
        await refreshMain();
      } catch (error: any) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

async function handleOpenExecutionLogDrawer(job: IObject) {
  currentLogJobId.value = (job as SchedulerJob).id;
  executionLogDrawerVisible.value = true;
  await nextTick();
  logContentRef.value?.fetchPageData(logSearchRef.value?.getQueryParams() ?? {}, true);
}

function handleLogQueryClick() {
  logContentRef.value?.fetchPageData(logSearchRef.value!.getQueryParams(), true);
}

function handleLogResetClick() {
  logContentRef.value?.fetchPageData(logSearchRef.value!.getQueryParams(), true);
}

function handleLogRowDelete(id: number) {
  logContentRef.value?.handleDelete(id);
}

function getTriggerTypeLabel(type: string | undefined) {
  const map: Record<string, string> = {
    cron: "Cron表达式",
    interval: "时间间隔",
    date: "固定日期",
    manual: "一次性任务",
  };
  return map[type || ""] || type || "-";
}

function getLogStatusType(status: string): "primary" | "success" | "warning" | "info" | "danger" {
  const map: Record<string, "primary" | "success" | "warning" | "info" | "danger"> = {
    pending: "info",
    running: "primary",
    success: "success",
    failed: "danger",
    timeout: "warning",
    cancelled: "info",
  };
  return map[status] || "info";
}

function getLogStatusLabel(status: string) {
  const map: Record<string, string> = {
    pending: "待执行",
    running: "执行中",
    success: "成功",
    failed: "失败",
    timeout: "超时",
    cancelled: "已取消",
  };
  return map[status] || status;
}

function handleViewJobState(row: JobLogTable | IObject) {
  const jobState = (row as JobLogTable).job_state;
  if (jobState) {
    try {
      jobStateData.value = JSON.parse(jobState);
    } catch {
      jobStateData.value = jobState;
    }
    jobStateVisible.value = true;
  }
}
</script>

<style scoped>
.job-page :deep(.data-table) {
  height: 100%;
}

.status-content {
  display: flex;
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
}

.status-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.terminal-wrapper {
  height: 500px;
}

.job-card-header {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

.job-card-title {
  display: flex;
  flex: 1;
  gap: 8px;
  align-items: center;
  min-width: 0;
}

.job-index {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(
    135deg,
    var(--el-color-primary) 0%,
    var(--el-color-primary-dark-2) 100%
  );
  border-radius: 50%;
}

.job-name {
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.job-info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 13px;
}

.job-info-item:last-child {
  margin-bottom: 0;
}

.job-info-label {
  flex-shrink: 0;
  width: 70px;
}

.job-info-value {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.job-card-footer {
  display: flex;
  justify-content: space-between;
}

.job-card-footer .el-button {
  flex: 1;
}

.execution-log-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.execution-log-drawer :deep(.el-card.data-table) {
  flex: 1;
  min-height: 0;
  margin-top: 16px;
}
</style>
