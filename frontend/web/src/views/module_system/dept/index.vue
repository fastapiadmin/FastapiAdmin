<!-- 部门配置：FA + 树形表格（对齐 system/menu 模版） -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="deptSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
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
        @refresh="loadDeptData"
      >
        <template #left>
          <div class="inline-flex flex-wrap items-center gap-2">
            <FaTableHeaderLeft
              :remove-ids="selectedIds"
              :perm-create="['module_system:dept:create']"
              :perm-delete="['module_system:dept:delete']"
              :perm-patch="['module_system:dept:patch']"
              :delete-loading="batchDeleting"
              @add="handleOpenDialog('create')"
              @delete="handleBatchDelete"
              @more="handleMoreClick"
            />
            <ElButton @click="toggleExpand">{{ isExpanded ? "收起" : "展开" }}</ElButton>
          </div>
        </template>
      </FaTableHeader>

      <FaTable
        ref="tableRef"
        row-key="id"
        :loading="loading"
        :columns="columns"
        :data="tableData"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        :default-expand-all="false"
        @selection-change="onTableSelectionChange"
      />
    </ElCard>

    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="640px"
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
          :items="deptDetailItems"
          max-height="75vh"
        />
      </template>
      <template v-else>
        <FaForm
          :key="deptFormRenderKey"
          scrollbar
          max-height="75vh"
          ref="dataFormRef"
          v-model="formData"
          :items="deptDialogFormItems"
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
  </div>
</template>

<script setup lang="ts">
import { useTableColumns } from "@/hooks/core/useTableColumns";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import DeptAPI, {
  type DeptForm,
  type DeptPageQuery,
  type DeptTable,
} from "@/api/module_system/dept";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import { useAuth } from "@/hooks/core/useAuth";
import { useUserStore } from "@stores";
import { formatTree } from "@utils/common";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";

defineOptions({
  name: "Dept",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();
const userStore = useUserStore();

type DeptSearchForm = {
  name?: string;
  status?: string;
  created_time?: string[];
};

function buildDeptQuery(p: DeptSearchForm): DeptPageQuery {
  return {
    name: p.name,
    status: p.status,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

function buildDeptRowActions(
  row: DeptTable,
  ctx: {
    onAddChild: (parentId: number) => void;
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "add",
      label: "新增",
      artType: "add",
      perm: "module_system:dept:create",
      run: () => ctx.onAddChild(row.id!),
    },
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:dept:detail",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_system:dept:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_system:dept:delete",
      run: () => ctx.onDelete(row.id!),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatDeptOperationCell(row: DeptTable, ctx: Parameters<typeof buildDeptRowActions>[1]) {
  const actions = buildDeptRowActions(row, ctx);
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 dept-table-actions",
  });
}

const searchForm = ref<DeptSearchForm>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const deptSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "部门名称",
    key: "name",
    type: "input",
    placeholder: "请输入部门名称",
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
]);

const tableRef = ref<{
  elTableRef?: { toggleRowExpansion: (row: DeptTable, expanded?: boolean) => void };
} | null>(null);
const tableData = ref<DeptTable[]>([]);
const loading = ref(false);
const isExpanded = ref(false);
const deptOptions = ref<OptionType[]>([]);

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<DeptTable>();

async function loadDeptData() {
  loading.value = true;
  try {
    const res = await DeptAPI.listDept(buildDeptQuery(searchForm.value));
    const tree = res.data.data || [];
    tableData.value = tree;
    deptOptions.value = formatTree(tree);
  } catch (e: unknown) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function deleteDeptRow(id: number) {
  try {
    await confirmDelete();
    await DeptAPI.deleteDept([id]);
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await loadDeptData();
  } catch {
    // 用户取消
  }
}

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<DeptTable>({ code: "" });

const deptDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "部门名称", prop: "name" },
    { label: "部门编码", prop: "code" },
    { label: "上级部门", prop: "parent_name" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "排序", prop: "order" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
    { label: "描述", prop: "description", span: 4 },
  ];

const formData = ref<DeptForm>({
  id: undefined,
  name: undefined,
  code: "",
  order: 1,
  parent_id: undefined,
  status: "0",
  description: undefined,
});

const CODE_PATTERN = /^[A-Za-z][A-Za-z0-9_]{1,15}$/;

const rules = reactive({
  name: [{ required: true, message: "请输入部门名称", trigger: "blur" }],
  code: [
    { required: true, message: "请输入部门编码", trigger: "blur" },
    {
      pattern: CODE_PATTERN,
      message: "字母开头，2-16位字母/数字/下划线",
      trigger: "blur",
    },
  ],
  order: [{ required: true, message: "请输入排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const initialFormData: DeptForm = {
  id: undefined,
  name: undefined,
  code: "",
  order: 1,
  parent_id: undefined,
  status: "0",
  description: undefined,
};

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const deptFormRenderKey = ref(0);

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } = useCrudForm<DeptForm>({
  formData,
  initialFormData,
  dialogVisible,
  dataFormRef,
  formRenderKey: deptFormRenderKey,
  detailApi: DeptAPI.detailDept,
  createApi: DeptAPI.createDept,
  updateApi: DeptAPI.updateDept,
  titles: { create: "新增部门", update: "修改部门", detail: "部门详情" },
  detailFormData,
  onCreateSuccess: async () => {
    await loadDeptData();
  },
  onUpdateSuccess: async () => {
    await loadDeptData();
  },
  onSubmitSuccess: async () => {
    await userStore.getUserInfo();
  },
});

const opCtx = {
  onAddChild: (parentId: number) =>
    void handleOpenDialog("create", undefined, { parent_id: parentId }),
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteDeptRow,
};

const { columnChecks, columns } = useTableColumns<DeptTable>(() => [
  { type: "selection", width: 48, fixed: "left" },
  { type: "globalIndex", width: 56, label: "序号" },
  { prop: "name", label: "部门名称", minWidth: 120, showOverflowTooltip: true },
  { prop: "code", label: "部门编码", minWidth: 120, showOverflowTooltip: true },
  {
    prop: "status",
    label: "状态",
    width: 88,
    formatter: (row: DeptTable) =>
      h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
        row.status === "0" ? "启用" : "停用"
      ),
  },
  { prop: "order", label: "排序", width: 88, showOverflowTooltip: true },
  { prop: "description", label: "描述", minWidth: 100, showOverflowTooltip: true },
  { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
  { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
  {
    prop: "operation",
    label: "操作",
    width: 220,
    fixed: "right",
    align: "right",
    formatter: (row: DeptTable) => formatDeptOperationCell(row, opCtx),
  },
]);

const deptDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "部门名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入部门名称", maxlength: 50 },
  },
  {
    label: "部门编码",
    key: "code",
    type: "input",
    span: 24,
    props: {
      placeholder: "字母开头，2-16位字母/数字/下划线",
      maxlength: 16,
      showWordLimit: true,
    },
  },
  {
    label: "上级部门",
    key: "parent_id",
    type: "treeselect",
    span: 24,
    props: {
      placeholder: "请选择上级部门",
      data: deptOptions.value,
      filterable: true,
      checkStrictly: true,
      renderAfterExpand: false,
    },
  },
  {
    label: "排序",
    key: "order",
    type: "number",
    span: 24,
    props: {
      controlsPosition: "right",
      min: 1,
      max: 999,
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

async function handleSearchBarSearch(params: DeptSearchForm) {
  await searchBarRef.value?.validate?.();
  searchForm.value = { ...params };
  await loadDeptData();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_time: undefined,
  };
  void loadDeptData();
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await DeptAPI.deleteDept(ids);
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await loadDeptData();
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
    await DeptAPI.batchDept({ ids, status });
    await loadDeptData();
    await userStore.getUserInfo();
  } catch {
    // 用户取消或操作失败
  }
}

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
  nextTick(() => {
    const el = tableRef.value?.elTableRef;
    if (!el || !tableData.value.length) return;
    const walk = (rows: DeptTable[]) => {
      rows.forEach((row) => {
        if (row.children?.length) {
          el.toggleRowExpansion(row, isExpanded.value);
          walk(row.children);
        }
      });
    };
    walk(tableData.value);
  });
}

onMounted(() => {
  void loadDeptData();
});
</script>
