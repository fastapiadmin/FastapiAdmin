<template>
  <div v-loading="loading" class="min-h-0">
    <ElEmpty
      v-if="!loading && isEmpty"
      :image-size="emptyImageSize"
      :description="emptyDescription"
      class="py-8"
    />
    <div v-else class="min-h-0" :class="gridClass">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaCardList" });

interface FaCardListProps {
  loading?: boolean;
  isEmpty?: boolean;
  emptyDescription?: string;
  emptyImageSize?: number;
  /** Tailwind/Grid class string for layout */
  gridClass?: string;
}

withDefaults(defineProps<FaCardListProps>(), {
  loading: false,
  isEmpty: false,
  emptyDescription: "暂无数据",
  emptyImageSize: 80,
  gridClass:
    "grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 auto-rows-max content-start",
});
</script>
