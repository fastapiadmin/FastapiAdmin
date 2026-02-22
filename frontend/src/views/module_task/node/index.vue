<template>
  <div class="app-container">
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="节点名称">
          <el-input v-model="queryFormData.name" placeholder="请输入节点名称" clearable />
        </el-form-item>
        <el-form-item prop="code" label="节点编码">
          <el-input v-model="queryFormData.code" placeholder="请输入节点编码" clearable />
        </el-form-item>
        <el-form-item prop="category" label="节点分类">
          <el-select
            v-model="queryFormData.category"
            placeholder="请选择节点分类"
            clearable
            style="width: 167.5px"
          >
            <el-option value="trigger" label="触发器节点" />
            <el-option value="action" label="动作节点" />
            <el-option value="condition" label="条件节点" />
            <el-option value="control" label="控制节点" />
          </el-select>
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_task:node:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_task:node:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="节点类型列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            节点类型列表
          </span>
        </div>
      </template>

      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_task:node:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_task:node:delete']"
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
              <el-tooltip content="刷新">
                <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        class="data-table__content"
        highlight-current-row
        height="450"
        max-height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" align="center" min-width="55" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="节点名称" prop="name" min-width="140" />
        <el-table-column label="节点编码" prop="code" min-width="120" />
        <el-table-column label="节点分类" prop="category" min-width="100">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">
              {{ getCategoryLabel(scope.row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="存储器" prop="jobstore" min-width="80" />
        <el-table-column label="执行器" prop="executor" min-width="80" />
        <el-table-column label="创建时间" prop="created_time" min-width="180" sortable />

        <OperationColumn :list-data-length="pageTableData.length">
          <template #default="scope">
            <el-space class="flex">
              <el-button
                type="warning"
                size="small"
                link
                icon="VideoPlay"
                @click="handleOpenExecuteDialog(scope.row)"
              >
                调试
              </el-button>
              <el-button
                v-hasPerm="['module_task:node:update']"
                type="primary"
                size="small"
                link
                icon="edit"
                @click="handleOpenDialog('update', scope.row.id)"
              >
                编辑
              </el-button>
              <el-button
                v-hasPerm="['module_task:node:delete']"
                type="danger"
                size="small"
                link
                icon="delete"
                @click="handleDelete([scope.row.id])"
              >
                删除
              </el-button>
            </el-space>
          </template>
        </OperationColumn>
      </el-table>

      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="1000px"
      @close="handleCloseDialog"
      @opened="handleDialogOpened"
    >
      <el-splitter direction="horizontal" style="height: 500px">
        <el-splitter-panel size="300px" :min="200" :max="400">
          <el-scrollbar style="height: 100%">
            <el-form
              ref="dataFormRef"
              :model="formData"
              :rules="rules"
              label-suffix=":"
              label-width="auto"
              style="padding: 0 10px"
            >
              <el-form-item label="节点名称" prop="name">
                <el-input v-model="formData.name" placeholder="请输入节点名称" :maxlength="50" />
              </el-form-item>
              <el-form-item label="节点编码" prop="code">
                <el-input v-model="formData.code" placeholder="请输入节点编码" :maxlength="32" />
              </el-form-item>
              <el-form-item label="节点分类" prop="category">
                <el-select v-model="formData.category" placeholder="请选择节点分类">
                  <el-option value="trigger" label="触发器节点" />
                  <el-option value="action" label="动作节点" />
                  <el-option value="condition" label="条件节点" />
                  <el-option value="control" label="控制节点" />
                </el-select>
              </el-form-item>
              <el-form-item label="存储器" prop="jobstore">
                <el-select v-model="formData.jobstore" placeholder="请选择存储器">
                  <el-option
                    v-for="item in dictStore.getDictArray('sys_job_store')"
                    :key="item.dict_value"
                    :label="item.dict_label"
                    :value="item.dict_value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="执行器" prop="executor">
                <el-select v-model="formData.executor" placeholder="请选择执行器">
                  <el-option
                    v-for="item in dictStore.getDictArray('sys_job_executor')"
                    :key="item.dict_value"
                    :label="item.dict_label"
                    :value="item.dict_value"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="位置参数" prop="args">
                <div class="dynamic-params">
                  <div v-for="(item, index) in argsList" :key="index" class="param-item">
                    <el-input v-model="argsList[index]" placeholder="参数值" />
                    <el-button
                      type="danger"
                      icon="Delete"
                      circle
                      @click="argsList.splice(index, 1)"
                    />
                  </div>
                  <el-button type="primary" icon="Plus" @click="argsList.push('')">
                    添加位置参数
                  </el-button>
                </div>
              </el-form-item>
              <el-form-item label="关键字参数" prop="kwargs">
                <div class="dynamic-params">
                  <div v-for="(item, index) in kwargsList" :key="index" class="param-item">
                    <el-input v-model="item.key" placeholder="键" />
                    <el-input v-model="item.value" placeholder="值" />
                    <el-button
                      type="danger"
                      icon="Delete"
                      circle
                      @click="kwargsList.splice(index, 1)"
                    />
                  </div>
                  <el-button
                    type="primary"
                    icon="Plus"
                    @click="kwargsList.push({ key: '', value: '' })"
                  >
                    添加关键词参数
                  </el-button>
                </div>
              </el-form-item>
              <el-form-item label="合并运行" prop="coalesce">
                <el-radio-group v-model="formData.coalesce">
                  <el-radio :value="true">是</el-radio>
                  <el-radio :value="false">否</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="最大实例数" prop="max_instances">
                <el-input-number
                  v-model="formData.max_instances"
                  controls-position="right"
                  :min="1"
                  :max="10"
                />
              </el-form-item>
            </el-form>
          </el-scrollbar>
        </el-splitter-panel>

        <el-splitter-panel>
          <div class="code-editor-container">
            <div class="code-editor-header">
              <span class="code-editor-title">处理器</span>
              <span class="code-editor-tip">定义 handler(*args, **kwargs) 函数</span>
            </div>
            <Codemirror
              ref="codeEditorRef"
              v-model:value="formData.func"
              :options="codeEditorOptions"
              border
              height="calc(100% - 40px)"
              width="100%"
            />
          </div>
        </el-splitter-panel>
      </el-splitter>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog
      v-model="executeDialogVisible"
      title="调试节点"
      width="600px"
      @close="handleCloseExecuteDialog"
    >
      <el-form
        ref="executeFormRef"
        :model="executeFormData"
        :rules="executeRules"
        label-suffix=":"
        label-width="auto"
      >
        <el-form-item label="节点名称">
          <el-input :value="currentExecuteNode?.name" disabled />
        </el-form-item>
        <el-form-item label="执行方式" prop="trigger">
          <el-radio-group v-model="executeFormData.trigger">
            <el-radio value="now">一次性任务</el-radio>
            <el-radio value="cron">Cron表达式</el-radio>
            <el-radio value="interval">时间间隔</el-radio>
            <el-radio value="date">固定日期</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item
          v-if="executeFormData.trigger === 'cron'"
          label="Cron表达式"
          prop="trigger_args"
        >
          <el-popover
            :visible="openCron"
            width="600px"
            trigger="click"
            :persistent="false"
            placement="left"
          >
            <template #reference>
              <el-input
                v-model="executeFormData.trigger_args"
                placeholder="请输入 * * * * * ? *"
                @click="openCron = true"
              />
            </template>
            <vue3CronPlus i18n="cn" @change="handlechangeCron" @close="openCron = false" />
          </el-popover>
        </el-form-item>

        <el-form-item
          v-else-if="executeFormData.trigger === 'interval'"
          label="间隔时间"
          prop="trigger_args"
        >
          <el-popover
            :visible="openInterval"
            width="500px"
            trigger="click"
            :persistent="false"
            placement="left"
          >
            <template #reference>
              <el-input
                v-model="executeFormData.trigger_args"
                placeholder="请点击设置间隔时间"
                @click="openInterval = true"
              />
            </template>
            <IntervalTab
              :cron-value="executeFormData.trigger_args"
              @confirm="handleIntervalConfirm"
              @cancel="openInterval = false"
            />
          </el-popover>
        </el-form-item>

        <el-form-item
          v-else-if="executeFormData.trigger === 'date'"
          label="执行时间"
          prop="trigger_args"
        >
          <el-date-picker
            v-model="executeFormData.trigger_args"
            type="datetime"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="请选择执行时间"
            style="width: 100%"
          />
        </el-form-item>

        <template
          v-if="
            executeFormData.trigger &&
            executeFormData.trigger !== 'now' &&
            executeFormData.trigger !== 'date'
          "
        >
          <el-form-item label="开始时间" prop="start_date">
            <el-date-picker
              v-model="executeFormData.start_date"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择开始时间（可选）"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="结束时间" prop="end_date">
            <el-date-picker
              v-model="executeFormData.end_date"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择结束时间（可选）"
              style="width: 100%"
            />
          </el-form-item>
        </template>
      </el-form>

      <template #footer>
        <el-button @click="handleCloseExecuteDialog">取消</el-button>
        <el-button type="primary" @click="handleExecuteNode">确认调试</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Node",
  inheritAttrs: false,
});

import NodeAPI, { NodeTable, NodeForm, NodePageQuery, TriggerType } from "@/api/module_task/node";
import { useDictStore } from "@/store/index";
import { nextTick, onMounted } from "vue";
import { vue3CronPlus } from "vue3-cron-plus";
import "vue3-cron-plus/dist/index.css";
import OperationColumn from "@/components/OperationColumn/index.vue";
import IntervalTab from "@/components/IntervalTab/index.vue";
import Codemirror, { CmComponentRef } from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import "codemirror/mode/python/python.js";
import "codemirror/theme/dracula.css";

const dictStore = useDictStore();

const codeEditorOptions: EditorConfiguration = {
  mode: "python",
  lineNumbers: true,
  smartIndent: true,
  indentUnit: 4,
  tabSize: 4,
  theme: "dracula",
  lineWrapping: true,
  autofocus: false,
};

const queryFormRef = ref();
const dataFormRef = ref();
const executeFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);
const openCron = ref(false);
const openInterval = ref(false);
const codeEditorRef = ref<CmComponentRef>();

const pageTableData = ref<NodeTable[]>([]);

const queryFormData = reactive<NodePageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  code: undefined,
  category: undefined,
});

const defaultCodeBlock = `def handler(*args, **kwargs) -> None:
    """
    节点执行函数示例
    
    参数:
    - args: 位置参数
    - kwargs: 关键字参数
    """
    from datetime import datetime
    
    print(f"开始执行任务: {args}-{kwargs}")
    print(f"{datetime.now()} 执行完成")
`;

const formData = reactive<NodeForm>({
  id: undefined,
  name: "",
  code: undefined,
  category: undefined,
  jobstore: "default",
  executor: "default",
  func: defaultCodeBlock,
  args: undefined,
  kwargs: undefined,
  coalesce: false,
  max_instances: 1,
  start_date: undefined,
  end_date: undefined,
});

const argsList = ref<string[]>([]);
const kwargsList = ref<{ key: string; value: string }[]>([]);

const executeDialogVisible = ref(false);
const currentExecuteNode = ref<NodeTable | null>(null);
const executeFormData = reactive<{
  trigger: TriggerType;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
}>({
  trigger: "now",
  trigger_args: undefined,
  start_date: undefined,
  end_date: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  name: [{ required: true, message: "请输入节点名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入节点编码", trigger: "blur" }],
});

const executeRules = reactive({
  trigger: [{ required: true, message: "请选择执行方式", trigger: "change" }],
  trigger_args: [{ required: true, message: "请设置执行参数", trigger: "blur" }],
});

function getCategoryType(category: string | undefined) {
  switch (category) {
    case "trigger":
      return "primary";
    case "action":
      return "success";
    case "condition":
      return "warning";
    case "control":
      return "danger";
    default:
      return "info";
  }
}

function getCategoryLabel(category: string | undefined) {
  switch (category) {
    case "trigger":
      return "触发器节点";
    case "action":
      return "动作节点";
    case "condition":
      return "条件节点";
    case "control":
      return "控制节点";
    default:
      return "未分类";
  }
}

async function handleRefresh() {
  await loadingData();
}

async function loadingData() {
  loading.value = true;
  try {
    const response = await NodeAPI.listNode(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadingData();
}

const initialFormData: Partial<NodeForm> = {
  id: undefined,
  name: "",
  code: undefined,
  category: undefined,
  jobstore: "sqlalchemy",
  executor: "default",
  func: defaultCodeBlock,
  args: undefined,
  kwargs: undefined,
  coalesce: false,
  max_instances: 1,
  start_date: undefined,
  end_date: undefined,
};

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
  argsList.value = [];
  kwargsList.value = [];
}

async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

async function handleOpenDialog(type: "create" | "update", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await NodeAPI.detailNode(id);
    dialogVisible.title = "修改节点";
    Object.assign(formData, response.data.data);
    const data = response.data.data;
    argsList.value = data.args ? data.args.split(",").map((v: string) => v.trim()) : [];
    kwargsList.value = data.kwargs
      ? Object.entries(JSON.parse(data.kwargs)).map(([key, value]) => ({
          key,
          value: String(value),
        }))
      : [];
  } else {
    dialogVisible.title = "新增节点";
    formData.id = undefined;
    argsList.value = [];
    kwargsList.value = [];
  }
  dialogVisible.visible = true;
}

function handleDialogOpened() {
  nextTick(() => {
    setTimeout(() => {
      codeEditorRef.value?.refresh?.();
    }, 100);
  });
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      const id = formData.id;
      try {
        const submitData = {
          ...formData,
          args: argsList.value.filter((v) => v.trim()).join(",") || undefined,
          kwargs:
            kwargsList.value.filter((v) => v.key.trim()).length > 0
              ? JSON.stringify(
                  Object.fromEntries(
                    kwargsList.value.filter((v) => v.key.trim()).map((v) => [v.key, v.value])
                  )
                )
              : undefined,
        };
        if (id) {
          await NodeAPI.updateNode(id, submitData);
        } else {
          await NodeAPI.createNode(submitData);
        }
        dialogVisible.visible = false;
        resetForm();
        handleResetQuery();
      } catch (error: any) {
        console.log(error);
      } finally {
        loading.value = false;
      }
    }
  });
}

async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await NodeAPI.deleteNode(ids);
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

const handlechangeCron = (cronStr: string) => {
  if (typeof cronStr == "string") {
    executeFormData.trigger_args = cronStr;
  }
};

const handleIntervalConfirm = (value: string) => {
  executeFormData.trigger_args = value;
  openInterval.value = false;
};

function handleOpenExecuteDialog(row: NodeTable) {
  currentExecuteNode.value = row;
  executeFormData.trigger = "now";
  executeFormData.trigger_args = undefined;
  executeFormData.start_date = undefined;
  executeFormData.end_date = undefined;
  executeDialogVisible.value = true;
}

function handleCloseExecuteDialog() {
  executeDialogVisible.value = false;
  currentExecuteNode.value = null;
  if (executeFormRef.value) {
    executeFormRef.value.resetFields();
  }
}

async function handleExecuteNode() {
  if (executeFormData.trigger !== "now") {
    const valid = await executeFormRef.value?.validate().catch(() => false);
    if (!valid) return;
  }

  try {
    loading.value = true;
    const params: any = {
      trigger: executeFormData.trigger,
    };

    if (executeFormData.trigger !== "now") {
      params.trigger_args = executeFormData.trigger_args;
      params.start_date = executeFormData.start_date;
      params.end_date = executeFormData.end_date;
    }

    await NodeAPI.executeNode(currentExecuteNode.value?.id as number, params);
    handleCloseExecuteDialog();
    loadingData();
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await dictStore.getDict(["sys_job_store", "sys_job_executor"]);
  loadingData();
});
</script>

<style scoped>
.code-editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-left: 16px;
}

.code-editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
}

.code-editor-title {
  font-size: 14px;
  font-weight: 600;
}

.code-editor-tip {
  font-size: 12px;
}

.dynamic-params {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.param-item {
  display: flex;
  gap: 8px;
  align-items: center;
}

.code-preview {
  max-height: 200px;
  padding: 10px;
  overflow-y: auto;
  font-family: monospace;
  word-break: break-all;
  white-space: pre-wrap;
  border-radius: 4px;
}
</style>
