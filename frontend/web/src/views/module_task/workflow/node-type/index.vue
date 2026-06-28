<!-- 工作流节点类型：ElSplitter + Codemirror -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="nodeTypeSearchItems"
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
            :perm-create="['module_task:workflow:node-type:create']"
            :perm-delete="['module_task:workflow:node-type:delete']"
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
      />
    </ElCard>

    <FaDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="1000px"
      destroy-on-close
      @close="handleCloseDialog"
      @opened="handleDialogOpened"
    >
      <ElSplitter direction="horizontal" :style="'height: 500px'">
        <ElSplitterPanel size="320px" :min="240" :max="420">
          <ElScrollbar :style="'height: 100%'">
            <FaForm
              :key="nodeTypeFormRenderKey"
              ref="formRef"
              v-model="formData"
              :items="nodeTypeDialogFormItems"
              :rules="rules"
              label-suffix=":"
              label-width="85px"
              :span="24"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
              class="crud-dialog-art-form node-splitter-art-form"
            >
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
            </FaForm>
          </ElScrollbar>
        </ElSplitterPanel>

        <ElSplitterPanel>
          <div class="code-editor-container">
            <div class="code-editor-header">
              <span class="code-editor-title">handler 代码</span>
              <span class="code-editor-tip">须定义 handler(*args, **kwargs) 函数</span>
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
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" :loading="submitting" @click="submitForm">保存</ElButton>
        </div>
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
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type FaForm from "@/components/forms/fa-form/index.vue";
import { useAuth } from "@/hooks/core/useAuth";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import { useTable } from "@/hooks/core/useTable";
import type { ColumnOption } from "@/types/component";
import { ElMessage } from "element-plus";
import type { FormRules } from "element-plus";
import { computed, nextTick, ref } from "vue";
import Codemirror, { CmComponentRef } from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import "codemirror/mode/python/python.js";
import "codemirror/theme/dracula.css";

const { hasAuth } = useAuth();

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
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      clearable: true,
      options: [
        { label: "启用", value: 0 },
        { label: "停用", value: 1 },
      ],
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

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const { selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<WorkflowNodeTypeTable>();
const createLoading = ref(false);

function categoryLabel(c?: string) {
  const m: Record<string, string> = {
    trigger: "触发器",
    action: "动作",
    condition: "条件",
    control: "控制",
  };
  return c ? m[c] || c : "-";
}

const deleteNodeTypeRow = async (row: WorkflowNodeTypeTable) => {
  if (!row.id) return;
  try {
    await confirmDelete(`确定删除节点类型「${row.name ?? row.id}」吗？`);
    await WorkflowNodeTypeAPI.deleteWorkflowNodeType([row.id]);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
};

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await WorkflowNodeTypeAPI.deleteWorkflowNodeType(ids);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

function buildNodeTypeRowActions(row: WorkflowNodeTypeTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_task:workflow:node-type:update",
      run: () => void openDialog(row.id),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_task:workflow:node-type:delete",
      run: () => void deleteNodeTypeRow(row),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatNodeTypeOperationCell(row: WorkflowNodeTypeTable) {
  return renderTableOperationCell(buildNodeTypeRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1",
  });
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
        status: {
          true: { type: "success", text: "是" },
          false: { type: "info", text: "否" },
        },
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
        width: 160,
        fixed: "right",
        align: "center",
        formatter: (row: WorkflowNodeTypeTable) => formatNodeTypeOperationCell(row),
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

// ─── Codemirror ──────────────────────────────────────────────────

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

const codeEditorRef = ref<CmComponentRef>();

// ─── 表单 ────────────────────────────────────────────────────────

const dialogVisible = ref(false);
const dialogTitle = ref("新增节点类型");
const editingId = ref<number | null>(null);
const submitting = ref(false);
const formRef = ref<InstanceType<typeof FaForm> | null>(null);
const nodeTypeFormRenderKey = ref(0);

const defaultForm = (): WorkflowNodeTypeForm => ({
  name: "",
  code: "",
  category: "action",
  func: `def handler(*args, **kwargs):
    """
    编写你的处理逻辑
    可访问:
    - args: 位置参数
    - kwargs: 关键字参数
    """
    print("handler executed")
    return {"status": "success"}
`,
  args: "",
  kwargs: "{}",
  sort_order: 0,
  is_active: true,
});

const formData = ref<WorkflowNodeTypeForm>(defaultForm());
const argsList = ref<string[]>([]);
const kwargsList = ref<{ key: string; value: string }[]>([]);

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

const rules: FormRules = {
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入编码", trigger: "blur" }],
  category: [{ required: true, message: "请选择分类", trigger: "change" }],
};

function resetForm() {
  Object.assign(formData.value, defaultForm());
  editingId.value = null;
  argsList.value = [];
  kwargsList.value = [];
  formRef.value?.resetFields();
  formRef.value?.clearValidate();
}

function handleCloseDialog() {
  resetForm();
}

function handleDialogOpened() {
  nextTick(() => {
    setTimeout(() => {
      codeEditorRef.value?.refresh?.();
    }, 100);
  });
}

async function handleAdd() {
  createLoading.value = true;
  try {
    await openDialog();
  } finally {
    createLoading.value = false;
  }
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
        formData.value.sort_order = d.sort_order ?? 0;
        formData.value.is_active = d.is_active ?? true;
        argsList.value = d.args ? d.args.split(",").map((v: string) => v.trim()) : [];
        kwargsList.value = d.kwargs
          ? Object.entries(JSON.parse(d.kwargs)).map(([key, value]) => ({
              key,
              value: String(value),
            }))
          : [];
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

  if (!formData.value.func || !formData.value.func.trim()) {
    ElMessage.error("请输入 handler 代码");
    return;
  }

  submitting.value = true;
  try {
    const submitData = {
      ...formData.value,
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
    if (editingId.value) {
      await WorkflowNodeTypeAPI.updateWorkflowNodeType(editingId.value, submitData);
      dialogVisible.value = false;
      await refreshUpdate();
    } else {
      await WorkflowNodeTypeAPI.createWorkflowNodeType(submitData);
      dialogVisible.value = false;
      await refreshCreate();
    }
  } catch {
    /* 接口错误已由拦截器提示 */
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.code-editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.code-editor-header {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.code-editor-title {
  font-size: 14px;
  font-weight: 600;
}

.code-editor-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
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

  .el-input {
    flex: 1;
  }
}
</style>
