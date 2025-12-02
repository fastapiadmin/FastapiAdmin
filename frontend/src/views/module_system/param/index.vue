<!-- 系统配置 -->
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
        <el-form-item prop="config_name" label="配置名称">
          <el-input v-model="queryFormData.config_name" placeholder="请输入配置名称" clearable />
        </el-form-item>
        <el-form-item prop="config_key" label="配置键名">
          <el-input v-model="queryFormData.config_key" placeholder="请输入配置键名" clearable />
        </el-form-item>
        <el-form-item prop="config_type" label="系统内置">
          <el-select
            v-model="queryFormData.config_type"
            placeholder="请选择系统内置"
            style="width: 167.5px"
            clearable
          >
            <el-option value="true" label="是" />
            <el-option value="false" label="否" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_system:param:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:param:query']"
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
            <el-tooltip content="配置管理，包括系统名称、系统描述、系统版本、系统logo等。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            系统配置列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:param:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:param:delete']"
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
                  v-hasPerm="['module_system:param:export']"
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
                  v-hasPerm="['module_system:param:refresh']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_system:param:query']" trigger="click">
                <el-button type="default" icon="operation" circle />
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item
                      v-for="column in tableColumns"
                      :key="column.prop"
                      :command="column"
                    >
                      <el-checkbox v-model="column.show">{{ column.label }}</el-checkbox>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
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
        :height="450"
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
          type="index"
          fixed
          label="序号"
          min-width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'config_name')?.show"
          key="config_name"
          label="配置名称"
          prop="config_name"
          min-width="100"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'config_key')?.show"
          key="config_key"
          label="配置键"
          prop="config_key"
          min-width="200"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'config_value')?.show"
          key="config_value"
          label="配置值"
          prop="config_value"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'config_type')?.show"
          key="config_type"
          label="系统内置"
          prop="config_type"
          min-width="100"
        >
          <template #default="scope">
            <el-tag v-if="scope.row.config_type" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'description')?.show"
          key="description"
          label="描述"
          prop="description"
          min-width="120"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_time')?.show"
          key="created_time"
          label="创建时间"
          prop="created_time"
          min-width="200"
          sortable
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show"
          key="updated_time"
          label="更新时间"
          prop="updated_time"
          min-width="200"
          sortable
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="200"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_system:param:query']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_system:param:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_system:param:delete']"
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
        <el-descriptions :column="4" border>
          <el-descriptions-item label="配置名称" :span="2">
            {{ detailFormData.config_name }}
          </el-descriptions-item>
          <el-descriptions-item label="系统内置" :span="2">
            <el-tag v-if="detailFormData.config_type" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="配置键" :span="2">
            {{ detailFormData.config_key }}
          </el-descriptions-item>
          <el-descriptions-item label="配置值" :span="2">
            {{ detailFormData.config_value }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ detailFormData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <el-form-item label="配置名称" prop="config_name">
            <el-input v-model="formData.config_name" placeholder="请输入配置名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="配置键" prop="config_key">
            <el-input v-model="formData.config_key" placeholder="请输入配置键" :maxlength="50" />
          </el-form-item>
          <el-form-item label="配置值" prop="config_value">
            <el-input v-model="formData.config_value" placeholder="请输入配置值" :maxlength="100" />
          </el-form-item>
          <el-form-item label="系统内置" prop="config_type">
            <el-radio-group v-model="formData.config_type">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button
            v-if="dialogVisible.type !== 'detail'"
            v-hasPerm="['module_system:param:create']"
            type="primary"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button
            v-else
            v-hasPerm="['module_system:param:detail']"
            type="primary"
            @click="handleCloseDialog"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>

    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :selection-data="selectionRows"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Params",
  inheritAttrs: false,
});

import ParamsAPI, { ConfigTable, ConfigForm, ConfigPageQuery } from "@/api/module_system/params";
import ExportModal from "@/components/CURD/ExportModal.vue";
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
const pageTableData = ref<ConfigTable[]>([]);

// 导出弹窗显示状态 & 选中行
const exportsDialogVisible = ref(false);
const selectionRows = ref<ConfigTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "config_name", label: "配置名称", show: true },
  { prop: "config_key", label: "配置键", show: true },
  { prop: "config_value", label: "配置值", show: true },
  { prop: "config_type", label: "系统内置", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 详情表单
const detailFormData = ref<ConfigTable>({} as ConfigTable);

// 分页查询参数
const queryFormData = reactive<ConfigPageQuery>({
  page_no: 1,
  page_size: 10,
  config_name: undefined,
  config_key: undefined,
  config_type: undefined,
  created_time: undefined,
});

// 编辑表单
const formData = reactive<ConfigForm>({
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  config_name: [{ required: true, message: "请输入系统配置名称", trigger: "blur" }],
  config_key: [{ required: true, message: "请输入系统配置键", trigger: "blur" }],
  config_value: [{ required: true, message: "请输入系统配置值", trigger: "blur" }],
  config_type: [{ required: true, message: "请选择系统配置类型", trigger: "blur" }],
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
    const response = await ParamsAPI.listParams(queryFormData);
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
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: ConfigForm = {
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
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

// 打开系统配置弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await ParamsAPI.detailParams(id);
    if (type === "detail") {
      dialogVisible.title = "系统配置详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改系统配置";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增系统配置";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 新增、编辑弹窗处理
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await ParamsAPI.updateParams(id, formData);
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await ParamsAPI.createParams(formData);
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      }
    }
  });
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
        await ParamsAPI.deleteParams(ids);
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

// 导出弹窗
async function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 导出字段
const exportColumns = [
  { prop: "config_name", label: "配置名称" },
  { prop: "config_key", label: "配置键" },
  { prop: "config_value", label: "配置值" },
  { prop: "config_type", label: "系统内置" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

// 导入/导出配置（用于导出弹窗）
const curdContentConfig = {
  permPrefix: "module_system:param",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    if (typeof query.config_type === "string") {
      query.config_type = query.config_type === "true";
    }
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await ParamsAPI.listParams(query);
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
