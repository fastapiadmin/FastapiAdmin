<!-- 公告通知：Fa 布局 + useTable，与 dict 页一致 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="noticeSearchItems"
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
    >
      <template #created_id>
        <FaUserTableSelect
          :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
          @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
          @confirm-click="afterUserSelectSearch"
          @clear-click="afterUserSelectSearch"
        />
      </template>
    </FaSearchBar>

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
            :perm-create="['module_system:notice:create']"
            :perm-delete="['module_system:notice:delete']"
            :perm-patch="['module_system:notice:patch']"
            :delete-loading="batchDeleting"
            :create-loading="createLoading"
            :more-loading="moreLoading"
            @add="handleAdd"
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
            icon="ri:notification-3-line"
            title="暂无公告"
            description="发布第一条系统公告，通知到所有用户"
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
            <div class="text-sm font-medium min-w-0 flex-1 truncate">{{ row.notice_title }}</div>
            <div class="flex gap-1 shrink-0">
              <FaStatusTag
                :type="row.notice_type === '2' ? 'warning' : 'primary'"
                :label="row.notice_type === '2' ? '公告' : '通知'"
              />
              <FaStatusTag
                :type="row.status === 0 ? 'success' : 'danger'"
                :label="row.status === 0 ? $t('common.enabled') : $t('common.disabled')"
              />
            </div>
          </div>
          <div class="mt-2 text-xs text-g-600 line-clamp-3">
            {{ row.description || "暂无描述" }}
          </div>
          <div class="mt-2 text-xs text-g-600">
            {{ $t("common.create") }}：{{ formatDateTime(row.created_time) }}
          </div>
          <div class="mt-1 text-xs text-g-600">
            {{ $t("common.update") }}：{{ formatDateTime(row.updated_time) }}
          </div>
          <div class="mobile-card-actions">
            <ElButton link type="primary" size="small" @click="handleOpenDialog('detail', row.id!)">
              {{ $t("common.detail") }}
            </ElButton>
            <ElButton link type="primary" size="small" @click="handleOpenDialog('update', row.id!)">
              {{ $t("common.edit") }}
            </ElButton>
            <ElButton
              link
              type="danger"
              size="small"
              @click="deleteNoticeRow(row.id!, row.notice_title ?? '')"
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
      >
        <template #empty>
          <FaEmptyState
            icon="ri:notification-3-line"
            title="暂无公告"
            description="发布第一条系统公告，通知到所有用户"
          >
            <ElButton type="primary" size="small" @click="handleAdd">{{
              $t("common.addNotice")
            }}</ElButton>
          </FaEmptyState>
        </template>
      </FaTable>
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
      size="xl"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :data="detailFormData"
          :items="noticeDetailItems"
          label-width="120px"
          max-height="70vh"
        >
          <template #notice_type="{ row }">
            <FaStatusTag
              :type="row?.notice_type === '1' ? 'primary' : 'warning'"
              :label="noticeTypeLabel(row?.notice_type as string)"
            />
          </template>
          <template #notice_content>
            <ElScrollbar max-height="min(280px, 34vh)">
              <FaMarkdownRenderer :content="detailFormData.notice_content ?? ''" />
            </ElScrollbar>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="noticeFormRenderKey"
          scrollbar
          max-height="70vh"
          ref="dataFormRef"
          v-model="formData"
          :items="noticeDialogFormItems"
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
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio :value="0">{{ $t("common.enabled") }}</ElRadio>
              <ElRadio :value="1">{{ $t("common.disabled") }}</ElRadio>
            </ElRadioGroup>
          </template>
          <template #notice_content>
            <FaWangEditor
              :model-value="formData.notice_content ?? ''"
              height="min(18vh, 280px)"
              placeholder="请输入公告内容，支持完整排版与插入..."
              :exclude-keys="[]"
              @update:model-value="(v: string) => (formData.notice_content = v)"
            />
          </template>
        </FaForm>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { useWindowSize } from "@vueuse/core";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmToggleStatus } from "@/hooks/core/useConfirm";
import NoticeAPI, { type NoticeForm, type NoticeTable } from "@/api/module_system/notice";
import {
  formatDateTime,
  renderTableOperationCell,
  resolveStatusColumns,
  type TableOperationAction,
} from "@utils";
import { useDictStore, useNoticeStore } from "@stores";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage } from "element-plus";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaDescriptions from "@/components/display/fa-descriptions/index.vue";

defineOptions({
  name: "Notice",
  inheritAttrs: false,
});

const dictStore = useDictStore();
const noticeStore = useNoticeStore();

type NoticeSearchForm = {
  notice_title?: string;
  notice_type?: string;
  status?: number;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
};

function noticeTypeLabel(val?: string) {
  if (!val) return "";
  const lab = dictStore.getDictLabel("sys_notice_type", val);
  if (typeof lab === "string") return lab;
  return lab.dict_label ?? val;
}

const searchForm = ref<NoticeSearchForm>({
  notice_title: undefined,
  notice_type: undefined,
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

const noticeTypeSearchOptions = computed(() =>
  dictStore.getDictArray("sys_notice_type").map((item) => ({
    label: item.dict_label,
    value: item.dict_value,
  }))
);

const noticeSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "标题",
    key: "notice_title",
    type: "input",
    placeholder: "请输入标题",
    clearable: true,
    span: 6,
  },
  {
    label: "类型",
    key: "notice_type",
    type: "select",
    props: {
      placeholder: "请选择类型",
      options: noticeTypeSearchOptions.value,
      clearable: true,
    },
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

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<NoticeTable>();

const createLoading = ref(false);
const moreLoading = ref(false);

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<NoticeTable>({});

const noticeDetailItems: import("@/components/display/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "标题", prop: "notice_title" },
    { label: "类型", prop: "notice_type", slot: "notice_type" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { 0: { type: "success", text: "启用" }, 1: { type: "danger", text: "停用" } },
      },
    },
    { label: "描述", prop: "description", span: 4 },
    { label: "内容", prop: "notice_content", slot: "notice_content", span: 4 },
    { label: "创建人", prop: "created_by.name" },
    { label: "更新人", prop: "updated_by.name" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

const formData = ref<NoticeForm>({
  id: undefined,
  notice_title: "",
  notice_type: "",
  notice_content: "",
  status: 0,
  description: undefined,
});

const rules = reactive({
  notice_title: [{ required: true, message: "请输入公告通知标题", trigger: "blur" }],
  notice_type: [{ required: true, message: "请选择公告通知类型", trigger: "blur" }],
  notice_content: [{ required: true, message: "请输入公告通知内容", trigger: "blur" }],
  status: [{ required: true, message: "请选择公告通知状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const noticeFormRenderKey = ref(0);

const initialFormData: NoticeForm = {
  id: undefined,
  notice_title: "",
  notice_type: "",
  notice_content: "",
  status: 0,
  description: undefined,
};

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<NoticeForm>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey: noticeFormRenderKey,
    detailApi: NoticeAPI.detailNotice,
    createApi: NoticeAPI.createNotice,
    updateApi: NoticeAPI.updateNotice,
    titles: { create: "新增公告通知", update: "修改公告通知", detail: "公告通知详情" },
    detailFormData,
    onCreateSuccess: async () => {
      await refreshCreate();
    },
    onUpdateSuccess: async () => {
      await refreshUpdate();
    },
    onSubmitSuccess: async () => {
      await noticeStore.getNotice(true);
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

const noticeDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "标题",
    key: "notice_title",
    type: "input",
    span: 24,
    props: { placeholder: "请输入标题", maxlength: 50 },
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 2,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
  {
    label: "类型",
    key: "notice_type",
    type: "select",
    span: 24,
    props: {
      placeholder: "请选择类型",
      clearable: true,
      class: "w-full! max-w-md",
      options: dictStore.getDictArray("sys_notice_type").map((item) => ({
        label: item.dict_label,
        value: item.dict_value,
      })),
    },
  },
  { key: "status", label: "状态", type: "radiogroup", span: 24 },
  {
    label: "内容",
    key: "notice_content",
    type: "input",
    span: 24,
    placeholder: "",
  },
]);

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
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
    apiFn: NoticeAPI.listNotice,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: resolveStatusColumns<NoticeTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "notice_title", label: "通知标题", minWidth: 140, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        status: {
          0: { type: "success", text: "启用" },
          1: { type: "danger", text: "停用" },
        },
      },
      {
        prop: "notice_type",
        label: "类型",
        minWidth: 100,
        status: {
          "1": { type: "primary", text: "通知" },
          "2": { type: "warning", text: "公告" },
        },
      },
      { prop: "description", label: "描述", minWidth: 140, showOverflowTooltip: true },
      {
        prop: "created_time",
        label: "创建时间",
        width: 190,
        sortable: true,
        showOverflowTooltip: true,
        formatter: (row: NoticeTable) => formatDateTime(row.created_time),
      },
      {
        prop: "updated_time",
        label: "更新时间",
        width: 190,
        sortable: true,
        showOverflowTooltip: true,
        formatter: (row: NoticeTable) => formatDateTime(row.updated_time),
      },
      {
        prop: "created_id",
        label: "创建人",
        minWidth: 90,
        formatter: (row: NoticeTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_id",
        label: "更新人",
        minWidth: 90,
        formatter: (row: NoticeTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 200,
        fixed: "right",
        align: "center",
        formatter: (row: NoticeTable) => formatNoticeOperationCell(row),
      },
    ]),
  },
});

function buildNoticeReplaceParams(p: NoticeSearchForm): Record<string, unknown> {
  return {
    notice_title: p.notice_title,
    notice_type: p.notice_type,
    status: p.status,
    created_id: p.created_id,
    updated_id: p.updated_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
    updated_time:
      Array.isArray(p.updated_time) && p.updated_time.length === 2 ? p.updated_time : undefined,
  };
}

async function handleSearchBarSearch(params: NoticeSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNoticeReplaceParams(params));
  await getData();
}

async function applyNoticeSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNoticeReplaceParams(searchForm.value));
  await getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyNoticeSearchFromForm();
}

async function onResetSearch() {
  searchForm.value = {
    notice_title: undefined,
    notice_type: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: undefined,
    updated_time: undefined,
  };
  await resetSearchParams();
}

async function deleteNoticeRow(id: number, name: string) {
  try {
    await confirmDelete(`确定删除「${name}」吗？`);
    await NoticeAPI.deleteNotice([id]);
    await noticeStore.getNotice(true);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

const { width: viewportWidth } = useWindowSize();

const allCardsSelected = computed(
  () => data.value.length > 0 && selectedRows.value.length === data.value.length
);

function isCardSelected(row: NoticeTable) {
  return selectedRows.value.some((item) => item.id === row.id);
}

function toggleCardRow(row: NoticeTable, checked: boolean | string | number) {
  const next = checked
    ? [...selectedRows.value.filter((item) => item.id !== row.id), row]
    : selectedRows.value.filter((item) => item.id !== row.id);
  onTableSelectionChange(next);
}

function toggleAllCards(checked: boolean | string | number) {
  onTableSelectionChange(checked ? [...data.value] : []);
}

const isNarrow = computed(() => viewportWidth.value < 1025);

function buildNoticeRowActions(row: NoticeTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:notice:detail",
      run: () => {
        if (row.id != null) void handleOpenDialog("detail", row.id);
      },
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:notice:update",
      run: () => {
        if (row.id != null) void handleOpenDialog("update", row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:notice:delete",
      run: () => {
        if (row.id != null) deleteNoticeRow(row.id, row.notice_title ?? "");
      },
    },
  ];
  return all;
}

function formatNoticeOperationCell(row: NoticeTable) {
  return renderTableOperationCell(buildNoticeRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 notice-table-actions",
  });
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(
      ids.length,
      (data.value as NoticeTable[])
        .filter((r) => ids.includes(r.id!))
        .map((r) => String(r.notice_title ?? r.id))
    );
    batchDeleting.value = true;
    await NoticeAPI.deleteNotice(ids);
    await noticeStore.getNotice(true);
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
    await NoticeAPI.batchNotice({ ids, status });
    await refreshData();
    await noticeStore.getNotice(true);
  } catch {
    // 用户取消或操作失败
  } finally {
    moreLoading.value = false;
  }
}

onMounted(async () => {
  await dictStore.getDict(["sys_notice_type"]);
});
</script>
