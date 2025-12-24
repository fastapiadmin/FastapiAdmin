<!-- 任务日志抽屉 -->
<template>
  <el-drawer
    v-model="drawerVisible"
    :title="'【' + props.jobName + '】任务日志'"
    :size="drawerSize"
  >
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="status" label="执行状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择执行状态"
            style="width: 167.5px"
            clearable
          >
            <el-option :value="true" label="成功" />
            <el-option :value="false" label="失败" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="执行时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_application:job:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_application:job:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <!-- 展开/收起 -->
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
            <el-tooltip
              content="任务执行日志记录每次定时任务的执行情况，包括成功、失败状态及错误信息。"
            >
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            任务执行日志列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_application:job:delete']"
                type="warning"
                icon="delete"
                @click="handleClearLog"
              >
                清空日志
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <!-- 将直接导出改为打开导出弹窗 -->
                <el-button
                  v-hasPerm="['module_application:job:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button type="default" icon="refresh" circle @click="handleRefresh" />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：任务日志列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        height="460"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" min-width="55" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="任务名称" prop="job_name" min-width="150" show-overflow-tooltip />
        <el-table-column label="任务组名" prop="job_group" min-width="120" show-overflow-tooltip />
        <el-table-column label="执行状态" prop="status" min-width="100" show-overflow-tooltip>
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'primary' : 'success'">
              {{ scope.row.status === "0" ? "运行中" : "完成" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="执行信息"
          prop="job_message"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column
          label="异常信息"
          prop="exception_info"
          min-width="250"
          show-overflow-tooltip
        />
        <el-table-column label="执行器" prop="job_executor" min-width="120" show-overflow-tooltip />
        <el-table-column
          label="调用目标"
          prop="invoke_target"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column label="位置参数" prop="job_args" min-width="150" show-overflow-tooltip />
        <el-table-column
          label="关键字参数"
          prop="job_kwargs"
          min-width="150"
          show-overflow-tooltip
        />
        <el-table-column label="触发器" prop="job_trigger" min-width="120" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_time" min-width="180" sortable />
        <el-table-column label="更新时间" prop="updated_time" min-width="180" sortable />
        <el-table-column fixed="right" label="操作" align="center" min-width="150">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_application:job:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_application:job:delete']"
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

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="2" border label-width="120px">
          <el-descriptions-item label="日志ID" :span="2">
            {{ detailFormData.id }}
          </el-descriptions-item>
          <el-descriptions-item label="任务名称" :span="2">
            {{ detailFormData.job_name }}
          </el-descriptions-item>
          <el-descriptions-item label="任务组名" :span="2">
            {{ detailFormData.job_group }}
          </el-descriptions-item>
          <el-descriptions-item label="执行状态" :span="2">
            <el-tag :type="detailFormData.status === '0' ? 'primary' : 'success'">
              {{ detailFormData.status === "0" ? "运行中" : "完成" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="执行信息" :span="2">
            {{ detailFormData.job_message || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="异常信息" :span="2">
            {{ detailFormData.exception_info || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="执行器" :span="2">
            {{ detailFormData.job_executor || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="调用目标" :span="2">
            {{ detailFormData.invoke_target || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="位置参数" :span="2">
            {{ detailFormData.job_args || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="关键字参数" :span="2">
            {{ detailFormData.job_kwargs || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="触发器" :span="2">
            {{ detailFormData.job_trigger || "-" }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
    </el-dialog>

    <!-- 导出弹窗 -->
    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="queryFormData"
      :page-data="pageTableData"
      :selection-data="selectionRows"
    />
  </el-drawer>
</template>

<script setup lang="ts">
// 添加 props 来接收 jobId 和 jobName
const props = defineProps({
  jobId: {
    type: Number,
    required: true,
  },
  jobName: {
    type: String,
    required: true,
  },
});

import JobAPI, { JobLogPageQuery, JobLogTable } from "@/api/module_application/job";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import ExportModal from "@/components/CURD/ExportModal.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { formatToDateTime } from "@/utils/dateUtil";

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "80%" : "60%"));

const queryFormRef = ref();
const dataTableRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);
const drawerVisible = ref<boolean>(false);

// 分页表单
const pageTableData = ref<JobLogTable[]>([]);

// 导出弹窗显示状态 & 选中行
const exportsDialogVisible = ref(false);
const selectionRows = ref<JobLogTable[]>([]);

// 详情表单
const detailFormData = ref<JobLogTable>({} as JobLogTable);

// 分页查询参数
const queryFormData = reactive<JobLogPageQuery>({
  page_no: 1,
  page_size: 10,
  status: undefined,
  created_time: undefined,
  job_id: props.jobId,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "detail",
});

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    // 调用任务日志列表接口
    const response = await JobAPI.listJobLog(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  queryFormData.status = undefined;
  queryFormData.created_time = undefined;
  dateRange.value = [];
  loadingData();
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  // 提取有效的数字ID，过滤掉 null/undefined 并转为 number
  selectIds.value = selection
    .map((item: any) => item?.id)
    .filter((id: any) => id !== null && id !== undefined)
    .map((id: any) => Number(id));
  // 记录选中行数据供导出弹窗使用
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
}

// 打开详情弹窗
async function handleOpenDialog(type: "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await JobAPI.detailJobLog(id);
    dialogVisible.title = "任务日志详情";
    Object.assign(detailFormData.value, response.data.data);
  }
  dialogVisible.visible = true;
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  // 如果没有有效ID，直接返回
  const validIds = ids.filter((id) => id !== null && id !== undefined) as number[];
  if (validIds.length === 0) return;

  ElMessageBox.confirm("确认删除该任务日志?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await JobAPI.deleteJobLog(validIds);
        // 删除后刷新并清空选择状态
        handleResetQuery();
        selectIds.value = [];
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 清空日志
async function handleClearLog() {
  ElMessageBox.confirm("确认清空所有任务日志?此操作不可恢复!", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await JobAPI.clearJobLog();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 打开导出弹窗
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 导出字段
const exportColumns = [
  { prop: "job_name", label: "任务名称" },
  { prop: "job_group", label: "任务组名" },
  { prop: "status", label: "执行状态" },
  { prop: "job_message", label: "执行信息" },
  { prop: "exception_info", label: "异常信息" },
  { prop: "job_executor", label: "执行器" },
  { prop: "invoke_target", label: "调用目标" },
  { prop: "job_args", label: "位置参数" },
  { prop: "job_kwargs", label: "关键字参数" },
  { prop: "job_trigger", label: "触发器" },
  { prop: "create_time", label: "创建时间" },
];

// 导出配置（用于导出弹窗）
const curdContentConfig = {
  permPrefix: "application:job_log",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await JobAPI.listJobLog(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

// 打开抽屉
function openDrawer() {
  drawerVisible.value = true;
}

// 关闭抽屉
function closeDrawer() {
  drawerVisible.value = false;
}

// 暴露方法给父组件
defineExpose({
  openDrawer,
  closeDrawer,
});

onMounted(() => {
  // 抽屉打开时会自动加载数据
  loadingData();
});
</script>

<style lang="scss" scoped></style>
