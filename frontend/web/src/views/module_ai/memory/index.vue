<!-- AI 会话记录：Art + useTable -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="memorySearchItems"
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
        @refresh="refreshData"
      >
        <template #left>
          <ArtTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_ai:chat:create']"
            :perm-delete="['module_ai:chat:delete']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @delete="handleBatchDelete"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="artTableRef"
        row-key="id"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="paginationBind"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      >
        <template #memory-title="{ row }">
          <ElInput
            v-if="editingRowId === row.id"
            ref="titleInputRef"
            v-model="editingTitle"
            size="small"
            @blur="handleSaveTitle(row)"
            @keyup.enter="handleSaveTitle(row)"
          />
          <span v-else class="editable-cell" title="点击编辑" @click="handleEditTitle(row)">
            {{ row.title || "未命名会话" }}
            <ElIcon class="edit-icon"><Edit /></ElIcon>
          </span>
        </template>
      </ArtTable>
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="920px"
      dialog-class="session-detail-dialog"
      modal-class="session-detail-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="2" border>
            <ElDescriptionsItem label="会话ID" :span="2">
              {{ detailFormData.session_id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="标题" :span="2">
              {{ detailFormData.title }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="用户ID" :span="1">
              {{ detailFormData.user_id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="团队ID" :span="1">
              {{ detailFormData.team_id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="部门名称" :span="1">
              {{ detailFormData.team_name || "未知部门" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="Agent ID" :span="1">
              {{ detailFormData.agent_id }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建时间" :span="1">
              {{ detailFormData.created_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新时间" :span="1">
              {{ detailFormData.updated_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="消息数量" :span="1">
              {{ detailFormData.message_count }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="会话摘要" :span="2">
              {{ detailFormData.summary || "无" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="元数据" :span="2">
              <pre v-if="detailFormData.metadata">{{
                JSON.stringify(detailFormData.metadata, null, 2)
              }}</pre>
              <span v-else>无</span>
            </ElDescriptionsItem>
          </ElDescriptions>

          <ElDivider content-position="left">消息记录</ElDivider>
          <ElTimeline v-if="detailFormData.messages && detailFormData.messages.length > 0">
            <ElTimelineItem
              v-for="(msg, index) in detailFormData.messages"
              :key="index"
              :type="msg.role === 'user' ? 'primary' : 'success'"
              :icon="msg.role === 'user' ? 'User' : 'ChatDotRound'"
            >
              <div class="message-item">
                <div class="message-header">
                  <ElTag size="small" :type="msg.role === 'user' ? 'primary' : 'success'">
                    {{ msg.role === "user" ? "用户" : "助手" }}
                  </ElTag>
                  <span v-if="msg.created_at" class="message-time">
                    {{ formatMsgTime(msg.created_at) }}
                  </span>
                </div>
                <div class="message-content">{{ msg.content }}</div>
              </div>
            </ElTimelineItem>
          </ElTimeline>
          <ElEmpty v-else description="暂无消息记录" :image-size="60" />
        </ElScrollbar>
      </template>
      <template v-else>
        <ArtForm
          :key="memoryFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="memoryDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        />
      </template>

      <template #footer>
        <div class="dialog-footer">
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
defineOptions({
  name: "ChatSession",
  inheritAttrs: false,
});

import { ref, reactive, computed, nextTick } from "vue";
import { Edit } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import AiChatAPI, { type ChatSession, type ChatSessionDetail } from "@/api/module_ai/chat";
import { formatToDateTime } from "@utils/common";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";
import type { ColumnOption } from "@/types/component";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";

type MemorySearchForm = {
  title?: string;
  created_at?: string[];
  updated_at?: string[];
};

function buildMemoryReplaceParams(u: MemorySearchForm): Record<string, unknown> {
  return {
    title: u.title,
    created_at: Array.isArray(u.created_at) && u.created_at.length === 2 ? u.created_at : undefined,
    updated_at: Array.isArray(u.updated_at) && u.updated_at.length === 2 ? u.updated_at : undefined,
  };
}

const searchForm = ref<MemorySearchForm>({
  title: undefined,
  created_at: undefined,
  updated_at: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const { hasAuth } = useAuth();

const memorySearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "标题",
    key: "title",
    type: "input",
    placeholder: "请输入标题",
    clearable: true,
    span: 6,
  },
  {
    label: "创建时间",
    key: "created_at",
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
    label: "更新时间",
    key: "updated_at",
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

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const memoryFormRenderKey = ref(0);

const memoryDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "标题",
    key: "title",
    type: "input",
    span: 24,
    props: { placeholder: "请输入标题", maxlength: 100 },
  },
]);
const titleInputRef = ref();
const editingRowId = ref<string | null>(null);
const editingTitle = ref("");

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<ChatSession[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is string => Boolean(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: ChatSession[]) {
  selectedRows.value = rows;
}

function deleteSessionRow(id: string) {
  ElMessageBox.confirm("确认删除该项数据？", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await AiChatAPI.deleteSession([id]);
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
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
        await AiChatAPI.deleteSession(ids);
        ElMessage.success("删除成功");
        selectedRows.value = [];
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
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
  refreshCreate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: AiChatAPI.getSessionList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<ChatSession>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "session_id",
        label: "会话ID",
        minWidth: 180,
        showOverflowTooltip: true,
      },
      {
        prop: "title",
        label: "标题",
        minWidth: 200,
        useSlot: true,
        slotName: "memory-title",
      },
      {
        prop: "user_id",
        label: "用户ID",
        minWidth: 120,
        visible: false,
      },
      {
        prop: "team_id",
        label: "团队ID",
        minWidth: 120,
        visible: false,
      },
      {
        prop: "team_name",
        label: "部门名称",
        minWidth: 120,
        showOverflowTooltip: true,
      },
      {
        prop: "agent_id",
        label: "Agent ID",
        minWidth: 120,
        showOverflowTooltip: true,
        visible: false,
      },
      {
        prop: "summary",
        label: "会话摘要",
        minWidth: 200,
        showOverflowTooltip: true,
        visible: false,
      },
      {
        prop: "message_count",
        label: "消息数量",
        width: 100,
        align: "center",
      },
      {
        prop: "created_time",
        label: "创建时间",
        width: 168,
        showOverflowTooltip: true,
      },
      {
        prop: "updated_time",
        label: "更新时间",
        width: 168,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 160,
        fixed: "right",
        align: "right",
        formatter: (row: ChatSession) => formatMemoryOperationCell(row),
      },
    ],
  },
});

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

const formData = reactive({
  id: undefined as string | undefined,
  title: "",
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "detail",
});

const detailFormData = ref<Partial<ChatSessionDetail>>({});

const rules = reactive({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
});

const initialFormData = {
  id: undefined as string | undefined,
  title: "",
};

function formatMsgTime(timestamp: number | null): string {
  if (!timestamp) return "";
  return formatToDateTime(new Date(timestamp * 1000));
}

async function handleSearchBarSearch(params: MemorySearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildMemoryReplaceParams(params));
  getData();
}

async function onResetSearch() {
  searchForm.value = {
    title: undefined,
    created_at: undefined,
    updated_at: undefined,
  };
  await resetSearchParams();
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

async function handleOpenDialog(type: "create" | "detail", id?: string) {
  await resetForm();
  dialogVisible.type = type;
  if (id) {
    const response = await AiChatAPI.getSessionDetail(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      detailFormData.value = response.data.data ?? {};
    }
  } else {
    dialogVisible.title = "新增会话";
    formData.id = undefined;
  }
  memoryFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

function buildMemoryRowActions(row: ChatSession): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_ai:chat:detail",
      run: () => {
        void handleOpenDialog("detail", row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_ai:chat:delete",
      run: () => {
        deleteSessionRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatMemoryOperationCell(row: ChatSession) {
  return renderTableOperationCell(buildMemoryRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 memory-table-actions",
  });
}

function handleEditTitle(row: ChatSession) {
  editingRowId.value = row.id;
  editingTitle.value = row.title || "";
  nextTick(() => {
    titleInputRef.value?.focus?.();
  });
}

async function handleSaveTitle(row: ChatSession) {
  if (editingRowId.value !== row.id) return;

  const newTitle = editingTitle.value.trim();
  if (!newTitle) {
    ElMessage.warning("标题不能为空");
    return;
  }

  if (newTitle === row.title) {
    editingRowId.value = null;
    return;
  }

  try {
    await AiChatAPI.updateSession(row.id, { title: newTitle });
    ElMessage.success("更新成功");
    row.title = newTitle;
    editingRowId.value = null;
  } catch (error: unknown) {
    console.error(error);
    ElMessage.error("更新失败");
  }
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    try {
      await AiChatAPI.createSession({ title: formData.title });
      dialogVisible.visible = false;
      await resetForm();
      await refreshCreate();
    } catch (error: unknown) {
      console.error(error);
    }
  });
}
</script>

<style lang="scss" scoped>
.edit-icon {
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.2s;
}

.editable-cell {
  display: flex;
  gap: 8px;
  align-items: center;
  cursor: pointer;

  &:hover {
    color: var(--el-color-primary);

    .edit-icon {
      opacity: 1;
    }
  }
}

.message-item {
  .message-header {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 8px;
  }

  .message-time {
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }

  .message-content {
    padding: 8px 12px;
    word-break: break-all;
    white-space: pre-wrap;
    background: var(--el-fill-color-light);
    border-radius: 4px;
  }
}

pre {
  max-height: 200px;
  padding: 8px;
  margin: 0;
  overflow: auto;
  font-size: 12px;
  background: var(--el-fill-color-light);
  border-radius: 4px;
}

:deep(.session-detail-dialog .el-dialog__body) {
  max-height: 60vh;
  padding: 20px;
  overflow-y: auto;
}

.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}
</style>
