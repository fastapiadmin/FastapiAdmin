<!-- 分页组件 -->
<template>
  <ElScrollbar>
    <div :class="{ hidden: hidden }" class="pagination">
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
import { watch } from "vue";

defineOptions({ name: "FaPagination" });

interface Props {
  total?: number;
  pageSizes?: number[];
  layout?: string;
  background?: boolean;
  disabled?: boolean;
  /** 页码按钮数量（透传 ElPagination） */
  pagerCount?: number;
  /** 分页器尺寸（透传 ElPagination） */
  size?: "" | "default" | "small" | "large";
  autoScroll?: boolean;
  hidden?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  total: 0,
  pageSizes: () => [10, 20, 30, 50, 100],
  layout: "total, sizes, prev, pager, next, jumper",
  background: true,
  disabled: false,
  pagerCount: undefined,
  size: undefined,
  autoScroll: true,
  hidden: false,
});

interface Emits {
  pagination: [params: { page: number; limit: number }];
}

const emit = defineEmits<Emits>();

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

watch(
  () => props.total,
  (newVal: number) => {
    const lastPage = Math.ceil(newVal / pageSize.value);
    if (newVal > 0 && currentPage.value > lastPage) {
      currentPage.value = lastPage;
      emit("pagination", { page: currentPage.value, limit: pageSize.value });
    }
  }
);

function handleSizeChange(val: number) {
  currentPage.value = 1;
  emit("pagination", { page: currentPage.value, limit: val });
}

function handleCurrentChange(val: number) {
  emit("pagination", { page: val, limit: pageSize.value });
}
</script>

<style lang="scss" scoped>
.pagination {
  display: flex;
  flex-shrink: 0;
  justify-content: center;
  // padding: 12px 0;

  /* 自定义分页按钮样式（透明背景 + 主题色边框） */
  :deep(.el-pagination) {
    .btn-prev,
    .btn-next {
      background-color: transparent;
      border: 1px solid var(--fa-gray-300);
      transition: border-color 0.15s;

      &:hover:not(.is-disabled) {
        color: var(--theme-color);
        border-color: var(--theme-color);
      }
    }

    li {
      box-sizing: border-box;
      font-weight: 400 !important;
      background-color: transparent;
      border: 1px solid var(--fa-gray-300);
      transition: border-color 0.15s;

      &.is-active {
        font-weight: 400;
        color: #fff;
        background-color: var(--theme-color);
        border: 1px solid var(--theme-color);
      }

      &:hover:not(.is-disabled) {
        border-color: var(--theme-color);
      }
    }
  }

  :deep(.el-select) {
    width: 102px !important;
  }
}

/* H5 端：ElPagination 内容较多一行展示不下，改为可换行展示 */
@media (width <= 640px) {
  .pagination :deep(.el-pagination) {
    display: flex;
    flex-wrap: wrap;
    gap: 15px 0;
    align-items: center;
    justify-content: center;
  }
}
</style>
