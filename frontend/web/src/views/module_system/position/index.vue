<!-- 岗位管理：FA + useTable；操作列前 3 个为 FaButtonTable，其余收入「更多」下拉 -->
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
      include-audit
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElCard class="fa-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
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
            :create-loading="createLoading"
            :more-loading="moreLoading"
            @add="handleAdd"
            @export="openExport"
            @delete="handleBatchDelete"
            @more="handleMoreClick"
          />
        </template>
      </FaTableHeader>

      <div v-if="isNarrow" class="mobile-card-list mt-4 flex flex-col gap-4">
        <div v-if="data.length" class="flex items-center gap-2 px-1">
          <ElCheckbox
            :model-value="allCardsSelected"
            :indeterminate="selectedRows.length > 0 && !allCardsSelected"
            @change="toggleAllCards"
          >
            {{ $t("common.selectAll") }}
          </ElCheckbox>
        </div>

        <div v-if="!data.length" class="py-12">
          <FaEmptyState
            icon="ri:briefcase-line"
            title="暂无岗位"
            description="新增第一个岗位后在这里展示"
          />
        </div>

        <div
          v-for="row in data"
          :key="row.id"
          class="p-4 rounded-lg bg-(--default-box-color) border border-(--default-border)"
        >
          <div class="flex items-start justify-between gap-2">
            <ElCheckbox
              class="mt-0.5 shrink-0"
              :model-value="isCardSelected(row)"
              @change="(val) => toggleCardRow(row, val)"
            />
            <div class="min-w-0 flex-1">
              <div class="text-sm font-medium truncate">{{ row.name }}</div>
              <div class="mt-0.5 text-xs text-g-600">
                {{ $t("common.sort") }}：{{ row.order ?? "—" }}
              </div>
            </div>
            <FaStatusTag
              :type="row.status === 0 ? 'success' : 'danger'"
              :label="row.status === 0 ? $t('common.enabled') : $t('common.disabled')"
            />
          </div>
          <div class="mt-3 text-xs text-g-600 line-clamp-2">{{ row.description || "—" }}</div>
          <div class="mt-1 text-xs text-g-600">
            {{ $t("common.create") }}：{{ formatDateTime(row.created_time) }}
          </div>
          <div class="mobile-card-actions">
            <ElButton link type="primary" size="small" @click="opCtx.onDetail(row.id!)">
              {{ $t("common.detail") }}
            </ElButton>
            <ElButton link type="primary" size="small" @click="opCtx.onEdit(row.id!)">
              {{ $t("common.edit") }}
            </ElButton>
            <ElButton
              link
              type="danger"
              size="small"
              @click="opCtx.onDelete(row.id!, row.name ?? '')"
            >
              {{ $t("common.delete") }}
            </ElButton>
          </div>
        </div>
        <ElPagination
          v-if="data.length"
          class="justify-center mt-1"
          layout="prev, pager, next"
          :current-page="pagination.current"
          :page-size="pagination.size"
          :total="pagination.total"
          @current-change="handleCurrentChange"
        />
      </div>
      <FaTable
        v-else
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
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @close="handleCloseDialog"
      @confirm="handleSubmit()"
      size="md"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :data="detailFormData"
          :items="positionDetailItems"
          max-height="70vh"
        />
      </template>
      <template v-else>
        <FaForm
          scrollbar
          max-height="70vh"
          :key="positionFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="positionDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="96"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
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
import { useWindowSize } from "@vueuse/core";
import PositionAPI, {
  type PositionForm,
  type PositionPageQuery,
  type PositionTable,
} from "@/api/module_system/position";
import { useUserStore } from "@stores";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage } from "element-plus";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import {
  formatDateTime,
  renderTableOperationCell,
  resolveStatusColumns,
  stripPaginationParams,
  cleanEmptyArrayParams,
  toCrudCols,
  type TableOperationAction,
} from "@utils";

defineOptions({
  name: "Position",
  inheritAttrs: false,
});

const userStore = useUserStore();

type PositionSearchForm = {
  name?: string;
  status?: number;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
};

function normalizePositionQuery(params: Record<string, unknown>): PositionPageQuery {
  return cleanEmptyArrayParams({ ...params }) as unknown as PositionPageQuery;
}

function buildPositionReplaceParams(p: PositionSearchForm): Record<string, unknown> {
  return {
    name: p.name,
    status: p.status,
    created_id: p.created_id,
    updated_id: p.updated_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
    updated_time:
      Array.isArray(p.updated_time) && p.updated_time.length === 2 ? p.updated_time : undefined,
  };
}

function buildPositionRowActions(
  row: PositionTable,
  ctx: {
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number, name: string) => void;
  }
): TableOperationAction[] {
  const all: TableOperationAction[] = [
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
      run: () => ctx.onDelete(row.id!, row.name ?? ""),
    },
  ];
  return all;
}

function formatPositionOperationCell(
  row: PositionTable,
  ctx: Parameters<typeof buildPositionRowActions>[1]
) {
  return renderTableOperationCell(buildPositionRowActions(row, ctx), {
    wrapperClass:
      "inline-flex flex-wrap items-center justify-end gap-1 position-table-actions align-middle",
  });
}

const searchForm = ref<PositionSearchForm>({
  name: undefined,
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: undefined,
  updated_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const STATUS_OPTIONS = [
  { label: "启用", value: 0 },
  { label: "停用", value: 1 },
] as const;

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
      options: STATUS_OPTIONS,
      clearable: true,
    },
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<PositionTable>();

const createLoading = ref(false);
const moreLoading = ref(false);

const { width: viewportWidth } = useWindowSize();

const allCardsSelected = computed(
  () => data.value.length > 0 && selectedRows.value.length === data.value.length
);

function isCardSelected(row: PositionTable) {
  return selectedRows.value.some((item) => item.id === row.id);
}

function toggleCardRow(row: PositionTable, checked: boolean | string | number) {
  const next = checked
    ? [...selectedRows.value.filter((item) => item.id !== row.id), row]
    : selectedRows.value.filter((item) => item.id !== row.id);
  onTableSelectionChange(next);
}

function toggleAllCards(checked: boolean | string | number) {
  onTableSelectionChange(checked ? [...data.value] : []);
}

const isNarrow = computed(() => viewportWidth.value < 1025);

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
    columnsFactory: resolveStatusColumns<PositionTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "岗位名称", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        status: {
          0: { type: "success", text: "启用" },
          1: { type: "danger", text: "停用" },
        },
      },
      { prop: "order", label: "岗位排序", width: 100, showOverflowTooltip: true },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "created_time",
        label: "创建时间",
        width: 190,
        formatter: (row: { created_time?: string | null; updated_time?: string | null }) =>
          formatDateTime(row.created_time),
        sortable: true,
        showOverflowTooltip: true,
      },
      {
        prop: "updated_time",
        label: "更新时间",
        width: 190,
        formatter: (row: { created_time?: string | null; updated_time?: string | null }) =>
          formatDateTime(row.updated_time),
        sortable: true,
        showOverflowTooltip: true,
      },
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
        align: "center",
        formatter: (row: PositionTable) => formatPositionOperationCell(row, opCtx),
      },
    ]),
  },
});

const positionCrudCols = toCrudCols(columns);

const exportQueryParams = computed(() => {
  return normalizePositionQuery(stripPaginationParams(searchParams)) as unknown as Record<
    string,
    unknown
  >;
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

const positionDetailItems: import("@/components/display/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "岗位名称", prop: "name" },
    { label: "排序", prop: "order" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { 0: { type: "success", text: "启用" }, 1: { type: "danger", text: "停用" } },
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
  code: undefined,
  order: 1,
  status: 0,
  description: undefined,
});

const { dialogVisible } = useCrudDialog();

const rules = reactive({
  name: [{ required: true, message: "请输入岗位名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入岗位编码", trigger: "blur" }],
  order: [{ required: true, message: "请输入岗位排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择岗位状态", trigger: "blur" }],
});

const initialFormData: PositionForm = {
  id: undefined,
  name: undefined,
  code: undefined,
  order: 1,
  status: 0,
  description: undefined,
};

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const positionFormRenderKey = ref(0);

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<PositionForm>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey: positionFormRenderKey,
    detailApi: PositionAPI.detailPosition,
    createApi: PositionAPI.createPosition,
    updateApi: PositionAPI.updatePosition,
    titles: { create: "新增岗位", update: "修改岗位", detail: "岗位详情" },
    detailFormData,
    onCreateSuccess: async () => {
      await refreshCreate();
    },
    onUpdateSuccess: async () => {
      await refreshUpdate();
    },
    onSubmitSuccess: async () => {
      await userStore.getUserInfo();
    },
  });

async function handleAdd() {
  createLoading.value = true;
  try {
    await handleOpenDialog("create");
  } finally {
    createLoading.value = false;
  }
}

const positionDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "岗位名称",
    key: "name",
    type: "input",
    span: 12,
    props: { placeholder: "请输入岗位名称", maxlength: 50 },
  },
  {
    label: "岗位编码",
    key: "code",
    type: "input",
    span: 12,
    props: { placeholder: "请输入岗位编码", maxlength: 64 },
  },
  {
    label: "排序",
    key: "order",
    type: "number",
    span: 12,
    props: { controlsPosition: "right", min: 1 },
  },
  {
    label: "状态",
    key: "status",
    type: "radiogroup",
    span: 12,
    props: {
      options: [
        { label: "启用", value: 0 },
        { label: "停用", value: 1 },
      ],
    },
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
const { exportVisible, openExport } = useImportExport();

async function handleSearchBarSearch(params: PositionSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPositionReplaceParams(params));
  await getData();
}

async function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: undefined,
    updated_time: undefined,
  };
  await resetSearchParams();
}

async function deletePositionRow(id: number, name: string) {
  try {
    await confirmDelete(`确定删除「${name}」吗？`);
    await PositionAPI.deletePosition([id]);
    await userStore.getUserInfo();
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
    await confirmBatchDelete(
      ids.length,
      selectedRows.value.map((r) => String(r.name ?? r.id))
    );
    batchDeleting.value = true;
    await PositionAPI.deletePosition(ids);
    await userStore.getUserInfo();
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

async function handleMoreClick(value: "enable" | "disable") {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  try {
    await confirmToggleStatus(value);
    moreLoading.value = true;
    const status = value === "enable" ? 0 : 1;
    await PositionAPI.batchPosition({ ids, status });
    await refreshData();
    await userStore.getUserInfo();
  } catch {
    // 用户取消
  } finally {
    moreLoading.value = false;
  }
}
</script>
