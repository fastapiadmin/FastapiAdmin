<!-- 系统配置：Art 布局 + useTable，与 notice 页一致 -->
<template>
  <div class="art-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="paramSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <FaTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_system:param:create']"
            :perm-export="['module_system:param:export']"
            :perm-delete="['module_system:param:delete']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @export="openExportModal"
            @delete="handleBatchDelete"
          />
        </template>
      </FaTableHeader>

      <FaTable
        ref="FaTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="paginationBind"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="640px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border>
            <ElDescriptionsItem label="配置名称" :span="2">
              {{ detailFormData.config_name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="系统内置" :span="2">
              <ElTag v-if="detailFormData.config_type" type="success">是</ElTag>
              <ElTag v-else type="danger">否</ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="配置键" :span="2">
              {{ detailFormData.config_key }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="配置值" :span="2">
              {{ detailFormData.config_value }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="2">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建时间" :span="2">
              {{ detailFormData.created_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新时间" :span="2">
              {{ detailFormData.updated_time }}
            </ElDescriptionsItem>
          </ElDescriptions>
        </ElScrollbar>
      </template>
      <template v-else>
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <FaForm
            :key="paramFormRenderKey"
            ref="dataFormRef"
            v-model="formData"
            :items="paramDialogFormItems"
            :rules="rules"
            label-suffix=":"
            :label-width="100"
            label-position="right"
            :span="24"
            :gutter="16"
            :show-reset="false"
            :show-submit="false"
            class="crud-dialog-art-form"
          >
            <template #config_type>
              <ElRadioGroup v-model="formData.config_type">
                <ElRadio :value="true">是</ElRadio>
                <ElRadio :value="false">否</ElRadio>
              </ElRadioGroup>
            </template>
          </FaForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton
            v-if="dialogVisible.type !== 'detail'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </FaDialog>

    <FaExportDialog
      v-model="exportModalVisible"
      :content-config="paramExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive } from "vue";
import { useTable } from "@/hooks/core/useTable";
import FaTable from "@/components/tables/fa-table/index.vue";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import FaExportDialog from "@/components/modal/fa-export-dialog/index.vue";
import type { IObject } from "@/components/modal/types";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import ParamsAPI, {
  type ConfigForm,
  type ConfigPageQuery,
  type ConfigTable,
} from "@/api/module_system/params";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useConfigStore } from "@stores";

defineOptions({
  name: "Params",
  inheritAttrs: false,
});

const configStore = useConfigStore();
const { hasAuth } = useAuth();

type ParamSearchForm = {
  config_name?: string;
  config_key?: string;
  config_type?: string;
  created_time?: string[];
};

function normalizeParamQuery(params: Record<string, unknown>): ConfigPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  if (p.config_type === "true" || p.config_type === true) p.config_type = true;
  else if (p.config_type === "false" || p.config_type === false) p.config_type = false;
  return p as unknown as ConfigPageQuery;
}

function buildParamReplaceParams(p: ParamSearchForm): Record<string, unknown> {
  return {
    config_name: p.config_name,
    config_key: p.config_key,
    config_type: p.config_type,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

const searchForm = ref<ParamSearchForm>({
  config_name: undefined,
  config_key: undefined,
  config_type: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const builtinOptions = ref([
  { label: "是", value: "true" },
  { label: "否", value: "false" },
]);

const paramSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "配置名称",
    key: "config_name",
    type: "input",
    placeholder: "请输入配置名称",
    clearable: true,
    span: 6,
  },
  {
    label: "配置键名",
    key: "config_key",
    type: "input",
    placeholder: "请输入配置键名",
    clearable: true,
    span: 6,
  },
  {
    label: "系统内置",
    key: "config_type",
    type: "select",
    props: {
      placeholder: "请选择系统内置",
      options: builtinOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "创建时间",
    key: "created_time",
    type: "datetimerange",
    span: 6,
    props: {
      type: "datetimerange",
      rangeSeparator: "至",
      startPlaceholder: "开始日期",
      endPlaceholder: "结束日期",
      format: "YYYY-MM-DD HH:mm:ss",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
      style: { width: "100%" },
    },
  },
]);

const FaTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<ConfigTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: ConfigTable[]) {
  selectedRows.value = rows;
}

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
  searchParams,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: ParamsAPI.listParams,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<ConfigTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { prop: "config_name", label: "配置名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "config_key", label: "配置键", minWidth: 200, showOverflowTooltip: true },
      { prop: "config_value", label: "配置值", minWidth: 200, showOverflowTooltip: true },
      {
        prop: "config_type",
        label: "系统内置",
        minWidth: 100,
        formatter: (row: ConfigTable) =>
          h(ElTag, { type: row.config_type ? "success" : "danger" }, () =>
            row.config_type ? "是" : "否"
          ),
      },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: ConfigTable) => formatParamOperationCell(row),
      },
    ],
  },
});

const paramCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<ConfigTable>) => {
    const t = (c as { type?: string }).type;
    return {
      prop: c.prop,
      label: c.label,
      type: t === "selection" ? ("selection" as const) : ("default" as const),
      show: true,
    };
  })
);

const exportQueryParams = computed(() => {
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  return normalizeParamQuery(sp);
});

const paramExportContentConfig = computed(() => ({
  permPrefix: "module_system:param",
  cols: paramCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeParamQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await ParamsAPI.exportParams(merged as ConfigPageQuery);
    return res.data as Blob;
  },
}));

const paginationBind = computed(() => {
  const p = pagination as unknown as {
    current?: number;
    size?: number;
    total?: number;
    page_no?: number;
    page_size?: number;
  };
  return {
    current: p.current ?? p.page_no ?? 1,
    size: p.size ?? p.page_size ?? 20,
    total: p.total ?? 0,
  };
});

const detailFormData = ref<ConfigTable>({} as ConfigTable);

const formData = ref<ConfigForm>({
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

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const paramFormRenderKey = ref(0);

const paramDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "配置名称",
    key: "config_name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入配置名称", maxlength: 50 },
  },
  {
    label: "配置键",
    key: "config_key",
    type: "input",
    span: 24,
    props: { placeholder: "请输入配置键", maxlength: 50 },
  },
  {
    label: "配置值",
    key: "config_value",
    type: "input",
    span: 24,
    props: { placeholder: "请输入配置值", maxlength: 100 },
  },
  {
    label: "系统内置",
    key: "config_type",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
]);
const submitLoading = ref(false);

const initialFormData: ConfigForm = {
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
};

const exportModalVisible = ref(false);

async function handleSearchBarSearch(params: ParamSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildParamReplaceParams(params));
  getData();
}

function onResetSearch() {
  searchForm.value = {
    config_name: undefined,
    config_key: undefined,
    config_type: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

async function resetForm() {
  dataFormRef.value?.ref?.resetFields();
  dataFormRef.value?.ref?.clearValidate();
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
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改系统配置";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增系统配置";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
  }
  paramFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.id;
    try {
      if (id) {
        await ParamsAPI.updateParams(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await ParamsAPI.createParams(formData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      configStore.isConfigLoaded = false;
      await configStore.getConfig();
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

function deleteParamRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ParamsAPI.deleteParams([id]);
      configStore.isConfigLoaded = false;
      await configStore.getConfig();
      ElMessage.success("删除成功");
      FaTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
}

function buildParamRowActions(row: ConfigTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:param:detail",
      run: () => {
        if (row.id != null) void handleOpenDialog("detail", row.id);
      },
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:param:update",
      run: () => {
        if (row.id != null) void handleOpenDialog("update", row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:param:delete",
      run: () => {
        if (row.id != null) deleteParamRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatParamOperationCell(row: ConfigTable) {
  return renderTableOperationCell(buildParamRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 param-table-actions",
  });
}

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await ParamsAPI.deleteParams(ids);
        configStore.isConfigLoaded = false;
        await configStore.getConfig();
        ElMessage.success("删除成功");
        FaTableRef.value?.elTableRef?.clearSelection();
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

function openExportModal() {
  exportModalVisible.value = true;
}
</script>

<style scoped lang="scss">
.art-table-card {
  flex: 1;
}

.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}
</style>
