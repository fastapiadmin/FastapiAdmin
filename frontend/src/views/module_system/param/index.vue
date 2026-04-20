<!-- 系统配置 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig">
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <!-- 与 PageContent 默认工具栏一致：flex 换行，避免 el-row/el-col 与外层 flex 挤压右侧按钮 -->
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_system:param:create']"
          :perm-delete="['module_system:param:delete']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
        />
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar">
            <template #prepend>
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:param:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </template>
          </CrudToolbarRight>
        </div>
      </template>

      <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="loading"
            row-key="id"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="onSelectionChange"
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'selection')?.show"
              type="selection"
              min-width="55"
              align="center"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'index')?.show"
              fixed
              label="序号"
              min-width="60"
            >
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'config_name')?.show"
              key="config_name"
              label="配置名称"
              prop="config_name"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'config_key')?.show"
              key="config_key"
              label="配置键"
              prop="config_key"
              min-width="200"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'config_value')?.show"
              key="config_value"
              label="配置值"
              prop="config_value"
              min-width="200"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'config_type')?.show"
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
              v-if="contentCols.find((col) => col.prop === 'description')?.show"
              key="description"
              label="描述"
              prop="description"
              min-width="120"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              key="created_time"
              label="创建时间"
              prop="created_time"
              min-width="200"
              sortable
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
              key="updated_time"
              label="更新时间"
              prop="updated_time"
              min-width="200"
              sortable
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
              fixed="right"
              label="操作"
              align="center"
              min-width="200"
            >
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_system:param:detail']"
                  type="info"
                  size="small"
                  link
                  icon="View"
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
                  @click="handleRowDelete(scope.row.id)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </PageContent>

    <EnhancedDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
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
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button
            v-if="dialogVisible.type !== 'detail'"
            v-hasPerm="['module_system:param:create']"
            type="primary"
            :loading="submitLoading"
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
    </EnhancedDialog>

    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="exportQueryParams"
      :page-data="exportPageData"
      :selection-data="exportSelectionData"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, unref } from "vue";
import { fetchAllPages } from "@/utils/fetchAllPages";
import ParamsAPI, { ConfigTable, ConfigForm, ConfigPageQuery } from "@/api/module_system/params";
import { useConfigStore } from "@/store";
import ExportModal from "@/components/CURD/ExportModal.vue";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDialog from "@/components/CURD/EnhancedDialog.vue";
import { useCrudList } from "@/components/CURD/useCrudList";
import type { IContentConfig, ISearchConfig, IObject } from "@/components/CURD/types";

defineOptions({
  name: "Params",
  inheritAttrs: false,
});

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
const dataFormRef = ref();
const submitLoading = ref(false);

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_system:param",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "config_name",
      label: "配置名称",
      type: "input",
      attrs: { placeholder: "请输入配置名称", clearable: true },
    },
    {
      prop: "config_key",
      label: "配置键名",
      type: "input",
      attrs: { placeholder: "请输入配置键名", clearable: true },
    },
    {
      prop: "config_type",
      label: "系统内置",
      type: "select",
      options: [
        { label: "是", value: "true" },
        { label: "否", value: "false" },
      ],
      attrs: { placeholder: "请选择系统内置", clearable: true, style: { width: "167.5px" } },
    },
    {
      prop: "created_time",
      label: "创建时间",
      type: "date-picker",
      initialValue: [],
      attrs: {
        type: "datetimerange",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        rangeSeparator: "至",
        startPlaceholder: "开始日期",
        endPlaceholder: "结束日期",
        style: { width: "340px" },
      },
    },
  ],
});

const contentCols = reactive<
  Array<{
    prop?: string;
    label?: string;
    show?: boolean;
  }>
>([
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

const configStore = useConfigStore();

function normalizeListQuery(params: IObject): ConfigPageQuery {
  const q = { ...params } as IObject;
  if (typeof q.config_type === "string") {
    q.config_type = q.config_type === "true";
  }
  return q as unknown as ConfigPageQuery;
}

const contentConfig = reactive<IContentConfig<ConfigPageQuery>>({
  permPrefix: "module_system:param",
  pk: "id",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  toolbar: [],
  defaultToolbar: ["refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await ParamsAPI.listParams(normalizeListQuery(params as IObject));
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: async (ids) => {
    await ParamsAPI.deleteParams(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n))
    );
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
  },
  deleteConfirm: {
    title: "警告",
    message: "确认删除该项数据?",
    type: "warning",
  },
});

function handleRowDelete(id: number) {
  contentRef.value?.handleDelete(id);
}

const detailFormData = ref<ConfigTable>({} as ConfigTable);

const formData = reactive<ConfigForm>({
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  config_name: [{ required: true, message: "请输入系统配置名称", trigger: "blur" }],
  config_key: [{ required: true, message: "请输入系统配置键", trigger: "blur" }],
  config_value: [{ required: true, message: "请输入系统配置值", trigger: "blur" }],
  config_type: [{ required: true, message: "请选择系统配置类型", trigger: "blur" }],
});

const initialFormData: ConfigForm = {
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
};

const exportsDialogVisible = ref(false);

const exportQueryParams = computed(() => searchRef.value?.getQueryParams() ?? {});

const exportPageData = computed(() => (unref(contentRef.value?.pageData) ?? []) as ConfigTable[]);

const exportSelectionData = computed(
  () => (contentRef.value?.getSelectionData() ?? []) as ConfigTable[]
);

const exportColumns = [
  { prop: "config_name", label: "配置名称" },
  { prop: "config_key", label: "配置键" },
  { prop: "config_value", label: "配置值" },
  { prop: "config_type", label: "系统内置" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

const curdContentConfig = {
  permPrefix: "module_system:param",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query = { ...normalizeListQuery(params) } as Record<string, unknown>;
    return fetchAllPages({
      initialQuery: query,
      fetchPage: async (q) => {
        const res = await ParamsAPI.listParams(q as unknown as ConfigPageQuery);
        return {
          total: res.data?.data?.total ?? 0,
          list: res.data?.data?.items ?? [],
        };
      },
    });
  },
} as unknown as IContentConfig;

function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

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

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      submitLoading.value = true;
      const id = formData.id;
      try {
        if (id) {
          await ParamsAPI.updateParams(id, { id, ...formData });
        } else {
          await ParamsAPI.createParams(formData);
        }
        dialogVisible.visible = false;
        await resetForm();
        refreshList();
        configStore.isConfigLoaded = false;
        await configStore.getConfig();
      } catch (error: any) {
        console.error(error);
      } finally {
        submitLoading.value = false;
      }
    }
  });
}
</script>
