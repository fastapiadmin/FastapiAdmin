<template>
  <el-drawer v-model="visible" :title="workflow ? '编辑流程' : '新建流程'" size="86%" destroy-on-close>
    <div class="wf-designer">
      <aside class="wf-side">
        <div class="wf-side__title">基础信息</div>
        <el-form label-position="top" size="small">
          <el-form-item label="流程名称" required>
            <el-input v-model="form.name" maxlength="64" placeholder="如：采购审批" />
          </el-form-item>
          <el-form-item label="流程说明">
            <el-input v-model="form.description" type="textarea" :rows="3" maxlength="500" />
          </el-form-item>
          <el-form-item label="状态">
            <el-switch v-model="form.status" :active-value="0" :inactive-value="1" active-text="启用" inactive-text="停用" />
          </el-form-item>
        </el-form>
        <el-divider />
        <div class="wf-side__title">添加节点</div>
        <div class="wf-palette">
          <button type="button" class="wf-palette__item" @click="addNode('approval')">
            <span class="wf-dot wf-dot--approval" />审批节点
          </button>
          <button type="button" class="wf-palette__item" @click="addNode('condition')">
            <span class="wf-dot wf-dot--condition" />条件节点
          </button>
        </div>
        <p class="wf-hint">节点按连线顺序执行。条件不满足时流程直接拒绝。</p>
      </aside>

      <section class="wf-canvas">
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          class="wf-flow"
          :default-viewport="{ zoom: 0.9 }"
          :min-zoom="0.3"
          :max-zoom="1.4"
          :fit-view-on-init="true"
          :delete-key-code="null"
          :default-edge-options="defaultEdgeOptions"
          @node-click="onNodeClick"
          @pane-click="selectedId = ''"
        >
          <Background pattern-color="#d8dbe6" :gap="18" />
          <Controls />
          <MiniMap pannable zoomable :width="160" :height="100" />
          <Panel position="top-left" class="wf-tools">
            <el-button size="small" @click="addNode('approval')">+ 审批</el-button>
            <el-button size="small" @click="addNode('condition')">+ 条件</el-button>
            <el-button size="small" :disabled="!canDelete" @click="deleteSelected">删除节点</el-button>
            <el-button size="small" @click="autoLayout">自动排列</el-button>
          </Panel>

          <template #node-start="{ data }">
            <div class="wf-node wf-node--start">
              <span class="wf-node__icon">▶</span>
              <span class="wf-node__label">{{ data.label }}</span>
              <Handle type="source" :position="Position.Right" />
            </div>
          </template>
          <template #node-end="{ data }">
            <div class="wf-node wf-node--end">
              <span class="wf-node__icon">■</span>
              <span class="wf-node__label">{{ data.label }}</span>
              <Handle type="target" :position="Position.Left" />
            </div>
          </template>
          <template #node-approval="{ data, selected }">
            <div class="wf-node wf-node--approval" :class="{ selected }">
              <Handle type="target" :position="Position.Left" />
              <span class="wf-node__icon">✓</span>
              <div class="wf-node__body">
                <span class="wf-node__label">{{ data.label }}</span>
                <span class="wf-node__meta">{{ userName(data.assignee_id) || '未设置审批人' }}</span>
              </div>
              <Handle type="source" :position="Position.Right" />
            </div>
          </template>
          <template #node-condition="{ data, selected }">
            <div class="wf-node wf-node--condition" :class="{ selected }">
              <Handle type="target" :position="Position.Left" />
              <span class="wf-node__icon">◇</span>
              <div class="wf-node__body">
                <span class="wf-node__label">{{ data.label }}</span>
                <span class="wf-node__meta">{{ conditionText(data) }}</span>
              </div>
              <Handle type="source" :position="Position.Right" />
            </div>
          </template>
        </VueFlow>
      </section>

      <aside class="wf-config">
        <template v-if="selectedNode">
          <div class="wf-side__title">节点配置</div>
          <el-form label-position="top" size="small">
            <el-form-item label="节点名称">
              <el-input v-model="selectedNode.data.label" maxlength="32" />
            </el-form-item>
            <template v-if="selectedNode.type === 'approval'">
              <el-form-item label="审批人" required>
                <el-select v-model="selectedNode.data.assignee_id" filterable placeholder="请选择审批人" style="width: 100%">
                  <el-option v-for="user in users" :key="user.value" :label="user.label" :value="user.value" />
                </el-select>
              </el-form-item>
              <p class="wf-hint">审批通过后进入下一节点；拒绝则流程结束。</p>
            </template>
            <template v-else-if="selectedNode.type === 'condition'">
              <el-form-item label="判断字段" required>
                <el-input v-model="selectedNode.data.field" placeholder="如 amount 或 user.level" />
              </el-form-item>
              <el-form-item label="运算符">
                <el-select v-model="selectedNode.data.operator" style="width: 100%">
                  <el-option label="等于" value="eq" />
                  <el-option label="不等于" value="ne" />
                  <el-option label="大于" value="gt" />
                  <el-option label="大于等于" value="gte" />
                  <el-option label="小于" value="lt" />
                  <el-option label="小于等于" value="lte" />
                  <el-option label="包含" value="contains" />
                </el-select>
              </el-form-item>
              <el-form-item label="比较值" required>
                <el-input v-model="selectedNode.data.value" placeholder="比较值" />
              </el-form-item>
              <p class="wf-hint">不满足条件时流程直接拒绝。</p>
            </template>
            <el-button v-if="selectedNode.type !== 'start' && selectedNode.type !== 'end'" type="danger" plain style="width: 100%" @click="deleteSelected">
              删除此节点
            </el-button>
          </el-form>
        </template>
        <el-empty v-else description="点击画布节点进行配置" :image-size="64" />
      </aside>
    </div>

    <template #footer>
      <div class="wf-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="submit">保存流程</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { MiniMap } from "@vue-flow/minimap";
import { Handle, MarkerType, Panel, Position, VueFlow } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "@vue-flow/minimap/dist/style.css";
import type { WorkflowForm, WorkflowItem, WorkflowStep, WorkflowStepType } from "@/api/module_task/workflow";

interface UserOption { label: string; value: number; }
interface FlowNodeData extends WorkflowStep { label: string; }
interface FlowNode { id: string; type: "start" | "end" | WorkflowStepType; position: { x: number; y: number }; data: FlowNodeData; }
interface FlowEdge { id: string; source: string; target: string; type: string; animated: boolean; markerEnd: string; }

const props = defineProps<{ modelValue: boolean; workflow: WorkflowItem | null; users: UserOption[] }>();
const emit = defineEmits<{ "update:modelValue": [value: boolean]; save: [payload: WorkflowForm] }>();
const visible = computed({ get: () => props.modelValue, set: (value: boolean) => emit("update:modelValue", value) });

const form = reactive<WorkflowForm>({ name: "", description: "", status: 0, steps: [] });
const nodes = ref<FlowNode[]>([]);
const edges = ref<FlowEdge[]>([]);
const selectedId = ref("");
const saving = ref(false);
let seed = 0;

const defaultEdgeOptions = { type: "smoothstep", animated: true, markerEnd: MarkerType.ArrowClosed };
const selectedNode = computed(() => nodes.value.find((node) => node.id === selectedId.value));
const canDelete = computed(() => selectedNode.value !== undefined && !["start", "end"].includes(selectedNode.value.type));

function uid(prefix: string) { seed += 1; return `${prefix}-${Date.now()}-${seed}`; }
function edge(source: string, target: string): FlowEdge { return { id: uid("edge"), source, target, ...defaultEdgeOptions }; }
function makeNode(type: WorkflowStepType, index: number, step?: WorkflowStep): FlowNode {
  return { id: uid(type), type, position: { x: 80 + index * 240, y: 200 }, data: {
    type, name: step?.name || (type === "approval" ? "审批" : "条件判断"), label: step?.name || (type === "approval" ? "审批" : "条件判断"),
    assignee_id: step?.assignee_id ?? null, field: step?.field ?? "amount",
    operator: step?.operator ?? "gte", value: step?.value ?? 1000,
  } };
}

function init() {
  const source = props.workflow;
  form.name = source?.name ?? "";
  form.description = source?.description ?? "";
  form.status = source?.status ?? 0;
  const steps = source?.steps ?? [];
  const built: FlowNode[] = [{ id: "start", type: "start", position: { x: 80, y: 200 }, data: { type: "approval", name: "开始", label: "开始" } as FlowNodeData }];
  steps.forEach((step, index) => built.push(makeNode(step.type, index + 1, step)));
  built.push({ id: "end", type: "end", position: { x: 80 + (steps.length + 1) * 240, y: 200 }, data: { type: "approval", name: "结束", label: "结束" } as FlowNodeData });
  nodes.value = built;
  edges.value = built.slice(0, -1).map((node, index) => edge(node.id, built[index + 1]!.id));
  selectedId.value = "";
}

function addNode(type: WorkflowStepType) {
  const end = nodes.value.find((node) => node.id === "end");
  if (!end) return;
  const incoming = edges.value.filter((item) => item.target === "end");
  if (incoming.length !== 1) return ElMessage.warning("结束节点前只能有一条连线");
  const prev = incoming[0]!;
  const node = makeNode(type, nodes.value.length - 1);
  end.position.x += 240;
  edges.value = edges.value.filter((item) => item.id !== prev.id);
  nodes.value.push(node);
  edges.value.push(edge(prev.source, node.id), edge(node.id, "end"));
  selectedId.value = node.id;
}

function deleteSelected() {
  const node = selectedNode.value;
  if (!node || ["start", "end"].includes(node.type)) return;
  const incoming = edges.value.find((item) => item.target === node.id);
  const outgoing = edges.value.find((item) => item.source === node.id);
  edges.value = edges.value.filter((item) => item.source !== node.id && item.target !== node.id);
  nodes.value = nodes.value.filter((item) => item.id !== node.id);
  if (incoming && outgoing) edges.value.push(edge(incoming.source, outgoing.target));
  selectedId.value = "";
}

function onNodeClick(event: { node: any }) { selectedId.value = event.node.id; }
function conditionText(data: FlowNodeData) {
  const operator = ({ eq: "=", ne: "≠", gt: ">", gte: "≥", lt: "<", lte: "≤", contains: "包含" } as Record<string, string>)[String(data.operator)] ?? String(data.operator);
  return `${data.field || "字段"} ${operator} ${data.value ?? ""}`;
}
function userName(id?: number | null) { return props.users.find((user) => user.value === id)?.label ?? ""; }

function autoLayout() {
  const map = new Map(nodes.value.map((node) => [node.id, node]));
  const seen = new Set<string>();
  let current = map.get("start");
  let index = 0;
  while (current && !seen.has(current.id)) {
    seen.add(current.id);
    current.position = { x: 80 + index * 240, y: 200 };
    index += 1;
    if (current.id === "end") break;
    const next = edges.value.find((item) => item.source === current!.id);
    current = next ? map.get(next.target) : undefined;
  }
}

function buildSteps() {
  if (!form.name.trim()) throw new Error("请填写流程名称");
  const map = new Map(nodes.value.map((node) => [node.id, node]));
  const steps: WorkflowStep[] = [];
  const seen = new Set<string>();
  let current = "start";
  while (current !== "end") {
    const outgoing = edges.value.filter((item) => item.source === current);
    if (outgoing.length !== 1) throw new Error("流程必须是单一路径：每个节点只能有一条出线");
    const next = outgoing[0]!.target;
    if (seen.has(next)) throw new Error("流程存在环，请检查连线");
    seen.add(next);
    const node = map.get(next);
    if (!node) throw new Error("流程连线指向了不存在的节点");
    if (node.id === "end") break;
    if (node.type === "approval") {
      if (!node.data.assignee_id) throw new Error(`「${node.data.label}」未设置审批人`);
      steps.push({ type: "approval", name: node.data.label, assignee_id: node.data.assignee_id });
    } else if (node.type === "condition") {
      if (!node.data.field) throw new Error(`「${node.data.label}」未设置判断字段`);
      steps.push({ type: "condition", name: node.data.label, field: node.data.field, operator: node.data.operator, value: node.data.value });
    }
    current = next;
  }
  if (!steps.some((step) => step.type === "approval")) throw new Error("至少需要一个审批节点");
  return steps;
}

function submit() {
  try {
    const steps = buildSteps();
    saving.value = true;
    emit("save", { name: form.name.trim(), description: form.description, status: form.status, steps });
  } catch (error) {
    ElMessage.warning(error instanceof Error ? error.message : "流程配置不完整");
  }
}

watch(() => props.modelValue, (value) => { if (value) init(); }, { immediate: true });
</script>

<style scoped>
.wf-designer { display: flex; height: calc(100vh - 148px); min-height: 520px; overflow: hidden; border: 1px solid var(--el-border-color-lighter); border-radius: 10px; }
.wf-side, .wf-config { flex: none; width: 260px; padding: 14px; overflow-y: auto; background: var(--el-fill-color-lighter); }
.wf-config { width: 290px; background: var(--el-bg-color); border-left: 1px solid var(--el-border-color-lighter); }
.wf-side { border-right: 1px solid var(--el-border-color-lighter); }
.wf-side__title { margin-bottom: 10px; color: var(--el-text-color-primary); font-size: 13px; font-weight: 600; }
.wf-palette { display: grid; gap: 8px; }
.wf-palette__item { display: flex; gap: 8px; align-items: center; width: 100%; padding: 9px 10px; color: var(--el-text-color-regular); font-size: 13px; text-align: left; cursor: pointer; background: var(--el-bg-color); border: 1px solid var(--el-border-color); border-radius: 8px; }
.wf-palette__item:hover { color: var(--el-color-primary); border-color: var(--el-color-primary); }
.wf-dot { width: 8px; height: 8px; border-radius: 50%; }
.wf-dot--approval { background: var(--el-color-primary); }
.wf-dot--condition { background: var(--el-color-warning); }
.wf-hint { margin: 10px 0 0; color: var(--el-text-color-secondary); font-size: 12px; line-height: 1.6; }
.wf-canvas { flex: 1; min-width: 0; background: var(--el-bg-color); }
.wf-flow { width: 100%; height: 100%; }
.wf-tools { display: flex; gap: 6px; padding: 6px; background: var(--el-bg-color); border: 1px solid var(--el-border-color-lighter); border-radius: 8px; box-shadow: 0 2px 8px rgb(0 0 0 / 6%); }
.wf-node { display: flex; gap: 8px; align-items: center; min-width: 176px; max-width: 220px; padding: 10px 12px; background: var(--el-bg-color); border: 1.5px solid var(--el-border-color); border-radius: 10px; box-shadow: 0 2px 6px rgb(0 0 0 / 5%); }
.wf-node.selected { border-color: var(--el-color-primary); box-shadow: 0 0 0 2px rgb(64 158 255 / 18%); }
.wf-node--start { border-color: #34a853; }
.wf-node--end { border-color: #909399; }
.wf-node--approval { border-color: color-mix(in srgb, var(--el-color-primary) 40%, var(--el-border-color)); }
.wf-node--condition { border-color: color-mix(in srgb, var(--el-color-warning) 45%, var(--el-border-color)); }
.wf-node__icon { display: inline-flex; flex: none; align-items: center; justify-content: center; width: 22px; height: 22px; color: var(--el-color-primary); font-size: 12px; background: var(--el-color-primary-light-9); border-radius: 6px; }
.wf-node--start .wf-node__icon { color: #1a7f37; background: #e8f5ec; }
.wf-node--end .wf-node__icon { color: #606266; background: #f2f3f5; }
.wf-node__body { display: flex; flex-direction: column; min-width: 0; }
.wf-node__label { overflow: hidden; color: var(--el-text-color-primary); font-size: 13px; font-weight: 600; text-overflow: ellipsis; white-space: nowrap; }
.wf-node__meta { overflow: hidden; margin-top: 2px; color: var(--el-text-color-secondary); font-size: 11px; text-overflow: ellipsis; white-space: nowrap; }
.wf-flow :deep(.vue-flow__minimap) { width: 160px; height: 100px; overflow: hidden; background: var(--el-bg-color); border: 1px solid var(--el-border-color-lighter); border-radius: 8px; }
.wf-footer { display: flex; justify-content: flex-end; gap: 8px; }
</style>
