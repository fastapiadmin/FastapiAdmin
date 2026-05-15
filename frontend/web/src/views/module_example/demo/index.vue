<!-- 示例 CRUD：与角色页同一套 Art 布局；弹窗与 Crud 一致（FaDialog + crud-embed-dialog） -->
<template>
  <div class="fa-full-height">
    <FaSearchBarWithAudit
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="demoBusinessSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearch"
      @reset="onResetSearch"
    />

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
            :perm-create="['module_example:demo:create']"
            :perm-import="['module_example:demo:import']"
            :perm-export="['module_example:demo:export']"
            :perm-delete="['module_example:demo:delete']"
            :perm-patch="['module_example:demo:patch']"
            :delete-loading="batchDeleting"
            @add="openEditDialog('add')"
            @import="openImport"
            @export="openExport"
            @delete="handleBatchDelete"
            @more="runBatchStatus"
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
          :items="demoDetailItems"
          max-height="70vh"
        >
          <template #i="{ row }">
            <JsonPretty v-if="row?.i != null" :value="row?.i" height="140px" />
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="demoFormRenderKey"
          scrollbar
          max-height="70vh"
          ref="dataFormRef"
          v-model="formData"
          :items="demoDialogFormItems"
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
          <template #i>
            <div class="flex flex-col gap-2">
              <div
                v-for="(item, index) in metadataList"
                :key="index"
                class="flex items-center gap-2"
              >
                <ElInput v-model="item.key" placeholder="键" />
                <ElInput v-model="item.value" placeholder="值" />
                <ElButton
                  type="primary"
                  icon="Plus"
                  circle
                  @click="metadataList.push({ key: '', value: '' })"
                />
                <ElButton
                  type="danger"
                  icon="Delete"
                  circle
                  @click="metadataList.splice(index, 1)"
                />
              </div>
              <ElButton
                v-if="metadataList.length === 0"
                type="primary"
                icon="Plus"
                @click="metadataList.push({ key: '', value: '' })"
              >
                添加元数据
              </ElButton>
            </div>
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <FaImportDialog
      v-model="importVisible"
      :content-config="demoImportContentConfig"
      default-template-file-name="demo_import_template.xlsx"
      @upload="handleCrudImportUpload"
    />

    <FaExportDialog
      v-model="exportVisible"
      :content-config="demoExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import type { IContentConfig, IObject } from "@/components/modal/types";
import type { AuditSearchFormParams } from "@/components/forms/fa-search-bar/auditSearchFormItems";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import DemoAPI, {
  type DemoForm,
  type DemoPageQuery,
  type DemoTable,
} from "@/api/module_example/demo";
import { ResultEnum } from "@/enums/api/result.enum";

defineOptions({
  name: "Demo",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type DemoSearchFormParams = { name?: string; status?: string } & AuditSearchFormParams;

function normalizeDemoQuery(params: Record<string, unknown>): DemoPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DemoPageQuery;
}

const searchForm = ref<DemoSearchFormParams>({
  name: undefined,
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: [],
  updated_time: [],
});

/** 搜索区域默认展开展示 */
const showSearchBar = ref(true);

const searchBarRef = ref<InstanceType<typeof FaSearchBarWithAudit> | null>(null);
const searchBarRules: Record<string, unknown> = {};
const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);
/** 名称、状态；创建人/更新人/时间由 FaSearchBarWithAudit 追加 */
const demoBusinessSearchItems = computed(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    placeholder: "请输入名称",
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
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<DemoTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: DemoTable[]) {
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
    apiFn: DemoAPI.getDemoList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<DemoTable>[] => [
      { type: "globalIndex", width: 56, label: "序号" },
      { type: "selection", width: 48, fixed: "left" },
      { prop: "id", label: "ID", width: 72 },
      { prop: "name", label: "名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "uuid", label: "UUID", minWidth: 168, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: DemoTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "info" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      { prop: "a", label: "整数", minWidth: 88, showOverflowTooltip: true },
      { prop: "b", label: "大整数", minWidth: 100, showOverflowTooltip: true },
      { prop: "c", label: "浮点数", minWidth: 88, showOverflowTooltip: true },
      {
        prop: "d",
        label: "布尔",
        width: 80,
        formatter: (row: DemoTable) =>
          h(ElTag, { type: row.d ? "success" : "danger" }, () => (row.d ? "是" : "否")),
      },
      { prop: "e", label: "日期", minWidth: 112, showOverflowTooltip: true },
      { prop: "f", label: "时间", minWidth: 96, showOverflowTooltip: true },
      { prop: "g", label: "日期时间", minWidth: 168, showOverflowTooltip: true },
      { prop: "h", label: "长文本", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "i",
        label: "元数据",
        minWidth: 160,
        formatter: (row: DemoTable) => {
          if (row.i == null) return h("span", { class: "text-g-500" }, "—");
          return h(JsonPretty, { value: row.i, height: "120px" });
        },
      },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_by",
        label: "创建人",
        minWidth: 100,
        formatter: (row: DemoTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_by",
        label: "更新人",
        minWidth: 100,
        formatter: (row: DemoTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: DemoTable) => formatDemoOperationCell(row),
      },
    ],
  },
});

/** 供 CrudImportModal / CrudExportModal 的列配置（与 CrudContent.cols 结构一致） */
const demoCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<DemoTable>) => {
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
  return normalizeDemoQuery(sp);
});

const demoImportContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_example:demo",
  cols: demoCrudCols.value,
  indexAction: async () => ({}),
  importTemplate: () => DemoAPI.downloadTemplateDemo(),
}));

const demoExportContentConfig = computed(() => ({
  permPrefix: "module_example:demo",
  cols: demoCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeDemoQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await DemoAPI.exportDemo(merged as DemoPageQuery);
    return res.data as Blob;
  },
}));

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const detailFormData = ref<DemoTable>({});

const demoDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "名称", prop: "name" },
    { label: "UUID", prop: "uuid" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "整数", prop: "a" },
    { label: "大整数", prop: "b" },
    { label: "浮点数", prop: "c" },
    {
      label: "布尔值",
      prop: "d",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    { label: "日期", prop: "e" },
    { label: "时间", prop: "f" },
    { label: "日期时间", prop: "g" },
    { label: "长文本", prop: "h" },
    { label: "元数据", prop: "i", slot: "i" },
    { label: "描述", prop: "description" },
    { label: "创建人", prop: "created_by.name" },
    { label: "更新人", prop: "updated_by.name" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

// 示例页新增/编辑表单 —— 元数据字段用具名插槽渲染
const demoDialogFormItems: FormItem[] = [
  {
    key: "name",
    label: "名称",
    type: "input",
    props: { placeholder: "请输入名称", maxlength: 50 },
  },
  {
    key: "status",
    label: "状态",
    type: "radiogroup",
    props: {
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
    },
  },
  { key: "a", label: "整数", type: "number", props: { placeholder: "请输入整数" } },
  { key: "b", label: "大整数", type: "number", props: { placeholder: "请输入大整数" } },
  {
    key: "c",
    label: "浮点数",
    type: "number",
    props: { placeholder: "请输入浮点数", step: 0.01, precision: 2 },
  },
  { key: "d", label: "布尔值", type: "switch" },
  {
    key: "e",
    label: "日期",
    type: "date",
    props: { placeholder: "请选择日期", valueFormat: "YYYY-MM-DD", style: "width: 100%" },
  },
  {
    key: "f",
    label: "时间",
    type: "timepicker",
    props: { placeholder: "请选择时间", valueFormat: "HH:mm:ss", style: "width: 100%" },
  },
  {
    key: "g",
    label: "日期时间",
    type: "datetime",
    props: {
      placeholder: "请选择日期时间",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
      style: "width: 100%",
    },
  },
  {
    key: "h",
    label: "长文本",
    type: "input",
    props: { type: "textarea", rows: 4, placeholder: "请输入长文本" },
  },
  {
    key: "description",
    label: "描述",
    type: "input",
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
  { key: "i", label: "元数据", type: "input" /* 由 #i 插槽接管 */ },
];

const formData = ref<DemoForm>({
  id: undefined,
  name: "",
  status: "0",
  description: undefined,
  a: undefined,
  b: undefined,
  c: undefined,
  d: true,
  e: undefined,
  f: undefined,
  g: undefined,
  h: undefined,
  i: undefined,
});

const rules = reactive({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const submitLoading = ref(false);
const demoFormRenderKey = ref(0);
const metadataList = ref<{ key: string; value: string }[]>([]);

const { importVisible, exportVisible, openImport, openExport } = useImportExport();

const initialFormData: DemoForm = {
  id: undefined,
  name: "",
  status: "0",
  description: undefined,
  a: undefined,
  b: undefined,
  c: undefined,
  d: true,
  e: undefined,
  f: undefined,
  g: undefined,
  h: undefined,
  i: undefined,
};

const handleSearch = async (params: DemoSearchFormParams) => {
  await searchBarRef.value?.validate();
  replaceSearchParams({
    name: params.name,
    status: params.status,
    created_id: params.created_id ?? undefined,
    updated_id: params.updated_id ?? undefined,
    created_time:
      Array.isArray(params.created_time) && params.created_time.length === 2
        ? params.created_time
        : undefined,
    updated_time:
      Array.isArray(params.updated_time) && params.updated_time.length === 2
        ? params.updated_time
        : undefined,
  } as Record<string, unknown>);
  getData();
};

const onResetSearch = async () => {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: [],
    updated_time: [],
  };
  await resetSearchParams();
};

function buildDemoRowActions(row: DemoTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      icon: "ri:file-list-3-line",
      perm: "module_example:demo:detail",
      run: () => void openDetailDialog(row),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_example:demo:update",
      run: () => void openEditDialog("edit", row),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_example:demo:delete",
      run: () => deleteDemoRow(row),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatDemoOperationCell(row: DemoTable) {
  return renderTableOperationCell(buildDemoRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 demo-table-actions",
  });
}

async function openDetailDialog(row: DemoTable) {
  if (!row.id) return;
  const response = await DemoAPI.getDemoDetail(row.id);
  dialogVisible.type = "detail";
  dialogVisible.title = "详情";
  detailFormData.value = response.data.data ?? { ...row };
  dialogVisible.visible = true;
}

async function openEditDialog(type: "add" | "edit", row?: DemoTable) {
  dialogVisible.type = type === "add" ? "create" : "update";
  if (type === "add") {
    dialogVisible.title = "新增示例";
    Object.assign(formData.value, initialFormData);
    formData.value.id = undefined;
    metadataList.value = [];
    demoFormRenderKey.value += 1;
  } else if (row?.id) {
    dialogVisible.title = "修改";
    const response = await DemoAPI.getDemoDetail(row.id);
    Object.assign(formData.value, response.data.data);
    if (formData.value.i && typeof formData.value.i === "object") {
      metadataList.value = Object.entries(formData.value.i).map(([key, value]) => ({
        key,
        value: String(value),
      }));
    } else {
      metadataList.value = [];
    }
  }
  dialogVisible.visible = true;
}

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData.value, initialFormData);
  metadataList.value = [];
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    const submitData = { ...formData.value };
    if (metadataList.value.length > 0) {
      const metadataObj: Record<string, string> = {};
      metadataList.value.forEach((item) => {
        if (item.key.trim()) {
          metadataObj[item.key.trim()] = item.value;
        }
      });
      submitData.i = Object.keys(metadataObj).length > 0 ? metadataObj : undefined;
    } else {
      submitData.i = undefined;
    }
    const id = formData.value.id;
    try {
      if (id) {
        await DemoAPI.updateDemo(id, { id, ...submitData });
        await refreshUpdate();
      } else {
        await DemoAPI.createDemo(submitData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

const deleteDemoRow = async (row: DemoTable) => {
  if (!row.id) return;
  try {
    await ElMessageBox.confirm(
      `确定删除「${row.name ?? row.id}」吗？此操作不可恢复！`,
      "删除确认",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await DemoAPI.deleteDemo([row.id!]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    ElMessage.info("已取消删除");
  }
};

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(
      `确定删除选中的 ${ids.length} 条数据吗？此操作不可恢复！`,
      "批量删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    batchDeleting.value = true;
    await DemoAPI.deleteDemo(ids);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    ElMessage.info("已取消删除");
  } finally {
    batchDeleting.value = false;
  }
}

async function runBatchStatus(status: string) {
  const ids = selectedIds.value;
  if (ids.length === 0) {
    ElMessage.warning("请先在列表中勾选数据");
    return;
  }
  try {
    await ElMessageBox.confirm(
      `确认对选中的 ${ids.length} 条数据${status === "0" ? "启用" : "停用"}？`,
      "批量设置",
      { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }
    );
    await DemoAPI.batchDemo({ ids, status });
    ElMessage.success("操作成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshData();
  } catch {
    // 用户取消
  }
}

async function handleCrudImportUpload(formData: FormData) {
  try {
    const res = await DemoAPI.importDemo(formData);
    if (res.data.code !== ResultEnum.SUCCESS) {
      ElMessage.error(res.data.msg || "导入失败");
      return;
    }
    ElMessage.success(res.data.msg || "导入成功");
    importVisible.value = false;
    await refreshData();
  } catch (error) {
    console.error("[Import]", error);
    ElMessage.error("导入失败");
  }
}
</script>
