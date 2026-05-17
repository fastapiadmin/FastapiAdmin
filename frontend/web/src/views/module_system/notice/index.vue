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
            :perm-create="['module_system:notice:create']"
            :perm-export="['module_system:notice:export']"
            :perm-delete="['module_system:notice:delete']"
            :perm-patch="['module_system:notice:patch']"
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
      width="920px"
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
          :items="noticeDetailItems"
          label-width="120px"
          max-height="75vh"
        >
          <template #notice_type="{ row }">
            <ElTag :type="row?.notice_type === '1' ? 'primary' : 'warning'">
              {{ noticeTypeLabel(row?.notice_type as string) }}
            </ElTag>
          </template>
          <template #notice_content>
            <div class="notice-html-preview">
              <template v-if="detailHasRenderableContent">
                <div v-html="detailContentHtml" />
              </template>
              <p v-else class="notice-html-empty">暂无内容</p>
            </div>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="noticeFormRenderKey"
          scrollbar
          max-height="75vh"
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
              <ElRadio value="0">启用</ElRadio>
              <ElRadio value="1">停用</ElRadio>
            </ElRadioGroup>
          </template>
          <template #notice_content>
            <FaWangEditor
              :model-value="formData.notice_content ?? ''"
              height="min(38vh, 280px)"
              placeholder="请输入公告内容，支持完整排版与插入..."
              :exclude-keys="[]"
              @update:model-value="(v: string) => (formData.notice_content = v)"
            />
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <FaExportDialog
      v-model="exportVisible"
      :content-config="noticeExportContentConfig"
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
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import type { ColumnOption } from "@/types/component";
import NoticeAPI, {
  type NoticeForm,
  type NoticePageQuery,
  type NoticeTable,
} from "@/api/module_system/notice";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import { useDictStore, useNoticeStore } from "@stores";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaUserTableSelect from "@/components/forms/fa-search-bar/FaUserTableSelect.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElTag, ElMessage } from "element-plus";

defineOptions({
  name: "Notice",
  inheritAttrs: false,
});

const dictStore = useDictStore();
const noticeStore = useNoticeStore();
const { hasAuth } = useAuth();

type NoticeSearchForm = {
  notice_title?: string;
  notice_type?: string;
  status?: string;
  created_time?: string[];
  created_id?: number;
};

function normalizeNoticeQuery(params: Record<string, unknown>): NoticePageQuery {
  return cleanEmptyArrayParams({ ...params }) as unknown as NoticePageQuery;
}

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

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<NoticeTable>();

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
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "描述", prop: "description" },
    { label: "内容", prop: "notice_content", slot: "notice_content", span: 4 },
    { label: "创建人", prop: "created_by.name" },
    { label: "更新人", prop: "updated_by.name" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

/** 详情富文本 HTML（用于预览） */
const detailContentHtml = computed({
  get: () => detailFormData.value.notice_content ?? "",
  set: (v: string) => {
    detailFormData.value.notice_content = v;
  },
});

/** 详情是否有可视文本 */
const detailHasRenderableContent = computed(() => {
  const raw = detailFormData.value.notice_content ?? "";
  if (!raw.trim()) return false;
  const plain = raw
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return plain.length > 0;
});

const formData = ref<NoticeForm>({
  id: undefined,
  notice_title: "",
  notice_type: "",
  notice_content: "",
  status: "0",
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
  status: "0",
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
      await noticeStore.getNotice();
    },
  });

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
  {
    label: "状态",
    key: "status",
    type: "input",
    span: 24,
    placeholder: "",
  },
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
    apiFn: NoticeAPI.listNotice,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<NoticeTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "notice_title", label: "通知标题", minWidth: 140, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: NoticeTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "danger" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      {
        prop: "notice_type",
        label: "类型",
        minWidth: 100,
        formatter: (row: NoticeTable) =>
          h(ElTag, { type: row.notice_type === "1" ? "primary" : "warning" }, () =>
            noticeTypeLabel(row.notice_type)
          ),
      },
      { prop: "notice_content", label: "内容", minWidth: 200, showOverflowTooltip: true },
      { prop: "description", label: "描述", minWidth: 140, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
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
        align: "right",
        formatter: (row: NoticeTable) => formatNoticeOperationCell(row),
      },
    ],
  },
});

const noticeCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<NoticeTable>) => {
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
  return normalizeNoticeQuery(sp);
});

const noticeExportContentConfig = computed(() => ({
  permPrefix: "module_system:notice",
  cols: noticeCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeNoticeQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await NoticeAPI.exportNotice(merged as NoticePageQuery);
    return res.data as Blob;
  },
}));

const { exportVisible, openExport } = useImportExport();

function buildNoticeReplaceParams(p: NoticeSearchForm): Record<string, unknown> {
  return {
    notice_title: p.notice_title,
    notice_type: p.notice_type,
    status: p.status,
    created_id: p.created_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

async function handleSearchBarSearch(params: NoticeSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNoticeReplaceParams(params));
  getData();
}

async function applyNoticeSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNoticeReplaceParams(searchForm.value));
  getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyNoticeSearchFromForm();
}

function onResetSearch() {
  searchForm.value = {
    notice_title: undefined,
    notice_type: undefined,
    status: undefined,
    created_time: undefined,
    created_id: undefined,
  };
  void resetSearchParams();
}

async function deleteNoticeRow(id: number) {
  try {
    await confirmDelete();
    await NoticeAPI.deleteNotice([id]);
    await noticeStore.getNotice();
    ElMessage.success("删除成功");
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
        if (row.id != null) deleteNoticeRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
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
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await NoticeAPI.deleteNotice(ids);
    await noticeStore.getNotice();
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
    await NoticeAPI.batchNotice({ ids, status });
    await refreshData();
    await noticeStore.getNotice();
  } catch {
    // 用户取消
  }
}

onMounted(async () => {
  await dictStore.getDict(["sys_notice_type"]);
});
</script>

<style scoped lang="scss">
/* 富文本预览区域阅读样式（与 FaWangEditor 输出 HTML 展示一致） */
.notice-html-preview {
  box-sizing: border-box;
  min-height: 120px;
  max-height: min(360px, 45vh);
  padding: 12px 16px;
  overflow-y: auto;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: calc(var(--custom-radius) / 3 + 2px);
}

.notice-html-empty {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-placeholder);
}

.notice-html-preview :deep(h1),
.notice-html-preview :deep(h2),
.notice-html-preview :deep(h3) {
  margin: 12px 0 8px;
}

.notice-html-preview :deep(p) {
  margin: 8px 0;
  line-height: 1.6;
}

.notice-html-preview :deep(table) {
  margin: 12px 0;
}

.notice-html-preview :deep(table th),
.notice-html-preview :deep(table td) {
  padding: 8px 12px;
}

.notice-html-preview :deep(pre) {
  padding: 12px;
  margin: 12px 0;
  overflow-x: auto;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.notice-html-preview :deep(blockquote) {
  padding-left: 16px;
  margin: 12px 0;
  color: var(--el-text-color-regular);
  border-left: 4px solid var(--el-color-primary);
}

.notice-html-preview :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
