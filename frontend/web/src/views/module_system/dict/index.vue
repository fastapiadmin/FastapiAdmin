<!-- 字典类型：Fa 布局；操作列最多 3 个外露 +「更多」 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="dictTypeSearchItems"
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
            :perm-create="['module_system:dict_type:create']"
            :perm-export="['module_system:dict_type:export']"
            :perm-delete="['module_system:dict_type:delete']"
            :perm-patch="['module_system:dict_type:patch']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @export="openExport"
            @delete="handleBatchDelete"
            @more="handleMoreClick"
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
          :column="2"
          :data="detailFormData"
          :items="dictDetailItems"
          max-height="70vh"
        >
          <template #dict_type="{ row }">
            <ElTag type="primary">{{ row?.dict_type }}</ElTag>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="dictFormRenderKey"
          scrollbar
          max-height="70vh"
          ref="dataFormRef"
          v-model="formData"
          :items="dictDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio value="0">启用</ElRadio>
              <ElRadio value="1">停用</ElRadio>
            </ElRadioGroup>
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <FaExportDialog
      v-model="exportVisible"
      :content-config="dictTypeExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />

    <DataDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :dict-type="currentDictType"
      :dict-label="currentDictLabel"
      :dict-type-id="currentDictTypeId"
    />
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import DictAPI, {
  type DictForm,
  type DictPageQuery,
  type DictTable,
} from "@/api/module_system/dict";
import { useDictStore } from "@stores";
import DataDrawer from "@views/module_system/dict/components/DataDrawer.vue";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";

defineOptions({
  name: "Dict",
  inheritAttrs: false,
});

type DictTypeSearchForm = {
  dict_name?: string;
  dict_type?: string;
  status?: string;
  created_time?: string[];
};

const dictStore = useDictStore();
const { hasAuth } = useAuth();

const searchForm = ref<DictTypeSearchForm>({
  dict_name: undefined,
  dict_type: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const dictTypeSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "字典名称",
    key: "dict_name",
    type: "input",
    placeholder: "请输入字典名称",
    clearable: true,
    span: 6,
  },
  {
    label: "字典类型",
    key: "dict_type",
    type: "input",
    placeholder: "请输入字典类型",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
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
  useTableSelection<DictTable>();

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<DictTable>({});

const dictDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "字典名称", prop: "dict_name" },
    { label: "字典类型", prop: "dict_type", slot: "dict_type" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "描述", prop: "description" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

const formData = ref<DictForm>({
  id: undefined,
  dict_name: "",
  dict_type: "",
  status: "0",
  description: undefined,
});

const rules = reactive({
  dict_name: [{ required: true, message: "请输入字典名称", trigger: "blur" }],
  dict_type: [{ required: true, message: "请选择字典类型", trigger: "blur" }],
  status: [{ required: true, message: "请选择字典状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const dictFormRenderKey = ref(0);

const initialFormData: DictForm = {
  id: undefined,
  dict_name: "",
  dict_type: "",
  status: "0",
  description: undefined,
};

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } = useCrudForm<DictForm>({
  formData,
  initialFormData,
  dialogVisible,
  dataFormRef,
  formRenderKey: dictFormRenderKey,
  detailApi: DictAPI.detailDictType,
  createApi: DictAPI.createDictType,
  updateApi: DictAPI.updateDictType,
  titles: { create: "新增字典", update: "修改字典", detail: "字典详情" },
  detailFormData,
  onCreateSuccess: async () => {
    await refreshCreate();
  },
  onUpdateSuccess: async () => {
    await refreshUpdate();
  },
  onSubmitSuccess: async () => {
    dictStore.clearDictData();
    if (formData.value.dict_type) {
      await dictStore.getDict([formData.value.dict_type]);
    }
  },
});

const dictDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "字典名称",
    key: "dict_name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入字典名称", maxlength: 50 },
  },
  {
    label: "字典类型",
    key: "dict_type",
    type: "input",
    span: 24,
    props: { placeholder: "请输入字典类型", maxlength: 50 },
  },
  {
    label: "状态",
    key: "status",
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
    apiFn: DictAPI.listDictType,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<DictTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "dict_name", label: "字典名称", minWidth: 140, showOverflowTooltip: true },
      {
        prop: "dict_type",
        label: "字典类型",
        minWidth: 180,
        formatter: (row: DictTable) => h(ElTag, { type: "primary" }, () => row.dict_type ?? ""),
      },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: DictTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "danger" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      { prop: "description", label: "描述", minWidth: 140, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: DictTable) => formatDictOperationCell(row),
      },
    ],
  },
});

const dictTypeCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<DictTable>) => {
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
  return cleanEmptyArrayParams(sp) as unknown as DictPageQuery;
});

const dictTypeExportContentConfig = computed(() => ({
  permPrefix: "module_system:dict_type",
  cols: dictTypeCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = cleanEmptyArrayParams({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await DictAPI.exportDictType(merged as unknown as DictPageQuery);
    return res.data as Blob;
  },
}));

const { exportVisible, openExport } = useImportExport();

const drawerVisible = ref(false);
const currentDictType = ref("");
const currentDictLabel = ref("");
const currentDictTypeId = ref(0);

async function handleSearchBarSearch(params: DictTypeSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams({
    dict_name: params.dict_name,
    dict_type: params.dict_type,
    status: params.status,
    created_time:
      Array.isArray(params.created_time) && params.created_time.length === 2
        ? params.created_time
        : undefined,
  } as Record<string, unknown>);
  getData();
}

function onResetSearch() {
  searchForm.value = {
    dict_name: undefined,
    dict_type: undefined,
    status: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

function buildDictRowActions(row: DictTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "dictData",
      label: "字典",
      artType: "view",
      icon: "ri:book-2-line",
      iconColor: "var(--el-color-warning)",
      perm: "module_system:dict_data:query",
      run: () => handleDictDataDrawer(row),
    },
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:dict_type:detail",
      run: () => void handleOpenDialog("detail", row.id),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:dict_type:update",
      run: () => void handleOpenDialog("update", row.id),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:dict_type:delete",
      run: () => {
        if (row.id != null) deleteDictTypeRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatDictOperationCell(row: DictTable) {
  return renderTableOperationCell(buildDictRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 dict-table-actions",
  });
}

function handleDictDataDrawer(dictTypeRow: DictTable) {
  currentDictType.value = dictTypeRow.dict_type || "";
  currentDictLabel.value = dictTypeRow.dict_name || "";
  currentDictTypeId.value = dictTypeRow.id ?? 0;
  drawerVisible.value = true;
}

async function deleteDictTypeRow(id: number) {
  try {
    await confirmDelete();
    await DictAPI.deleteDictType([id]);
    dictStore.clearDictData();
    const dictTypes = Object.keys(dictStore.dictData);
    if (dictTypes.length > 0) await dictStore.getDict(dictTypes);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await DictAPI.deleteDictType(ids);
    dictStore.clearDictData();
    const dictTypes = Object.keys(dictStore.dictData);
    if (dictTypes.length > 0) await dictStore.getDict(dictTypes);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

async function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  try {
    await confirmToggleStatus(status);
    await DictAPI.batchDictType({ ids, status });
    await refreshData();
    dictStore.clearDictData();
    const dictTypes = Object.keys(dictStore.dictData);
    if (dictTypes.length > 0) await dictStore.getDict(dictTypes);
  } catch {
    // 用户取消
  }
}
</script>
