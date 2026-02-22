<template>
  <div class="json-pretty-wrapper" :style="{ maxHeight: height }">
    <VueJsonPretty
      v-if="isJson"
      :data="parsed"
      :show-line="true"
      :show-icon="true"
      :show-double-quotes="false"
      :show-length="true"
      :deep="3"
    />
    <pre v-else class="json-pretty-fallback">{{ displayText }}</pre>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

const props = defineProps({
  value: { type: [String, Object, Array, Number, Boolean], default: "" },
  height: { type: String, default: "240px" },
});

const parsed = computed(() => {
  const v: any = props.value;
  if (typeof v === "string") {
    try {
      return JSON.parse(v);
    } catch {
      return v; // 非 JSON 字符串，原样展示
    }
  }
  return v;
});

const isJson = computed(() => typeof parsed.value === "object" && parsed.value !== null);
const displayText = computed(() => {
  const v: any = props.value;
  return typeof v === "string" ? v : JSON.stringify(v, null, 2);
});
</script>

<style scoped>
.json-pretty-wrapper {
  padding: 8px;
  overflow: auto;
  background-color: var(--el-fill-color-blank);
  border: 1px solid #e5e7eb;
  border-radius: 4px;
}

.json-pretty-fallback {
  margin: 0;
  font-family:
    ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New",
    monospace;
  font-size: 12px;
  word-break: break-all;
  white-space: pre-wrap;
}
</style>
