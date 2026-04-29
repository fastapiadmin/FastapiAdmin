<!-- 折叠按钮 -->
<template>
  <div class="hamburger-wrapper" @click="toggleClick">
    <div :class="['i-svg:collapse', { hamburger: true, 'is-active': isActive }]" />
  </div>
</template>

<script setup lang="ts">
defineProps({
  isActive: { type: Boolean, required: true },
});

const emit = defineEmits(["toggleClick"]);

function toggleClick() {
  emit("toggleClick");
}
</script>

<style scoped lang="scss">
.hamburger-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 15px;
  cursor: pointer;

  .hamburger {
    vertical-align: middle;
    color: var(--el-text-color-secondary);
    transform: scaleX(-1);
    transition: all 0.3s ease;

    &:hover {
      color: var(--el-color-primary);
    }

    &.is-active {
      transform: scaleX(1);
    }
  }
}
</style>
