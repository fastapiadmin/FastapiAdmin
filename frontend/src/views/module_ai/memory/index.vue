<!-- AI智能助手会话列表 -->
<template>
  <div class="app-container">
    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            会话记忆
            <el-tooltip content="对话会话列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </span>
        </div>
        <!-- 搜索区域 -->
        <div v-show="visible" class="search-container">
          <el-form
            ref="queryFormRef"
            :model="queryFormData"
            label-suffix=":"
            :inline="true"
            @submit.prevent="handleQuery"
          >
            <el-form-item prop="title" label="标题">
              <el-input v-model="queryFormData.title" placeholder="请输入标题" clearable />
            </el-form-item>
            <el-form-item v-if="isExpand" prop="created_time" label="创建时间">
              <DatePicker
                v-model="createdDateRange"
                @update:model-value="handleCreatedDateRangeChange"
              />
            </el-form-item>
            <el-form-item v-if="isExpand" prop="updated_time" label="更新时间">
              <DatePicker
                v-model="updatedDateRange"
                @update:model-value="handleUpdatedDateRangeChange"
              />
            </el-form-item>
            <!-- 查询、重置、展开/收起按钮 -->
            <el-form-item>
              <el-button
                v-hasPerm="['module_example:demo:query']"
                type="primary"
                icon="search"
                @click="handleQuery"
              >
                查询
              </el-button>
              <el-button
                v-hasPerm="['module_example:demo:query']"
                icon="refresh"
                @click="handleResetQuery"
              >
                重置
              </el-button>
              <!-- 展开/收起 -->
              <template v-if="isExpandable">
                <el-link
                  class="ml-3"
                  type="primary"
                  underline="never"
                  @click="isExpand = !isExpand"
                >
                  {{ isExpand ? "收起" : "展开" }}
                  <el-icon>
                    <template v-if="isExpand">
                      <ArrowUp />
                    </template>
                    <template v-else>
                      <ArrowDown />
                    </template>
                  </el-icon>
                </el-link>
              </template>
            </el-form-item>
          </el-form>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_ai:chat:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_ai:chat:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="搜索显示/隐藏">
                <el-button
                  v-hasPerm="['*:*:*']"
                  type="info"
                  icon="search"
                  circle
                  @click="visible = !visible"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_ai:chat:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <div class="data-table__content">
        <el-table
          ref="tableRef"
          v-loading="loading"
          :data="pageTableData"
          height="calc(100vh - 440px)"
          max-height="calc(100vh - 440px)"
          border
          stripe
          @selection-change="handleSelectionChange"
        >
          <template #empty>
            <el-empty :image-size="80" description="暂无数据" />
          </template>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
            type="selection"
            min-width="55"
            align="center"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'index')?.show"
            fixed
            label="序号"
            min-width="60"
          >
            <template #default="scope">
              {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
            </template>
          </el-table-column>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'session_id')?.show"
            label="会话ID"
            prop="session_id"
            min-width="180"
            show-overflow-tooltip
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'title')?.show"
            label="标题"
            prop="title"
            min-width="200"
          >
            <template #default="scope">
              <el-input
                v-if="editingRowId === scope.row.id"
                ref="titleInputRef"
                v-model="editingTitle"
                size="small"
                @blur="handleSaveTitle(scope.row)"
                @keyup.enter="handleSaveTitle(scope.row)"
              />
              <span
                v-else
                class="editable-cell"
                title="点击编辑"
                @click="handleEditTitle(scope.row)"
              >
                {{ scope.row.title || "未命名会话" }}
                <el-icon class="edit-icon"><Edit /></el-icon>
              </span>
            </template>
          </el-table-column>
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'user_id')?.show"
            label="用户ID"
            prop="user_id"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'team_id')?.show"
            label="团队ID"
            prop="team_id"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'team_name')?.show"
            label="部门名称"
            prop="team_name"
            min-width="120"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'agent_id')?.show"
            label="Agent ID"
            prop="agent_id"
            min-width="120"
            show-overflow-tooltip
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'summary')?.show"
            label="会话摘要"
            prop="summary"
            min-width="200"
            show-overflow-tooltip
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'message_count')?.show"
            label="消息数量"
            prop="message_count"
            min-width="100"
            align="center"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'created_time')?.show"
            label="创建时间"
            prop="created_time"
            min-width="180"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show"
            label="更新时间"
            prop="updated_time"
            min-width="180"
          />
          <el-table-column
            v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
            fixed="right"
            label="操作"
            align="center"
            min-width="120"
          >
            <template #default="scope">
              <el-button
                v-hasPerm="['module_ai:chat:detail']"
                type="info"
                size="small"
                link
                icon="document"
                @click="handleOpenDialog('detail', scope.row.id)"
              >
                详情
              </el-button>
              <el-button
                v-hasPerm="['module_ai:chat:delete']"
                type="danger"
                size="small"
                link
                icon="delete"
                @click="handleDelete([scope.row.id])"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      class="session-detail-dialog"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="会话ID" :span="2">
            {{ detailFormData.session_id }}
          </el-descriptions-item>
          <el-descriptions-item label="标题" :span="2">
            {{ detailFormData.title }}
          </el-descriptions-item>
          <el-descriptions-item label="用户ID" :span="1">
            {{ detailFormData.user_id }}
          </el-descriptions-item>
          <el-descriptions-item label="团队ID" :span="1">
            {{ detailFormData.team_id }}
          </el-descriptions-item>
          <el-descriptions-item label="部门名称" :span="1">
            {{ detailFormData.team_name || "未知部门" }}
          </el-descriptions-item>
          <el-descriptions-item label="Agent ID" :span="1">
            {{ detailFormData.agent_id }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="1">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="1">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
          <el-descriptions-item label="消息数量" :span="1">
            {{ detailFormData.message_count }}
          </el-descriptions-item>
          <el-descriptions-item label="会话摘要" :span="2">
            {{ detailFormData.summary || "无" }}
          </el-descriptions-item>
          <el-descriptions-item label="元数据" :span="2">
            <pre v-if="detailFormData.metadata">{{
              JSON.stringify(detailFormData.metadata, null, 2)
            }}</pre>
            <span v-else>无</span>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 消息列表 -->
        <el-divider content-position="left">消息记录</el-divider>
        <el-timeline v-if="detailFormData.messages && detailFormData.messages.length > 0">
          <el-timeline-item
            v-for="(msg, index) in detailFormData.messages"
            :key="index"
            :type="msg.role === 'user' ? 'primary' : 'success'"
            :icon="msg.role === 'user' ? 'User' : 'ChatDotRound'"
          >
            <div class="message-item">
              <div class="message-header">
                <el-tag size="small" :type="msg.role === 'user' ? 'primary' : 'success'">
                  {{ msg.role === "user" ? "用户" : "助手" }}
                </el-tag>
                <span v-if="msg.created_at" class="message-time">
                  {{ formatTime(msg.created_at) }}
                </span>
              </div>
              <div class="message-content">{{ msg.content }}</div>
            </div>
          </el-timeline-item>
        </el-timeline>
        <el-empty v-else description="暂无消息记录" :image-size="60" />
      </template>
      <!-- 新增表单 -->
      <template v-else>
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
          inline
        >
          <el-form-item label="标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入标题" :maxlength="100" />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "ChatSession",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, nextTick } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import AiChatAPI, { ChatSession } from "@/api/module_ai/chat";
import DatePicker from "@/components/DatePicker/index.vue";
import { QuestionFilled, ArrowUp, ArrowDown, Edit } from "@element-plus/icons-vue";
import { formatToDateTime } from "@/utils/dateUtil";

const visible = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const titleInputRef = ref();
const total = ref(0);
const selectIds = ref<string[]>([]);
const selectionRows = ref<ChatSession[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 编辑标题相关
const editingRowId = ref<string | null>(null);
const editingTitle = ref("");

// 分页表单
const pageTableData = ref<ChatSession[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "session_id", label: "会话ID", show: true },
  { prop: "title", label: "标题", show: true },
  { prop: "user_id", label: "用户ID", show: false },
  { prop: "team_id", label: "团队ID", show: false },
  { prop: "team_name", label: "部门名称", show: true },
  { prop: "agent_id", label: "Agent ID", show: false },
  { prop: "summary", label: "会话摘要", show: false },
  { prop: "message_count", label: "消息数量", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 详情表单
const detailFormData = ref<ChatSession>({
  session_id: "",
  agent_id: null,
  team_id: null,
  team_name: null,
  workflow_id: null,
  user_id: null,
  session_data: null,
  agent_data: null,
  team_data: null,
  workflow_data: null,
  metadata: null,
  runs: null,
  summary: null,
  created_at: null,
  updated_at: null,
  id: "",
  title: null,
  created_time: null,
  updated_time: null,
  message_count: 0,
  messages: [],
});
// 日期范围临时变量
const createdDateRange = ref<[Date, Date] | []>([]);
// 更新时间范围临时变量
const updatedDateRange = ref<[Date, Date] | []>([]);

// 处理创建时间范围变化
function handleCreatedDateRangeChange(range: [Date, Date]) {
  createdDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_at = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_at = undefined;
  }
}

// 处理更新时间范围变化
function handleUpdatedDateRangeChange(range: [Date, Date]) {
  updatedDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.updated_at = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.updated_at = undefined;
  }
}

// 分页查询参数
const queryFormData = reactive({
  page_no: 1,
  page_size: 10,
  title: undefined,
  created_at: undefined as string[] | undefined,
  updated_at: undefined as string[] | undefined,
});

// 编辑表单
const formData = reactive({
  id: undefined as string | undefined,
  title: "",
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "detail",
});

// 表单验证规则
const rules = reactive({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
});

// 格式化时间
function formatTime(timestamp: number | null): string {
  if (!timestamp) return "";
  return formatToDateTime(new Date(timestamp * 1000));
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await AiChatAPI.getSessionList(queryFormData);
    const items = response.data.data?.items;
    const validItems = Array.isArray(items) ? items : [];
    pageTableData.value = validItems;
    total.value = response.data.data?.total || 0;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 重置日期范围选择器
  createdDateRange.value = [];
  updatedDateRange.value = [];
  queryFormData.created_at = undefined;
  queryFormData.updated_at = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData = {
  id: undefined as string | undefined,
  title: "",
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: "create" | "detail", id?: string) {
  resetForm();
  dialogVisible.type = type;
  if (id) {
    const response = await AiChatAPI.getSessionDetail(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      const sessionData = response.data.data || {};
      Object.assign(detailFormData.value, sessionData);
    }
  } else {
    dialogVisible.title = "新增会话";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 处理编辑标题
function handleEditTitle(row: ChatSession) {
  editingRowId.value = row.id;
  editingTitle.value = row.title || "";
  nextTick(() => {
    titleInputRef.value?.focus();
  });
}

// 处理保存标题
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
    loading.value = true;
    await AiChatAPI.updateSession(row.id, { title: newTitle });
    ElMessage.success("更新成功");
    row.title = newTitle;
    editingRowId.value = null;
  } catch (error: any) {
    console.error(error);
    ElMessage.error("更新失败");
  } finally {
    loading.value = false;
  }
}

// 提交表单（防抖）
async function handleSubmit() {
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      const submitData = { ...formData };
      try {
        await AiChatAPI.createSession({ title: submitData.title });
        dialogVisible.visible = false;
        resetForm();
        handleCloseDialog();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: string[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await AiChatAPI.deleteSession(ids);
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

onMounted(() => {
  loadingData();
});
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

// 弹窗样式 - 滚动条在弹窗内
:deep(.session-detail-dialog .el-dialog__body) {
  max-height: 60vh;
  padding: 20px;
  overflow-y: auto;
}
</style>
