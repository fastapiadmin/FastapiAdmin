<template>
  <div
    class="flex items-start gap-4 p-4 rounded-lg border bg-(--el-fill-color-blank) transition-shadow duration-200 hover:shadow-[0_2px_8px_rgb(0_0_0/6%)]"
    :class="modified ? 'border-(--el-color-primary)!' : 'border-(--el-border-color-light)'"
  >
    <div
      class="param-field-label w-28 shrink-0 text-sm font-medium leading-9 text-right text-(--el-text-color-regular)"
    >
      {{ label }}
      <ElTag v-if="modified" size="small" type="warning" class="ml-0.5">已修改</ElTag>
    </div>
    <div class="param-field-control flex-1 min-w-0">
      <slot />
    </div>
    <div class="param-field-actions shrink-0 flex flex-col gap-2">
      <ElButton text size="small" :disabled="!modified" @click="$emit('save')">
        <FaSvgIcon icon="ri:save-line" class="mr-0.5" />
        保存
      </ElButton>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "ParamFieldCard" });

interface Props {
  label: string;
  modified: boolean;
}

defineProps<Props>();

interface Emits {
  (e: "save"): void;
}

defineEmits<Emits>();
</script>
