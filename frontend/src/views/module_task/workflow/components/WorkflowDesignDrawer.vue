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
            <div class="panel-section">
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
                  :key="item.id"
                  :type="getCategoryType(item.category) as any"
                  effect="plain"
                  draggable="true"
                  style="justify-content: center; cursor: move; user-select: none"
                  @dragstart="onDragStart($event, item)"
                  @dragend="onDragEnd"
                >
                  {{ item.name }}
                  <span style="margin-left: 4px; font-size: 10px; opacity: 0.7">
                    [{{ getCategoryText(item.category) }}]
                  </span>
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
                <Panel position="top-right" class="workflow-toolbar">
                  <el-dropdown trigger="click" @command="handleEdgeStyleChange">
                    <el-button class="vue-flow__controls-button" title="连线样式" :icon="Share" />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item
                          command="bezier"
                          :class="{ active: edgeStyle === 'bezier' }"
                        >
                          平滑曲线
                        </el-dropdown-item>
                        <el-dropdown-item
                          command="smoothstep"
                          :class="{ active: edgeStyle === 'smoothstep' }"
                        >
                          阶梯折线
                        </el-dropdown-item>
                        <el-dropdown-item
                          command="straight"
                          :class="{ active: edgeStyle === 'straight' }"
                        >
                          直线
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  <el-button
                    class="vue-flow__controls-button"
                    :title="edgeAnimated ? '关闭动画' : '开启动画'"
                    :icon="VideoPlay"
                    @click="handleEdgeAnimatedChange(!edgeAnimated)"
                  />
                  <el-dropdown trigger="click">
                    <el-button class="vue-flow__controls-button" title="布局">
                      <el-icon><Rank /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item
                          @click="
                            layoutDirection = 'LR';
                            handleLayout();
                          "
                        >
                          横向布局
                        </el-dropdown-item>
                        <el-dropdown-item
                          @click="
                            layoutDirection = 'TB';
                            handleLayout();
                          "
                        >
                          纵向布局
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </Panel>
                <MiniMap pannable zoomable />
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
import { Panel, VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { MiniMap } from "@vue-flow/minimap";
import { Controls } from "@vue-flow/controls";
import { Search, Share, VideoPlay, Rank } from "@element-plus/icons-vue";
import type { Node, Edge, DefaultEdgeOptions, MarkerType } from "@vue-flow/core";
import dagre from "dagre";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "@vue-flow/minimap/dist/style.css";
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

const edgeStyle = ref<string>("smoothstep");
const edgeAnimated = ref<boolean>(true);

const handleEdgeStyleChange = (value: string) => {
  edgeStyle.value = value;
  defaultEdgeOptions.type = value;
  setEdges(
    getEdgesRef.value.map((edge) => ({
      ...edge,
      type: value,
    }))
  );
};

const handleEdgeAnimatedChange = (value: boolean) => {
  edgeAnimated.value = value;
  defaultEdgeOptions.animated = value;
  setEdges(
    getEdgesRef.value.map((edge) => ({
      ...edge,
      animated: value,
    }))
  );
};

const layoutDirection = ref<"LR" | "TB">("LR");

const handleLayout = () => {
  const currentNodes = getNodesRef.value;
  const currentEdges = getEdgesRef.value;

  if (currentNodes.length === 0) {
    ElMessage.warning("画布中没有节点，无法布局");
    return;
  }

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  const nodeWidth = 180;
  const nodeHeight = 60;

  dagreGraph.setGraph({
    rankdir: layoutDirection.value,
    nodesep: 80,
    ranksep: 120,
    marginx: 50,
    marginy: 50,
  });

  currentNodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  currentEdges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = currentNodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });

  setNodes(layoutedNodes);
  setEdges(
    currentEdges.map((edge) => ({
      ...edge,
      type: edgeStyle.value,
      animated: edgeAnimated.value,
    }))
  );
  ElMessage.success("画布布局完成");
};

const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);

const searchKeyword = ref("");

type LoadedNodeType = {
  id: number;
  type: string;
  name: string;
  category: string;
};

const allNodes = ref<LoadedNodeType[]>([]);

const filteredNodes = computed(() => {
  if (!searchKeyword.value) {
    return allNodes.value;
  }
  const keyword = searchKeyword.value.toLowerCase();
  return allNodes.value.filter((node) => node.name.toLowerCase().includes(keyword));
});

const getCategoryType = (category: string) => {
  const typeMap: Record<string, string> = {
    trigger: "warning",
    action: "",
    condition: "success",
    control: "info",
  };
  return typeMap[category] || "";
};

const getCategoryText = (category: string) => {
  const textMap: Record<string, string> = {
    trigger: "触发器",
    action: "动作",
    condition: "条件",
    control: "控制",
  };
  return textMap[category] || category;
};

const nodeTypesRegistry = ref<Record<string, Component>>({});

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
      allNodes.value = res.data.data.map((nodeType: any) => ({
        id: nodeType.id,
        type: nodeType.code,
        name: nodeType.name,
        category: nodeType.category || "action",
      }));

      const newTypes: Record<string, Component> = {};
      res.data.data.forEach((nodeType: any) => {
        newTypes[nodeType.code] = markRaw(DynamicNode);
      });

      nodeTypesRegistry.value = newTypes;
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
  addEdges({
    ...connection,
    type: edgeStyle.value,
    animated: edgeAnimated.value,
  });
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

:deep(.vue-flow__controls) {
  display: flex;
  flex-direction: column;
}

:deep(.vue-flow__controls-button) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  color: #000;
  cursor: pointer;
  border: none;
}

:deep(.el-dropdown) {
  display: flex;
}

.workflow-toolbar {
  display: flex;
  gap: 4px;
  padding: 8px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.drawer-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
