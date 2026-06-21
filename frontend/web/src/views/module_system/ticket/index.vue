<!-- 工单管理：Fa 布局 + useTable，与公告通知页一致 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="ticketSearchItems"
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
      <template #assigned_id>
        <FaUserTableSelect
          :model-value="searchForm.assigned_id == null ? undefined : searchForm.assigned_id"
          @update:model-value="(v: number | undefined) => (searchForm.assigned_id = v)"
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
            :perm-create="['module_system:ticket:create']"
            :perm-export="['module_system:ticket:export']"
            :perm-delete="['module_system:ticket:delete']"
            :perm-patch="['module_system:ticket:patch']"
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
      width="960px"
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
          :items="ticketDetailItems"
          label-width="120px"
          max-height="75vh"
        >
          <template #ticket_type="{ row }">
            <FaStatusTag
              :type="typeTag(row?.ticket_type as string)"
              :label="typeLabel(row?.ticket_type as string)"
            />
          </template>
          <template #status="{ row }">
            <FaStatusTag
              :type="statusTag(row?.status as string)"
              :label="statusLabel(row?.status as string)"
            />
          </template>
          <template #ticket_content>
            <ElScrollbar class="ticket-html-preview" view-class="p-3">
              <template v-if="detailHasRenderableContent">
                <div v-html="detailContentHtml" />
              </template>
              <p v-else class="ticket-html-empty">暂无内容</p>
            </ElScrollbar>
          </template>
          <template #reply_content>
            <ElScrollbar v-if="detailFormData.reply" class="ticket-html-preview" view-class="p-3">
              <div v-html="sanitizedReply" />
            </ElScrollbar>
            <p v-else class="ticket-html-empty">暂无回复</p>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="ticketFormRenderKey"
          scrollbar
          max-height="75vh"
          ref="dataFormRef"
          v-model="formData"
          :items="ticketDialogFormItems"
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
          <template #ticket_type>
            <ElSelect v-model="formData.ticket_type" placeholder="请选择工单类型">
              <ElOption label="💡 建议" value="suggestion" />
              <ElOption label="🐛 缺陷" value="bug" />
              <ElOption label="⚡ 优化" value="optimize" />
              <ElOption label="📋 其他" value="other" />
            </ElSelect>
          </template>
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio :value="0">待处理</ElRadio>
              <ElRadio :value="1">处理中</ElRadio>
              <ElRadio :value="2">已完成</ElRadio>
              <ElRadio :value="3">已关闭</ElRadio>
            </ElRadioGroup>
          </template>
          <template #assigned_id>
            <FaUserTableSelect
              :model-value="formData.assigned_id == null ? undefined : formData.assigned_id"
              @update:model-value="
                (v: number | undefined) => (formData.assigned_id = v ?? undefined)
              "
            />
          </template>
          <template #ticket_content>
            <FaWangEditor
              :model-value="formData.ticket_content ?? ''"
              height="min(38vh, 320px)"
              placeholder="请详细描述您的问题、建议或优化想法..."
              :exclude-keys="[]"
              @update:model-value="(v: string) => (formData.ticket_content = v)"
            />
          </template>
          <template #reply_content>
            <FaWangEditor
              :model-value="formData.reply_content ?? ''"
              height="min(38vh, 280px)"
              placeholder="请输入回复内容..."
              :exclude-keys="[]"
              @update:model-value="(v: string) => (formData.reply_content = v)"
            />
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <FaExportDialog
      v-model="exportVisible"
      :content-config="ticketExportContentConfig"
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
import TicketAPI, {
  type TicketForm,
  type TicketPageQuery,
  type TicketTable,
} from "@/api/module_system/ticket";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage, ElSelect, ElOption, ElRadioGroup, ElRadio, ElScrollbar } from "element-plus";
import DOMPurify from "dompurify";

defineOptions({
  name: "Ticket",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type TicketSearchForm = {
  title?: string;
  ticket_type?: string;
  status?: number;
  created_time?: string[];
  created_id?: number;
  assigned_id?: number;
};

function normalizeTicketQuery(params: Record<string, unknown>): TicketPageQuery {
  return cleanEmptyArrayParams({ ...params }) as unknown as TicketPageQuery;
}

const TYPE_MAP: Record<string, string> = {
  suggestion: "建议",
  bug: "缺陷",
  optimize: "优化",
  other: "其他",
};

const STATUS_MAP: Record<string, string> = {
  "0": "待处理",
  "1": "处理中",
  "2": "已完成",
  "3": "已关闭",
};

function typeLabel(t: string) {
  return TYPE_MAP[t] || t;
}
function statusLabel(s: string) {
  return STATUS_MAP[s] || s;
}
function typeTag(t: string): any {
  return { suggestion: "success", bug: "danger", optimize: "warning", other: "info" }[t] || "info";
}
function statusTag(s: string): any {
  return { "0": "warning", "1": "", "2": "success", "3": "info" }[s] || "info";
}

const searchForm = ref<TicketSearchForm>({
  title: undefined,
  ticket_type: undefined,
  status: undefined,
  created_time: undefined,
  created_id: undefined,
  assigned_id: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "待处理", value: "0" },
  { label: "处理中", value: "1" },
  { label: "已完成", value: "2" },
  { label: "已关闭", value: "3" },
]);

const ticketTypeSearchOptions = ref([
  { label: "💡 建议", value: "suggestion" },
  { label: "🐛 缺陷", value: "bug" },
  { label: "⚡ 优化", value: "optimize" },
  { label: "📋 其他", value: "other" },
]);

const ticketSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "工单标题",
    key: "title",
    type: "input",
    placeholder: "请输入工单标题",
    clearable: true,
    span: 6,
  },
  {
    label: "工单类型",
    key: "ticket_type",
    type: "select",
    props: {
      placeholder: "请选择类型",
      options: ticketTypeSearchOptions.value,
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
  {
    label: "处理人",
    key: "assigned_id",
    type: "input",
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<TicketTable>();

const createLoading = ref(false);
const moreLoading = ref(false);

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<TicketTable & { reply_content?: string }>(
  {} as TicketTable & { reply_content?: string }
);

const ticketDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "工单标题", prop: "title", span: 4 },
    { label: "工单类型", prop: "ticket_type", slot: "ticket_type" },
    {
      label: "状态",
      prop: "status",
      slot: "status",
    },
    { label: "处理人", prop: "assigned_by.name" },
    { label: "描述", prop: "description", span: 4 },
    { label: "详细内容", prop: "ticket_content", slot: "ticket_content", span: 4 },
    { label: "回复内容", prop: "reply", slot: "reply_content", span: 4 },
    { label: "创建人", prop: "created_by.name" },
    { label: "更新人", prop: "updated_by.name" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

/** 详情富文本 HTML（用于预览，已做 XSS 净化） */
const detailContentHtml = computed({
  get: () => {
    const raw = detailFormData.value.ticket_content ?? "";
    return DOMPurify.sanitize(raw);
  },
  set: (v: string) => {
    detailFormData.value.ticket_content = v;
  },
});

/** 回复富文本 HTML（已做 XSS 净化） */
const sanitizedReply = computed(() => {
  const raw = detailFormData.value.reply ?? "";
  return raw ? DOMPurify.sanitize(raw) : "";
});

/** 详情是否有可视文本 */
const detailHasRenderableContent = computed(() => {
  const raw = detailFormData.value.ticket_content ?? "";
  if (!raw.trim()) return false;
  const plain = raw
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return plain.length > 0;
});

const formData = ref<TicketForm & { reply_content?: string }>({
  id: undefined,
  title: "",
  ticket_type: "suggestion",
  ticket_content: "",
  status: 0,
  description: undefined,
  assigned_id: undefined,
  reply_content: undefined,
});

const rules = reactive({
  title: [{ required: true, message: "请输入工单标题", trigger: "blur" }],
  ticket_type: [{ required: true, message: "请选择工单类型", trigger: "blur" }],
  ticket_content: [{ required: true, message: "请输入工单内容", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const ticketFormRenderKey = ref(0);

const initialFormData: TicketForm & { reply_content?: string } = {
  id: undefined,
  title: "",
  ticket_type: "suggestion",
  ticket_content: "",
  status: 0,
  description: undefined,
  assigned_id: undefined,
  reply_content: undefined,
};

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } = useCrudForm<
  TicketForm & { reply_content?: string }
>({
  formData,
  initialFormData,
  dialogVisible,
  dataFormRef,
  formRenderKey: ticketFormRenderKey,
  detailApi: TicketAPI.detailTicket,
  createApi: TicketAPI.createTicket,
  updateApi: TicketAPI.updateTicket,
  titles: { create: "提交工单", update: "处理工单", detail: "工单详情" },
  detailFormData,
  onCreateSuccess: async () => {
    await refreshCreate();
  },
  onUpdateSuccess: async () => {
    await refreshUpdate();
  },
  onSubmitSuccess: async () => {
    await refreshData();
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

const ticketDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "工单标题",
    key: "title",
    type: "input",
    span: 24,
    props: { placeholder: "请输入工单标题", maxlength: 200 },
  },
  {
    label: "工单类型",
    key: "ticket_type",
    type: "select",
    span: 12,
    props: {
      placeholder: "请选择类型",
      clearable: true,
    },
  },
  {
    label: "状态",
    key: "status",
    type: "input",
    span: 12,
    placeholder: "",
  },
  {
    label: "处理人",
    key: "assigned_id",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "详细描述",
    key: "ticket_content",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "回复内容",
    key: "reply_content",
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
    apiFn: TicketAPI.listTicket,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: resolveStatusColumns<TicketTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "title", label: "工单标题", minWidth: 180, showOverflowTooltip: true },
      {
        prop: "ticket_type",
        label: "工单类型",
        width: 100,
        status: {
          suggestion: { type: "success", text: "建议" },
          bug: { type: "danger", text: "缺陷" },
          optimize: { type: "warning", text: "优化" },
          other: { type: "info", text: "其他" },
        },
      },
      {
        prop: "status",
        label: "状态",
        width: 100,
        status: {
          "0": { type: "warning", text: "待处理" },
          "1": { type: "info", text: "处理中" },
          "2": { type: "success", text: "已完成" },
          "3": { type: "info", text: "已关闭" },
        },
      },
      {
        prop: "assigned_by",
        label: "处理人",
        minWidth: 100,
        formatter: (row: TicketTable) => row.assigned_by?.name ?? "—",
      },
      { prop: "ticket_content", label: "内容摘要", minWidth: 200, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_by",
        label: "创建人",
        minWidth: 100,
        formatter: (row: TicketTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 280,
        fixed: "right",
        align: "right",
        formatter: (row: TicketTable) => formatTicketOperationCell(row),
      },
    ]),
  },
});

const ticketCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<TicketTable>) => {
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
  return normalizeTicketQuery(sp);
});

const ticketExportContentConfig = computed(() => ({
  permPrefix: "module_system:ticket",
  cols: ticketCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeTicketQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await TicketAPI.exportTicket(merged as TicketPageQuery);
    return res.data as unknown as Blob;
  },
}));

const { exportVisible, openExport } = useImportExport();

function buildTicketReplaceParams(p: TicketSearchForm): Record<string, unknown> {
  return {
    title: p.title,
    ticket_type: p.ticket_type,
    status: p.status,
    created_id: p.created_id,
    assigned_id: p.assigned_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

async function handleSearchBarSearch(params: TicketSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildTicketReplaceParams(params));
  getData();
}

async function applyTicketSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildTicketReplaceParams(searchForm.value));
  getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyTicketSearchFromForm();
}

function onResetSearch() {
  searchForm.value = {
    title: undefined,
    ticket_type: undefined,
    status: undefined,
    created_time: undefined,
    created_id: undefined,
    assigned_id: undefined,
  };
  void resetSearchParams();
}

async function deleteTicketRow(id: number) {
  try {
    await confirmDelete();
    await TicketAPI.deleteTicket([id]);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

function buildTicketRowActions(row: TicketTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:ticket:detail",
      run: () => {
        if (row.id != null) void handleOpenDialog("detail", row.id);
      },
    },
    {
      key: "process",
      label: "处理",
      artType: "edit",
      icon: "ri:settings-line",
      perm: "module_system:ticket:update",
      run: () => {
        if (row.id != null) void handleOpenDialog("update", row.id);
      },
    },
    {
      key: "close",
      label: "关闭",
      artType: "delete",
      icon: "ri:close-circle-line",
      perm: "module_system:ticket:update",
      run: () => {
        if (row.id != null) void closeTicket(row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:ticket:delete",
      run: () => {
        if (row.id != null) deleteTicketRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatTicketOperationCell(row: TicketTable) {
  return renderTableOperationCell(buildTicketRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 ticket-table-actions",
  });
}

async function closeTicket(id: number) {
  try {
    await TicketAPI.updateTicket(id, { status: 3 });
    ElMessage.success("工单已关闭");
    await refreshData();
  } catch {
    ElMessage.error("关闭失败");
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await TicketAPI.deleteTicket(ids);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

async function handleMoreClick(status: number) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  try {
    await confirmToggleStatus(status);
    moreLoading.value = true;
    await TicketAPI.batchTicket({ ids, status });
    await refreshData();
  } catch {
    // 用户取消
  } finally {
    moreLoading.value = false;
  }
}
</script>

<style scoped lang="scss">
/* 富文本预览区域阅读样式（与 FaWangEditor 输出 HTML 展示一致） */
.ticket-html-preview {
  box-sizing: border-box;
  min-height: 120px;
  max-height: min(360px, 45vh);
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: calc(var(--custom-radius) / 3 + 2px);
}

.ticket-html-empty {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-placeholder);
}

.ticket-html-preview :deep(h1),
.ticket-html-preview :deep(h2),
.ticket-html-preview :deep(h3) {
  margin: 12px 0 8px;
}

.ticket-html-preview :deep(p) {
  margin: 8px 0;
  line-height: 1.6;
}

.ticket-html-preview :deep(table) {
  margin: 12px 0;
}

.ticket-html-preview :deep(table th),
.ticket-html-preview :deep(table td) {
  padding: 8px 12px;
}

.ticket-html-preview :deep(pre) {
  padding: 12px;
  margin: 12px 0;
  overflow-x: auto;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.ticket-html-preview :deep(blockquote) {
  padding-left: 16px;
  margin: 12px 0;
  color: var(--el-text-color-regular);
  border-left: 4px solid var(--el-color-primary);
}

.ticket-html-preview :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
