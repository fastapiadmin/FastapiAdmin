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
      width="820px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @close="handleCloseDialog"
      @confirm="handleSubmit()"
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
            <FaMarkdownRenderer :content="detailFormData.notice_content ?? ''" />
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
          :label-width="100"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio :value="0">启用</ElRadio>
              <ElRadio :value="1">停用</ElRadio>
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
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmToggleStatus } from "@/hooks/core/useConfirm";
import NoticeAPI, { type NoticeForm, type NoticeTable } from "@/api/module_system/notice";
import { renderTableOperationCell, resolveStatusColumns, type TableOperationAction } from "@utils";
import { useDictStore, useNoticeStore } from "@stores";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage } from "element-plus";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaDescriptions from "@/components/others/fa-descriptions/index.vue";

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
const { selectedIds, batchDeleting, onTableSelectionChange } = useTableSelection<NoticeTable>();

const createLoading = ref(false);
const moreLoading = ref(false);

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<NoticeTable>({});

const noticeDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
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
    { label: "描述", prop: "description" },
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
        width: 168,
        sortable: true,
        showOverflowTooltip: true,
      },
      {
        prop: "updated_time",
        label: "更新时间",
        width: 168,
        sortable: true,
        showOverflowTooltip: true,
      },
      {
        prop: "created_id",
        label: "创建人",
        minWidth: 100,
        formatter: (row: NoticeTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_id",
        label: "更新人",
        minWidth: 100,
        formatter: (row: NoticeTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 220,
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
