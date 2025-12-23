<template>
  <div class="custom-node">
    <div class="node-header">{{ data.label }}</div>

    <!-- Handle 定义 -->
    <Handle :id="'top-' + id" type="source" position="top" :style="{ background: '#4a5568' }" />
    <Handle :id="'left-' + id" type="source" position="left" :style="{ background: '#4a5568' }" />
    <Handle :id="'right-' + id" type="source" position="right" :style="{ background: '#4a5568' }" />
    <Handle
      :id="'bottom-' + id"
      type="source"
      position="bottom"
      :style="{ background: '#4a5568' }"
    />
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import { Handle } from "@vue-flow/core";

defineProps({
  id: String,
  data: Object,
});
</script>

<style scoped>
.custom-node {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 40px;
  color: white;
  background-color: #4a5568;
  background-color: rgba(148, 146, 146, 0.32);
  border: 1px solid rgba(148, 146, 146, 0.79);
  border-radius: 3px;
}

.node-header {
  font-size: 14px;
  font-weight: bold;
}
</style>
