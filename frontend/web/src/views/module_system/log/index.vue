<!-- 日志管理：Fa 布局 + useTable，与 dict 页一致 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="logSearchItems"
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
            :perm-export="['module_system:log:export']"
            :perm-delete="['module_system:log:delete']"
            :delete-loading="batchDeleting"
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
      width="960px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      form-mode="detail"
      @confirm="handleCloseDialog"
    >
      <FaDescriptions
        :column="8"
        :data="formData"
        :items="logDetailItems"
        label-width="200px"
        max-height="75vh"
      >
        <template #type="{ row }">
          <ElTag :type="row?.type === 1 ? 'success' : 'primary'">
            {{ row?.type === 1 ? "登录日志" : "操作日志" }}
          </ElTag>
        </template>
        <template #request_method="{ row }">
          <ElTag :type="getMethodType(row?.request_method as string)">
            {{ row?.request_method }}
          </ElTag>
        </template>
        <template #response_code="{ row }">
          <ElTag :type="getStatusCodeType(row?.response_code as number)">
            {{ row?.response_code }}
          </ElTag>
        </template>
        <template #request_payload="{ row }">
          <FaJsonPretty :value="row?.request_payload as any" height="80px" />
        </template>
        <template #response_json="{ row }">
          <FaJsonPretty :value="row?.response_json as any" height="140px" />
        </template>
      </FaDescriptions>
    </FaDialog>

    <FaExportDialog
      v-model="exportVisible"
      :content-config="logExportContentConfig"
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
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import type { ColumnOption } from "@/types/component";
import LogAPI, { type LogPageQuery, type LogTable } from "@/api/module_system/log";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaUserTableSelect from "@/components/forms/fa-search-bar/FaUserTableSelect.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaCopyButton from "@/components/others/fa-copy-button/index.vue";
import { ElTag, ElMessage } from "element-plus";

defineOptions({
  name: "Log",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type LogSearchForm = {
  request_path?: string;
  type?: number;
  created_id?: number;
  created_time?: string[];
};

function normalizeLogQuery(params: Record<string, unknown>): LogPageQuery {
  return cleanEmptyArrayParams({ ...params }) as unknown as LogPageQuery;
}

function buildLogReplaceParams(p: LogSearchForm): Record<string, unknown> {
  return {
    request_path: p.request_path,
    type:
      p.type !== undefined && p.type !== null && p.type !== ("" as unknown as number)
        ? Number(p.type)
        : undefined,
    created_id: p.created_id,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

const searchForm = ref<LogSearchForm>({
  request_path: undefined,
  type: undefined,
  created_id: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const logTypeOptions = ref([
  { label: "登录日志", value: 1 },
  { label: "操作日志", value: 2 },
]);

const logSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "请求路径",
    key: "request_path",
    type: "input",
    placeholder: "请输入请求路径",
    clearable: true,
    span: 6,
  },
  {
    label: "日志类型",
    key: "type",
    type: "select",
    props: {
      placeholder: "请选择日志类型",
      options: logTypeOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "创建人",
    key: "created_id",
    type: "input",
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
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<LogTable>();

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
  refreshRemove,
} = useTable({
  core: {
    apiFn: LogAPI.listLog,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<LogTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "type",
        label: "日志类型",
        minWidth: 100,
        formatter: (row: LogTable) =>
          h(ElTag, { type: row.type === 1 ? "success" : "primary" }, () =>
            row.type === 1 ? "登录日志" : "操作日志"
          ),
      },
      { prop: "request_path", label: "请求路径", minWidth: 200, showOverflowTooltip: true },
      {
        prop: "request_method",
        label: "请求方法",
        minWidth: 100,
        formatter: (row: LogTable) =>
          h(ElTag, { type: getMethodType(row.request_method) }, () => row.request_method ?? ""),
      },
      {
        prop: "response_code",
        label: "状态码",
        minWidth: 100,
        formatter: (row: LogTable) =>
          h(ElTag, { type: getStatusCodeType(row.response_code) }, () =>
            String(row.response_code ?? "")
          ),
      },
      {
        prop: "request_ip",
        label: "请求IP",
        minWidth: 180,
        formatter: (row: LogTable) =>
          h("span", { class: "inline-flex items-center flex-wrap gap-0.5" }, [
            row.request_ip ?? "",
            row.request_ip
              ? h(FaCopyButton, {
                  text: row.request_ip,
                  style: { marginLeft: "2px" },
                })
              : null,
          ]),
      },
      { prop: "process_time", label: "处理时间", minWidth: 120 },
      { prop: "request_browser", label: "浏览器", minWidth: 220, showOverflowTooltip: true },
      { prop: "request_os", label: "系统", minWidth: 100 },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_id",
        label: "创建人",
        minWidth: 120,
        formatter: (row: LogTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_id",
        label: "更新人",
        minWidth: 120,
        formatter: (row: LogTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 160,
        fixed: "right",
        align: "right",
        formatter: (row: LogTable) => formatLogOperationCell(row),
      },
    ],
  },
});

const logCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<LogTable>) => {
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
  return normalizeLogQuery(sp);
});

const logExportContentConfig = computed(() => ({
  permPrefix: "module_system:log",
  cols: logCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeLogQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await LogAPI.exportLog(merged as LogPageQuery);
    return res.data as Blob;
  },
}));

const formData = ref<LogTable>({});

const logDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] = [
  { label: "日志类型", prop: "type", slot: "type" },
  { label: "请求路径", prop: "request_path" },
  { label: "请求方法", prop: "request_method", slot: "request_method" },
  { label: "响应状态码", prop: "response_code", slot: "response_code" },
  { label: "请求IP", prop: "request_ip" },
  { label: "处理时间", prop: "process_time" },
  { label: "浏览器", prop: "request_browser" },
  { label: "操作系统", prop: "request_os" },
  { label: "请求参数", prop: "request_payload", slot: "request_payload", span: 4 },
  { label: "响应数据", prop: "response_json", slot: "response_json", span: 4 },
  { label: "登录地点", prop: "login_location" },
  { label: "描述", prop: "description", span: 4 },
  { label: "创建人", prop: "created_by.name" },
  { label: "更新人", prop: "updated_by.name" },
  { label: "创建时间", prop: "created_time" },
  { label: "更新时间", prop: "updated_time" },
];

const { dialogVisible, closeDialog } = useCrudDialog();

function getStatusCodeType(code?: number) {
  if (code === undefined) return "info";
  if (code >= 200 && code < 300) return "success";
  if (code >= 300 && code < 400) return "warning";
  return "danger";
}

function getMethodType(method?: string) {
  if (method === undefined) return "info";
  if (method === "GET") return "info";
  if (method === "POST") return "success";
  if (method === "PUT" || method === "PATCH") return "warning";
  if (method === "DELETE") return "danger";
  return "info";
}

const { exportVisible, openExport } = useImportExport();

async function handleSearchBarSearch(params: LogSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildLogReplaceParams(params));
  getData();
}

async function applyLogSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildLogReplaceParams(searchForm.value));
  getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyLogSearchFromForm();
}

function onResetSearch() {
  searchForm.value = {
    request_path: undefined,
    type: undefined,
    created_id: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

async function resetForm() {
  Object.assign(formData, {});
}

async function handleCloseDialog() {
  closeDialog();
  await resetForm();
}

async function handleOpenDialog(id: number) {
  dialogVisible.title = "日志详情";
  const response = await LogAPI.detailLog(id);
  Object.assign(formData, response.data.data ?? {});
  dialogVisible.visible = true;
}

async function deleteLogRow(id: number) {
  try {
    await confirmDelete();
    await LogAPI.deleteLog([id]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

function buildLogRowActions(row: LogTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:log:detail",
      run: () => {
        if (row.id != null) void handleOpenDialog(row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:log:delete",
      run: () => {
        if (row.id != null) deleteLogRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatLogOperationCell(row: LogTable) {
  return renderTableOperationCell(buildLogRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 log-table-actions",
  });
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await LogAPI.deleteLog(ids);
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
