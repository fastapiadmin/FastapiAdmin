<template>
  <div class="flex flex-col h-full">
    <div
      class="flex items-center justify-between px-4 py-3 font-semibold border-b border-(--el-border-color-lighter)"
    >
      <span>连线配置</span>
      <ElButton type="text" class="p-1" @click="handleClose">
        <ElIcon><Close /></ElIcon>
      </ElButton>
    </div>

    <ElScrollbar class="flex-1" view-class="p-4">
      <FaForm
        v-model="formData"
        :items="edgeFormItems"
        label-width="80px"
        size="small"
        label-position="right"
        :span="24"
        :gutter="12"
        :show-reset="false"
        :show-submit="false"
        class="panel-art-form"
      >
        <template #color>
          <ElColorPicker v-model="formData.color" />
        </template>
      </FaForm>

      <div
        class="flex gap-2 pt-4 border-t border-(--el-border-color-lighter) [&_.el-button]:flex-1"
      >
        <ElButton type="primary" size="small" @click="handleSave">保存</ElButton>
        <ElButton type="danger" size="small" @click="handleDelete">删除连线</ElButton>
      </div>
    </ElScrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";

import { Close } from "@element-plus/icons-vue";
import FaForm from "@/components/forms/fa-form/index.vue";

interface Props {
  edge?: Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
  edge: () => ({}),
});

const emit = defineEmits(["close", "save", "delete"]);

const formData = ref({
  label: props.edge?.label || "",
  type: props.edge?.type || "smoothstep",
  color: props.edge?.style?.stroke || "#000000",
  strokeWidth: props.edge?.style?.strokeWidth || 2,
  animated: props.edge?.animated || false,
  condition: props.edge?.data?.condition || "",
  description: props.edge?.data?.description || "",
});

const edgeFormItems = computed(() => [
  {
    label: "连线名称",
    key: "label",
    type: "input",
    span: 24,
    props: { placeholder: "请输入连线名称" },
  },
  {
    label: "连线类型",
    key: "type",
    type: "select",
    span: 24,
    props: {
      placeholder: "请选择连线类型",
      options: [
        { label: "折线", value: "smoothstep" },
        { label: "曲线", value: "default" },
        { label: "直线", value: "straight" },
      ],
    },
  },
  {
    label: "连线颜色",
    key: "color",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "线条宽度",
    key: "strokeWidth",
    type: "number",
    span: 24,
    props: { min: 1, max: 10 },
  },
  {
    label: "启用动画",
    key: "animated",
    type: "switch",
    span: 24,
  },
  {
    label: "条件表达式",
    key: "condition",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 3,
      placeholder: "请输入条件表达式",
    },
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 2,
      placeholder: "请输入描述信息",
    },
  },
]);

watch(
  () => props.edge,
  (newEdge) => {
    if (newEdge) {
      formData.value = {
        label: newEdge.label || "",
        type: newEdge.type || "smoothstep",
        color: newEdge.style?.stroke || "#000000",
        strokeWidth: newEdge.style?.strokeWidth || 2,
        animated: newEdge.animated || false,
        condition: newEdge.data?.condition || "",
        description: newEdge.data?.description || "",
      };
    }
  },
  { deep: true }
);

function handleClose() {
  emit("close");
}

function handleSave() {
  emit("save", formData.value);
}

function handleDelete() {
  emit("delete");
}
</script>

<style scoped lang="scss">
.panel-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.panel-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}

.panel-art-form :deep(section) {
  padding: 0;
}
</style>
