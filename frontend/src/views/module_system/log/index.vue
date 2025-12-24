<!-- 日志管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="request_path" label="请求路径">
          <el-input v-model="queryFormData.request_path" placeholder="请输入请求路径" clearable />
        </el-form-item>
        <el-form-item prop="type" label="日志类型">
          <el-select
            v-model="queryFormData.type"
            placeholder="请选择日志类型"
            style="width: 167.5px"
            clearable
          >
            <el-option label="登录日志" value="1" />
            <el-option label="操作日志" value="2" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="isExpand" prop="created_id" label="创建人">
          <UserTableSelect
            v-model="queryFormData.created_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_system:log:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:log:query']"
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
            <el-tooltip content="日志管理维护系统的日志。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            日志列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:log:delete']"
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
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:log:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_system:log:query']"
                  type="default"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        height="500"
        max-height="500"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column prop="selection" type="selection" min-width="55" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="日志类型" prop="type" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.type === 1 ? 'success' : 'primary'">
              {{ scope.row.type === 1 ? "登录日志" : "操作日志" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="请求路径"
          prop="request_path"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column label="请求方法" prop="request_method" min-width="100">
          <template #default="scope">
            <el-tag :type="getMethodType(scope.row.request_method)">
              {{ scope.row.request_method }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态码" prop="response_code" min-width="100">
          <template #default="scope">
            <el-tag :type="getStatusCodeType(scope.row.response_code)">
              {{ scope.row.response_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="请求IP" prop="request_ip" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            <el-text>{{ scope.row.request_ip }}</el-text>
            <CopyButton
              v-if="scope.row.request_ip"
              :text="scope.row.request_ip"
              :style="{ marginLeft: '2px' }"
            />
          </template>
        </el-table-column>
        <el-table-column label="处理时间" prop="process_time" min-width="120" />
        <el-table-column
          label="浏览器"
          prop="request_browser"
          min-width="220"
          show-overflow-tooltip
        />
        <el-table-column label="系统" prop="request_os" min-width="100" />
        <el-table-column label="描述" prop="description" min-width="120" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_time" min-width="200" sortable />
        <el-table-column label="创建人" prop="created_id" min-width="120">
          <template #default="scope">
            {{ scope.row.created_by?.name }}
          </template>
        </el-table-column>
        <el-table-column label="更新人" prop="updated_id" min-width="120">
          <template #default="scope">
            {{ scope.row.updated_by?.name }}
          </template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" align="center" min-width="150">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_system:log:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_system:log:delete']"
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
        <el-descriptions :column="8" border label-width="200px">
          <el-descriptions-item label="日志类型" :span="2">
            <el-tag :type="formData.type === 1 ? 'success' : 'primary'">
              {{ formData.type === 1 ? "登录日志" : "操作日志" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="请求路径" :span="2">
            {{ formData.request_path }}
          </el-descriptions-item>
          <el-descriptions-item label="请求方法" :span="2">
            <el-tag :type="getMethodType(formData.request_method)">
              {{ formData.request_method }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="响应状态码" :span="2">
            <el-tag :type="getStatusCodeType(formData.response_code)">
              {{ formData.response_code }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="请求IP" :span="2">
            {{ formData.request_ip }}
          </el-descriptions-item>
          <el-descriptions-item label="处理时间" :span="2">
            {{ formData.process_time }}
          </el-descriptions-item>
          <el-descriptions-item label="浏览器" :span="2">
            {{ formData.request_browser }}
          </el-descriptions-item>
          <el-descriptions-item label="操作系统" :span="2">
            {{ formData.request_os }}
          </el-descriptions-item>
          <el-descriptions-item label="请求参数" :span="8">
            <JsonPretty :value="formData.request_payload" height="80px" />
          </el-descriptions-item>
          <el-descriptions-item label="响应数据" :span="8">
            <JsonPretty :value="formData.response_json" height="140px" />
          </el-descriptions-item>
          <el-descriptions-item label="登录地点" :span="4">
            {{ formData.login_location }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="8">
            {{ formData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人" :span="4">
            {{ formData.created_by?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="更新人" :span="4">
            {{ formData.updated_by?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="4">
            {{ formData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="4">
            {{ formData.updated_time }}
          </el-descriptions-item>
        </el-descriptions>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button
            v-hasPerm="['module_system:log:detail']"
            type="primary"
            @click="handleCloseDialog"
          >
            确定
          </el-button>
        </div>
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
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Log",
  inheritAttrs: false,
});

import LogAPI, { LogTable, LogPageQuery } from "@/api/module_system/log";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { formatToDateTime } from "@/utils/dateUtil";

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<LogTable[]>([]);

// 导出弹窗状态和选中行数据
const exportsDialogVisible = ref(false);
const selectionRows = ref<LogTable[]>([]);

// 详情表单
const formData = ref<LogTable>({});

// 分页查询参数
const queryFormData = reactive<LogPageQuery>({
  page_no: 1,
  page_size: 10,
  type: undefined,
  request_path: undefined,
  creator_name: undefined,
  created_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
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

const getStatusCodeType = (code?: number) => {
  if (code === undefined) {
    return "info";
  }
  if (code >= 200 && code < 300) {
    return "success";
  } else if (code >= 300 && code < 400) {
    return "warning";
  } else if (code >= 400 && code < 500) {
    return "danger";
  } else {
    return "danger";
  }
};

const getMethodType = (method?: string) => {
  if (method === undefined) {
    return "info";
  }
  if (method === "GET") {
    return "info";
  } else if (method === "POST") {
    return "success";
  } else if (method === "PUT" || method === "PATCH") {
    return "warning";
  } else if (method === "DELETE") {
    return "danger";
  } else {
    return "info";
  }
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await LogAPI.listLog(queryFormData);
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

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  loadingData();
}

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  formData.value.id = undefined;
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开日志详情弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await LogAPI.detailLog(id);
    if (type === "detail") {
      dialogVisible.title = "日志详情";
      Object.assign(formData.value, response.data.data);
    }
  }
  dialogVisible.visible = true;
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await LogAPI.deleteLog(ids);
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
  { prop: "type", label: "日志类型" },
  { prop: "request_path", label: "请求路径" },
  { prop: "request_method", label: "请求方法" },
  { prop: "response_code", label: "状态码" },
  { prop: "request_ip", label: "请求IP" },
  { prop: "login_location", label: "登录地点" },
  { prop: "process_time", label: "处理时间" },
  { prop: "request_browser", label: "浏览器" },
  { prop: "request_os", label: "系统" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

// 导入/导出配置（用于导出弹窗）
const curdContentConfig = {
  permPrefix: "module_system:log",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await LogAPI.listLog(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
