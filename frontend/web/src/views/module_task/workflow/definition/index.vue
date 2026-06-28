<!-- 工作流定义：Art + useTable -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="workflowSearchItems"
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
            :perm-create="['module_task:workflow:definition:create']"
            :perm-delete="['module_task:workflow:definition:delete']"
            :delete-loading="batchDeleting"
            :create-loading="createLoading"
            @add="handleAdd"
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
      </FaTable>
    </ElCard>

    <FaWorkflowDesignDrawer
      v-model:visible="createVisible"
      :workflow="selectedWorkflow"
      @refresh="onDrawerRefresh"
    />
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Workflow",
  inheritAttrs: false,
});

import WorkflowDefinitionAPI, { type WorkflowTable } from "@/api/module_task/workflow/definition";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaWorkflowDesignDrawer from "./components/FaWorkflowDesignDrawer.vue";
import { useTable } from "@/hooks/core/useTable";
import type { ColumnOption } from "@/types/component";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@/utils/table";
import { ElMessage, ElMessageBox } from "element-plus";
import { computed, ref } from "vue";

const { hasAuth } = useAuth();

const BATCH_DELETE_MSG = "确认删除选中的工作流吗？";

type WorkflowSearchForm = {
  name?: string;
  code?: string;
  status?: number;
};

function buildWorkflowReplaceParams(u: WorkflowSearchForm): Record<string, unknown> {
  return {
    name: u.name,
    code: u.code,
    status: u.status,
  };
}

const searchForm = ref<WorkflowSearchForm>({
  name: undefined,
  code: undefined,
  status: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const workflowSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "流程名称",
    key: "name",
    type: "input",
    placeholder: "请输入流程名称",
    clearable: true,
    span: 6,
  },
  {
    label: "流程编码",
    key: "code",
    type: "input",
    placeholder: "请输入流程编码",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      clearable: true,
      options: [
        { label: "草稿", value: 0 },
        { label: "已发布", value: 1 },
        { label: "已归档", value: 2 },
      ],
    },
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<WorkflowTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => typeof id === "number")
);
const batchDeleting = ref(false);
const createLoading = ref(false);

function onTableSelectionChange(rows: WorkflowTable[]) {
  selectedRows.value = rows;
}

async function deleteWorkflowRow(id: number | undefined) {
  if (id == null) return;
  try {
    await ElMessageBox.confirm("确认删除该工作流吗？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await WorkflowDefinitionAPI.deleteWorkflow([id]);
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
    await WorkflowDefinitionAPI.deleteWorkflow(ids);
    selectedRows.value = [];
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

function buildWorkflowRowActions(row: WorkflowTable): TableOperationAction[] {
  const all: TableOperationAction[] = [];
  if (row.status === 0) {
    all.push({
      key: "publish",
      label: "发布",
      artType: "add",
      perm: "module_task:workflow:definition:update",
      run: () => handlePublish(row),
    });
  }
  if (row.status === 1) {
    all.push({
      key: "execute",
      label: "执行",
      artType: "view",
      perm: "module_task:workflow:definition:execute",
      run: () => handleExecute("execute", row),
    });
  }
  all.push(
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_task:workflow:definition:update",
      run: () => handleEdit(row),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_task:workflow:definition:delete",
      run: () => deleteWorkflowRow(row.id),
    }
  );
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatWorkflowOperationCell(row: WorkflowTable) {
  return renderTableOperationCell(buildWorkflowRowActions(row));
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
  refreshUpdate,
} = useTable({
  core: {
    apiFn: WorkflowDefinitionAPI.getWorkflowList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<WorkflowTable>[] => [
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
        minWidth: 160,
        showOverflowTooltip: true,
      },
      {
        prop: "code",
        label: "编码",
        minWidth: 120,
        showOverflowTooltip: true,
      },
      {
        prop: "status",
        label: "状态",
        minWidth: 100,
        align: "center",
        status: {
          0: { type: "info", text: "草稿" },
          1: { type: "success", text: "已发布" },
          2: { type: "warning", text: "已归档" },
        },
      },
      {
        prop: "description",
        label: "描述",
        minWidth: 160,
        showOverflowTooltip: true,
      },
      {
        prop: "created_time",
        label: "创建时间",
        minWidth: 180,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 160,
        fixed: "right",
        align: "center",
        formatter: (row: WorkflowTable) => formatWorkflowOperationCell(row),
      },
    ],
  },
});

async function handleSearchBarSearch(params: WorkflowSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildWorkflowReplaceParams(params));
  getData();
}

async function onResetSearch() {
  searchForm.value = {
    name: undefined,
    code: undefined,
    status: undefined,
  };
  await resetSearchParams();
}

const selectedWorkflow = ref<WorkflowTable>();
const createVisible = ref(false);

async function handleAdd() {
  createLoading.value = true;
  try {
    handleCreate();
  } finally {
    createLoading.value = false;
  }
}

function handleCreate() {
  selectedWorkflow.value = undefined;
  createVisible.value = true;
}

function handleEdit(record: WorkflowTable) {
  selectedWorkflow.value = record;
  createVisible.value = true;
}

function onDrawerRefresh() {
  void refreshUpdate();
}

async function handlePublish(record: WorkflowTable) {
  try {
    await ElMessageBox.confirm("确定要发布此工作流吗？发布后可执行。", "确认发布", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    if (!record.id) {
      ElMessage.error("工作流ID不存在");
      return;
    }
    await WorkflowDefinitionAPI.publishWorkflow(record.id, {});
    await refreshUpdate();
  } catch {
    /* 接口错误已由拦截器提示 */
  }
}

async function handleExecute(action: string, record: WorkflowTable) {
  if (action !== "execute") return;
  try {
    await ElMessageBox.confirm("确定要立即执行此工作流吗？", "确认执行", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    if (!record.id) {
      ElMessage.error("工作流ID不存在");
      return;
    }
    const res = await WorkflowDefinitionAPI.executeWorkflow({
      workflow_id: record.id,
      variables: {},
    });
    if (res.data?.data) {
      const result = res.data.data;
      ElMessage.success(`工作流执行${result.status === 0 ? "成功" : "失败"}`);
    }
    await refreshUpdate();
  } catch {
    ElMessage.error("执行失败");
  }
}
</script>

<style scoped lang="scss"></style>
