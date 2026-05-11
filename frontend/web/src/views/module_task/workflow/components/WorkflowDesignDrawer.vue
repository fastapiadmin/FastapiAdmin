<template>
  <ElDrawer
    v-model="dialogVisible"
    :title="drawerTitle"
    :close-on-click-modal="true"
    size="80%"
    class="workflow-drawer"
    @close="handleClose"
  >
    <ElContainer class="workflow-create-content">
      <ElSplitter direction="horizontal" style="height: 100%">
        <ElSplitterPanel size="250px" :min="200" :max="400">
          <ElScrollbar style="height: 100%">
            <div class="panel-section">
              <div class="section-title">基础信息</div>
              <FaForm
                ref="formRef"
                v-model="formData"
                :items="workflowBaseFormItems"
                :rules="formRules"
                label-width="50px"
                label-position="right"
                size="small"
                :span="24"
                :gutter="12"
                :show-reset="false"
                :show-submit="false"
                class="workflow-base-art-form"
              />
            </div>

            <ElDivider style="margin: 4px 0" />

            <div class="panel-section">
              <div class="section-title">节点</div>
              <ElInput
                v-model="searchKeyword"
                placeholder="搜索节点名称"
                clearable
                size="small"
                class="search-box"
              >
                <template #prefix>
                  <ElIcon><Search /></ElIcon>
                </template>
              </ElInput>
              <ElSpace direction="vertical" :size="8" fill style="width: 100%; margin-top: 8px">
                <ElTag
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
                </ElTag>
              </ElSpace>
            </div>
          </ElScrollbar>
        </ElSplitterPanel>

        <ElSplitterPanel>
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
                  <ElButton
                    class="vue-flow__controls-button"
                    title="格式化画布"
                    :icon="Grid"
                    @click="handleFormatCanvas"
                  />
                  <ElDropdown trigger="click" @command="handleEdgeStyleChange">
                    <ElButton class="vue-flow__controls-button" title="连线样式" :icon="Share" />
                    <template #dropdown>
                      <ElDropdownMenu>
                        <ElDropdownItem
                          command="bezier"
                          :class="{ active: edgeStyle === 'bezier' }"
                        >
                          平滑曲线
                        </ElDropdownItem>
                        <ElDropdownItem
                          command="smoothstep"
                          :class="{ active: edgeStyle === 'smoothstep' }"
                        >
                          阶梯折线
                        </ElDropdownItem>
                        <ElDropdownItem
                          command="straight"
                          :class="{ active: edgeStyle === 'straight' }"
                        >
                          直线
                        </ElDropdownItem>
                      </ElDropdownMenu>
                    </template>
                  </ElDropdown>
                  <ElButton
                    class="vue-flow__controls-button"
                    :title="edgeAnimated ? '关闭动画' : '开启动画'"
                    :icon="VideoPlay"
                    @click="handleEdgeAnimatedChange(!edgeAnimated)"
                  />
                  <ElDropdown trigger="click">
                    <ElButton class="vue-flow__controls-button" title="布局方向">
                      <ElIcon><Rank /></ElIcon>
                    </ElButton>
                    <template #dropdown>
                      <ElDropdownMenu>
                        <ElDropdownItem
                          @click="
                            layoutDirection = 'LR';
                            handleLayout();
                          "
                        >
                          横向布局
                        </ElDropdownItem>
                        <ElDropdownItem
                          @click="
                            layoutDirection = 'TB';
                            handleLayout();
                          "
                        >
                          纵向布局
                        </ElDropdownItem>
                      </ElDropdownMenu>
                    </template>
                  </ElDropdown>
                </Panel>
                <MiniMap pannable zoomable />
              </VueFlow>
            </div>
          </div>
        </ElSplitterPanel>

        <ElSplitterPanel v-if="updateState" size="320px" :min="280" :max="400">
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
        </ElSplitterPanel>
      </ElSplitter>
    </ElContainer>

    <template #footer>
      <div class="drawer-footer">
        <ElButton @click="handleClose">取消</ElButton>
        <ElButton type="primary" @click="handleFinish">保存</ElButton>
      </div>
    </template>
  </ElDrawer>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed, onMounted, markRaw, type Component } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Panel, VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { MiniMap } from "@vue-flow/minimap";
import { Controls } from "@vue-flow/controls";
import type { Node, Edge, DefaultEdgeOptions, MarkerType } from "@vue-flow/core";
import { Search, Share, VideoPlay, Rank, Grid } from "@element-plus/icons-vue";
import dagre from "dagre";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import "@vue-flow/minimap/dist/style.css";
import "element-plus/dist/index.css";

import DynamicNode from "./DynamicNode.vue";
import NodeConfigPanel from "./NodeConfigPanel.vue";
import EdgeConfigPanel from "./EdgeConfigPanel.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import WorkflowDefinitionAPI, {
  type WorkflowTable,
  type WorkflowForm,
} from "@/api/module_task/workflow/definition";
import WorkflowNodeTypeAPI from "@/api/module_task/workflow/node-type";

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

const formRef = ref<InstanceType<typeof FaForm> | null>(null);
const workflowId = ref<number>();

const formData = ref<Partial<WorkflowForm>>({
  code: "",
  name: "",
  description: "",
});

const formRules = {
  code: [{ required: true, message: "请输入流程编码", trigger: "blur" }],
  name: [{ required: true, message: "请输入流程名称", trigger: "blur" }],
};

const workflowBaseFormItems = computed<FormItem[]>(() => [
  {
    label: "编码",
    key: "code",
    type: "input",
    span: 24,
    props: { placeholder: "请输入流程编码" },
  },
  {
    label: "名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入流程名称" },
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 2,
      placeholder: "请输入流程描述",
    },
  },
]);

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

const handleFormatCanvas = () => {
  const currentNodes = getNodesRef.value;
  const currentEdges = getEdgesRef.value;

  if (currentNodes.length === 0) {
    ElMessage.warning("画布中没有节点，无法格式化");
    return;
  }

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  const nodeWidth = 180;
  const nodeHeight = 60;

  dagreGraph.setGraph({
    rankdir: layoutDirection.value,
    nodesep: 100,
    ranksep: 150,
    marginx: 80,
    marginy: 80,
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
  ElMessage.success("画布格式化完成");
};

const nodes = ref<Node[]>([]);
const edges = ref<Edge[]>([]);

const searchKeyword = ref("");

type LoadedNodeType = {
  id: number;
  type: string;
  name: string;
  category: string;
  args?: string;
  kwargs?: string;
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
    action: "primary",
    condition: "success",
    control: "info",
  };
  return typeMap[category] || "info";
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
    const res = await WorkflowNodeTypeAPI.getWorkflowNodeTypeOptions();
    if (res.data && res.data.data) {
      allNodes.value = res.data.data.map((nodeType: any) => ({
        id: nodeType.id,
        type: nodeType.code,
        name: nodeType.name,
        category: nodeType.category || "action",
        args: nodeType.args || "",
        kwargs: nodeType.kwargs || "{}",
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
    WorkflowDefinitionAPI.getWorkflowDetail(workflowId.value)
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
    return WorkflowDefinitionAPI.updateWorkflow(workflowId.value, saveData as WorkflowForm);
  } else {
    return WorkflowDefinitionAPI.createWorkflow(saveData as WorkflowForm).then((res) => {
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
        description: newWorkflow.description,
      });
      workflowId.value = newWorkflow.id;
      nodes.value = newWorkflow.nodes || [];
      edges.value = newWorkflow.edges || [];
    } else {
      Object.assign(formData, {
        code: "",
        name: "",
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
    await formRef.value.validate?.();
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

// 历史记录管理
const history = ref<{ nodes: Node[]; edges: Edge[] }[]>([]);
const historyIndex = ref(-1);

function saveToHistory(nodesData: Node[], edgesData: Edge[]) {
  history.value = history.value.slice(0, historyIndex.value + 1);
  history.value.push({ nodes: nodesData, edges: edgesData });
  historyIndex.value = history.value.length - 1;
}

// 拖拽相关函数
function onDragStart(event: DragEvent, node: LoadedNodeType) {
  if (event.dataTransfer) {
    event.dataTransfer.setData("application/vueflow", JSON.stringify(node));
    event.dataTransfer.effectAllowed = "move";
  }
}

function onDragEnd() {
  // 拖拽结束
}

function onDragOver(event: DragEvent) {
  event.preventDefault();
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = "move";
  }
}

function handleNodeDrop(
  event: DragEvent,
  screenToFlowCoordinate: (position: { x: number; y: number }) => { x: number; y: number },
  onNodesInitialized: (callback: () => void) => void,
  updateNode: (id: string, node: Partial<Node>) => void,
  addNodes: (nodes: Node[]) => void
) {
  const data = event.dataTransfer?.getData("application/vueflow");
  if (!data) return;

  const nodeType = JSON.parse(data);
  const position = screenToFlowCoordinate({ x: event.clientX, y: event.clientY });

  const newNode: Node = {
    id: `node-${Date.now()}`,
    type: nodeType.type,
    position,
    data: {
      label: nodeType.name,
      type: nodeType.type,
      category: nodeType.category,
      args: nodeType.args,
      kwargs: nodeType.kwargs,
    },
  };

  addNodes([newNode]);
}

// 节点操作函数
function updateNodeData(
  nodeId: string,
  data: any,
  getNodes: () => Node[],
  setNodes: (nodes: Node[]) => void
) {
  const currentNodes = getNodes();
  const nodeIndex = currentNodes.findIndex((n) => n.id === nodeId);
  if (nodeIndex === -1) return false;

  const updatedNodes = [...currentNodes];
  updatedNodes[nodeIndex] = {
    ...updatedNodes[nodeIndex],
    data: {
      ...updatedNodes[nodeIndex].data,
      ...data,
    },
  };
  setNodes(updatedNodes);
  return true;
}

function deleteNode(
  nodeId: string,
  getNodes: () => Node[],
  setNodes: (nodes: Node[]) => void,
  getEdges: () => Edge[],
  setEdges: (edges: Edge[]) => void
) {
  const currentNodes = getNodes();
  const currentEdges = getEdges();
  const filteredNodes = currentNodes.filter((n) => n.id !== nodeId);
  const filteredEdges = currentEdges.filter((e) => e.source !== nodeId && e.target !== nodeId);
  setNodes(filteredNodes);
  setEdges(filteredEdges);
}

// 边操作函数
function updateEdgeData(
  edgeId: string,
  data: any,
  getEdges: () => Edge[],
  setEdges: (edges: Edge[]) => void
) {
  const currentEdges = getEdges();
  const edgeIndex = currentEdges.findIndex((e) => e.id === edgeId);
  if (edgeIndex === -1) return false;

  const updatedEdges = [...currentEdges];
  updatedEdges[edgeIndex] = {
    ...updatedEdges[edgeIndex],
    ...data,
    data: {
      ...updatedEdges[edgeIndex].data,
      ...data,
    },
  };
  setEdges(updatedEdges);
  return true;
}

function deleteEdge(edgeId: string, getEdges: () => Edge[], setEdges: (edges: Edge[]) => void) {
  const currentEdges = getEdges();
  const filteredEdges = currentEdges.filter((e) => e.id !== edgeId);
  setEdges(filteredEdges);
}
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
  box-shadow: 0 2px 8px rgb(0 0 0 / 10%);
}

.drawer-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.workflow-base-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.workflow-base-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

.workflow-base-art-form :deep(section) {
  padding: 0;
}
</style>
