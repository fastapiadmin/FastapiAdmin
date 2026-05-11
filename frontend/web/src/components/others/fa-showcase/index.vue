<template>
  <component :is="tag" class="fa-widget-demo-title">
    <slot />
  </component>
</template>

<script setup lang="ts">
/**
 * Widget 演示页章节标题（与历史 `page-title` Tailwind 一致）。
 * 业务页如需同款排版可直接复用；CRUD 列表页优先用 FaSearchBar + 表格区标题即可。
 */
withDefaults(
  defineProps<{
    /** 页面唯一主标题用 h1，分区用 h2 */
    tag?: "h1" | "h2";
  }>(),
  { tag: "h1" }
);
</script>

<style scoped>
@reference "@styles/core/tailwind.css";

.fa-widget-demo-title {
  @apply my-5 text-xl font-medium first:mt-0;
}
</style>
