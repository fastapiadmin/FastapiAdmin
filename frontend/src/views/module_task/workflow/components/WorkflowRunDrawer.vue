<template>
  <el-drawer v-model="drawerVisible" size="80%">
    <div class="app-container">
      <!-- 搜索区域 -->
      <div v-show="searchVisible" class="search-container">
        <el-form
          ref="queryFormRef"
          :model="queryFormData"
          label-suffix=":"
          :inline="true"
          @submit.prevent="handleQuery"
        >
          <el-form-item prop="workflow_name" label="工作流名称">
            <el-input
              v-model="queryFormData.workflow_name"
              placeholder="请输入工作流名称"
              clearable
            />
          </el-form-item>
          <el-form-item prop="status" label="运行状态">
            <el-select
              v-model="queryFormData.status"
              placeholder="请选择运行状态"
              style="width: 150px"
              clearable
            >
              <el-option label="待执行" value="pending" />
              <el-option label="运行中" value="running" />
              <el-option label="已暂停" value="paused" />
              <el-option label="已完成" value="completed" />
              <el-option label="失败" value="failed" />
              <el-option label="已取消" value="cancelled" />
              <el-option label="已终止" value="terminated" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="isExpand" prop="initiator" label="发起人">
            <UserTableSelect
              v-model="queryFormData.initiator"
              @confirm-click="handleConfirm"
              @clear-click="handleQuery"
            />
          </el-form-item>
          <el-form-item v-if="isExpand" prop="created_time" label="创建时间">
            <DatePicker v-model="startDateRange" @update:model-value="handleStartDateRangeChange" />
          </el-form-item>
          <el-form-item v-if="isExpand" prop="updated_time" label="更新时间">
            <DatePicker v-model="endDateRange" @update:model-value="handleEndDateRangeChange" />
          </el-form-item>
          <el-form-item>
            <el-button
              v-hasPerm="['module_task:workflow_run:query']"
              type="primary"
              icon="search"
              @click="handleQuery"
            >
              查询
            </el-button>
            <el-button
              v-hasPerm="['module_task:workflow_run:query']"
              icon="refresh"
              @click="handleResetQuery"
            >
              重置
            </el-button>
            <template v-if="isExpandable">
              <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
                {{ isExpand ? "收起" : "展开" }}
                <el-icon>
                  <template v-if="isExpand">
                    <ArrowUp />
                  </template>
                  <template v-else>
                    <ArrowDown />
                  </template>
                </el-icon>
              </el-link>
            </template>
          </el-form-item>
        </el-form>
      </div>

      <!-- 内容区域 -->
      <el-card class="data-table">
        <template #header>
          <div class="card-header">
            <span>
              流程执行记录
              <el-tooltip content="流程执行记录列表">
                <QuestionFilled class="w-4 h-4 mx-1" />
              </el-tooltip>
            </span>
          </div>
        </template>

        <!-- 功能区域 -->
        <div class="data-table__toolbar">
          <div class="data-table__toolbar--left">
            <el-row :gutter="10">
              <el-col :span="1.5">
                <el-button
                  v-hasPerm="['module_task:workflow_run:delete']"
                  type="danger"
                  icon="delete"
                  :disabled="selectIds.length === 0"
                  @click="handleDelete(selectIds)"
                >
                  批量删除
                </el-button>
              </el-col>
            </el-row>
          </div>
          <div class="data-table__toolbar--right">
            <el-row :gutter="10">
              <el-col :span="1.5">
                <el-tooltip content="搜索显示/隐藏">
                  <el-button
                    v-hasPerm="['*:*:*']"
                    type="info"
                    icon="search"
                    circle
                    @click="searchVisible = !searchVisible"
                  />
                </el-tooltip>
              </el-col>
              <el-col :span="1.5">
                <el-tooltip content="刷新">
                  <el-button
                    v-hasPerm="['module_task:workflow_run:query']"
                    type="primary"
                    icon="refresh"
                    circle
                    @click="handleRefresh"
                  />
                </el-tooltip>
              </el-col>
              <el-col :span="1.5">
                <el-popover placement="bottom" trigger="click">
                  <template #reference>
                    <el-button type="danger" icon="operation" circle></el-button>
                  </template>
                  <el-scrollbar max-height="350px">
                    <template v-for="column in tableColumns" :key="column.prop">
                      <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                    </template>
                  </el-scrollbar>
                </el-popover>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 表格区域 -->
        <el-table
          ref="tableRef"
          v-loading="loading"
          :data="pageTableData"
          highlight-current-row
          class="data-table__content"
          height="450"
          max-height="450"
          border
          stripe
          @selection-change="handleSelectionChange"
        >
          <template #empty>
            <el-empty :image-size="80" description="暂无数据" />
          </template>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
            type="selection"
            min-width="55"
            align="center"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'index')?.show"
            fixed
            label="序号"
            min-width="60"
          >
            <template #default="scope">
              {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
            </template>
          </el-table-column>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'id')?.show"
            label="ID"
            prop="id"
            min-width="80"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'workflow_name')?.show"
            label="工作流名称"
            prop="workflow_name"
            min-width="200"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'workflow_version')?.show"
            label="工作流版本"
            prop="workflow_version"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'business_key')?.show"
            label="业务键"
            prop="business_key"
            min-width="150"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'initiator_name')?.show"
            label="发起人"
            prop="initiator_name"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'status')?.show"
            label="状态"
            prop="status"
            min-width="100"
          >
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'start_time')?.show"
            label="开始时间"
            prop="start_time"
            min-width="180"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'end_time')?.show"
            label="结束时间"
            prop="end_time"
            min-width="180"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'duration')?.show"
            label="执行时长(秒)"
            prop="duration"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'retry_count')?.show"
            label="重试次数"
            prop="retry_count"
            min-width="100"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'error_message')?.show"
            label="错误信息"
            prop="error_message"
            min-width="200"
            show-overflow-tooltip
          >
            <template #default="scope">
              <span v-if="scope.row.error_message" class="error-message">
                {{ scope.row.error_message }}
              </span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
            fixed="right"
            label="操作"
            align="center"
            min-width="280"
          >
            <template #default="scope">
              <el-button
                v-hasPerm="['module_task:workflow_run:detail']"
                type="info"
                size="small"
                link
                icon="document"
                @click="handleOpenDialog('detail', scope.row)"
              >
                详情
              </el-button>
              <el-dropdown
                v-if="scope.row.status === 'running' || scope.row.status === 'paused'"
                @command="(e) => handleAction(e, scope.row)"
              >
                <el-button
                  v-hasPerm="['module_task:workflow_run:action']"
                  type="primary"
                  size="small"
                  link
                >
                  操作
                  <el-icon><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item v-if="scope.row.status === 'running'" command="pause">
                      暂停
                    </el-dropdown-item>
                    <el-dropdown-item v-if="scope.row.status === 'paused'" command="resume">
                      恢复
                    </el-dropdown-item>
                    <el-dropdown-item command="terminate">终止</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-button
                v-if="scope.row.status === 'failed'"
                v-hasPerm="['module_task:workflow_run:retry']"
                type="primary"
                size="small"
                link
                icon="refresh"
                @click="handleRetry(scope.row)"
              >
                重试
              </el-button>
              <el-button
                v-if="scope.row.status === 'failed'"
                v-hasPerm="['module_task:workflow_run:detail']"
                type="warning"
                size="small"
                link
                icon="warning"
                @click="handleShowErrorSuggestion(scope.row)"
              >
                错误建议
              </el-button>
              <el-button
                v-hasPerm="['module_task:workflow_run:delete']"
                type="danger"
                size="small"
                link
                icon="delete"
                @click="handleDelete([scope.row.id])"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页区域 -->
        <template #footer>
          <pagination
            v-model:total="total"
            v-model:page="queryFormData.page_no"
            v-model:limit="queryFormData.page_size"
            @pagination="loadingData"
          />
        </template>
      </el-card>

      <!-- 详情弹窗 -->
      <el-dialog
        v-model="detailDialogVisible.visible"
        :title="detailDialogVisible.title"
        width="60%"
        @close="handleCloseDialog"
      >
        <el-descriptions :column="2" border class="detail-info">
          <el-descriptions-item label="执行ID">{{ detailFormData.id }}</el-descriptions-item>
          <el-descriptions-item label="工作流名称">
            {{ detailFormData.workflow_name }}
          </el-descriptions-item>
          <el-descriptions-item label="工作流版本">
            {{ detailFormData.workflow_version }}
          </el-descriptions-item>
          <el-descriptions-item label="业务键">
            {{ detailFormData.business_key || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="发起人">
            {{ detailFormData.initiator_name || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(detailFormData.status)">
              {{ getStatusText(detailFormData.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开始时间">
            {{ detailFormData.start_time || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="结束时间">
            {{ detailFormData.end_time || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="执行时长">
            {{ detailFormData.duration ? `${detailFormData.duration}秒` : "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="重试次数">
            {{ detailFormData.retry_count }}/{{ detailFormData.max_retry }}
          </el-descriptions-item>
          <el-descriptions-item label="错误信息" :span="2">
            <span v-if="detailFormData.error_message" class="error-message">
              {{ detailFormData.error_message }}
            </span>
            <span v-else>-</span>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>执行进度</el-divider>

        <div class="progress-container">
          <el-progress
            :percentage="executionProgress"
            :status="
              detailFormData.status === 'failed'
                ? 'exception'
                : detailFormData.status === 'completed'
                  ? 'success'
                  : ''
            "
            :stroke-width="20"
          />
          <div class="progress-stats">
            <el-statistic title="总节点数" :value="totalNodes" />
            <el-statistic title="已完成" :value="completedNodes" />
            <el-statistic title="运行中" :value="runningNodes" />
            <el-statistic title="失败" :value="failedNodes" />
          </div>
        </div>

        <template #footer>
          <el-button @click="handleCloseDialog">关闭</el-button>
        </template>
      </el-dialog>

      <!-- 错误建议弹窗 -->
      <el-dialog v-model="errorSuggestionVisible" title="错误处理建议" width="600px">
        <el-alert
          v-if="selectedErrorRun"
          :title="`工作流执行失败: ${selectedErrorRun.workflow_name}`"
          type="error"
          :closable="false"
          show-icon
          style="margin-bottom: 16px"
        >
          <template #default>
            <div class="error-content">
              <div class="error-message">
                <strong>错误信息:</strong>
                {{ selectedErrorRun.error_message }}
              </div>
              <div class="retry-info">
                <strong>重试次数:</strong>
                {{ selectedErrorRun.retry_count }}/{{ selectedErrorRun.max_retry }}
              </div>
            </div>
          </template>
        </el-alert>

        <el-card v-if="errorSuggestion" shadow="never" class="suggestion-card">
          <template #header>
            <div class="card-header">
              <span>处理建议</span>
            </div>
          </template>
          <div class="suggestion-content">
            <el-steps direction="vertical" :active="errorSuggestion.steps.length">
              <el-step
                v-for="(step, index) in errorSuggestion.steps"
                :key="index"
                :title="step.title"
                :description="step.description"
              />
            </el-steps>
          </div>
        </el-card>

        <template #footer>
          <el-button @click="errorSuggestionVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleRetryFromSuggestion">立即重试</el-button>
        </template>
      </el-dialog>
    </div>
  </el-drawer>
</template>

<script setup lang="ts">
defineOptions({
  name: "WorkflowRunDrawer",
  inheritAttrs: false,
});

import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { ArrowUp, ArrowDown, QuestionFilled } from "@element-plus/icons-vue";
import {
  WorkflowRunAPI,
  type WorkflowRunTable,
  type WorkflowRunPageQuery,
} from "@/api/module_task/workflow";
import DatePicker from "@/components/DatePicker/index.vue";
import { formatToDateTime } from "@/utils/dateUtil";

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  workflowName: {
    type: String,
    default: undefined,
  },
});

const emit = defineEmits(["update:visible"]);

const drawerVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

const queryFormRef = ref();
const tableRef = ref();

const searchVisible = ref(true);
const isExpand = ref(false);
const isExpandable = ref(true);
const loading = ref(false);
const selectIds = ref<number[]>([]);
const total = ref(0);

const queryFormData = reactive<WorkflowRunPageQuery>({
  page_no: 1,
  page_size: 10,
  workflow_name: "",
  status: "",
  initiator: undefined,
  created_time: [],
  updated_time: [],
});

const startDateRange = ref<[Date, Date]>();
const endDateRange = ref<[Date, Date]>();

const pageTableData = ref<WorkflowRunTable[]>([]);

const tableColumns = ref([
  { prop: "selection", label: "选择", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "id", label: "ID", show: true },
  { prop: "workflow_name", label: "工作流名称", show: true },
  { prop: "workflow_version", label: "工作流版本", show: true },
  { prop: "business_key", label: "业务键", show: true },
  { prop: "initiator_name", label: "发起人", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "start_time", label: "开始时间", show: true },
  { prop: "end_time", label: "结束时间", show: true },
  { prop: "duration", label: "执行时长(秒)", show: true },
  { prop: "retry_count", label: "重试次数", show: true },
  { prop: "error_message", label: "错误信息", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const detailDialogVisible = reactive({
  visible: false,
  type: "",
  title: "",
});

const detailFormData = ref<WorkflowRunTable>({
  id: 0,
  workflow_id: 0,
  workflow_name: "",
  workflow_version: "",
  business_key: "",
  initiator: 0,
  initiator_name: "",
  status: "",
  start_time: "",
  end_time: "",
  duration: 0,
  retry_count: 0,
  max_retry: 3,
  error_message: "",
  node_executions: [],
});

const errorSuggestionVisible = ref(false);
const selectedErrorRun = ref<WorkflowRunTable>();
const errorSuggestion = ref<{
  steps: Array<{ title: string; description: string }>;
}>();

const executionProgress = computed(() => {
  if (!detailFormData.value.node_executions || detailFormData.value.node_executions.length === 0) {
    return 0;
  }
  const completed = detailFormData.value.node_executions.filter(
    (n) => n.status === "completed"
  ).length;
  return Math.round((completed / detailFormData.value.node_executions.length) * 100);
});

const totalNodes = computed(() => detailFormData.value.node_executions?.length || 0);
const completedNodes = computed(
  () => detailFormData.value.node_executions?.filter((n) => n.status === "completed").length || 0
);
const runningNodes = computed(
  () => detailFormData.value.node_executions?.filter((n) => n.status === "running").length || 0
);
const failedNodes = computed(
  () => detailFormData.value.node_executions?.filter((n) => n.status === "failed").length || 0
);

const loadingData = async () => {
  loading.value = true;
  try {
    const res = await WorkflowRunAPI.getWorkflowRunList(queryFormData);
    if (res.data) {
      pageTableData.value = res.data.data.items || [];
      total.value = res.data.data.total || 0;
    }
  } catch {
    ElMessage.error("加载数据失败");
  } finally {
    loading.value = false;
  }
};

const handleQuery = () => {
  queryFormData.page_no = 1;
  loadingData();
};

const handleResetQuery = () => {
  Object.assign(queryFormData, {
    page_no: 1,
    page_size: 10,
    workflow_name: "",
    status: "",
    initiator: undefined,
    created_time: [],
    updated_time: [],
  });
  startDateRange.value = undefined;
  endDateRange.value = undefined;
  loadingData();
};

const handleConfirm = () => {
  handleQuery();
};

const handleStartDateRangeChange = (dates: [Date, Date] | null) => {
  if (dates) {
    queryFormData.created_time = [formatToDateTime(dates[0]), formatToDateTime(dates[1])];
  } else {
    queryFormData.created_time = [];
  }
};

const handleEndDateRangeChange = (dates: [Date, Date] | null) => {
  if (dates) {
    queryFormData.updated_time = [formatToDateTime(dates[0]), formatToDateTime(dates[1])];
  } else {
    queryFormData.updated_time = [];
  }
};

const handleRefresh = () => {
  loadingData();
};

const handleSelectionChange = (selection: WorkflowRunTable[]) => {
  selectIds.value = selection.map((item) => item.id).filter((id): id is number => id !== undefined);
};

const handleOpenDialog = (type: string, row?: WorkflowRunTable) => {
  detailDialogVisible.type = type;
  if (type === "detail" && row) {
    detailDialogVisible.title = "执行记录详情";
    detailFormData.value = { ...row };
  }
  detailDialogVisible.visible = true;
};

const handleCloseDialog = () => {
  detailDialogVisible.visible = false;
};

const handleAction = async (action: string, row: WorkflowRunTable) => {
  if (!row.id) {
    ElMessage.error("无效的记录ID");
    return;
  }

  try {
    await ElMessageBox.confirm(
      `确认要${action === "pause" ? "暂停" : action === "resume" ? "恢复" : "终止"}该执行记录吗？`,
      "提示",
      {
        type: "warning",
      }
    );

    let res;
    if (action === "pause") {
      res = await WorkflowRunAPI.pauseWorkflowRun(row.id);
    } else if (action === "resume") {
      res = await WorkflowRunAPI.resumeWorkflowRun(row.id);
    } else if (action === "terminate") {
      res = await WorkflowRunAPI.terminateWorkflowRun(row.id);
    }

    if (res) {
      ElMessage.success("操作成功");
      loadingData();
    }
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("操作失败");
    }
  }
};

const handleRetry = async (row: WorkflowRunTable) => {
  if (!row.id) {
    ElMessage.error("无效的记录ID");
    return;
  }

  if (row.retry_count >= row.max_retry) {
    ElMessage.warning(`已达到最大重试次数 (${row.max_retry})，无法继续重试`);
    return;
  }

  try {
    await ElMessageBox.confirm("确认要重试该执行记录吗？", "提示", {
      type: "warning",
    });

    const res = await WorkflowRunAPI.retryWorkflowRun(row.id);
    if (res) {
      ElMessage.success("重试成功");
      loadingData();
    }
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("重试失败");
    }
  }
};

const handleDelete = async (ids: number[]) => {
  try {
    await ElMessageBox.confirm(`确认要删除选中的 ${ids.length} 条记录吗？`, "提示", {
      type: "warning",
    });

    const res = await WorkflowRunAPI.deleteWorkflowRun(ids);
    if (res) {
      ElMessage.success("删除成功");
      loadingData();
    }
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("删除失败");
    }
  }
};

const handleShowErrorSuggestion = (row: WorkflowRunTable) => {
  selectedErrorRun.value = row;
  errorSuggestion.value = generateErrorSuggestion(row);
  errorSuggestionVisible.value = true;
};

const handleRetryFromSuggestion = () => {
  if (selectedErrorRun.value) {
    errorSuggestionVisible.value = false;
    handleRetry(selectedErrorRun.value);
  }
};

const generateErrorSuggestion = (row: WorkflowRunTable) => {
  const suggestions: Array<{ title: string; description: string }> = [];

  if (row.error_message?.includes("timeout")) {
    suggestions.push({
      title: "检查网络连接",
      description: "确认网络连接正常，目标服务可访问",
    });
    suggestions.push({
      title: "增加超时时间",
      description: "在节点配置中增加超时时间设置",
    });
  } else if (row.error_message?.includes("permission")) {
    suggestions.push({
      title: "检查权限设置",
      description: "确认当前用户有执行该操作的权限",
    });
    suggestions.push({
      title: "联系管理员",
      description: "如需更高权限，请联系系统管理员",
    });
  } else if (row.error_message?.includes("not found")) {
    suggestions.push({
      title: "检查资源是否存在",
      description: "确认相关资源（文件、数据等）存在且可访问",
    });
    suggestions.push({
      title: "验证配置参数",
      description: "检查节点配置中的参数是否正确",
    });
  } else {
    suggestions.push({
      title: "查看详细日志",
      description: "点击查看详情，查看完整的执行日志",
    });
    suggestions.push({
      title: "检查节点配置",
      description: "确认节点配置参数正确，依赖服务正常运行",
    });
    suggestions.push({
      title: "重试执行",
      description: "如果是临时性错误，可以尝试重试",
    });
  }

  return { steps: suggestions };
};

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    pending: "info",
    running: "primary",
    paused: "warning",
    completed: "success",
    failed: "danger",
    cancelled: "info",
    terminated: "danger",
  };
  return types[status] || "";
};

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: "待执行",
    running: "运行中",
    paused: "已暂停",
    completed: "已完成",
    failed: "失败",
    cancelled: "已取消",
    terminated: "已终止",
  };
  return texts[status] || status;
};

onMounted(() => {
  if (props.workflowName) {
    queryFormData.workflow_name = props.workflowName;
  }
  loadingData();
});
</script>

<style scoped lang="scss">
.detail-info {
  margin-bottom: 20px;
}

.progress-container {
  margin-top: 20px;

  .progress-stats {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
}

.error-message {
  color: #f56c6c;
  .retry-info {
    margin: 8px 0;
  }
}

.error-content {
  .retry-info {
    margin: 8px 0;
  }
}

.suggestion-card {
  margin-top: 16px;

  .card-header {
    font-weight: bold;
  }

  .suggestion-content {
    :deep(.el-step) {
      margin-bottom: 16px;
    }
  }
}

.ml-3 {
  margin-left: 12px;
}
</style>
