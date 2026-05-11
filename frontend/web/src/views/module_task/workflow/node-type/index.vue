<!-- 工作流节点类型：Art + useTable -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="nodeTypeSearchItems"
      :rules="searchBarRules"
      :is-expand="true"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

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
            :perm-create="['module_task:workflow:node-type:create']"
            :perm-delete="['module_task:workflow:node-type:delete']"
            :delete-loading="batchDeleting"
            @add="openDialog()"
            @delete="handleBatchDelete"
          />
        </template>
      </FaTableHeader>

      <FaTable
        ref="faTableRef"
        row-key="id"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      >
        <template #node-type-operation="{ row }">
          <ElSpace class="flex">
            <ElButton
              v-hasPerm="['module_task:workflow:node-type:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="openDialog(row.id)"
            >
              编辑
            </ElButton>
            <ElButton
              v-hasPerm="['module_task:workflow:node-type:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="deleteNodeTypeRow(row.id)"
            >
              删除
            </ElButton>
          </ElSpace>
        </template>
      </FaTable>
    </ElCard>

    <FaDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="720px"
      destroy-on-close
      @close="handleCloseDialog"
    >
      <FaForm
        :key="nodeTypeFormRenderKey"
        ref="formRef"
        v-model="formData"
        :items="nodeTypeDialogFormItems"
        :rules="rules"
        label-width="100px"
        label-position="right"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form"
      />
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" :loading="submitting" @click="submitForm">保存</ElButton>
      </template>
    </FaDialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "WorkflowNodeType",
  inheritAttrs: false,
});

import WorkflowNodeTypeAPI, {
  type WorkflowNodeTypeForm,
  type WorkflowNodeTypeTable,
} from "@/api/module_task/workflow/node-type";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaTable from "@/components/tables/fa-table/index.vue";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import { useTable } from "@/hooks/core/useTable";
import type { ColumnOption } from "@/types/component";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import type { FormRules } from "element-plus";
import { computed, h, ref } from "vue";

const BATCH_DELETE_MSG = "确认删除选中的编排节点类型吗？";

type NodeTypeSearchForm = {
  name?: string;
  code?: string;
  category?: string;
};

function buildNodeTypeReplaceParams(u: NodeTypeSearchForm): Record<string, unknown> {
  return {
    name: u.name,
    code: u.code,
    category: u.category,
  };
}

const searchForm = ref<NodeTypeSearchForm>({
  name: undefined,
  code: undefined,
  category: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const nodeTypeSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    placeholder: "名称",
    clearable: true,
    span: 6,
  },
  {
    label: "编码",
    key: "code",
    type: "input",
    placeholder: "编码",
    clearable: true,
    span: 6,
  },
  {
    label: "分类",
    key: "category",
    type: "select",
    props: {
      placeholder: "全部",
      clearable: true,
      options: [
        { label: "触发器", value: "trigger" },
        { label: "动作", value: "action" },
        { label: "条件", value: "condition" },
        { label: "控制", value: "control" },
      ],
    },
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<WorkflowNodeTypeTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => typeof id === "number")
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: WorkflowNodeTypeTable[]) {
  selectedRows.value = rows;
}

function categoryLabel(c?: string) {
  const m: Record<string, string> = {
    trigger: "触发器",
    action: "动作",
    condition: "条件",
    control: "控制",
  };
  return c ? m[c] || c : "-";
}

async function deleteNodeTypeRow(id: number | undefined) {
  if (id == null) return;
  try {
    await ElMessageBox.confirm("确认删除该节点类型吗？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await WorkflowNodeTypeAPI.deleteWorkflowNodeType([id]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(BATCH_DELETE_MSG, "批量删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    batchDeleting.value = true;
    await WorkflowNodeTypeAPI.deleteWorkflowNodeType(ids);
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

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
  refreshRemove,
  refreshCreate,
  refreshUpdate,
} = useTable({
  core: {
    apiFn: WorkflowNodeTypeAPI.getWorkflowNodeTypeList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<WorkflowNodeTypeTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "id",
        label: "ID",
        width: 88,
        align: "center",
      },
      {
        prop: "name",
        label: "名称",
        minWidth: 140,
        showOverflowTooltip: true,
      },
      {
        prop: "code",
        label: "编码",
        minWidth: 120,
        showOverflowTooltip: true,
      },
      {
        prop: "category",
        label: "分类",
        minWidth: 100,
        formatter: (row) => categoryLabel(row.category),
      },
      {
        prop: "sort_order",
        label: "排序",
        width: 88,
        align: "center",
      },
      {
        prop: "is_active",
        label: "启用",
        width: 88,
        align: "center",
        formatter: (row) =>
          h(ElTag, { type: row.is_active ? "success" : "info" }, () =>
            row.is_active ? "是" : "否"
          ),
      },
      {
        prop: "created_time",
        label: "创建时间",
        minWidth: 170,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 140,
        fixed: "right",
        align: "center",
        useSlot: true,
        slotName: "node-type-operation",
      },
    ],
  },
});

async function handleSearchBarSearch(params: NodeTypeSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNodeTypeReplaceParams(params));
  getData();
}

async function onResetSearch() {
  searchForm.value = {
    name: undefined,
    code: undefined,
    category: undefined,
  };
  await resetSearchParams();
}

const dialogVisible = ref(false);
const dialogTitle = ref("新增节点类型");
const editingId = ref<number | null>(null);
const submitting = ref(false);
const formRef = ref<InstanceType<typeof FaForm> | null>(null);
const nodeTypeFormRenderKey = ref(0);

const nodeTypeDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    span: 24,
    props: { maxlength: 128, showWordLimit: true },
  },
  {
    label: "编码",
    key: "code",
    type: "input",
    span: 24,
    props: { maxlength: 64, showWordLimit: true, disabled: !!editingId.value },
  },
  {
    label: "分类",
    key: "category",
    type: "select",
    span: 24,
    props: {
      style: { width: "100%" },
      options: [
        { label: "触发器", value: "trigger" },
        { label: "动作", value: "action" },
        { label: "条件", value: "condition" },
        { label: "控制", value: "control" },
      ],
    },
  },
  {
    label: "代码块",
    key: "func",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 12,
      placeholder: "须定义 handler(*args, **kwargs)，可接收 upstream、variables",
    },
  },
  {
    label: "位置参数",
    key: "args",
    type: "input",
    span: 24,
    props: { placeholder: "逗号分隔，如 a, b" },
  },
  {
    label: "关键字参数",
    key: "kwargs",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 3,
      placeholder: 'JSON，如 {"key": "v"}',
    },
  },
  {
    label: "排序",
    key: "sort_order",
    type: "number",
    span: 24,
    props: { min: 0 },
  },
  {
    label: "启用",
    key: "is_active",
    type: "switch",
    span: 24,
  },
]);

const defaultForm = (): WorkflowNodeTypeForm => ({
  name: "",
  code: "",
  category: "action",
  func: "",
  args: "",
  kwargs: "{}",
  sort_order: 0,
  is_active: true,
});

const formData = ref<WorkflowNodeTypeForm>(defaultForm());

const rules: FormRules = {
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入编码", trigger: "blur" }],
  category: [{ required: true, message: "请选择分类", trigger: "change" }],
  func: [{ required: true, message: "请输入代码块", trigger: "blur" }],
};

function resetForm() {
  Object.assign(formData.value, defaultForm());
  editingId.value = null;
  formRef.value?.ref?.resetFields();
  formRef.value?.ref?.clearValidate();
}

function handleCloseDialog() {
  resetForm();
}

async function openDialog(id?: number) {
  resetForm();
  dialogTitle.value = id ? "编辑节点类型" : "新增节点类型";
  editingId.value = id ?? null;
  if (id) {
    try {
      const res = await WorkflowNodeTypeAPI.getWorkflowNodeTypeDetail(id);
      const d = res.data?.data as WorkflowNodeTypeTable | undefined;
      if (d) {
        formData.value.name = d.name || "";
        formData.value.code = d.code || "";
        formData.value.category = (d.category as WorkflowNodeTypeForm["category"]) || "action";
        formData.value.func = d.func || "";
        formData.value.args = d.args || "";
        formData.value.kwargs = d.kwargs || "{}";
        formData.value.sort_order = d.sort_order ?? 0;
        formData.value.is_active = d.is_active ?? true;
      }
    } catch {
      ElMessage.error("加载详情失败");
      return;
    }
  }
  nodeTypeFormRenderKey.value += 1;
  dialogVisible.value = true;
}

async function submitForm() {
  if (!formRef.value) return;
  await formRef.value.validate();
  if (formData.value.kwargs?.trim()) {
    try {
      JSON.parse(formData.value.kwargs);
    } catch {
      ElMessage.error("关键字参数须为合法 JSON");
      return;
    }
  }
  submitting.value = true;
  try {
    if (editingId.value) {
      await WorkflowNodeTypeAPI.updateWorkflowNodeType(editingId.value, formData.value);
      ElMessage.success("更新成功");
      dialogVisible.value = false;
      await refreshUpdate();
    } else {
      await WorkflowNodeTypeAPI.createWorkflowNodeType(formData.value);
      ElMessage.success("创建成功");
      dialogVisible.value = false;
      await refreshCreate();
    }
  } catch {
    ElMessage.error(editingId.value ? "更新失败" : "创建失败");
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}
</style>
