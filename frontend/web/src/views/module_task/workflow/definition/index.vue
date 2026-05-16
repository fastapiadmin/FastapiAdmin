<!-- 工作流定义：Art + useTable -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="workflowSearchItems"
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
            :perm-create="['module_task:workflow:definition:create']"
            :perm-delete="['module_task:workflow:definition:delete']"
            :delete-loading="batchDeleting"
            @add="handleCreate"
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
        <template #workflow-operation="{ row }">
          <ElSpace class="flex">
            <ElButton
              v-if="row.status === 'draft'"
              v-hasPerm="['module_task:workflow:definition:update']"
              type="success"
              size="small"
              link
              icon="upload"
              @click="handlePublish(row)"
            >
              发布
            </ElButton>
            <ElDropdown
              v-if="row.status === 'published'"
              v-hasPerm="['module_task:workflow:definition:execute']"
              @command="(e: string) => handleExecute(e, row)"
            >
              <ElButton type="warning" size="small" link icon="video-play">
                执行
                <ElIcon><ArrowDown /></ElIcon>
              </ElButton>
              <template #dropdown>
                <ElDropdownMenu>
                  <ElDropdownItem command="execute">立即执行</ElDropdownItem>
                </ElDropdownMenu>
              </template>
            </ElDropdown>
            <ElButton
              v-hasPerm="['module_task:workflow:definition:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleEdit(row)"
            >
              编辑
            </ElButton>
            <ElButton
              v-hasPerm="['module_task:workflow:definition:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="deleteWorkflowRow(row.id)"
            >
              删除
            </ElButton>
          </ElSpace>
        </template>
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
  name: "WorkflowDefinition",
  inheritAttrs: false,
});

import WorkflowDefinitionAPI, { type WorkflowTable } from "@/api/module_task/workflow/definition";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaTable from "@/components/tables/fa-table/index.vue";
import FaTableHeader from "@/components/tables/fa-table-header/index.vue";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import { useTable } from "@/hooks/core/useTable";
import type { ColumnOption } from "@/types/component";
import { ArrowDown } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { computed, h, ref } from "vue";

const BATCH_DELETE_MSG = "确认删除选中的工作流吗？";

type WorkflowSearchForm = {
  name?: string;
  code?: string;
  status?: string;
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
        { label: "草稿", value: "draft" },
        { label: "已发布", value: "published" },
        { label: "已归档", value: "archived" },
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
    await WorkflowDefinitionAPI.deleteWorkflow(ids);
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

function getStatusType(status: string): "success" | "warning" | "info" | "danger" | "primary" {
  const typeMap: Record<string, "success" | "warning" | "info" | "danger" | "primary"> = {
    draft: "info",
    published: "success",
    archived: "warning",
  };
  return typeMap[status] ?? "info";
}

function getStatusText(status: string) {
  const textMap: Record<string, string> = {
    draft: "草稿",
    published: "已发布",
    archived: "已归档",
  };
  return textMap[status] || status;
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
        formatter: (row) =>
          h(ElTag, { type: getStatusType(row.status ?? "") }, () =>
            getStatusText(row.status ?? "")
          ),
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
        width: 260,
        fixed: "right",
        align: "center",
        useSlot: true,
        slotName: "workflow-operation",
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
    ElMessage.success("发布成功");
    await refreshUpdate();
  } catch {
    ElMessage.error("发布失败");
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
      ElMessage.success(`工作流执行${result.status === "completed" ? "成功" : "失败"}`);
    }
    await refreshUpdate();
  } catch {
    ElMessage.error("执行失败");
  }
}
</script>

<style scoped lang="scss"></style>
