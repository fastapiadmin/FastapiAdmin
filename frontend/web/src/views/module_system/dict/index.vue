<!-- 字典类型：Art 布局；操作列最多 3 个外露 +「更多」 -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
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

    <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <ArtTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <ArtTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_system:dict_type:create']"
            :perm-export="['module_system:dict_type:export']"
            :perm-delete="['module_system:dict_type:delete']"
            :perm-patch="['module_system:dict_type:patch']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @export="openExportModal"
            @delete="handleBatchDelete"
            @more="handleMoreClick"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="artTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="paginationBind"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="640px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="2" border>
            <ElDescriptionsItem label="字典名称" :span="2">
              {{ detailFormData.dict_name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="字典类型" :span="2">
              <ElTag type="primary">{{ detailFormData.dict_type }}</ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag v-if="detailFormData.status === '0'" type="success">启用</ElTag>
              <ElTag v-else type="danger">停用</ElTag>
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
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ArtForm
            :key="dictFormRenderKey"
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
          </ArtForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <ArtExportDialog
      v-model="exportModalVisible"
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
import { h, computed, ref, reactive } from "vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IObject } from "@/components/Core/modal/types";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";
import type { ColumnOption } from "@/types/component";
import DictAPI, {
  type DictForm,
  type DictPageQuery,
  type DictTable,
} from "@/api/module_system/dict";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
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

function normalizeDictTypeQuery(params: Record<string, unknown>): DictPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DictPageQuery;
}

const dictStore = useDictStore();
const { hasAuth } = useAuth();

const searchForm = ref<DictTypeSearchForm>({
  dict_name: undefined,
  dict_type: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<DictTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: DictTable[]) {
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
    apiFn: DictAPI.listDictType,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<DictTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
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
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  return normalizeDictTypeQuery(sp);
});

const dictTypeExportContentConfig = computed(() => ({
  permPrefix: "module_system:dict_type",
  cols: dictTypeCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeDictTypeQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await DictAPI.exportDictType(merged as DictPageQuery);
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

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const detailFormData = ref<DictTable>({});

const formData = reactive<DictForm>({
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

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const dictFormRenderKey = ref(0);

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

const initialFormData: DictForm = {
  id: undefined,
  dict_name: "",
  dict_type: "",
  status: "0",
  description: undefined,
};

const exportModalVisible = ref(false);

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
    const response = await DictAPI.detailDictType(id);
    if (type === "detail") {
      dialogVisible.title = "字典详情";
      detailFormData.value = response.data.data ?? {};
    } else if (type === "update") {
      dialogVisible.title = "修改字典";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增字典";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
  }
  dictFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    const id = formData.id;
    try {
      if (id) {
        await DictAPI.updateDictType(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await DictAPI.createDictType(formData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      dictStore.clearDictData();
      if (formData.dict_type) {
        await dictStore.getDict([formData.dict_type]);
      }
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

function deleteDictTypeRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await DictAPI.deleteDictType([id]);
      dictStore.clearDictData();
      const dictTypes = Object.keys(dictStore.dictData);
      if (dictTypes.length > 0) {
        await dictStore.getDict(dictTypes);
      }
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
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
        await DictAPI.deleteDictType(ids);
        dictStore.clearDictData();
        const dictTypes = Object.keys(dictStore.dictData);
        if (dictTypes.length > 0) {
          await dictStore.getDict(dictTypes);
        }
        ElMessage.success("删除成功");
        artTableRef.value?.elTableRef?.clearSelection();
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await DictAPI.batchDictType({ ids, status });
      await refreshData();
      dictStore.clearDictData();
      const dictTypes = Object.keys(dictStore.dictData);
      if (dictTypes.length > 0) {
        await dictStore.getDict(dictTypes);
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
