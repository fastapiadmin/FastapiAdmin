<!-- 操作列自适应宽度 -->
<template>
  <el-table-column
    :label="label"
    :fixed="fixed"
    :align="align"
    :show-overflow-tooltip="showOverflowTooltip"
    :width="finalWidth"
  >
    <template #default="{ row, column, $index }">
      <div v-auto-width class="operation-buttons">
        <slot v-bind="{ row, column, $index }"></slot>
      </div>
    </template>
  </el-table-column>
</template>

<script setup lang="ts">
interface Props {
  listDataLength: number;
  prop?: string;
  label?: string;
  fixed?: string | boolean;
  align?: string;
  width?: number | string;
  showOverflowTooltip?: boolean;
  minWidth?: number | string;
}

const props = withDefaults(defineProps<Props>(), {
  label: "操作",
  fixed: "right",
  align: "center",
  minWidth: 80,
});

const count = ref(0);
const operationWidth = ref(Number(props.minWidth) || 80);

// 计算操作列宽度
const calculateWidth = () => {
  count.value++;

  if (count.value !== props.listDataLength) return;
  const maxWidth = getOperationMaxWidth();
  operationWidth.value = Math.max(maxWidth, Number(props.minWidth));
  count.value = 0;
};

// 计算最终宽度
const finalWidth = computed(() => {
  const widthNum = typeof props.width === "number" ? props.width : Number(props.width);
  const minWidthNum = typeof props.minWidth === "number" ? props.minWidth : Number(props.minWidth);
  return widthNum || operationWidth.value || minWidthNum;
});

// 自适应宽度指令
const vAutoWidth = {
  mounted() {
    // 初次挂载的时候计算一次
    calculateWidth();
  },
  updated() {
    // 数据更新时重新计算一次
    calculateWidth();
  },
};

/**
 * 获取按钮数量和宽带来获取操作组的最大宽度
 * 注意使用时需要使用 `class="operation-buttons"` 的标签包裹操作按钮
 * @returns {number} 返回操作组的最大宽度
 */
const getOperationMaxWidth = () => {
  const el = document.getElementsByClassName("operation-buttons");

  // 取操作组的最大宽度
  let maxWidth = 0;
  let totalWidth: any = 0;
  Array.prototype.forEach.call(el, (item) => {
    // 获取每个item的dom
    const buttons = item.querySelectorAll(".el-button");
    // 获取每行按钮的总宽度
    totalWidth = Array.from(buttons).reduce((acc, button: any) => {
      return acc + button.scrollWidth + 14; // 每个按钮的宽度加上预留宽度
    }, 0);

    // 获取最大的宽度
    if (totalWidth > maxWidth) maxWidth = totalWidth;
  });

  return maxWidth;
};
</script>
