<template>
  <div class="dynamic-node" :class="nodeClass">
    <div class="node-content">
      <span class="node-label">{{ data.label }}</span>
    </div>
    <Handle
      v-if="nodeType.code !== 'input'"
      :id="'top-' + id"
      type="target"
      position="top"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'input'"
      :id="'left-' + id"
      type="target"
      position="left"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'output'"
      :id="'right-' + id"
      type="source"
      position="right"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'output'"
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Handle } from "@vue-flow/core";

const props = defineProps({
  id: String,
  data: Object,
  nodeStatus: String,
});

const nodeType = computed(() => {
  if (props.data?.type === "input") {
    return {
      code: "input",
      name: "开始",
      color: "#67c23a",
    };
  }
  if (props.data?.type === "output") {
    return {
      code: "output",
      name: "结束",
      color: "#f56c6c",
    };
  }
  return {
    code: "custom",
    name: "自定义节点",
    color: "#409EFF",
  };
});

const nodeClass = computed(() => {
  if (props.data?.type === "input") {
    return "start-node";
  }
  if (props.data?.type === "output") {
    return "end-node";
  }
  return "custom-node";
});
</script>

<style lang="scss">
.vue-flow__node-input {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 80px !important;
  height: 80px !important;
  padding: 0 !important;
  color: #ffffff !important;
  cursor: pointer !important;
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%) !important;
  border: 3px solid #5daf34 !important;
  border-radius: 50% !important;
  box-shadow:
    0 6px 12px rgba(103, 194, 58, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.vue-flow__node-output {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 80px !important;
  height: 80px !important;
  padding: 0 !important;
  color: #ffffff !important;
  cursor: pointer !important;
  background: linear-gradient(135deg, #f56c6c 0%, #e04e4e 100%) !important;
  border: 3px solid #e04e4e !important;
  border-radius: 50% !important;
  box-shadow:
    0 6px 12px rgba(245, 108, 108, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.dynamic-node {
  padding: 12px 16px;
  cursor: pointer;
  border: 2px solid #409eff;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.vue-flow__node-input .dynamic-node,
.vue-flow__node-output .dynamic-node {
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  box-shadow: none;
}

.node-content {
  display: flex;
  gap: 8px;
  align-items: center;
}

.node-label {
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  letter-spacing: 0.5px;
}
</style>
