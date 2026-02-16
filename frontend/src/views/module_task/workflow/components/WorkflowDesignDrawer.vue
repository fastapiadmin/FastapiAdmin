<template>
  <el-drawer
    v-model="dialogVisible"
    :title="drawerTitle"
    :close-on-click-modal="true"
    size="80%"
    class="workflow-drawer"
    @close="handleClose"
  >
    <el-container class="workflow-create-content">
      <el-splitter direction="horizontal" style="height: 100%">
        <el-splitter-panel size="250px" :min="200" :max="400">
          <el-scrollbar style="height: 100%">
            <div class="basic-info-section">
              <div class="section-title">基础信息</div>
              <el-form
                ref="formRef"
                :model="formData"
                label-width="50px"
                :rules="formRules"
                size="small"
              >
                <el-form-item label="编码" prop="code">
                  <el-input v-model="formData.code" placeholder="请输入流程编码" />
                </el-form-item>
                <el-form-item label="名称" prop="name">
                  <el-input v-model="formData.name" placeholder="请输入流程名称" />
                </el-form-item>
                <el-form-item label="分类" prop="category">
                  <el-select
                    v-model="formData.category"
                    placeholder="请选择流程分类"
                    style="width: 100%"
                  >
                    <el-option label="数据处理" value="data" />
                    <el-option label="业务流程" value="business" />
                    <el-option label="通知流程" value="notification" />
                    <el-option label="审批流程" value="approval" />
                  </el-select>
                </el-form-item>
                <el-form-item label="描述" prop="description">
                  <el-input
                    v-model="formData.description"
                    type="textarea"
                    :rows="2"
                    placeholder="请输入流程描述"
                  />
                </el-form-item>
              </el-form>
            </div>

            <el-divider style="margin: 4px 0" />

            <div class="panel-section">
              <div class="section-title">节点</div>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索节点名称"
                clearable
                size="small"
                class="search-box"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-space direction="vertical" :size="8" fill style="width: 100%; margin-top: 8px">
                <el-tag
                  v-for="item in filteredNodes"
                  :key="'id' in item ? item.id : item.type"
                  :type="getNodeType(item)"
                  effect="plain"
                  draggable="true"
                  style="justify-content: center; cursor: move; user-select: none"
                  @dragstart="onDragStart($event, item)"
                  @dragend="onDragEnd"
                >
                  {{ item.name }}
                </el-tag>
              </el-space>
            </div>
          </el-scrollbar>
        </el-splitter-panel>

        <el-splitter-panel>
          <div class="canvas-main">
            <div class="canvas-container" @click="handleCanvasClick">
              <VueFlow
                v-model:nodes="nodes"
                v-model:edges="edges"
                class="basic-flow"
                :default-viewport="{ zoom: 1.5 }"
                :min-zoom="0.2"
                :max-zoom="4"
                :node-types="nodeTypesRegistry"
                :default-edge-options="defaultEdgeOptions"
                @node-click="onNodeClick"
                @edge-click="onEdgeClick"
                @drop="onDrop"
                @dragover="onDragOver"
              >
                <Controls />
                <Background pattern-color="#aaa" :gap="16" />
              </VueFlow>
            </div>
          </div>
        </el-splitter-panel>

        <el-splitter-panel v-if="updateState" size="320px" :min="280" :max="400">
          <NodeConfigPanel
            v-if="updateState === 'node'"
            :node="selectedNode"
            @close="handleClosePanel"
            @save="handleSaveNode"
            @delete="handleDeleteNode"
          />
          <EdgeConfigPanel
            v-if="updateState === 'edge'"
            :edge="selectedEdge"
            @close="handleClosePanel"
            @save="handleSaveEdge"
            @delete="handleDeleteEdge"
          />
        </el-splitter-panel>
      </el-splitter>
    </el-container>

    <template #footer>
      <div class="drawer-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleFinish">保存</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed, onMounted, markRaw, type Component } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { Search } from "@element-plus/icons-vue";
import type { Node, Edge, DefaultEdgeOptions, MarkerType } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "element-plus/dist/index.css";

import DynamicNode from "./DynamicNode.vue";
import NodeConfigPanel from "./NodeConfigPanel.vue";
import EdgeConfigPanel from "./EdgeConfigPanel.vue";
import NodeAPI from "@/api/module_task/node";
import WorkflowAPI, { type WorkflowTable, type WorkflowForm } from "@/api/module_task/workflow";
import { useWorkflowHistory } from "@/composables/useWorkflowHistory";
import { useNodeDrag } from "@/composables/useNodeDrag";
import { useNodeOperations } from "@/composables/useNodeOperations";

defineOptions({
  name: "WorkflowCreateDrawer",
  inheritAttrs: false,
});

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  workflow: {
    type: Object as () => WorkflowTable | undefined,
    default: undefined,
  },
});

const emit = defineEmits(["update:visible", "refresh"]);

const formRef = ref();
const workflowId = ref<number>();

const formData = reactive<Partial<WorkflowForm>>({
  code: "",
  name: "",
  category: "business",
  description: "",
});

const formRules = {
  code: [{ required: true, message: "请输入流程编码", trigger: "blur" }],
  name: [{ required: true, message: "请输入流程名称", trigger: "blur" }],
  category: [{ required: true, message: "请选择流程分类", trigger: "change" }],
};

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

const drawerTitle = computed(() => {
  return props.workflow ? "编辑工作流" : "创建工作流";
});

const {
  onInit,
  onConnect,
  addEdges,
  getNodes: getNodesRef,
  getEdges: getEdgesRef,
  setEdges,
  setNodes,
  screenToFlowCoordinate,
  onNodesInitialized,
  updateNode,
  addNodes,
} = useVueFlow();

const defaultEdgeOptions: DefaultEdgeOptions = {
  type: "smoothstep",
  animated: true,
  markerEnd: "arrowclosed" as MarkerType,
};

const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);

const searchKeyword = ref("");

type BaseNodeType = {
  type: string;
  name: string;
  color: string;
};

type LoadedNodeType = {
  id: number;
  type: string;
  name: string;
  class: string;
};

const allNodes = ref<(BaseNodeType | LoadedNodeType)[]>([
  {
    type: "input",
    name: "开始",
    color: "#67c23a",
  },
  {
    type: "output",
    name: "结束",
    color: "#f56c6c",
  },
]);

const filteredNodes = computed(() => {
  if (!searchKeyword.value) {
    return allNodes.value;
  }
  const keyword = searchKeyword.value.toLowerCase();
  return allNodes.value.filter((node) => node.name.toLowerCase().includes(keyword));
});

const getNodeType = (item: BaseNodeType | LoadedNodeType) => {
  if (item.type === "input") return "success";
  if (item.type === "output") return "danger";
  return undefined;
};

const nodeTypesRegistry = ref<Record<string, Component>>({
  input: markRaw(DynamicNode),
  output: markRaw(DynamicNode),
});

const updateState = ref("");
const selectedEdge = ref<Edge>();
const selectedNode = ref<Node>();
const loading = ref(false);

const { saveToHistory } = useWorkflowHistory(50);
const { onDragStart, onDragEnd, onDragOver, onDrop: handleNodeDrop } = useNodeDrag();
const { deleteNode, updateNodeData, deleteEdge, updateEdgeData } = useNodeOperations();

const getNodes = () => getNodesRef.value;
const getEdges = () =>
  getEdgesRef.value.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    label: typeof edge.label === "string" ? edge.label : undefined,
    type: edge.type,
    animated: edge.animated,
    style: edge.style,
    data: edge.data,
  }));

const loadNodeTypes = async () => {
  loading.value = true;
  try {
    const res = await NodeAPI.getNodeTypeOptions();
    if (res.data && res.data.data) {
      const loadedNodesWithColor: (BaseNodeType | LoadedNodeType)[] = res.data.data.map(
        (nodeType: any) => ({
          id: nodeType.id,
          type: nodeType.code,
          name: nodeType.name,
          class: "custom-drag-item",
          color: "#409eff",
        })
      );

      allNodes.value = [...allNodes.value, ...loadedNodesWithColor];

      const newTypes: Record<string, Component> = {};
      res.data.data.forEach((nodeType: any) => {
        newTypes[nodeType.code] = markRaw(DynamicNode);
      });

      nodeTypesRegistry.value = {
        ...nodeTypesRegistry.value,
        ...newTypes,
      };
    }
  } catch {
    ElMessage.error("加载节点类型失败");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadNodeTypes();
});

onInit((vueFlowInstance) => {
  vueFlowInstance.fitView();
  if (workflowId.value) {
    WorkflowAPI.getWorkflowDetail(workflowId.value)
      .then((res) => {
        if (res.data && res.data.data) {
          nodes.value = res.data.data.nodes || [];
          edges.value = res.data.data.edges || [];
          if (nodes.value.length === 0) {
            initializeDefaultNodes();
          }
          saveToHistory(nodes.value as any, edges.value as any);
        }
      })
      .catch(() => {
        ElMessage.error("流程加载失败");
      });
  } else {
    saveToHistory(nodes.value as any, edges.value as any);
  }
});

onConnect((connection) => {
  addEdges(connection);
  saveToHistory(nodes.value as any, edges.value as any);
});

function handleValidate() {
  const errors = [];
  const warnings = [];

  const allNodesList = getNodes();
  const allEdgesList = getEdges();

  if (allNodesList.length === 0) {
    errors.push("流程中没有节点");
  }

  const startNodes = allNodesList.filter((n: Node) => n.type === "input");
  const endNodes = allNodesList.filter((n: Node) => n.type === "output");

  if (startNodes.length === 0) {
    errors.push("流程缺少开始节点");
  } else if (startNodes.length > 1) {
    warnings.push("流程有多个开始节点");
  }

  if (endNodes.length === 0) {
    errors.push("流程缺少结束节点");
  } else if (endNodes.length > 1) {
    warnings.push("流程有多个结束节点");
  }

  const nodeIds = new Set(allNodesList.map((n: Node) => n.id));
  allEdgesList.forEach((edge: Edge) => {
    if (!nodeIds.has(edge.source)) {
      errors.push(`连线 ${edge.label || edge.id} 的源节点不存在`);
    }
    if (!nodeIds.has(edge.target)) {
      errors.push(`连线 ${edge.label || edge.id} 的目标节点不存在`);
    }
  });

  const orphanNodes = allNodesList.filter(
    (node: Node) => !allEdgesList.some((e: Edge) => e.source === node.id || e.target === node.id)
  );

  if (orphanNodes.length > 0) {
    warnings.push(
      `有 ${orphanNodes.length} 个孤立节点: ${orphanNodes.map((n: Node) => n.data.label).join(", ")}`
    );
  }

  if (errors.length > 0) {
    ElMessageBox.alert(
      `<div style="max-height: 300px; overflow-y: auto;">
        <strong>错误 (${errors.length}):</strong>
        <ul>${errors.map((e) => `<li style="color: #f56c6c;">${e}</li>`).join("")}</ul>
        ${
          warnings.length > 0
            ? `<strong>警告 (${warnings.length}):</strong>
        <ul>${warnings.map((w) => `<li style="color: #e6a23c;">${w}</li>`).join("")}</ul>`
            : ""
        }
      </div>`,
      "流程验证结果",
      {
        confirmButtonText: "确定",
        dangerouslyUseHTMLString: true,
      }
    );
    throw new Error("验证失败");
  } else if (warnings.length > 0) {
    ElMessageBox.alert(
      `<div style="max-height: 300px; overflow-y: auto;">
        <strong>流程验证通过，但有警告 (${warnings.length}):</strong>
        <ul>${warnings.map((w) => `<li style="color: #e6a23c;">${w}</li>`).join("")}</ul>
      </div>`,
      "流程验证结果",
      {
        confirmButtonText: "确定",
        dangerouslyUseHTMLString: true,
      }
    );
  }
}

const onEdgeClick = (event: any) => {
  event.event.stopPropagation();
  selectedEdge.value = event.edge;
  updateState.value = "edge";
};

const handleCanvasClick = (event: MouseEvent) => {
  if (
    event.target instanceof HTMLElement &&
    (event.target.classList.contains("vue-flow__node") || event.target.closest(".vue-flow__node"))
  ) {
    return;
  }
  updateState.value = "";
  selectedNode.value = undefined;
  selectedEdge.value = undefined;
};

const onNodeClick = (event: any) => {
  event.event.stopPropagation();
  selectedNode.value = event.node;
  updateState.value = "node";
};

function onDrop(event: DragEvent) {
  handleNodeDrop(event, screenToFlowCoordinate, onNodesInitialized, updateNode, addNodes);
}

function handleClosePanel() {
  updateState.value = "";
  selectedNode.value = undefined;
  selectedEdge.value = undefined;
}

function handleSaveNode(data: any) {
  if (!selectedNode.value) return;
  const nodeId = selectedNode.value!.id;
  if (nodeId && updateNodeData(nodeId, data, getNodes, setNodes)) {
    saveToHistory(nodes.value as any, edges.value as any);
  }
}

function handleDeleteNode() {
  if (!selectedNode.value) return;
  const nodeId = selectedNode.value!.id;
  if (!nodeId) return;

  ElMessageBox.confirm("确定要删除该节点吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    deleteNode(nodeId, getNodes, setNodes, getEdges, setEdges);
    ElMessage.success("节点删除成功");
    handleClosePanel();
    saveToHistory(nodes.value as any, edges.value as any);
  });
}

function handleSaveEdge(data: any) {
  if (!selectedEdge.value) return;
  const edgeId = selectedEdge.value!.id;
  if (edgeId && updateEdgeData(edgeId, data, getEdges, setEdges)) {
    saveToHistory(nodes.value as any, edges.value as any);
  }
}

function handleDeleteEdge() {
  if (!selectedEdge.value) return;
  const edgeId = selectedEdge.value!.id;
  if (!edgeId) return;

  ElMessageBox.confirm("确定要删除该连线吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    deleteEdge(edgeId, getEdges, setEdges);
    ElMessage.success("连线删除成功");
    handleClosePanel();
    saveToHistory(nodes.value as any, edges.value as any);
  });
}

function handleSave() {
  const workflowData = {
    nodes: nodes.value,
    edges: edges.value,
  };

  const saveData = {
    ...formData,
    nodes: workflowData.nodes,
    edges: workflowData.edges,
  };

  if (workflowId.value) {
    return WorkflowAPI.updateWorkflow(workflowId.value, saveData as WorkflowForm);
  } else {
    return WorkflowAPI.createWorkflow(saveData as WorkflowForm).then((res) => {
      if (res.data && res.data.data) {
        workflowId.value = res.data.data.id;
      }
    });
  }
}

function initializeDefaultNodes() {
  nodes.value = [
    {
      id: `node-${Date.now()}`,
      type: "input",
      position: { x: 100, y: 100 },
      data: { label: "开始" },
    },
    {
      id: `node-${Date.now() + 1}`,
      type: "output",
      position: { x: 400, y: 100 },
      data: { label: "结束" },
    },
  ] as Node[];
}

watch(
  () => props.workflow,
  (newWorkflow) => {
    if (newWorkflow) {
      Object.assign(formData, {
        code: newWorkflow.code,
        name: newWorkflow.name,
        category: newWorkflow.category,
        description: newWorkflow.description,
      });
      workflowId.value = newWorkflow.id;
      nodes.value = newWorkflow.nodes || [];
      edges.value = newWorkflow.edges || [];
    } else {
      Object.assign(formData, {
        code: "",
        name: "",
        category: "business",
        description: "",
      });
      workflowId.value = undefined;
      nodes.value = [];
      edges.value = [];
    }
  },
  { immediate: true }
);

const handleFinish = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    await handleValidate();
    await handleSave();
    ElMessage.success("流程保存成功");
    emit("refresh");
    handleClose();
  } catch (error) {
    console.error("保存流程失败", error);
  }
};

const handleClose = () => {
  emit("update:visible", false);
};
</script>

<style scoped lang="scss">
.workflow-drawer {
  :deep(.el-drawer__body) {
    display: flex;
    flex-direction: column;
  }
}

.workflow-create-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

:deep(.el-splitter) {
  flex: 1;
}

:deep(.el-splitter-panel) {
  overflow: hidden;
}

.basic-info-section {
  padding: 12px;

  .section-title {
    margin-bottom: 12px;
    font-size: 14px;
    font-weight: bold;
  }
}

.panel-section {
  padding: 12px;

  .section-title {
    margin-bottom: 12px;
    font-size: 14px;
    font-weight: bold;
  }
}

.search-box {
  margin-bottom: 12px;
}

.canvas-main {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0;
}

.canvas-container {
  flex: 1;
  overflow: hidden;
}

.drawer-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
