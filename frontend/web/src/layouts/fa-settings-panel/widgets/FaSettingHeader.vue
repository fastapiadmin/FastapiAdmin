<template>
  <div>
    <div class="flex justify-end">
      <div
        @click="$emit('close')"
        class="flex items-center justify-center cursor-pointer size-7.5 transition-all! duration-200 rounded hover:bg-g-300/80"
      >
        <FaSvgIcon icon="ri:close-fill" class="block text-xl text-g-600" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaSettingHeader" });

interface Emits {
  close: [];
}

defineEmits<Emits>();
</script>
