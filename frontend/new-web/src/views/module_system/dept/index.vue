<!-- 部门配置：Art + 树形表格（对齐 system/menu 模版） -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
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

    <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <ArtTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="loadDeptData"
      >
        <template #left>
          <div class="inline-flex flex-wrap items-center gap-2">
            <ArtTableHeaderLeft
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
      </ArtTableHeader>

      <ArtTable
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

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="640px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border>
            <ElDescriptionsItem label="部门名称" :span="2">
              {{ detailFormData.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="部门编码" :span="2">
              {{ detailFormData.code }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="上级部门" :span="2">
              {{ detailFormData.parent_name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "启用" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="排序" :span="2">
              {{ detailFormData.order }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建时间" :span="2">
              {{ detailFormData.created_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新时间" :span="2">
              {{ detailFormData.updated_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="4">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
          </ElDescriptions>
        </ElScrollbar>
      </template>
      <template v-else>
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ArtForm
            :key="deptFormRenderKey"
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
          </ArtForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>
  </div>
</template>

<script setup lang="ts">
import { h, ref, reactive, computed, nextTick, onMounted } from "vue";
import { useTableColumns } from "@/hooks/core/useTableColumns";
import DeptAPI, {
  type DeptForm,
  type DeptPageQuery,
  type DeptTable,
} from "@/api/module_system/dept";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { useUserStore } from "@/store";
import { formatTree } from "@/utils/common";
import { renderTableOperationCell, type TableOperationAction } from "@/utils/table";

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
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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
const selectedRows = ref<DeptTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);
const deptOptions = ref<OptionType[]>([]);

function onTableSelectionChange(rows: DeptTable[]) {
  selectedRows.value = rows;
}

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

function deleteDeptRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await DeptAPI.deleteDept([id]);
      await userStore.getUserInfo();
      ElMessage.success("删除成功");
      selectedRows.value = [];
      await loadDeptData();
    })
    .catch(() => {});
}

const opCtx = {
  onAddChild: (parentId: number) => void handleOpenDialog("create", undefined, parentId),
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteDeptRow,
};

const { columnChecks, columns } = useTableColumns<DeptTable>(() => [
  { type: "selection", width: 48, fixed: "left" },
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

const detailFormData = ref<DeptTable>({ code: "" });

const formData = reactive<DeptForm>({
  id: undefined,
  name: undefined,
  code: "",
  order: 1,
  parent_id: undefined,
  status: "0",
  description: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
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

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const deptFormRenderKey = ref(0);

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

async function resetForm() {
  dataFormRef.value?.ref?.resetFields();
  dataFormRef.value?.ref?.clearValidate();
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(
  type: "create" | "update" | "detail",
  id?: number,
  parentId?: number
) {
  dialogVisible.type = type;
  if (id) {
    const response = await DeptAPI.detailDept(id);
    if (type === "detail") {
      dialogVisible.title = "部门详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改部门";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增部门";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
    if (parentId) {
      formData.parent_id = parentId;
    }
  }
  deptFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    const id = formData.id;
    try {
      if (id) {
        await DeptAPI.updateDept(id, { id, ...formData });
      } else {
        await DeptAPI.createDept(formData);
      }
      dialogVisible.visible = false;
      await resetForm();
      await loadDeptData();
      await userStore.getUserInfo();
    } catch (error: unknown) {
      console.error(error);
    }
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
        await DeptAPI.deleteDept(ids);
        await userStore.getUserInfo();
        ElMessage.success("删除成功");
        selectedRows.value = [];
        await loadDeptData();
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
      try {
        await DeptAPI.batchDept({ ids, status });
        await loadDeptData();
        await userStore.getUserInfo();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {});
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

<style scoped lang="scss">
.art-table-card {
  flex: 1;
}

.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

:deep(.dept-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
