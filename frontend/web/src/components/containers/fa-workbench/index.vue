<!-- 工作区：FastHub 式「左卡片 + 间距 + 右卡片」，固定宽度、不提供拖拽与分割线 -->
<template>
  <div
    class="fa-workbench"
    :style="{
      '--fa-workbench-side-w': `${sideWidth}px`,
      '--fa-workbench-side-h': `${sideHeight}px`,
    }"
  >
    <div class="fa-workbench__side">
      <slot name="side" />
    </div>
    <div class="fa-workbench__main">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaWorkbench" });

withDefaults(
  defineProps<{
    /** 左栏宽度（水平布局） */
    sideWidth?: number;
    /** 窄屏上下布局时上栏高度 */
    sideHeight?: number;
  }>(),
  {
    sideWidth: 380,
    sideHeight: 320,
  }
);
</script>

<style lang="scss" scoped>
.fa-workbench {
  display: flex;
  flex: 1;
  gap: 16px;
  min-height: 0;
}

.fa-workbench__side {
  display: flex;
  flex: 0 0 auto;
  width: var(--fa-workbench-side-w);
  min-width: 0;
  min-height: 0;
}

.fa-workbench__side > * {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
}

.fa-workbench__main {
  box-sizing: border-box;
  display: flex;
  flex: 1 1 auto;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: auto;
}

.fa-workbench__main > * {
  flex: 1 1 auto;
  min-height: 0;
}

/* 1280 仍是常见桌面宽度：左栏 + 主区并排足够放得下；1024 以下再上下排列 */
@media (width <= 1024px) {
  .fa-workbench {
    flex-direction: column;
  }

  .fa-workbench__side {
    width: 100%;
    height: var(--fa-workbench-side-h);
  }
}
</style>
