<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { UserAPI } from "@/api/module_system/user";
import WorkflowDesigner from "./components/WorkflowDesigner.vue";
import WorkflowAPI, {
  type WorkflowForm,
  type WorkflowInstance,
  type WorkflowItem,
  type WorkflowStep,
  type WorkflowTask,
} from "@/api/module_task/workflow";

defineOptions({ name: "Workflow" });

const loading = ref(false);
const saving = ref(false);
const workflows = ref<WorkflowItem[]>([]);
const instances = ref<WorkflowInstance[]>([]);
const pendingTasks = ref<WorkflowTask[]>([]);
const userOptions = ref<Array<{ label: string; value: number }>>([]);

const query = reactive({ page_no: 1, page_size: 10, name: "" });
const total = ref(0);

const editorVisible = ref(false);
const editingWorkflow = ref<WorkflowItem | null>(null);

const runVisible = ref(false);
const runningWorkflow = ref<WorkflowItem | null>(null);
const runContext = ref('{\n  "amount": 1000,\n  "department": "技术部"\n}');

function statusText(status: number) {
  return status === 0 ? "启用" : "停用";
}

function instanceStatusText(status: WorkflowInstance["status"]) {
  return { running: "进行中", completed: "已完成", rejected: "已拒绝" }[status] ?? status;
}

function instanceTagType(status: WorkflowInstance["status"]) {
  return status === "completed" ? "success" : status === "rejected" ? "danger" : "warning";
}

async function loadWorkflows() {
  loading.value = true;
  try {
    const res = await WorkflowAPI.getPage(query);
    workflows.value = res.data.data.items;
    total.value = res.data.data.total;
  } finally {
    loading.value = false;
  }
}

async function loadInstances() {
  const res = await WorkflowAPI.getInstances({ page_no: 1, page_size: 10 });
  instances.value = res.data.data.items;
}

async function loadPending() {
  const res = await WorkflowAPI.getPendingTasks();
  pendingTasks.value = res.data.data;
}

async function loadUsers() {
  const res = await UserAPI.listUser({ page_no: 1, page_size: 200 });
  const items = ((res.data.data as any).items ?? []) as Array<{ id: number; name?: string; username?: string }>;
  userOptions.value = items.map((user) => ({
    label: `${user.name ?? ""}（${user.username ?? ""}）`,
    value: user.id,
  }));
}

async function refresh() {
  await Promise.all([loadWorkflows(), loadInstances(), loadPending()]);
}

function openCreate() {
  editingWorkflow.value = null;
  editorVisible.value = true;
}

function openEdit(row: any) {
  editingWorkflow.value = JSON.parse(JSON.stringify(row)) as WorkflowItem;
  editorVisible.value = true;
}

async function saveWorkflow(payload: WorkflowForm) {
  saving.value = true;
  try {
    if (editingWorkflow.value?.id) await WorkflowAPI.update(editingWorkflow.value.id, payload);
    else await WorkflowAPI.create(payload);
    ElMessage.success(editingWorkflow.value?.id ? "流程已更新" : "流程已创建");
    editorVisible.value = false;
    await refresh();
  } finally {
    saving.value = false;
  }
}

async function removeWorkflow(row: any) {
  await ElMessageBox.confirm(`确认删除流程「${row.name}」？已发起的实例不受影响。`, "删除流程", { type: "warning" });
  await WorkflowAPI.remove([row.id]);
  ElMessage.success("已删除");
  await refresh();
}

function openRun(row: any) {
  runningWorkflow.value = row;
  runContext.value = '{\n  "amount": 1000,\n  "department": "技术部"\n}';
  runVisible.value = true;
}

async function executeWorkflow() {
  if (!runningWorkflow.value) return;
  let context: Record<string, unknown>;
  try {
    context = JSON.parse(runContext.value || "{}");
  } catch {
    return ElMessage.error("上下文必须是合法 JSON");
  }
  await WorkflowAPI.execute(runningWorkflow.value.id, context);
  ElMessage.success("流程已发起");
  runVisible.value = false;
  await refresh();
}

async function actTask(task: any, approved: boolean) {
  const action = approved ? "通过" : "拒绝";
  const { value } = await ElMessageBox.prompt(`确认${action}「${task.step_name}」？`, `${action}审批`, {
    inputPlaceholder: "审批意见（可选）",
    confirmButtonText: action,
    cancelButtonText: "取消",
    inputValue: "",
  });
  await WorkflowAPI.act(task.id, approved, value || undefined);
  ElMessage.success(`已${action}`);
  await refresh();
}

onMounted(async () => {
  await Promise.all([loadUsers(), refresh()]);
});
</script>

<template>
  <div class="app-container">
    <el-card shadow="never">
      <div class="toolbar">
        <div>
          <el-input v-model="query.name" placeholder="搜索流程名称" clearable style="width: 220px" @keyup.enter="loadWorkflows" />
          <el-button class="ml-2" @click="loadWorkflows">查询</el-button>
        </div>
        <el-button type="primary" @click="openCreate">新建流程</el-button>
      </div>

      <el-table v-loading="loading" :data="workflows" row-key="id">
        <el-table-column prop="name" label="流程名称" min-width="160" />
        <el-table-column prop="description" label="说明" min-width="220" show-overflow-tooltip />
        <el-table-column label="步骤" width="90">
          <template #default="{ row }">{{ row.steps?.length ?? 0 }} 步</template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="230" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" :disabled="row.status !== 0" @click="openRun(row)">发起</el-button>
            <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="removeWorkflow(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="query.page_no"
        v-model:page-size="query.page_size"
        class="pagination"
        layout="total, prev, pager, next"
        :total="total"
        @current-change="loadWorkflows"
      />
    </el-card>

    <el-card shadow="never" class="mt-4">
      <template #header>
        <div class="card-title">
          <span>待我审批</span>
          <el-badge :value="pendingTasks.length" :hidden="!pendingTasks.length" />
        </div>
      </template>
      <el-empty v-if="!pendingTasks.length" description="暂无待审批任务" :image-size="72" />
      <el-table v-else :data="pendingTasks" row-key="id">
        <el-table-column prop="step_name" label="审批节点" min-width="140" />
        <el-table-column prop="instance_id" label="实例" width="90" />
        <el-table-column prop="created_time" label="到达时间" min-width="170" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button link type="success" @click="actTask(row, true)">通过</el-button>
            <el-button link type="danger" @click="actTask(row, false)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="never" class="mt-4">
      <template #header><span>最近实例</span></template>
      <el-empty v-if="!instances.length" description="还没有实例，先发起一个流程" :image-size="72" />
      <el-table v-else :data="instances" row-key="id">
        <el-table-column prop="workflow_name" label="流程" min-width="160" />
        <el-table-column label="进度" width="120">
          <template #default="{ row }">{{ Math.min(row.current_index + 1, row.steps.length) }} / {{ row.steps.length }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="instanceTagType(row.status)" size="small">{{ instanceStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="error" label="说明" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_time" label="发起时间" min-width="170" />
      </el-table>
    </el-card>

    <WorkflowDesigner
      v-model="editorVisible"
      :workflow="editingWorkflow"
      :users="userOptions"
      @save="saveWorkflow"
    />

    <el-dialog v-model="runVisible" :title="`发起：${runningWorkflow?.name ?? ''}`" width="520px" destroy-on-close>
      <p class="run-tip">上下文用于条件判断，必须是 JSON 对象；审批任务会进入审批人的待办。</p>
      <el-input v-model="runContext" type="textarea" :rows="8" spellcheck="false" />
      <template #footer>
        <el-button @click="runVisible = false">取消</el-button>
        <el-button type="primary" @click="executeWorkflow">发起流程</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.step-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 8px 0 10px;
  font-size: 14px;
  font-weight: 600;
}

.step-card {
  display: flex;
  gap: 10px;
  padding: 12px;
  margin-bottom: 10px;
  background: var(--el-fill-color-lighter);
  border-radius: 10px;
}

.step-index {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: #fff;
  font-size: 12px;
  background: var(--el-color-primary);
  border-radius: 50%;
  flex: none;
}

.step-body {
  flex: 1;
  min-width: 0;
}

.step-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.step-label {
  color: var(--el-text-color-secondary);
  font-size: 13px;
  flex: none;
}

.step-hint {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.run-tip {
  margin: 0 0 10px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}
</style>
