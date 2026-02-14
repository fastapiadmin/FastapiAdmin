<!-- AI智能助手消息列表 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div v-show="visible" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="session_id" label="会话ID">
          <el-input v-model="queryFormData.session_id" placeholder="请输入会话ID" clearable />
        </el-form-item>
        <el-form-item prop="type" label="类型">
          <el-select
            v-model="queryFormData.type"
            placeholder="请选择类型"
            style="width: 170px"
            clearable
          >
            <el-option value="user" label="用户" />
            <el-option value="assistant" label="助手" />
          </el-select>
        </el-form-item>
        <el-form-item prop="content" label="内容">
          <el-input v-model="queryFormData.content" placeholder="请输入内容" clearable />
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
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
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

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            对话消息列表
            <el-tooltip content="对话消息列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_ai:chat_message:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_ai:chat_message:delete']"
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
                  v-hasPerm="['module_ai:chat_message:query']"
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
      <el-table
        ref="tableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        height="450"
        max-height="450"
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
          min-width="120"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'type')?.show"
          label="类型"
          prop="type"
          min-width="100"
        >
          <template #default="scope">
            <el-tag :type="scope.row.type === 'user' ? 'primary' : 'success'">
              {{ scope.row.type === "user" ? "用户" : "助手" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'content')?.show"
          label="内容"
          prop="content"
          min-width="300"
          show-overflow-tooltip
        >
          <template #default="scope">
            <MarkdownRenderer :content="scope.row.content" :max-length="100" />
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'timestamp')?.show"
          label="时间戳"
          prop="timestamp"
          min-width="180"
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
          min-width="180"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_example:demo:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_example:demo:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_example:demo:delete']"
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
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="会话ID" :span="2">
            {{ detailFormData.session_id }}
          </el-descriptions-item>
          <el-descriptions-item label="类型" :span="2">
            <el-tag :type="detailFormData.type === 'user' ? 'primary' : 'success'">
              {{ detailFormData.type === "user" ? "用户" : "助手" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="内容" :span="4">
            <div v-if="detailFormData.content">
              <MarkdownRenderer :content="detailFormData.content" />
            </div>
            <div v-else class="empty-content">暂无内容</div>
          </el-descriptions-item>
          <el-descriptions-item label="时间戳" :span="2">
            {{ detailFormData.timestamp }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
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
          <el-form-item label="会话ID" prop="session_id">
            <el-input-number v-model="formData.session_id" placeholder="请输入会话ID" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-radio-group v-model="formData.type">
              <el-radio value="user">用户</el-radio>
              <el-radio value="assistant">助手</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <WangEditor v-model="formData.content" height="200px" />
          </el-form-item>
          <el-form-item label="时间戳" prop="timestamp">
            <el-input-number v-model="formData.timestamp" placeholder="请输入时间戳" />
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
  name: "ChatMessage",
  inheritAttrs: false,
});

import { ref, reactive, onMounted } from "vue";
import { ElMessageBox } from "element-plus";
import AiChatMessageAPI, {
  MessageTable,
  MessageForm,
  MessagePageQuery,
} from "@/api/module_ai/chat_message";
import { QuestionFilled, ArrowUp, ArrowDown } from "@element-plus/icons-vue";
import { formatToDateTime } from "@/utils/dateUtil";
import MarkdownRenderer from "@/components/MarkdownRenderer/index.vue";
import WangEditor from "@/components/WangEditor/index.vue";

const visible = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const selectionRows = ref<MessageTable[]>([]);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);

// 日期范围临时变量
const createdDateRange = ref<[Date, Date] | []>([]);
// 更新时间范围临时变量
const updatedDateRange = ref<[Date, Date] | []>([]);

// 处理创建时间范围变化
function handleCreatedDateRangeChange(range: [Date, Date]) {
  createdDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 处理更新时间范围变化
function handleUpdatedDateRangeChange(range: [Date, Date]) {
  updatedDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.updated_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.updated_time = undefined;
  }
}

// 分页表单
const pageTableData = ref<MessageTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "session_id", label: "会话ID", show: true },
  { prop: "type", label: "类型", show: true },
  { prop: "content", label: "内容", show: true },
  { prop: "timestamp", label: "时间戳", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 详情表单
const detailFormData = ref<MessageTable>({
  session_id: 0,
  type: "user",
  content: "",
  timestamp: 0,
});

// 分页查询参数
const queryFormData = reactive<MessagePageQuery>({
  page_no: 1,
  page_size: 10,
  session_id: undefined,
  type: undefined,
  content: undefined,
  created_time: undefined,
});

// 编辑表单
const formData = reactive<MessageForm>({
  id: undefined,
  session_id: undefined,
  type: "user",
  content: "",
  timestamp: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  session_id: [{ required: true, message: "请输入会话ID", trigger: "blur" }],
  type: [{ required: true, message: "请选择类型", trigger: "change" }],
  content: [{ required: true, message: "请输入内容", trigger: "blur" }],
});

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await AiChatMessageAPI.listMessage(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
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
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: MessageForm = {
  id: undefined,
  session_id: undefined,
  type: "user",
  content: "",
  timestamp: undefined,
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
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  resetForm();
  dialogVisible.type = type;
  if (id) {
    const response = await AiChatMessageAPI.detailMessage(id);
    console.log("详情数据:", response.data.data);
    if (type === "detail") {
      dialogVisible.title = "详情";
      detailFormData.value = { ...response.data.data };
      console.log("detailFormData.value:", detailFormData.value);
    } else if (type === "update") {
      dialogVisible.title = "修改";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增消息";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 提交表单（防抖）
async function handleSubmit() {
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      const submitData = { ...formData };
      const id = formData.id;
      if (id) {
        try {
          await AiChatMessageAPI.updateMessage(id, { id, ...submitData });
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await AiChatMessageAPI.createMessage(submitData);
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
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await AiChatMessageAPI.deleteMessage(ids);
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
.empty-content {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}
</style>
