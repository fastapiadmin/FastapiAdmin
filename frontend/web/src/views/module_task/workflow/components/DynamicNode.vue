<template>
  <div
    class="dynamic-node"
    :class="nodeClass"
    @mouseenter="showHandles = true"
    @mouseleave="showHandles = false"
  >
    <div class="node-content">
      <span class="node-label">{{ data.label }}</span>
      <span v-if="data.config && Object.keys(data.config).length > 0" class="node-badge">
        {{ Object.keys(data.config).length }}
      </span>
    </div>
    <Handle
      v-if="nodeType.code !== 'input'"
      :id="'top-' + id"
      type="target"
      position="top"
      :class="{ 'handle-visible': showHandles }"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'input'"
      :id="'left-' + id"
      type="target"
      position="left"
      :class="{ 'handle-visible': showHandles }"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'output'"
      :id="'right-' + id"
      type="source"
      position="right"
      :class="{ 'handle-visible': showHandles }"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
    <Handle
      v-if="nodeType.code !== 'output'"
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :class="{ 'handle-visible': showHandles }"
      :style="{ background: nodeType.color || '#3b82f6' }"
    />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { Handle } from "@vue-flow/core";

const props = defineProps({
  id: String,
  data: Object,
  nodeStatus: String,
});

const showHandles = ref(false);

const nodeType = computed(() => {
  return {
    code: props.data?.type || "custom",
    name: props.data?.label || "自定义节点",
    color: getCategoryColor(props.data?.category),
  };
});

function getCategoryColor(category) {
  const colorMap = {
    trigger: "#e6a23c",
    action: "#409eff",
    condition: "#67c23a",
    control: "#909399",
  };
  return colorMap[category] || "#409eff";
}

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

.node-badge {
  padding: 0 6px;
  font-size: 10px;
  font-weight: 500;
  color: #fff;
  background: #409eff;
  border-radius: 10px;
}

.vue-flow__handle {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.vue-flow__handle.handle-visible,
.vue-flow__handle.vue-flow__handle-connecting,
.vue-flow__handle.vue-flow__handle-valid {
  opacity: 1;
}
</style>
