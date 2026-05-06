<!-- 定时任务节点：Art + useTable -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="nodeSearchItems"
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
            :perm-create="['module_task:cronjob:node:create']"
            :perm-delete="['module_task:cronjob:node:delete']"
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
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="1000px"
      @close="handleCloseDialog"
      @opened="handleDialogOpened"
    >
      <ElSplitter direction="horizontal" style="height: 500px">
        <ElSplitterPanel size="300px" :min="200" :max="400">
          <ElScrollbar style="height: 100%">
            <ArtForm
              :key="nodeFormRenderKey"
              ref="dataFormRef"
              v-model="formData"
              :items="nodeDialogFormItems"
              :rules="rules"
              label-suffix=":"
              label-width="auto"
              :span="24"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
              class="crud-dialog-art-form node-splitter-art-form"
            >
              <template #jobstore>
                <ElSelect v-model="formData.jobstore" placeholder="请选择存储器">
                  <ElOption
                    v-for="item in dictStore.getDictArray('sys_job_store')"
                    :key="item.dict_value"
                    :label="item.dict_label"
                    :value="item.dict_value"
                  />
                </ElSelect>
              </template>
              <template #executor>
                <ElSelect v-model="formData.executor" placeholder="请选择执行器">
                  <ElOption
                    v-for="item in dictStore.getDictArray('sys_job_executor')"
                    :key="item.dict_value"
                    :label="item.dict_label"
                    :value="item.dict_value"
                  />
                </ElSelect>
              </template>
              <template #args>
                <div class="dynamic-params">
                  <div v-for="(_item, index) in argsList" :key="index" class="param-item">
                    <ElInput v-model="argsList[index]" placeholder="参数值" />
                    <ElButton
                      type="danger"
                      icon="Delete"
                      circle
                      @click="argsList.splice(index, 1)"
                    />
                  </div>
                  <ElButton type="primary" icon="Plus" @click="argsList.push('')">
                    添加位置参数
                  </ElButton>
                </div>
              </template>
              <template #kwargs>
                <div class="dynamic-params">
                  <div v-for="(item, index) in kwargsList" :key="index" class="param-item">
                    <ElInput v-model="item.key" placeholder="键" />
                    <ElInput v-model="item.value" placeholder="值" />
                    <ElButton
                      type="danger"
                      icon="Delete"
                      circle
                      @click="kwargsList.splice(index, 1)"
                    />
                  </div>
                  <ElButton
                    type="primary"
                    icon="Plus"
                    @click="kwargsList.push({ key: '', value: '' })"
                  >
                    添加关键词参数
                  </ElButton>
                </div>
              </template>
              <template #coalesce>
                <ElRadioGroup v-model="formData.coalesce">
                  <ElRadio :value="true">是</ElRadio>
                  <ElRadio :value="false">否</ElRadio>
                </ElRadioGroup>
              </template>
              <template #max_instances>
                <ElInputNumber
                  v-model="formData.max_instances"
                  controls-position="right"
                  :min="1"
                  :max="10"
                />
              </template>
            </ArtForm>
          </ElScrollbar>
        </ElSplitterPanel>

        <ElSplitterPanel>
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
        </ElSplitterPanel>
      </ElSplitter>

      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton type="primary" :loading="submitLoading" @click="handleSubmit">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <ArtDialog
      v-model="executeDialogVisible"
      title="调试节点"
      width="700px"
      @close="handleCloseExecuteDialog"
    >
      <ArtForm
        :key="executeFormRenderKey"
        ref="executeFormRef"
        v-model="executeFormData"
        :items="executeDialogFormItems"
        :rules="executeRules"
        label-suffix=":"
        label-width="auto"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form execute-debug-art-form"
      >
        <template #trigger>
          <ElRadioGroup v-model="executeFormData.trigger">
            <ElRadio value="now">立即执行</ElRadio>
            <ElRadio value="cron">Cron表达式</ElRadio>
            <ElRadio value="interval">时间间隔</ElRadio>
            <ElRadio value="date">固定日期</ElRadio>
          </ElRadioGroup>
        </template>
        <template #trigger_args>
          <template v-if="executeFormData.trigger === 'cron'">
            <ElPopover
              :visible="openCron"
              width="700px"
              trigger="click"
              :persistent="false"
              placement="auto-end"
              popper-class="node-cron-popover-fix"
            >
              <template #reference>
                <ElInput
                  v-model="executeFormData.trigger_args"
                  placeholder="请输入 * * * * * ? *"
                  @click="openCron = true"
                />
              </template>
              <vue3CronPlus i18n="cn" @change="handlechangeCron" @close="openCron = false" />
            </ElPopover>
          </template>
          <template v-else-if="executeFormData.trigger === 'interval'">
            <ElPopover
              :visible="openInterval"
              width="600px"
              trigger="click"
              :persistent="false"
              placement="auto-end"
            >
              <template #reference>
                <ElInput
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
            </ElPopover>
          </template>
          <template v-else-if="executeFormData.trigger === 'date'">
            <ElDatePicker
              v-model="executeFormData.trigger_args"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择执行时间"
              style="width: 100%"
            />
          </template>
        </template>
      </ArtForm>

      <template #footer>
        <ElButton @click="handleCloseExecuteDialog">取消</ElButton>
        <ElButton type="primary" :loading="submitLoading" @click="handleExecuteNode">确认</ElButton>
      </template>
    </ArtDialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Node",
  inheritAttrs: false,
});

import NodeAPI, { NodeTable, NodeForm, TriggerType } from "@/api/module_task/cronjob/node";
import { useDictStore } from "@/store/index";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import type { ColumnOption } from "@/types/component";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@/utils/table";
import { useTable } from "@/hooks/core/useTable";
import { computed, nextTick, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { vue3CronPlus } from "vue3-cron-plus";
import "vue3-cron-plus/dist/index.css";
import IntervalTab from "@/components/IntervalTab/index.vue";
import Codemirror, { CmComponentRef } from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import "codemirror/mode/python/python.js";
import "codemirror/theme/dracula.css";

const dictStore = useDictStore();
const { hasAuth } = useAuth();

const BATCH_DELETE_NODE_MSG =
  "确认删除选中的节点吗？\n" +
  "此操作将同时删除节点定义并移除调度器中的相关任务。\n" +
  "正在运行的任务会被立即移除，待执行任务的日志将被标记为已取消。";

type NodeSearchForm = {
  name?: string;
  code?: string;
};

function buildNodeReplaceParams(u: NodeSearchForm): Record<string, unknown> {
  return {
    name: u.name,
    code: u.code,
  };
}

const searchForm = ref<NodeSearchForm>({
  name: undefined,
  code: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const nodeSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "节点名称",
    key: "name",
    type: "input",
    placeholder: "请输入节点名称",
    clearable: true,
    span: 6,
  },
  {
    label: "节点编码",
    key: "code",
    type: "input",
    placeholder: "请输入节点编码",
    clearable: true,
    span: 6,
  },
]);

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<NodeTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => typeof id === "number")
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: NodeTable[]) {
  selectedRows.value = rows;
}

function deleteNodeRow(id: number | undefined) {
  if (id == null) return;
  ElMessageBox.confirm("确认删除该节点吗？将从调度器移除相关任务。", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await NodeAPI.deleteNode([id]);
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
}

function buildNodeRowActions(row: NodeTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "execute",
      label: "调试",
      artType: "more",
      icon: "ri:play-circle-line",
      iconColor: "var(--el-color-primary)",
      perm: "module_task:cronjob:node:execute",
      run: () => handleOpenExecuteDialog(row),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_task:cronjob:node:update",
      run: () => {
        if (row.id != null) void handleOpenDialog("update", row.id);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_task:cronjob:node:delete",
      run: () => {
        void deleteNodeRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatNodeOperationCell(row: NodeTable) {
  return renderTableOperationCell(buildNodeRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 cronjob-node-table-actions",
  });
}

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(BATCH_DELETE_NODE_MSG, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await NodeAPI.deleteNode(ids);
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
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: NodeAPI.listNode,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<NodeTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "name",
        label: "节点名称",
        minWidth: 140,
        showOverflowTooltip: true,
      },
      {
        prop: "code",
        label: "节点编码",
        minWidth: 120,
        showOverflowTooltip: true,
      },
      {
        prop: "jobstore",
        label: "存储器",
        minWidth: 80,
      },
      {
        prop: "executor",
        label: "执行器",
        minWidth: 80,
      },
      {
        prop: "created_time",
        label: "创建时间",
        minWidth: 180,
        sortable: true,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: NodeTable) => formatNodeOperationCell(row),
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
    size: p.size ?? p.page_size ?? 10,
    total: p.total ?? 0,
  };
});

async function handleSearchBarSearch(params: NodeSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildNodeReplaceParams(params));
  getData();
}

async function onResetSearch() {
  searchForm.value = {
    name: undefined,
    code: undefined,
  };
  await resetSearchParams();
}

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

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const executeFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const nodeFormRenderKey = ref(0);
const executeFormRenderKey = ref(0);
const submitLoading = ref(false);
const openCron = ref(false);
const openInterval = ref(false);
const codeEditorRef = ref<CmComponentRef>();

const defaultCodeBlock = `def handler(*args, **kwargs):
    """
    Demo: 调用工程中的方法处理数据
    
    演示如何:
    1. 从工程中导入方法
    2. 调用处理器处理数据
    3. 返回处理结果
    """
    
    # 从工程中导入方法
    from app.plugin.module_task.cronjob.node.handlers.demo_handler import (
        demo_handler,
        process_data
    )
    
    print("=" * 50)
    print("Demo 任务开始执行")
    print("=" * 50)
    
    # 1. 调用 demo_handler
    print("1. 调用 demo_handler:")
    result1 = demo_handler("参数1", "参数2", key="value")
    print(f"   返回: {result1}")
    
    # 2. 调用 process_data 计算平均值
    print("2. 数据处理 - 计算平均值:")
    numbers = [10, 20, 30, 40, 50]
    result2 = process_data(numbers, operation="avg")
    print(f"   输入: {numbers}")
    print(f"   结果: {result2}")
    
    # 3. 调用 process_data 计算总和
    print("3. 数据处理 - 计算总和:")
    result3 = process_data(numbers, operation="sum")
    print(f"   输入: {numbers}")
    print(f"   结果: {result3}")
    
    print("=" * 50)
    print("Demo 任务执行完成")
    print("=" * 50)
    
    return {
        "status": "success",
        "demo_result": result1,
        "avg_result": result2,
        "sum_result": result3
    }
`;

const formData = reactive<NodeForm>({
  id: undefined,
  name: "",
  code: undefined,
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
  node_display_name: string;
  trigger: TriggerType;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
}>({
  node_display_name: "",
  trigger: "now",
  trigger_args: undefined,
  start_date: undefined,
  end_date: undefined,
});

const executeDialogFormItems = computed<FormItem[]>(() => {
  const trig = executeFormData.trigger;
  const showRange = !!trig && trig !== "now" && trig !== "date";
  let triggerArgsLabel = "执行参数";
  if (trig === "cron") triggerArgsLabel = "Cron表达式";
  else if (trig === "interval") triggerArgsLabel = "间隔时间";
  else if (trig === "date") triggerArgsLabel = "执行时间";

  return [
    {
      label: "节点名称",
      key: "node_display_name",
      type: "input",
      span: 24,
      props: { disabled: true },
    },
    {
      label: "执行方式",
      key: "trigger",
      type: "input",
      span: 24,
      placeholder: "",
    },
    {
      label: triggerArgsLabel,
      key: "trigger_args",
      type: "input",
      span: 24,
      placeholder: "",
      hidden: trig === "now" || !trig,
    },
    {
      label: "开始时间",
      key: "start_date",
      type: "datetime",
      span: 24,
      hidden: !showRange,
      props: {
        type: "datetime",
        format: "YYYY-MM-DD HH:mm:ss",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        placeholder: "请选择开始时间（可选）",
        style: { width: "100%" },
      },
    },
    {
      label: "结束时间",
      key: "end_date",
      type: "datetime",
      span: 24,
      hidden: !showRange,
      props: {
        type: "datetime",
        format: "YYYY-MM-DD HH:mm:ss",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        placeholder: "请选择结束时间（可选）",
        style: { width: "100%" },
      },
    },
  ];
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

const nodeDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "节点名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入节点名称", maxlength: 50 },
  },
  {
    label: "节点编码",
    key: "code",
    type: "input",
    span: 24,
    props: { placeholder: "请输入节点编码", maxlength: 32 },
  },
  {
    label: "存储器",
    key: "jobstore",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "执行器",
    key: "executor",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "位置参数",
    key: "args",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "关键字参数",
    key: "kwargs",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "合并运行",
    key: "coalesce",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "最大实例数",
    key: "max_instances",
    type: "number",
    span: 24,
    props: {
      controlsPosition: "right",
      min: 1,
      max: 10,
    },
  },
]);

const executeRules = reactive({
  trigger: [{ required: true, message: "请选择执行方式", trigger: "change" }],
  trigger_args: [{ required: true, message: "请设置执行参数", trigger: "blur" }],
});

const initialFormData: Partial<NodeForm> = {
  id: undefined,
  name: "",
  code: undefined,
  jobstore: "sqlalchemy",
  executor: "default",
  func: defaultCodeBlock,
  args: undefined,
  kwargs: undefined,
  coalesce: false,
  max_instances: 5,
  start_date: undefined,
  end_date: undefined,
};

async function resetForm() {
  dataFormRef.value?.ref?.resetFields();
  dataFormRef.value?.ref?.clearValidate();
  Object.assign(formData, initialFormData);
  argsList.value = [];
  kwargsList.value = [];
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
  nodeFormRenderKey.value += 1;
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
  dataFormRef.value?.validate(async (valid: any) => {
    if (valid) {
      submitLoading.value = true;
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
        if (id) {
          await refreshUpdate();
        } else {
          await refreshCreate();
        }
      } catch (error: any) {
        console.log(error);
      } finally {
        submitLoading.value = false;
      }
    }
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
  executeFormData.node_display_name = row.name ?? "";
  executeFormData.trigger = "now";
  executeFormData.trigger_args = undefined;
  executeFormData.start_date = undefined;
  executeFormData.end_date = undefined;
  executeFormRenderKey.value += 1;
  executeDialogVisible.value = true;
}

function handleCloseExecuteDialog() {
  executeDialogVisible.value = false;
  currentExecuteNode.value = null;
  executeFormRef.value?.ref?.resetFields();
}

async function handleExecuteNode() {
  if (executeFormData.trigger !== "now") {
    const execForm = executeFormRef.value;
    const elForm = execForm?.ref;
    if (!elForm) return;
    const valid = await elForm.validate().catch(() => false);
    if (!valid) return;
  }

  try {
    submitLoading.value = true;
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

    await refreshUpdate();
  } catch (error: any) {
    ElMessage.error({
      message: error.response?.data?.msg || "调试失败",
      type: "error",
      duration: 3000,
    });
    console.error(error);
  } finally {
    submitLoading.value = false;
  }
}

onMounted(async () => {
  await dictStore.getDict(["sys_job_store", "sys_job_executor"]);
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

.execution-log-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.node-splitter-art-form :deep(.el-row > .el-col:last-child),
.execute-debug-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.node-splitter-art-form :deep(.el-form-item__content),
.execute-debug-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

.node-splitter-art-form :deep(section) {
  padding-right: 10px;
  padding-left: 10px;
}
</style>

<!-- popover 挂载到 body，需单独写；修复 vue3-cron-plus 全局 .el-tag--info { margin-left: -60px } 误伤多选下拉里 tag -->
<style lang="scss">
.node-cron-popover-fix {
  .vue3-cron-plus-container .el-select .el-tag {
    margin-left: 0 !important;
  }

  /* 具体秒数等多选行：避免文案与选择器挤在同一行错位 */
  .vue3-cron-plus-container .tabBody .el-radio.long {
    align-items: flex-start;
    height: auto;
    white-space: normal;

    .el-radio__label {
      display: flex;
      flex-wrap: wrap;
      gap: 6px 8px;
      align-items: center;
      line-height: 1.5;
    }

    .el-select {
      flex: 1 1 200px;
      min-width: 180px;
      max-width: 100%;
    }
  }
}
</style>
