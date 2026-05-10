<!--
  分页：基于 ElPagination，统一 v-model page/limit 与父层的 `@pagination`。
  - total 变化时清空「连续相同 page:limit」过滤，避免与列表首次请求叠在一起。
  - 不在此 watch(total) 再次 emit（ElPagination 已按 total 钳页并触发 change）。
-->
<template>
  <ElScrollbar>
    <div :class="{ hidden: hidden }">
      <ElPagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :background="background"
        :disabled="disabled"
        :layout="layout"
        :page-sizes="pageSizes"
        :pager-count="pagerCount"
        :size="size"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </ElScrollbar>
</template>

<script setup lang="ts">
import { ref, watch, type PropType } from "vue";

/**
 * Props：`page` / `limit` 为 defineModel；其余透传 EP。
 * 事件：仅 `pagination`，载荷 `{ page, limit }`。
 */
const props = defineProps({
  total: {
    type: Number as PropType<number>,
    default: 0,
  },
  pageSizes: {
    type: Array as PropType<number[]>,
    default() {
      return [10, 20, 30, 50, 100];
    },
  },
  layout: {
    type: String,
    default: "total, sizes, prev, pager, next, jumper",
  },
  background: {
    type: Boolean,
    default: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  /** 页码按钮数量（透传 ElPagination） */
  pagerCount: {
    type: Number as PropType<number>,
    default: undefined,
  },
  /** 分页器尺寸（透传 ElPagination） */
  size: {
    type: String as PropType<"" | "default" | "small" | "large">,
    default: undefined,
  },
  hidden: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["pagination"]);

/** 上一次对外发出的 `page:limit`，用于过滤 EP 连续重复的 change */
const lastEmittedSig = ref<string | null>(null);

watch(
  () => props.total,
  () => {
    lastEmittedSig.value = null;
  }
);

/** 合并 EP 可能触发的重复事件，同一签名只 emit 一次 */
function emitPagination(page: number, limit: number) {
  const sig = `${page}:${limit}`;
  if (lastEmittedSig.value === sig) {
    return;
  }
  lastEmittedSig.value = sig;
  emit("pagination", { page, limit });
}

const currentPage = defineModel("page", {
  type: Number,
  required: true,
  default: 1,
});

const pageSize = defineModel("limit", {
  type: Number,
  required: true,
  default: 10,
});

function handleSizeChange(val: number) {
  /** disabled 时仍可能收到 EP 事件，在此短路 */
  if (props.disabled) {
    return;
  }
  const nextSize = Number(val);
  if (!Number.isFinite(nextSize) || nextSize <= 0) return;
  if (nextSize === Number(pageSize.value)) return;
  currentPage.value = 1;
  emitPagination(Number(currentPage.value), nextSize);
}

function handleCurrentChange(val: number) {
  if (props.disabled) {
    return;
  }
  const nextPage = Number(val);
  if (!Number.isFinite(nextPage) || nextPage < 1) return;
  emitPagination(nextPage, Number(pageSize.value));
}
</script>
