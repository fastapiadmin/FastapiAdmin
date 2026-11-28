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
const activeCount = computed(() => workflows.value.filter((item) => item.status === 0).length);
const runningCount = computed(() => instances.value.filter((item) => item.status === "running").length);

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
  const res = await UserAPI.listUser({ page_no: 1, page_size: 100 });
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
  <div class="app-container workflow-page">
    <section class="wf-hero">
      <div class="wf-hero__copy">
        <div class="wf-eyebrow">任务管理 / 流程编排</div>
        <h1>流程编排</h1>
        <p>用可视化画布编排审批与条件，发起后自动生成待办任务，进度与结果全程留痕。</p>
      </div>
      <el-button type="primary" size="large" @click="openCreate">新建流程</el-button>
    </section>

    <section class="wf-stats">
      <div class="wf-stat">
        <span class="wf-stat__label">流程总数</span>
        <strong>{{ total }}</strong>
        <small>已配置流程</small>
      </div>
      <div class="wf-stat">
        <span class="wf-stat__label">启用中</span>
        <strong>{{ activeCount }}</strong>
        <small>可发起流程</small>
      </div>
      <div class="wf-stat">
        <span class="wf-stat__label">待我审批</span>
        <strong>{{ pendingTasks.length }}</strong>
        <small>需要你处理</small>
      </div>
      <div class="wf-stat">
        <span class="wf-stat__label">运行中实例</span>
        <strong>{{ runningCount }}</strong>
        <small>最近实例</small>
      </div>
    </section>

    <el-card class="wf-card" shadow="never">
      <div class="wf-card__head">
        <div>
          <h2>流程列表</h2>
          <span>管理流程定义、发起与编辑</span>
        </div>
        <div class="wf-search">
          <el-input v-model="query.name" placeholder="搜索流程名称" clearable @keyup.enter="loadWorkflows" />
          <el-button @click="loadWorkflows">查询</el-button>
        </div>
      </div>
      <el-table v-loading="loading" :data="workflows" row-key="id" class="wf-table">
        <el-table-column prop="name" label="流程名称" min-width="180">
          <template #default="{ row }">
            <div class="wf-name">
              <span class="wf-name__dot" :class="{ 'is-off': row.status !== 0 }" />
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" min-width="240" show-overflow-tooltip>
          <template #default="{ row }">{{ row.description || "—" }}</template>
        </el-table-column>
        <el-table-column label="步骤" width="90">
          <template #default="{ row }">{{ row.steps?.length ?? 0 }} 步</template>
        </el-table-column>
        <el-table-column label="状态" width="96">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'success' : 'info'" effect="light" round size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="230" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" :disabled="row.status !== 0" @click="openRun(row)">发起</el-button>
            <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="removeWorkflow(row)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="还没有流程，新建一个开始编排" :image-size="72" />
        </template>
      </el-table>
      <div class="wf-pagination">
        <el-pagination
          v-model:current-page="query.page_no"
          v-model:page-size="query.page_size"
          layout="total, prev, pager, next"
          :total="total"
          @current-change="loadWorkflows"
        />
      </div>
    </el-card>

    <div class="wf-bottom">
      <el-card class="wf-card" shadow="never">
        <div class="wf-card__head wf-card__head--compact">
          <div>
            <h2>待我审批</h2>
            <span>通过或拒绝后流程自动继续</span>
          </div>
          <el-badge :value="pendingTasks.length" :hidden="!pendingTasks.length" />
        </div>
        <div v-if="!pendingTasks.length" class="wf-empty">
          <div class="wf-empty__icon">✓</div>
          <p>暂无待审批任务</p>
          <span>有新的审批时会出现在这里</span>
        </div>
        <div v-else class="wf-task-list">
          <div v-for="task in pendingTasks" :key="task.id" class="wf-task">
            <div class="wf-task__main">
              <strong>{{ task.step_name }}</strong>
              <span>实例 #{{ task.instance_id }} · {{ task.created_time || "刚刚" }}</span>
            </div>
            <div class="wf-task__actions">
              <el-button size="small" type="success" plain @click="actTask(task, true)">通过</el-button>
              <el-button size="small" type="danger" plain @click="actTask(task, false)">拒绝</el-button>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="wf-card" shadow="never">
        <div class="wf-card__head wf-card__head--compact">
          <div>
            <h2>最近实例</h2>
            <span>最近发起的流程与执行状态</span>
          </div>
        </div>
        <el-table :data="instances" row-key="id" class="wf-table wf-table--compact">
          <el-table-column prop="workflow_name" label="流程" min-width="150" show-overflow-tooltip />
          <el-table-column label="进度" width="88">
            <template #default="{ row }">{{ Math.min(row.current_index + 1, row.steps.length) }} / {{ row.steps.length }}</template>
          </el-table-column>
          <el-table-column label="状态" width="92">
            <template #default="{ row }">
              <el-tag :type="instanceTagType(row.status)" effect="light" round size="small">
                {{ instanceStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_time" label="发起时间" min-width="160" show-overflow-tooltip />
          <template #empty>
            <el-empty description="还没有实例，先发起一个流程" :image-size="64" />
          </template>
        </el-table>
      </el-card>
    </div>

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
.workflow-page {
  padding: 20px 24px 32px;
  background: var(--el-bg-color-page);
  min-height: 100%;
}

.wf-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 24px 28px;
  border-radius: 16px;
  background:
    radial-gradient(120% 160% at 100% 0%, rgb(79 107 255 / 12%), transparent 55%),
    linear-gradient(135deg, var(--el-bg-color) 0%, var(--el-fill-color-lighter) 100%);
  border: 1px solid var(--el-border-color-lighter);
}

.wf-eyebrow {
  margin-bottom: 8px;
  color: var(--el-color-primary);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
}

.wf-hero h1 {
  margin: 0;
  color: var(--el-text-color-primary);
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.wf-hero p {
  margin: 8px 0 0;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.wf-stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin: 16px 0;
}

.wf-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 18px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 14px;
}

.wf-stat__label {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.wf-stat strong {
  color: var(--el-text-color-primary);
  font-size: 26px;
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
}

.wf-stat small {
  color: var(--el-text-color-placeholder);
  font-size: 11px;
}

.wf-card {
  border-radius: 14px;
  border-color: var(--el-border-color-lighter);
}

.wf-card :deep(.el-card__body) {
  padding: 18px 20px;
}

.wf-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.wf-card__head--compact {
  margin-bottom: 10px;
}

.wf-card__head h2 {
  margin: 0;
  color: var(--el-text-color-primary);
  font-size: 16px;
  font-weight: 600;
}

.wf-card__head span {
  display: block;
  margin-top: 4px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.wf-search {
  display: flex;
  gap: 8px;
  width: 320px;
  max-width: 45%;
}

.wf-search .el-input {
  flex: 1;
}

.wf-table :deep(.el-table__header th.el-table__cell) {
  background: var(--el-fill-color-lighter);
  color: var(--el-text-color-secondary);
  font-weight: 500;
  height: 42px;
}

.wf-table :deep(.el-table__row td.el-table__cell) {
  padding: 12px 0;
}

.wf-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.wf-name__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--el-color-success);
}

.wf-name__dot.is-off {
  background: var(--el-text-color-placeholder);
}

.wf-pagination {
  display: flex;
  justify-content: flex-end;
  padding-top: 14px;
}

.wf-bottom {
  display: grid;
  grid-template-columns: minmax(300px, 0.9fr) minmax(0, 1.4fr);
  gap: 16px;
  margin-top: 16px;
}

.wf-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 150px;
  color: var(--el-text-color-secondary);
  text-align: center;
}

.wf-empty__icon {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  margin-bottom: 10px;
  color: var(--el-color-success);
  font-size: 20px;
  background: var(--el-color-success-light-9);
  border-radius: 50%;
}

.wf-empty p {
  margin: 0;
  color: var(--el-text-color-primary);
  font-size: 14px;
  font-weight: 500;
}

.wf-empty span {
  margin-top: 4px;
  font-size: 12px;
}

.wf-task-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wf-task {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 10px;
}

.wf-task__main {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.wf-task__main strong {
  color: var(--el-text-color-primary);
  font-size: 13px;
}

.wf-task__main span {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.wf-task__actions {
  flex: none;
}

.wf-table--compact :deep(.el-table__row td.el-table__cell) {
  padding: 10px 0;
}

.run-tip {
  margin: 0 0 10px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

@media (max-width: 1100px) {
  .wf-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .wf-bottom {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .workflow-page {
    padding: 14px;
  }

  .wf-hero {
    align-items: flex-start;
    flex-direction: column;
  }

  .wf-search {
    width: 100%;
    max-width: none;
  }

  .wf-card__head {
    flex-direction: column;
  }
}
</style>
