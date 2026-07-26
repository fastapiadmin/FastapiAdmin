<template>
  <div class="param-fields-wrap max-w-180">
    <ElButton v-if="modified" type="primary" size="small" @click="$emit('saveGroup')">
      {{ saveText || `保存${title}` }}
    </ElButton>
    <div class="space-y-4">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "ParamTabPane" });

interface Props {
  title: string;
  modified: boolean;
  saveText?: string;
}

withDefaults(defineProps<Props>(), {
  saveText: "",
});

interface Emits {
  (e: "saveGroup"): void;
}

defineEmits<Emits>();
</script>
