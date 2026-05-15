<!-- 岗位管理：FA + useTable；操作列前 3 个为 ArtButtonTable，其余收入「更多」下拉 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="positionSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    >
      <template #created_id>
        <UserTableSelect
          :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
          @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
          @confirm-click="afterUserSelectSearch"
          @clear-click="afterUserSelectSearch"
        />
      </template>
    </FaSearchBar>

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
            :perm-create="['module_system:position:create']"
            :perm-export="['module_system:position:export']"
            :perm-delete="['module_system:position:delete']"
            :perm-patch="['module_system:position:patch']"
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
      width="720px"
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
          :items="positionDetailItems"
          max-height="75vh"
        />
      </template>
      <template v-else>
        <FaForm
          scrollbar
          max-height="75vh"
          :key="positionFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="positionDialogFormItems"
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
      :content-config="positionExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import PositionAPI, {
  type PositionForm,
  type PositionPageQuery,
  type PositionTable,
} from "@/api/module_system/position";
import { useAuth } from "@/hooks/core/useAuth";
import { useUserStore } from "@stores";
import UserTableSelect from "@views/module_system/user/components/UserTableSelect.vue";

defineOptions({
  name: "Position",
  inheritAttrs: false,
});

const MAX_INLINE_ROW_ACTIONS = 3;
const { hasAuth } = useAuth();
const userStore = useUserStore();

type PositionSearchForm = {
  name?: string;
  status?: string;
  created_time?: string[];
  created_id?: number;
};

function normalizePositionQuery(params: Record<string, unknown>): PositionPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as PositionPageQuery;
}

function buildPositionReplaceParams(p: PositionSearchForm): Record<string, unknown> {
  return {
    name: p.name,
    status: p.status,
    created_id: p.created_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

type RowAction = {
  key: string;
  label: string;
  artType: "add" | "edit" | "delete" | "view" | "more";
  icon?: string;
  perm: string;
  disabled?: boolean;
  run: () => void;
};

function buildPositionRowActions(
  row: PositionTable,
  ctx: {
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): RowAction[] {
  const all: RowAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:position:detail",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_system:position:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_system:position:delete",
      run: () => ctx.onDelete(row.id!),
    },
  ];
  return all.filter((a) => hasAuth(a.perm));
}

function formatPositionOperationCell(
  row: PositionTable,
  ctx: Parameters<typeof buildPositionRowActions>[1]
) {
  const actions = buildPositionRowActions(row, ctx);
  if (actions.length === 0) {
    return h("span", { class: "text-g-400" }, "—");
  }
  const inline = actions.slice(0, MAX_INLINE_ROW_ACTIONS);
  const overflow = actions.slice(MAX_INLINE_ROW_ACTIONS);

  const inlineNodes = inline.map((a) =>
    h(ElTooltip, { content: a.label, placement: "top" }, () =>
      h("span", { class: "inline-flex" }, [
        h(FaButtonTable, {
          type: a.artType,
          icon: a.icon,
          onClick: a.run,
        }),
      ])
    )
  );

  if (overflow.length === 0) {
    return h(
      "div",
      { class: "inline-flex flex-wrap items-center justify-end gap-1 position-table-actions" },
      inlineNodes
    );
  }

  const dropdown = h(
    ElDropdown,
    { trigger: "click" },
    {
      default: () =>
        h(ElTooltip, { content: "更多", placement: "top" }, () =>
          h("span", { class: "inline-flex align-middle" }, [
            h(FaButtonTable, {
              type: "more",
              onClick: () => {},
            }),
          ])
        ),
      dropdown: () =>
        h(
          ElDropdownMenu,
          null,
          overflow.map((a) =>
            h(
              ElDropdownItem,
              {
                key: a.key,
                disabled: a.disabled,
                onClick: () => a.run(),
              },
              () => a.label
            )
          )
        ),
    }
  );

  return h(
    "div",
    { class: "inline-flex flex-wrap items-center justify-end gap-1 position-table-actions" },
    [...inlineNodes, dropdown]
  );
}

const searchForm = ref<PositionSearchForm>({
  name: undefined,
  status: undefined,
  created_time: undefined,
  created_id: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const positionSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "岗位名称",
    key: "name",
    type: "input",
    placeholder: "请输入岗位名称",
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
  {
    label: "创建人",
    key: "created_id",
    type: "input",
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<PositionTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: PositionTable[]) {
  selectedRows.value = rows;
}

async function deletePositionRow(id: number) {
  try {
    await ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await PositionAPI.deletePosition([id]);
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

const opCtx = {
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deletePositionRow,
};

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
    apiFn: PositionAPI.listPosition,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<PositionTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "岗位名称", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: PositionTable) =>
          h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
            row.status === "0" ? "启用" : "停用"
          ),
      },
      { prop: "order", label: "岗位排序", width: 100, showOverflowTooltip: true },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_id",
        label: "创建人",
        minWidth: 100,
        formatter: (row: PositionTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_id",
        label: "更新人",
        minWidth: 100,
        formatter: (row: PositionTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 200,
        fixed: "right",
        align: "right",
        formatter: (row: PositionTable) => formatPositionOperationCell(row, opCtx),
      },
    ],
  },
});

const positionCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<PositionTable>) => {
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
  delete sp.page_no;
  delete sp.page_size;
  return normalizePositionQuery(sp) as unknown as Record<string, unknown>;
});

const positionExportContentConfig = computed(() => ({
  permPrefix: "module_system:position",
  cols: positionCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizePositionQuery({
      ...(exportQueryParams.value as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await PositionAPI.exportPosition(merged as PositionPageQuery);
    return res.data as Blob;
  },
}));

const detailFormData = ref<PositionTable>({});

const positionDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "岗位名称", prop: "name" },
    { label: "排序", prop: "order" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "创建人", prop: "created_by.name" },
    { label: "更新人", prop: "updated_by.name" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
    { label: "描述", prop: "description", span: 4 },
  ];

const formData = ref<PositionForm>({
  id: undefined,
  name: undefined,
  order: 1,
  status: "0",
  description: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  name: [{ required: true, message: "请输入岗位名称", trigger: "blur" }],
  order: [{ required: true, message: "请输入岗位排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择岗位状态", trigger: "blur" }],
});

const initialFormData: PositionForm = {
  id: undefined,
  name: undefined,
  order: 1,
  status: "0",
  description: undefined,
};

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const positionFormRenderKey = ref(0);

const positionDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "岗位名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入岗位名称", maxlength: 50 },
  },
  {
    label: "排序",
    key: "order",
    type: "number",
    span: 24,
    props: { controlsPosition: "right", min: 1 },
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
const submitLoading = ref(false);
const { exportVisible, openExport } = useImportExport();

async function handleSearchBarSearch(params: PositionSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPositionReplaceParams(params));
  getData();
}

async function applyPositionSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPositionReplaceParams(searchForm.value));
  getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyPositionSearchFromForm();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_time: undefined,
    created_id: undefined,
  };
  void resetSearchParams();
}

async function resetForm() {
  dataFormRef.value?.resetFields();
  dataFormRef.value?.clearValidate();
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await PositionAPI.detailPosition(id);
    if (type === "detail") {
      dialogVisible.title = "岗位详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改岗位";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增岗位";
    Object.assign(formData.value, initialFormData);
    formData.value.id = undefined;
  }
  positionFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.value.id;
    try {
      if (id) {
        await PositionAPI.updatePosition(id, { id, ...formData.value });
        await refreshUpdate();
      } else {
        await PositionAPI.createPosition(formData.value);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      await userStore.getUserInfo();
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    batchDeleting.value = true;
    await PositionAPI.deletePosition(ids);
    await userStore.getUserInfo();
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
    await ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await PositionAPI.batchPosition({ ids, status });
    await refreshData();
    await userStore.getUserInfo();
  } catch {
    // 用户取消
  }
}
</script>

<style scoped lang="scss">
.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

:deep(.position-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
