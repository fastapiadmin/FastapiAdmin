<template>
  <div class="app-container">
    <div class="top-toolbar">
      <div class="toolbar-right" style="margin-left: auto">
        <ElButton type="primary" class="m-2">保存</ElButton>
      </div>
    </div>
    <div class="main-layout">
      <div class="left-panel">
        <!-- 可拖拽的元素 -->
        <div class="flex-center">
          <div
            class="drag-item text-center start-item"
            draggable="true"
            @dragstart="onDragStart($event, '开始')"
            @dragend="onDragEnd"
          >
            <span>开始</span>
          </div>
          <div
            class="drag-item text-center end-item ml-2"
            draggable="true"
            @dragstart="onDragStart($event, '结束')"
            @dragend="onDragEnd"
          >
            <span>结束</span>
          </div>
        </div>
        <div class="scroll-container" style="height: calc(100% - 50px)">
          <div
            v-for="(item, index) in pointsList"
            :key="index"
            class="drag-item text-center w-full mt-2"
            draggable="true"
            @dragstart="onDragStart($event, item.name)"
            @dragend="onDragEnd"
          >
            <span>{{ item.name }}</span>
          </div>
        </div>
      </div>
      <div class="canvas-container">
        <VueFlow
          :nodes="nodes"
          :edges="edges"
          class="basic-flow"
          :default-viewport="{ zoom: 1 }"
          :min-zoom="0.2"
          :max-zoom="4"
          :node-types="nodeTypes"
          :default-edge-options="defaultEdgeOptions"
          :connect-on-click="true"
          @node-click="onNodeClick"
          @edge-click="onEdgeClick"
          @drop="onDrop"
          @dragover="onDragOver"
        >
          <Controls />
          <Background pattern-color="#aaa" :gap="16" />
          <MiniMap />
        </VueFlow>
      </div>
      <div v-if="updateState" class="right-panel">
        <div class="panel-header">
          <span>{{ updateState === "edge" ? "连接线规则配置" : "点位规则配置" }}</span>
          <ElButton type="text" class="float-right" icon="close" @click="updateState = ''" />
        </div>
        <div v-if="updateState === 'edge'" class="gap-y-2">
          <ElInput v-model="selectedEdge.label" placeholder="线名称" clearable class="mb-2" />
          <ElSelect v-model="selectedEdge.type" placeholder="线类型" class="mb-2">
            <ElOption label="折线" value="smoothstep" />
            <ElOption label="曲线" value="default" />
            <ElOption label="直线" value="straight" />
          </ElSelect>
          <ElSelect v-model="selectedEdge.animated" placeholder="线动画" class="mb-2">
            <ElOption label="开启" :value="true" />
            <ElOption label="关闭" :value="null" />
          </ElSelect>
          <ElButton type="primary" size="small" @click="updateEdge">修改</ElButton>
          <ElButton type="danger" size="small" @click="removeEdge">删除</ElButton>
        </div>
        <div v-else class="gap-y-2">
          <ElInput
            v-model="selectedNode.data.label"
            placeholder="点位名称"
            clearable
            class="mb-2"
          />
          <ElButton type="danger" size="small" @click="removeNode">删除</ElButton>
        </div>
      </div>
    </div>
    <!-- 删除连线对话框 -->
    <ElDialog v-model="removeEdgeDialogVisible" title="删除连线" width="30%">
      <span>是否要删除该连线？</span>
      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="removeEdgeDialogVisible = false">取消</ElButton>
          <ElButton type="danger" @click="confirmRemoveEdge">确定</ElButton>
        </div>
      </template>
    </ElDialog>

    <!-- 删除点位对话框 -->
    <ElDialog v-model="removeNodeDialogVisible" title="删除点位" width="30%">
      <span>是否要删除该点位？</span>
      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="removeNodeDialogVisible = false">取消</ElButton>
          <ElButton type="danger" @click="confirmRemoveNode">确定</ElButton>
        </div>
      </template>
    </ElDialog>
  </div>
</template>

<script setup>
defineOptions({
  name: "Workflow",
  inheritAttrs: false,
});
import { ref, markRaw } from "vue";
import { VueFlow, useVueFlow, MarkerType } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import { Controls } from "@vue-flow/controls";
import { MiniMap } from "@vue-flow/minimap";
import "@vue-flow/core/dist/style.css";
import "@vue-flow/core/dist/theme-default.css";
import "@vue-flow/controls/dist/style.css";
import CustomNode from "./CustomNode.vue";
import { ElButton, ElInput, ElSelect, ElOption, ElDialog, ElMessage } from "element-plus";
import "element-plus/dist/index.css";
const {
  onInit,
  onNodeDragStop,
  onConnect,
  addEdges,
  getNodes,
  getEdges,
  setEdges,
  setNodes,
  screenToFlowCoordinate,
  onNodesInitialized,
  updateNode,
  addNodes,
} = useVueFlow();
// 默认连线配置
const defaultEdgeOptions = {
  type: "smoothstep", // 默认边类型
  animated: true, // 是否启用动画
  markerEnd: {
    type: "arrowclosed", // 默认箭头样式
    color: "black",
  },
};
// 节点
const nodes = ref([
  {
    id: "5",
    type: "input",
    data: { label: "开始" },
    position: { x: 235, y: 100 },
    class: "round-start",
  },
  {
    id: "6",
    type: "custom", // 使用自定义类型
    data: { label: "工位：流程1" },
    position: { x: 200, y: 200 },
    class: "light",
  },
  {
    id: "7",
    type: "output",
    data: { label: "结束" },
    position: { x: 235, y: 300 },
    class: "round-stop",
  },
]);
const nodeTypes = ref({
  custom: markRaw(CustomNode), // 注册自定义节点类型
});
// 线
const edges = ref([
  {
    id: "e4-5",
    type: "straight",
    source: "5",
    target: "6",
    sourceHandle: "top-6",
    label: "测试1",
    markerEnd: {
      type: MarkerType.ArrowClosed, // 使用闭合箭头
      color: "black",
    },
  },
  {
    id: "e4-6",
    type: "straight",
    source: "6",
    target: "7",
    sourceHandle: "bottom-6",
    label: "测试2",
    markerEnd: {
      type: MarkerType.ArrowClosed, // 使用闭合箭头
      color: "black",
    },
  },
]);
onInit((vueFlowInstance) => {
  vueFlowInstance.fitView();
});

onNodeDragStop(({ event, nodes, node }) => {
  console.log("Node Drag Stop", { event, nodes, node });
});

onConnect((connection) => {
  addEdges(connection);
});
// -----------------------------------------------
// 拖动块
const pointsList = ref([{ name: "测试1" }, { name: "测试2" }]);
// --------------------------------------------------------------
const updateState = ref("");
const selectedEdge = ref({}); // 存储选中的边
const removeEdgeDialogVisible = ref(false);
const removeNodeDialogVisible = ref(false);
const onEdgeClick = ({ edge }) => {
  selectedEdge.value = edge; // 选中边
  updateState.value = "edge";
  console.log(selectedEdge.value);
};
function updateEdge() {
  // 获取当前所有的边
  const allEdges = getEdges.value;
  // 切换边类型：根据当前类型来切换
  const newType = selectedEdge.value.type === "smoothstep" ? null : "smoothstep";
  // 更新选中边的类型
  setEdges([
    ...allEdges.filter((e) => e.id !== selectedEdge.value.id), // 移除旧的边
    { ...selectedEdge.value, type: newType, label: "Node 3" }, // 更新边的类型
  ]);
}
function removeEdge() {
  removeEdgeDialogVisible.value = true;
}

function confirmRemoveEdge() {
  // 获取当前所有的边
  const allEdges = getEdges.value;
  // 更新选中边的类型
  setEdges([
    ...allEdges.filter((e) => e.id !== selectedEdge.value.id), // 移除边
  ]);
  ElMessage.success("连线删除成功");
  updateState.value = null;
  selectedEdge.value = {};
  removeEdgeDialogVisible.value = false;
}

const selectedNode = ref({}); // 存储选中的节点
const onNodeClick = ({ node }) => {
  selectedNode.value = node; // 更新选中的节点
  updateState.value = "node";
  console.log("选中的节点：", node);
};

function removeNode() {
  removeNodeDialogVisible.value = true;
}

function confirmRemoveNode() {
  // 获取当前所有的边
  const allNodes = getNodes.value;
  // 更新选中边的类型
  setNodes([
    ...allNodes.filter((e) => e.id !== selectedNode.value.id), // 移除边
  ]);
  // 获取当前所有的边
  const allEdges = getEdges.value;
  setEdges([
    ...allEdges.filter(
      (e) => e.source !== selectedNode.value.id && e.target !== selectedNode.value.id
    ), // 移除边
  ]);
  ElMessage.success("点位删除成功");
  updateState.value = null;
  selectedNode.value = {};
  console.log(getEdges.value);
  removeNodeDialogVisible.value = false;
}

// 拖拽相关状态
const dragItem = ref(null);
// 拖拽开始时设置拖拽的元素
function onDragStart(event, state) {
  dragItem.value = {
    id: `node-${Date.now()}`, // 动态生成唯一 id
    data: { label: state === "开始" ? "开始" : state === "结束" ? "结束" : "工位：" + state },
    type: state === "开始" ? "input" : state === "结束" ? "output" : "custom",
    position: { x: event.clientX, y: event.clientY },
    animated: false,
    class: state === "开始" ? "round-start" : state === "结束" ? "round-stop" : "light",
  };
}

// 拖拽结束时清除状态
function onDragEnd() {
  dragItem.value = null;
}

// 拖拽目标画布区域时允许放置
function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  const position = screenToFlowCoordinate({
    x: event.clientX,
    y: event.clientY,
  });

  const newNode = {
    ...dragItem.value,
    position,
  };
  const { off } = onNodesInitialized(() => {
    updateNode(dragItem.value?.id, (node) => ({
      position: {
        x: node.position.x - node.dimensions.width / 2,
        y: node.position.y - node.dimensions.height / 2,
      },
    }));

    off();
  });

  // 更新节点数据
  // nodes.value.push(newNode)
  dragItem.value = null;
  addNodes(newNode);
}
</script>
<style>
/* 顶部工具栏 */
.top-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.2rem;
  padding: 0 10px;
  border-bottom: 1px solid rgba(161, 158, 158, 0.3);
  border-left: 1px solid rgba(161, 158, 158, 0.3);
}

/* 主要布局容器 */
.main-layout {
  display: flex;
  flex: 1;
  height: calc(100vh - 3.2rem);
}

/* 左侧面板 */
.left-panel {
  z-index: 988;
  width: 13rem;
  padding: 10px;
  background-color: rgba(122, 122, 122, 0.1);
  border-right: 1px solid rgba(161, 158, 158, 0.3);
  border-left: 1px solid rgba(161, 158, 158, 0.3);
  border-radius: 3px;
}

/* 画布容器 */
.canvas-container {
  position: relative;
  flex: 1;
  overflow: hidden;
}

/* 右侧面板 */
.right-panel {
  z-index: 988;
  width: 13rem;
  padding: 10px;
  background-color: rgba(122, 122, 122, 0.1);
  border-left: 1px solid rgba(161, 158, 158, 0.3);
  border-radius: 3px;
}

/* 画布样式 */
.basic-flow {
  width: 100%;
  height: 100%;
}

.round-start {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  color: white;
  text-align: center;
  background-color: rgba(0, 128, 0, 0.6);
  border: 0;
  border-radius: 50%;
}
.round-stop {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  color: white;
  text-align: center;
  background-color: rgba(255, 0, 0, 0.6);
  border: 0;
  border-radius: 50%;
}

/* 可拖拽的元素样式 */
.drag-item {
  padding: 5px;
  background-color: #4a5568;
  border-radius: 5px;
}

/* 开始和结束拖拽元素的样式 */
.start-item {
  background-color: rgba(0, 128, 0, 0.6) !important;
}

.end-item {
  background-color: rgba(255, 0, 0, 0.6) !important;
}

.module-top .vue-flow__controls .vue-flow__controls-button {
  cursor: pointer;
  background-color: rgba(182, 181, 181, 0);
  border: none;
}
.module-top .vue-flow__controls .vue-flow__controls-button svg {
  width: 1.5rem;
  height: 1.5rem;
  padding-top: 2px;
  padding-left: -1px;
  margin-top: 2px;
}

.scroll-container {
  overflow-x: hidden;
  overflow-y: auto;
}

/* 面板头部 */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 5px;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(161, 158, 158, 0.3);
}
</style>
