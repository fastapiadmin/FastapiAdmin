<!-- 公告通知：Art 布局 + useTable，与 dict 页一致 -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
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
            :perm-create="['module_system:notice:create']"
            :perm-export="['module_system:notice:export']"
            :perm-delete="['module_system:notice:delete']"
            :perm-patch="['module_system:notice:patch']"
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
      width="920px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border label-width="120px">
            <ElDescriptionsItem label="标题" :span="2">
              {{ detailFormData.notice_title }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="类型" :span="2">
              <ElTag :type="detailFormData.notice_type === '1' ? 'primary' : 'warning'">
                {{ noticeTypeLabel(detailFormData.notice_type) }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "启用" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="2">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="内容" :span="4">
              <div class="notice-html-preview">
                <template v-if="detailHasRenderableContent">
                  <div v-html="detailContentHtml" />
                </template>
                <p v-else class="notice-html-empty">暂无内容</p>
              </div>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建人" :span="2">
              {{ detailFormData.created_by?.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新人" :span="2">
              {{ detailFormData.updated_by?.name }}
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
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <!-- ArtForm + items + 栅格；弹窗内关闭内置提交/重置，仍用底部按钮 -->
          <ArtForm
            :key="noticeFormRenderKey"
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
              <ArtWangEditor
                :model-value="formData.notice_content ?? ''"
                height="min(38vh, 280px)"
                placeholder="请输入公告内容，支持完整排版与插入..."
                :exclude-keys="[]"
                @update:model-value="(v: string) => (formData.notice_content = v)"
              />
            </template>
          </ArtForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton
            v-if="dialogVisible.type !== 'detail'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <ArtExportDialog
      v-model="exportModalVisible"
      :content-config="noticeExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive, nextTick, onMounted } from "vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IObject } from "@/components/Core/modal/types";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import type { ColumnOption } from "@/types/component";
import NoticeAPI, {
  type NoticeForm,
  type NoticePageQuery,
  type NoticeTable,
} from "@/api/module_system/notice";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useDictStore, useNoticeStore } from "@stores/index";
import UserTableSelect from "@views/module_system/user/components/UserTableSelect.vue";
import ArtWangEditor from "@/components/Core/forms/art-wang-editor/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";

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
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as NoticePageQuery;
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
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<NoticeTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: NoticeTable[]) {
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
    apiFn: NoticeAPI.listNotice,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<NoticeTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
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
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
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

const detailFormData = ref<NoticeTable>({});

/** 详情富文本 HTML（用于预览） */
const detailContentHtml = computed({
  get: () => detailFormData.value.notice_content ?? "",
  set: (v: string) => {
    detailFormData.value.notice_content = v;
  },
});

/** 详情是否有可视文本（排除仅空标签） */
const detailHasRenderableContent = computed(() => {
  const raw = detailFormData.value.notice_content ?? "";
  if (!raw.trim()) return false;
  const plain = raw
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return plain.length > 0;
});

const formData = reactive<NoticeForm>({
  id: undefined,
  notice_title: "",
  notice_type: "",
  notice_content: "",
  status: "0",
  description: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  notice_title: [{ required: true, message: "请输入公告通知标题", trigger: "blur" }],
  notice_type: [{ required: true, message: "请选择公告通知类型", trigger: "blur" }],
  notice_content: [{ required: true, message: "请输入公告通知内容", trigger: "blur" }],
  status: [{ required: true, message: "请选择公告通知状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const submitLoading = ref(false);

/** 每次打开弹窗递增，令 ArtForm 重新挂载并同步初始 model（与示例页声明式 items 一致） */
const noticeFormRenderKey = ref(0);

/** 公告编辑表单字段配置（ArtForm + items） */
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
      class: "!w-full max-w-md",
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

const initialFormData: NoticeForm = {
  id: undefined,
  notice_title: "",
  notice_type: "",
  notice_content: "",
  status: "0",
  description: undefined,
};

const exportModalVisible = ref(false);

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

async function resetForm() {
  const inner = dataFormRef.value?.ref;
  inner?.resetFields();
  inner?.clearValidate();
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await NoticeAPI.detailNotice(id);
    if (type === "detail") {
      dialogVisible.title = "公告通知详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改公告通知";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增公告通知";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
  }
  noticeFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.id;
    try {
      if (id) {
        await NoticeAPI.updateNotice(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await NoticeAPI.createNotice(formData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      await noticeStore.getNotice();
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

function deleteNoticeRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await NoticeAPI.deleteNotice([id]);
      await noticeStore.getNotice();
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
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
        await NoticeAPI.deleteNotice(ids);
        await noticeStore.getNotice();
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
      await NoticeAPI.batchNotice({ ids, status });
      await refreshData();
      await noticeStore.getNotice();
    })
    .catch(() => {});
}

function openExportModal() {
  exportModalVisible.value = true;
}

onMounted(async () => {
  await dictStore.getDict(["sys_notice_type"]);
});
</script>

<style scoped lang="scss">
.art-table-card {
  flex: 1;
}

/* ArtForm 底部预留的操作栏列在弹窗内不需要占位 */
.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

/* 富文本预览区域阅读样式（与 ArtWangEditor 输出 HTML 展示一致） */
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
