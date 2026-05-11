<!-- 调度任务：Art + useTable（主列表卡片；抽屉内表格） -->
<template>
  <div class="art-full-height job-page flex flex-col min-h-0">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="jobSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleJobSearchBarSearch"
      @reset="onJobResetSearch"
    />

    <ElCard
      class="flex flex-1 min-h-0 flex-col art-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <FaTableHeader
        v-model:columns="jobColumnChecks"
        v-model:showSearchBar="showSearchBar"
        layout="search,refresh"
        :loading="jobLoading"
        @refresh="refreshJobList"
      >
        <template #left>
          <div class="status-content">
            <span>调度器监控</span>
            <div class="status-item">
              <span class="label">状态：</span>
              <ElTag :type="getSchedulerStatusType(schedulerStatus.status)" size="large">
                {{ schedulerStatus.status }}
              </ElTag>
            </div>
            <div class="status-item">
              <span class="label">运行中：</span>
              <ElTag :type="schedulerStatus.is_running ? 'success' : 'danger'" size="large">
                {{ schedulerStatus.is_running ? "是" : "否" }}
              </ElTag>
            </div>
            <div class="status-item">
              <span class="label">任务数量：</span>
              <ElTag type="warning" size="large">{{ schedulerStatus.job_count }}</ElTag>
            </div>
            <div class="status-actions">
              <ElButton
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="success"
                icon="VideoPlay"
                :disabled="schedulerStatus.status !== '停止'"
                @click="handleStartScheduler"
              >
                启动
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="warning"
                icon="VideoPause"
                :disabled="schedulerStatus.status !== '运行中'"
                @click="handlePauseScheduler"
              >
                暂停
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="primary"
                icon="RefreshRight"
                :disabled="schedulerStatus.status !== '暂停'"
                @click="handleResumeScheduler"
              >
                恢复
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="danger"
                icon="SwitchButton"
                :disabled="schedulerStatus.status === '停止'"
                @click="handleShutdownScheduler"
              >
                关闭
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:task']"
                type="danger"
                icon="Delete"
                :disabled="schedulerStatus.job_count === 0"
                @click="handleClearAllJobs"
              >
                清空任务
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:query']"
                type="info"
                icon="Monitor"
                @click="handleOpenConsole"
              >
                控制台
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:scheduler']"
                type="primary"
                icon="Refresh"
                @click="handleSyncJobs"
              >
                同步
              </ElButton>
              <ElButton
                v-hasPerm="['module_task:cronjob:job:update']"
                type="warning"
                icon="Refresh"
                @click="refreshJobList"
              >
                刷新
              </ElButton>
            </div>
          </div>
        </template>
      </FaTableHeader>

      <div v-loading="jobLoading" class="job-cards-container min-h-0 flex-1 overflow-auto">
        <ElEmpty
          v-if="!jobLoading && (!jobList || jobList.length === 0)"
          :image-size="80"
          description="暂无数据"
        />
        <ElRow v-else :gutter="16">
          <ElCol
            v-for="(job, index) in jobList"
            :key="job.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
            class="job-card-col"
          >
            <ElCard class="job-card" shadow="hover">
              <template #header>
                <div class="job-card-header">
                  <div class="job-card-title">
                    <span class="job-index">{{ index + 1 }}</span>
                    <span class="job-name" :title="job.name">{{ job.name }}</span>
                  </div>
                  <ElTag :type="getJobStatusType(job.status)" size="small">
                    {{ getJobStatusLabel(job.status) }}
                  </ElTag>
                </div>
              </template>

              <div class="job-card-body">
                <div class="job-info-item">
                  <span class="job-info-label">任务ID:</span>
                  <span class="job-info-value">{{ job.id }}</span>
                </div>
                <div class="job-info-item">
                  <span class="job-info-label">触发器:</span>
                  <ElTag
                    v-if="String(job.trigger ?? '').includes('cron')"
                    type="primary"
                    size="small"
                    class="job-trigger-tag"
                  >
                    <ElIcon><Clock /></ElIcon>
                    {{ formatTrigger(job.trigger) }}
                  </ElTag>
                  <ElTag
                    v-else-if="String(job.trigger ?? '').includes('interval')"
                    type="success"
                    size="small"
                    class="job-trigger-tag"
                  >
                    <ElIcon><Timer /></ElIcon>
                    {{ formatTrigger(job.trigger) }}
                  </ElTag>
                  <ElTag
                    v-else-if="String(job.trigger ?? '').includes('date')"
                    type="warning"
                    size="small"
                    class="job-trigger-tag"
                  >
                    <ElIcon><Calendar /></ElIcon>
                    {{ formatTrigger(job.trigger) }}
                  </ElTag>
                  <ElTag v-else type="info" size="small" class="job-trigger-tag">
                    {{ formatTrigger(job.trigger) }}
                  </ElTag>
                </div>
                <div class="job-info-item">
                  <span class="job-info-label">下次执行:</span>
                  <span class="job-info-value">{{ job.next_run_time || "无" }}</span>
                </div>
              </div>

              <template #footer>
                <div class="job-card-footer">
                  <ElButton
                    v-if="job.status === '暂停中'"
                    v-hasPerm="['module_task:cronjob:job:task']"
                    type="primary"
                    size="small"
                    icon="VideoPlay"
                    @click="handleResumeJob(job.id)"
                  >
                    恢复
                  </ElButton>
                  <ElButton
                    v-if="job.status === '运行中'"
                    v-hasPerm="['module_task:cronjob:job:task']"
                    type="warning"
                    size="small"
                    icon="VideoPause"
                    @click="handlePauseJob(job.id)"
                  >
                    暂停
                  </ElButton>
                  <ElButton
                    v-if="job.status !== '已停止' && job.status !== '未知'"
                    v-hasPerm="['module_task:cronjob:job:task']"
                    type="success"
                    size="small"
                    icon="CaretRight"
                    @click="handleRunJobNow(job.id)"
                  >
                    调试
                  </ElButton>
                  <ElButton
                    v-if="job.status !== '未知'"
                    v-hasPerm="['module_task:cronjob:job:task']"
                    type="danger"
                    size="small"
                    icon="Close"
                    @click="handleRemoveJob(job.id)"
                  >
                    移除
                  </ElButton>
                  <ElButton
                    v-hasPerm="['module_task:cronjob:job:query']"
                    type="info"
                    size="small"
                    icon="List"
                    @click="handleOpenExecutionLogDrawer(job)"
                  >
                    记录
                  </ElButton>
                </div>
              </template>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>
    </ElCard>

    <FaDialog v-model="consoleVisible" title="调度器控制台" width="900px">
      <div class="terminal-wrapper">
        <Terminal name="scheduler-console" :show-header="false" theme="dark" />
      </div>
      <template #footer>
        <ElButton @click="handleRefreshConsole">刷新</ElButton>
        <ElButton @click="handleClearConsole">清空</ElButton>
        <ElButton type="primary" @click="consoleVisible = false">关闭</ElButton>
      </template>
    </FaDialog>

    <FaDrawer v-model="executionLogDrawerVisible" title="执行记录" direction="rtl" size="80%">
      <div class="execution-log-drawer flex flex-col min-h-0">
        <FaSearchBar
          ref="logSearchBarRef"
          v-model="logSearchForm"
          :items="logSearchItems"
          :rules="logSearchBarRules"
          :is-expand="false"
          :show-expand="false"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          @search="handleLogSearchBarSearch"
          @reset="onLogResetSearch"
        />
        <ElCard class="art-table-card log-table-card mt-3 flex flex-1 min-h-0 flex-col">
          <FaTableHeader
            v-model:columns="logColumnChecks"
            layout="search,refresh"
            :loading="logLoading"
            @refresh="refreshLogData"
          >
            <template #left>
              <FaTableHeaderLeft
                :remove-ids="logSelectedIds"
                :perm-delete="['module_task:cronjob:job:delete']"
                :delete-loading="logBatchDeleting"
                @delete="handleLogBatchDelete"
              />
            </template>
          </FaTableHeader>
          <FaTable
            ref="logFaTableRef"
            row-key="id"
            :loading="logLoading"
            :data="logTableData"
            :columns="logColumns"
            :pagination="logPaginationBind"
            @selection-change="onLogTableSelectionChange"
            @pagination:size-change="logHandleSizeChange"
            @pagination:current-change="logHandleCurrentChange"
          >
            <template #log_job_state="{ row }">
              <ElButton
                v-if="row.job_state"
                type="primary"
                size="small"
                link
                @click="handleViewJobState(row)"
              >
                查看
              </ElButton>
              <span v-else>-</span>
            </template>
            <template #log_operation="{ row }">
              <ElButton
                v-hasPerm="['module_task:cronjob:job:delete']"
                type="danger"
                size="small"
                link
                @click="deleteLogRow(row.id)"
              >
                删除
              </ElButton>
            </template>
          </FaTable>
        </ElCard>
      </div>
    </FaDrawer>

    <FaDialog v-model="jobStateVisible" title="执行元数据" width="800px">
      <JsonPretty :value="jobStateData" height="400px" />
      <template #footer>
        <ElButton type="primary" @click="jobStateVisible = false">关闭</ElButton>
      </template>
    </FaDialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Job",
  inheritAttrs: false,
});

import JobAPI, { SchedulerStatus, SchedulerJob, JobLogTable } from "@/api/module_task/cronjob/job";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import FaDrawer from "@/components/modal/fa-drawer/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaTable from "@/components/tables/fa-table/index.vue";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";
import { useTable } from "@/hooks/core/useTable";
import type { ColumnOption } from "@/types/component";
import { Calendar, Clock, Timer } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { computed, h, nextTick, ref } from "vue";
import { Terminal, TerminalApi } from "vue-web-terminal";

const schedulerStatus = ref<SchedulerStatus>({
  status: "未知",
  is_running: false,
  job_count: 0,
});

type JobSearchForm = {
  name?: string;
  status?: string;
};

function buildJobReplaceParams(u: JobSearchForm): Record<string, unknown> {
  return {
    name: u.name,
    status: u.status,
  };
}

const searchForm = ref<JobSearchForm>({
  name: undefined,
  status: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const jobSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "任务名称",
    key: "name",
    type: "input",
    placeholder: "请输入任务名称",
    clearable: true,
    span: 6,
  },
  {
    label: "任务状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      clearable: true,
      options: [
        { label: "运行中", value: "运行中" },
        { label: "暂停", value: "暂停" },
        { label: "停止", value: "停止" },
      ],
    },
    span: 6,
  },
]);

async function loadSchedulerStatus() {
  try {
    const statusRes = await JobAPI.getSchedulerStatus();
    schedulerStatus.value = statusRes.data.data;
  } catch (error: unknown) {
    console.error(error);
  }
}

/** 调度器任务列表为全量列表接口，无分页；筛选在前端完成 */
const jobList = ref<SchedulerJob[]>([]);
const jobLoading = ref(false);
/** 主区域为卡片列表无表格列配置，仅占位满足 FaTableHeader v-model */
const jobColumnChecks = ref<ColumnOption<SchedulerJob>[]>([]);

function matchesJobStatusFilter(jobStatus: string | undefined, filter?: string): boolean {
  if (!filter) return true;
  const map: Record<string, string[]> = {
    运行中: ["运行中"],
    暂停: ["暂停", "暂停中"],
    停止: ["停止", "已停止"],
  };
  const aliases = map[filter];
  if (!aliases) return true;
  const s = jobStatus ?? "";
  return aliases.some((a) => s === a || s.includes(a));
}

async function fetchSchedulerJobs() {
  jobLoading.value = true;
  try {
    const res = await JobAPI.getSchedulerJobs();
    const raw = res.data?.data;
    const list: SchedulerJob[] = Array.isArray(raw) ? raw : [];
    const nameQ = searchForm.value.name?.trim();
    const statusQ = searchForm.value.status;
    jobList.value = list.filter((j) => {
      if (nameQ && !(j.name ?? "").includes(nameQ)) return false;
      if (!matchesJobStatusFilter(j.status, statusQ)) return false;
      return true;
    });
    await loadSchedulerStatus();
  } catch (error: unknown) {
    console.error(error);
    jobList.value = [];
  } finally {
    jobLoading.value = false;
  }
}

const refreshJobList = fetchSchedulerJobs;

async function handleJobSearchBarSearch() {
  await searchBarRef.value?.validate?.();
  replaceJobSearchParams(buildJobReplaceParams(params));
  getJobList();
}

async function onJobResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
  };
  await resetJobSearchParams();
}

type LogSearchForm = {
  status?: string;
  trigger_type?: string;
};

function buildLogReplaceParams(u: LogSearchForm): Record<string, unknown> {
  return {
    status: u.status,
    trigger_type: u.trigger_type,
  };
}

const logSearchForm = ref<LogSearchForm>({
  status: undefined,
  trigger_type: undefined,
});

const logSearchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const logSearchBarRules: Record<string, unknown> = {};

const logSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "执行状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      clearable: true,
      options: [
        { label: "待执行", value: "pending" },
        { label: "执行中", value: "running" },
        { label: "成功", value: "success" },
        { label: "失败", value: "failed" },
        { label: "超时", value: "timeout" },
        { label: "已取消", value: "cancelled" },
      ],
    },
    span: 8,
  },
  {
    label: "触发方式",
    key: "trigger_type",
    type: "select",
    props: {
      placeholder: "请选择",
      clearable: true,
      options: [
        { label: "Cron表达式", value: "cron" },
        { label: "时间间隔", value: "interval" },
        { label: "固定日期", value: "date" },
        { label: "一次性任务", value: "manual" },
      ],
    },
    span: 8,
  },
]);

const currentLogJobId = ref<string | undefined>(undefined);
const logFaTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const logSelectedRows = ref<JobLogTable[]>([]);
const logSelectedIds = computed(() =>
  logSelectedRows.value.map((r) => r.id).filter((id): id is number => typeof id === "number")
);
const logBatchDeleting = ref(false);

function onLogTableSelectionChange(rows: JobLogTable[]) {
  logSelectedRows.value = rows;
}

const {
  columns: logColumns,
  columnChecks: logColumnChecks,
  data: logTableData,
  loading: logLoading,
  pagination: logPagination,
  getData: getLogData,
  replaceSearchParams: replaceLogSearchParams,
  resetSearchParams: resetLogSearchParams,
  handleSizeChange: logHandleSizeChange,
  handleCurrentChange: logHandleCurrentChange,
  refreshData: refreshLogData,
  refreshRemove: refreshLogRemove,
} = useTable({
  core: {
    apiFn: JobAPI.getJobLogList,
    immediate: false,
    apiParams: {
      page_no: 1,
      page_size: 10,
      job_id: "",
      status: undefined,
      trigger_type: undefined,
    },
    columnsFactory: (): ColumnOption<JobLogTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "job_id",
        label: "任务ID",
        minWidth: 80,
        showOverflowTooltip: true,
      },
      {
        prop: "job_name",
        label: "任务名称",
        minWidth: 140,
        showOverflowTooltip: true,
      },
      {
        prop: "trigger_type",
        label: "触发方式",
        minWidth: 120,
        formatter: (row) =>
          h(ElTag, { size: "small" }, () => getTriggerTypeLabel(row.trigger_type)),
      },
      {
        prop: "status",
        label: "状态",
        minWidth: 80,
        formatter: (row) =>
          h(ElTag, { type: getLogStatusType(row.status), size: "small" }, () =>
            getLogStatusLabel(row.status)
          ),
      },
      {
        prop: "next_run_time",
        label: "下次执行时间",
        minWidth: 200,
        showOverflowTooltip: true,
      },
      {
        prop: "result",
        label: "执行结果",
        minWidth: 100,
        showOverflowTooltip: true,
      },
      {
        prop: "error",
        label: "错误信息",
        minWidth: 100,
        showOverflowTooltip: true,
      },
      {
        prop: "job_state",
        label: "执行元数据",
        minWidth: 100,
        useSlot: true,
        slotName: "log_job_state",
      },
      {
        prop: "created_time",
        label: "创建时间",
        minWidth: 160,
        showOverflowTooltip: true,
      },
      {
        prop: "updated_time",
        label: "更新时间",
        minWidth: 160,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 88,
        fixed: "right",
        align: "center",
        useSlot: true,
        slotName: "log_operation",
      },
    ],
  },
});

function deleteLogRow(id: number | undefined) {
  if (id == null) return;
  ElMessageBox.confirm("确认删除该执行记录？", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await JobAPI.deleteJobLog([id]);
      ElMessage.success("删除成功");
      logFaTableRef.value?.elTableRef?.clearSelection();
      await refreshLogRemove();
    })
    .catch(() => {});
}

function handleLogBatchDelete() {
  const ids = logSelectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm("确认删除选中的执行记录？", "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        logBatchDeleting.value = true;
        await JobAPI.deleteJobLog(ids);
        ElMessage.success("删除成功");
        logSelectedRows.value = [];
        await refreshLogRemove();
      } finally {
        logBatchDeleting.value = false;
      }
    })
    .catch(() => {});
}

const logPaginationBind = computed(() => {
  const p = logPagination as unknown as {
    current?: number;
    size?: number;
    total?: number;
    page_no?: number;
    page_size?: number;
  };
  return {
    current: p.current ?? p.page_no ?? 1,
    size: p.size ?? p.page_size ?? 10,
    total: p.total ?? 0,
  };
});

async function handleLogSearchBarSearch(params: LogSearchForm) {
  await logSearchBarRef.value?.validate?.();
  if (!currentLogJobId.value) return;
  replaceLogSearchParams({
    ...buildLogReplaceParams(params),
    job_id: currentLogJobId.value,
  });
  getLogData();
}

async function onLogResetSearch() {
  logSearchForm.value = {
    status: undefined,
    trigger_type: undefined,
  };
  await resetLogSearchParams();
  if (currentLogJobId.value) {
    replaceLogSearchParams({ job_id: currentLogJobId.value });
    getLogData();
  }
}

const consoleVisible = ref(false);

const executionLogDrawerVisible = ref(false);
const jobStateVisible = ref(false);
const jobStateData = ref<any>(null);

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
    await refreshJobList();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleStartScheduler() {
  try {
    await JobAPI.startScheduler();
    await refreshJobList();
  } catch (error: any) {
    console.error(error);
  }
}

async function handlePauseScheduler() {
  try {
    await JobAPI.pauseScheduler();
    await refreshJobList();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeScheduler() {
  try {
    await JobAPI.resumeScheduler();
    await refreshJobList();
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
    await refreshJobList();
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
    await refreshJobList();
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
    await refreshJobList();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleResumeJob(jobId: string) {
  try {
    await JobAPI.resumeJob(jobId);
    await refreshJobList();
  } catch (error: any) {
    console.error(error);
  }
}

async function handleRunJobNow(jobId: string) {
  try {
    await JobAPI.runJobNow(jobId);
    await refreshJobList();
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
        await refreshJobList();
      } catch (error: any) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

async function handleOpenExecutionLogDrawer(job: SchedulerJob) {
  currentLogJobId.value = job.id;
  logSearchForm.value = {
    status: undefined,
    trigger_type: undefined,
  };
  executionLogDrawerVisible.value = true;
  await nextTick();
  replaceLogSearchParams({
    job_id: job.id,
    page_no: 1,
    page_size: 10,
  });
  getLogData();
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

function handleViewJobState(row: JobLogTable) {
  const jobState = row.job_state;
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
  height: 100%;
}

.log-table-card {
  flex: 1;
  min-height: 0;
}

.execution-log-drawer :deep(.el-card.data-table) {
  flex: 1;
  min-height: 0;
}
</style>
