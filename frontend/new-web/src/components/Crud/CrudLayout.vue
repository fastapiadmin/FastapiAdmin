<!-- 列表页基础外壳：与 examples/tables、系统用户页一致 — art-full-height + 主内容 art-table-card -->
<template>
  <div
    class="base-crud-page app-container flex min-h-0 flex-col"
    :class="[{ 'base-crud-page--fill': fill }, fill ? 'art-full-height' : '', rootClass]"
  >
    <div v-if="$slots.search" class="base-crud-page__search min-h-0 shrink-0">
      <slot name="search" />
    </div>

    <div class="base-crud-page__main flex min-h-0 flex-1 flex-col gap-4">
      <slot />
    </div>

    <slot name="extra" />
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "CrudLayout" });

withDefaults(
  defineProps<{
    /** 占满父级剩余高度（flex 子项常用） */
    fill?: boolean;
    /** 追加到根节点 class */
    rootClass?: string | string[] | Record<string, boolean>;
  }>(),
  {
    fill: true,
  }
);
</script>
