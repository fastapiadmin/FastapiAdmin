<!-- 系统配置：Fa 布局 + useTable，与 notice 页一致 -->
<template>
  <div class="fa-full-height">
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

    <ElCard
      shadow="hover"
      class="fa-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
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
            @export="openExport"
            @delete="handleBatchDelete"
          />
        </template>
      </FaTableHeader>

      <FaTable
        ref="faTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
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
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :data="detailFormData"
          :items="paramDetailItems"
          max-height="75vh"
        />
      </template>
      <template v-else>
        <FaForm
          :key="paramFormRenderKey"
          scrollbar
          max-height="75vh"
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
      </template>
    </FaDialog>

    <FaExportDialog
      v-model="exportVisible"
      :content-config="paramExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import type { ColumnOption } from "@/types/component";
import ParamsAPI, {
  type ConfigForm,
  type ConfigPageQuery,
  type ConfigTable,
} from "@/api/module_system/params";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import { useConfigStore } from "@stores";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElTag, ElMessage } from "element-plus";

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
  const p = cleanEmptyArrayParams({ ...params });
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

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<ConfigTable>();

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<ConfigTable>({} as ConfigTable);

const paramDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "配置名称", prop: "config_name" },
    {
      label: "系统内置",
      prop: "config_type",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    { label: "配置键", prop: "config_key" },
    { label: "配置值", prop: "config_value" },
    { label: "描述", prop: "description" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

const formData = ref<ConfigForm>({
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
});

const rules = reactive({
  config_name: [{ required: true, message: "请输入系统配置名称", trigger: "blur" }],
  config_key: [{ required: true, message: "请输入系统配置键", trigger: "blur" }],
  config_value: [{ required: true, message: "请输入系统配置值", trigger: "blur" }],
  config_type: [{ required: true, message: "请选择系统配置类型", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const paramFormRenderKey = ref(0);

const initialFormData: ConfigForm = {
  id: undefined,
  config_name: "",
  config_key: "",
  config_value: "",
  config_type: false,
  description: "",
};

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<ConfigForm>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey: paramFormRenderKey,
    detailApi: ParamsAPI.detailParams,
    createApi: ParamsAPI.createParams,
    updateApi: ParamsAPI.updateParams,
    titles: { create: "新增系统配置", update: "修改系统配置", detail: "系统配置详情" },
    detailFormData,
    onCreateSuccess: async () => {
      await refreshCreate();
    },
    onUpdateSuccess: async () => {
      await refreshUpdate();
    },
    onSubmitSuccess: async () => {
      configStore.isConfigLoaded = false;
      await configStore.getConfig();
    },
  });

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
      { type: "globalIndex", width: 56, label: "序号" },
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
  const sp = stripPaginationParams(searchParams as Record<string, unknown>);
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

const { exportVisible, openExport } = useImportExport();

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

async function deleteParamRow(id: number) {
  try {
    await confirmDelete();
    await ParamsAPI.deleteParams([id]);
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
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

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await ParamsAPI.deleteParams(ids);
    configStore.isConfigLoaded = false;
    await configStore.getConfig();
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}
</script>
