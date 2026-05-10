<!-- 日志管理：Art 布局 + useTable，与 dict 页一致 -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
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
        <UserTableSelect
          :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
          @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
          @confirm-click="afterUserSelectSearch"
          @clear-click="afterUserSelectSearch"
        />
      </template>
    </ArtSearchBar>

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
            :perm-export="['module_system:log:export']"
            :perm-delete="['module_system:log:delete']"
            :delete-loading="batchDeleting"
            @export="openExportModal"
            @delete="handleBatchDelete"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="artTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="960px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
        <ElDescriptions :column="8" border label-width="200px">
          <ElDescriptionsItem label="日志类型" :span="2">
            <ElTag :type="formData.type === 1 ? 'success' : 'primary'">
              {{ formData.type === 1 ? "登录日志" : "操作日志" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="请求路径" :span="2">
            {{ formData.request_path }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="请求方法" :span="2">
            <ElTag :type="getMethodType(formData.request_method)">
              {{ formData.request_method }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="响应状态码" :span="2">
            <ElTag :type="getStatusCodeType(formData.response_code)">
              {{ formData.response_code }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="请求IP" :span="2">
            {{ formData.request_ip }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="处理时间" :span="2">
            {{ formData.process_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="浏览器" :span="2">
            {{ formData.request_browser }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="操作系统" :span="2">
            {{ formData.request_os }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="请求参数" :span="4">
            <JsonPretty :value="formData.request_payload" height="80px" />
          </ElDescriptionsItem>
          <ElDescriptionsItem label="响应数据" :span="4">
            <JsonPretty :value="formData.response_json" height="140px" />
          </ElDescriptionsItem>
          <ElDescriptionsItem label="登录地点" :span="2">
            {{ formData.login_location }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="描述" :span="4">
            {{ formData.description }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="创建人" :span="2">
            {{ formData.created_by?.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新人" :span="2">
            {{ formData.updated_by?.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="创建时间" :span="2">
            {{ formData.created_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新时间" :span="2">
            {{ formData.updated_time }}
          </ElDescriptionsItem>
        </ElDescriptions>
      </ElScrollbar>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <ArtExportDialog
      v-model="exportModalVisible"
      :content-config="logExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, nextTick } from "vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IObject } from "@/components/Core/modal/types";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";
import CopyButton from "@/components/CopyButton/index.vue";
import type { ColumnOption } from "@/types/component";
import LogAPI, { type LogPageQuery, type LogTable } from "@/api/module_system/log";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import UserTableSelect from "@views/module_system/user/components/UserTableSelect.vue";

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
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as LogPageQuery;
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
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<LogTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: LogTable[]) {
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
              ? h(CopyButton, {
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
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  delete sp.page_no;
  delete sp.page_size;
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

const dialogVisible = ref({
  title: "",
  visible: false,
});

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

const exportModalVisible = ref(false);

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
  formData.value = {};
}

async function handleCloseDialog() {
  dialogVisible.value.visible = false;
  await resetForm();
}

async function handleOpenDialog(id: number) {
  dialogVisible.value.title = "日志详情";
  const response = await LogAPI.detailLog(id);
  Object.assign(formData.value, response.data.data ?? {});
  dialogVisible.value.visible = true;
}

function deleteLogRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await LogAPI.deleteLog([id]);
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
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
        await LogAPI.deleteLog(ids);
        ElMessage.success("删除成功");
        artTableRef.value?.elTableRef?.clearSelection();
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

function openExportModal() {
  exportModalVisible.value = true;
}
</script>
