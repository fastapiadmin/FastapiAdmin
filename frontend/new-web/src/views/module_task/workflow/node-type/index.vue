<template>
  <div class="app-container">
    <CrudSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <CrudContent ref="contentRef" :content-config="contentConfig" @add-click="openDialog()">
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
            <el-table-column type="selection" align="center" min-width="55" />
            <el-table-column type="index" fixed label="序号" min-width="60">
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="ID" prop="id" min-width="70" />
            <el-table-column label="名称" prop="name" min-width="140" show-overflow-tooltip />
            <el-table-column label="编码" prop="code" min-width="120" show-overflow-tooltip />
            <el-table-column label="分类" prop="category" min-width="100">
              <template #default="scope">
                {{ categoryLabel(scope.row.category) }}
              </template>
            </el-table-column>
            <el-table-column label="排序" prop="sort_order" min-width="80" />
            <el-table-column label="启用" prop="is_active" min-width="80">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                  {{ scope.row.is_active ? "是" : "否" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" prop="created_time" min-width="170" />

            <OperationColumn :list-data-length="data.length">
              <template #default="scope">
                <el-space class="flex">
                  <el-button
                    v-hasPerm="['module_task:workflow:node-type:update']"
                    type="primary"
                    size="small"
                    link
                    icon="edit"
                    @click="openDialog(scope.row.id)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    v-hasPerm="['module_task:workflow:node-type:delete']"
                    type="danger"
                    size="small"
                    link
                    icon="delete"
                    @click="handleRowDelete(scope.row.id)"
                  >
                    删除
                  </el-button>
                </el-space>
              </template>
            </OperationColumn>
          </el-table>
        </div>
      </template>
    </CrudContent>

    <EnhancedDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="720px"
      destroy-on-close
      @close="handleCloseDialog"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" maxlength="128" show-word-limit />
        </el-form-item>
        <el-form-item label="编码" prop="code">
          <el-input v-model="form.code" maxlength="64" show-word-limit :disabled="!!editingId" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" style="width: 100%">
            <el-option label="触发器" value="trigger" />
            <el-option label="动作" value="action" />
            <el-option label="条件" value="condition" />
            <el-option label="控制" value="control" />
          </el-select>
        </el-form-item>
        <el-form-item label="代码块" prop="func">
          <el-input
            v-model="form.func"
            type="textarea"
            :rows="12"
            placeholder="须定义 handler(*args, **kwargs)，可接收 upstream、variables"
          />
        </el-form-item>
        <el-form-item label="位置参数" prop="args">
          <el-input v-model="form.args" placeholder="逗号分隔，如 a, b" />
        </el-form-item>
        <el-form-item label="关键字参数" prop="kwargs">
          <el-input
            v-model="form.kwargs"
            type="textarea"
            :rows="3"
            placeholder='JSON，如 {"key": "v"}'
          />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="启用" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitForm">保存</el-button>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "WorkflowNodeType",
  inheritAttrs: false,
});

import { onMounted, reactive, ref } from "vue";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import CrudSearch from "@/components/CURD/CrudSearch.vue";
import CrudContent from "@/components/CURD/CrudContent.vue";
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import type { IContentConfig, ISearchConfig } from "@/components/Crud/types";
import { useCrudList } from "@/components/Crud/useCrudList";
import OperationColumn from "@/components/OperationColumn/index.vue";
import WorkflowNodeTypeAPI, {
  type WorkflowNodeTypeForm,
  type WorkflowNodeTypePageQuery,
  type WorkflowNodeTypeTable,
} from "@/api/module_task/workflow/node-type";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

const dialogVisible = ref(false);
const dialogTitle = ref("新增节点类型");
const editingId = ref<number | null>(null);
const submitting = ref(false);
const formRef = ref<FormInstance>();

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_task:workflow:node-type",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "name",
      label: "名称",
      type: "input",
      attrs: { placeholder: "名称", clearable: true },
    },
    {
      prop: "code",
      label: "编码",
      type: "input",
      attrs: { placeholder: "编码", clearable: true },
    },
    {
      prop: "category",
      label: "分类",
      type: "select",
      options: [
        { label: "触发器", value: "trigger" },
        { label: "动作", value: "action" },
        { label: "条件", value: "condition" },
        { label: "控制", value: "control" },
      ],
      attrs: { placeholder: "全部", clearable: true, style: { width: "170px" } },
    },
  ],
});

function normalizeNodeTypeQuery(params: Record<string, unknown>): WorkflowNodeTypePageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (p.category === "" || p.category === null) p.category = undefined;
  return p as unknown as WorkflowNodeTypePageQuery;
}

const contentConfig = reactive<IContentConfig<WorkflowNodeTypePageQuery>>({
  permPrefix: "module_task:workflow:node-type",
  cols: [],
  hideColumnFilter: true,
  toolbar: [
    { name: "add", text: "新增", attrs: { icon: "plus", type: "success" }, perm: "create" },
    "delete",
  ],
  defaultToolbar: ["refresh"],
  initialFetch: false,
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await WorkflowNodeTypeAPI.getWorkflowNodeTypeList(
      normalizeNodeTypeQuery(params as unknown as Record<string, unknown>)
    );
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: (ids) =>
    WorkflowNodeTypeAPI.deleteWorkflowNodeType(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n) && n > 0)
    ),
  deleteConfirm: {
    title: "警告",
    message: "确认删除选中的编排节点类型吗？",
    type: "warning",
  },
});

function handleRowDelete(id?: number) {
  if (id == null) return;
  contentRef.value?.handleDelete(id);
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

const form = reactive<WorkflowNodeTypeForm>(defaultForm());

const rules: FormRules = {
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入编码", trigger: "blur" }],
  category: [{ required: true, message: "请选择分类", trigger: "change" }],
  func: [{ required: true, message: "请输入代码块", trigger: "blur" }],
};

function resetForm() {
  Object.assign(form, defaultForm());
  editingId.value = null;
  formRef.value?.resetFields();
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
        form.name = d.name || "";
        form.code = d.code || "";
        form.category = (d.category as WorkflowNodeTypeForm["category"]) || "action";
        form.func = d.func || "";
        form.args = d.args || "";
        form.kwargs = d.kwargs || "{}";
        form.sort_order = d.sort_order ?? 0;
        form.is_active = d.is_active ?? true;
      }
    } catch {
      ElMessage.error("加载详情失败");
      return;
    }
  }
  dialogVisible.value = true;
}

async function submitForm() {
  if (!formRef.value) return;
  await formRef.value.validate();
  if (form.kwargs?.trim()) {
    try {
      JSON.parse(form.kwargs);
    } catch {
      ElMessage.error("关键字参数须为合法 JSON");
      return;
    }
  }
  submitting.value = true;
  try {
    if (editingId.value) {
      await WorkflowNodeTypeAPI.updateWorkflowNodeType(editingId.value, form);
      ElMessage.success("更新成功");
    } else {
      await WorkflowNodeTypeAPI.createWorkflowNodeType(form);
      ElMessage.success("创建成功");
    }
    dialogVisible.value = false;
    refreshList();
  } catch {
    ElMessage.error(editingId.value ? "更新失败" : "创建失败");
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  refreshList();
});
</script>

<style scoped lang="scss"></style>
