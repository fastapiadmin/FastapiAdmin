<!-- AI智能助手会话列表 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent
      ref="contentRef"
      :content-config="contentConfig"
      @add-click="handleOpenDialog('create')"
    >
      <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="loading"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="onSelectionChange"
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
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
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
                  {{ scope.row.title || '未命名会话' }}
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
                  icon="View"
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
                  @click="handleRowDelete(scope.row.id)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </PageContent>

    <!-- 弹窗区域 -->
    <EnhancedDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      dialog-class="session-detail-dialog"
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
            {{ detailFormData.team_name || '未知部门' }}
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
            {{ detailFormData.summary || '无' }}
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
                  {{ msg.role === 'user' ? '用户' : '助手' }}
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
    </EnhancedDialog>
  </div>
</template>

<script setup lang="ts">
  defineOptions({
    name: 'ChatSession',
    inheritAttrs: false,
  });

  import { ref, reactive, nextTick } from 'vue';
  import { ElMessage } from 'element-plus';
  import AiChatAPI, { ChatSession } from '@/api/module_ai/chat';
  import EnhancedDialog from '@/components/CURD/EnhancedDialog.vue';
  import PageSearch from '@/components/CURD/PageSearch.vue';
  import PageContent from '@/components/CURD/PageContent.vue';
  import { useCrudList } from '@/components/CURD/useCrudList';
  import type { ISearchConfig, IContentConfig } from '@/components/CURD/types';
  import { Edit } from '@element-plus/icons-vue';
  import { formatToDateTime } from '@/utils/dateUtil';

  const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
  const dataFormRef = ref();
  const titleInputRef = ref();

  // 编辑标题相关
  const editingRowId = ref<string | null>(null);
  const editingTitle = ref('');

  // 表格列配置
  const tableColumns = ref([
    { prop: 'selection', label: '选择框', show: true },
    { prop: 'index', label: '序号', show: true },
    { prop: 'session_id', label: '会话ID', show: true },
    { prop: 'title', label: '标题', show: true },
    { prop: 'user_id', label: '用户ID', show: false },
    { prop: 'team_id', label: '团队ID', show: false },
    { prop: 'team_name', label: '部门名称', show: true },
    { prop: 'agent_id', label: 'Agent ID', show: false },
    { prop: 'summary', label: '会话摘要', show: false },
    { prop: 'message_count', label: '消息数量', show: true },
    { prop: 'created_time', label: '创建时间', show: true },
    { prop: 'updated_time', label: '更新时间', show: true },
    { prop: 'operation', label: '操作', show: true },
  ]);

  // 详情表单
  const detailFormData = ref<ChatSession>({
    session_id: '',
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
    id: '',
    title: null,
    created_time: null,
    updated_time: null,
    message_count: 0,
    messages: [],
  });
  const searchConfig = reactive<ISearchConfig>({
    permPrefix: 'module_ai:chat',
    colon: true,
    isExpandable: true,
    showNumber: 1,
    form: { labelWidth: 'auto' },
    formItems: [
      {
        prop: 'title',
        label: '标题',
        type: 'input',
        attrs: { placeholder: '请输入标题', clearable: true },
      },
      {
        prop: 'created_at',
        label: '创建时间',
        type: 'date-picker',
        attrs: {
          type: 'datetimerange',
          rangeSeparator: '至',
          startPlaceholder: '开始日期',
          endPlaceholder: '结束日期',
          format: 'YYYY-MM-DD HH:mm:ss',
          valueFormat: 'YYYY-MM-DD HH:mm:ss',
          style: { width: '340px' },
        },
      },
      {
        prop: 'updated_at',
        label: '更新时间',
        type: 'date-picker',
        attrs: {
          type: 'datetimerange',
          rangeSeparator: '至',
          startPlaceholder: '开始日期',
          endPlaceholder: '结束日期',
          format: 'YYYY-MM-DD HH:mm:ss',
          valueFormat: 'YYYY-MM-DD HH:mm:ss',
          style: { width: '340px' },
        },
      },
    ],
  });

  const contentConfig = reactive<IContentConfig>({
    permPrefix: 'module_ai:chat',
    cols: [],
    hideColumnFilter: true,
    toolbar: ['add', 'delete', 'patch'],
    defaultToolbar: ['import', 'export', 'refresh', 'filter'],
    pagination: {
      pageSize: 10,
      pageSizes: [10, 20, 30, 50],
    },
    request: { page_no: 'page_no', page_size: 'page_size' },
    indexAction: async (params) => {
      const res = await AiChatAPI.getSessionList(
        params as {
          page_no: number;
          page_size: number;
          title?: string;
          created_at?: string[];
          updated_at?: string[];
        }
      );
      return {
        total: res.data.data?.total ?? 0,
        list: res.data.data?.items ?? [],
      };
    },
    deleteAction: (ids) =>
      AiChatAPI.deleteSession(
        ids
          .split(',')
          .map((s) => s.trim())
          .filter(Boolean)
      ),
    deleteConfirm: {
      title: '警告',
      message: '确认删除该项数据?',
      type: 'warning',
    },
  });

  // 编辑表单
  const formData = reactive({
    id: undefined as string | undefined,
    title: '',
  });

  // 弹窗状态
  const dialogVisible = reactive({
    title: '',
    visible: false,
    type: 'create' as 'create' | 'detail',
  });

  // 表单验证规则
  const rules = reactive({
    title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  });

  // 格式化时间
  function formatTime(timestamp: number | null): string {
    if (!timestamp) return '';
    return formatToDateTime(new Date(timestamp * 1000));
  }

  function handleRowDelete(id: string) {
    contentRef.value?.handleDelete(id);
  }

  // 定义初始表单数据常量
  const initialFormData = {
    id: undefined as string | undefined,
    title: '',
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

  // 关闭弹窗
  async function handleCloseDialog() {
    dialogVisible.visible = false;
    resetForm();
  }

  // 打开弹窗
  async function handleOpenDialog(type: 'create' | 'detail', id?: string) {
    resetForm();
    dialogVisible.type = type;
    if (id) {
      const response = await AiChatAPI.getSessionDetail(id);
      if (type === 'detail') {
        dialogVisible.title = '详情';
        const sessionData = response.data.data || {};
        Object.assign(detailFormData.value, sessionData);
      }
    } else {
      dialogVisible.title = '新增会话';
      formData.id = undefined;
    }
    dialogVisible.visible = true;
  }

  // 处理编辑标题
  function handleEditTitle(row: ChatSession) {
    editingRowId.value = row.id;
    editingTitle.value = row.title || '';
    nextTick(() => {
      titleInputRef.value?.focus();
    });
  }

  // 处理保存标题
  async function handleSaveTitle(row: ChatSession) {
    if (editingRowId.value !== row.id) return;

    const newTitle = editingTitle.value.trim();
    if (!newTitle) {
      ElMessage.warning('标题不能为空');
      return;
    }

    if (newTitle === row.title) {
      editingRowId.value = null;
      return;
    }

    try {
      await AiChatAPI.updateSession(row.id, { title: newTitle });
      ElMessage.success('更新成功');
      row.title = newTitle;
      editingRowId.value = null;
    } catch (error: any) {
      console.error(error);
      ElMessage.error('更新失败');
    }
  }

  // 提交表单（防抖）
  async function handleSubmit() {
    dataFormRef.value.validate(async (valid: any) => {
      if (valid) {
        const submitData = { ...formData };
        try {
          await AiChatAPI.createSession({ title: submitData.title });
          dialogVisible.visible = false;
          resetForm();
          refreshList();
        } catch (error: any) {
          console.error(error);
        }
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

  // 弹窗样式 - 滚动条在弹窗内
  :deep(.session-detail-dialog .el-dialog__body) {
    max-height: 60vh;
    padding: 20px;
    overflow-y: auto;
  }
</style>
