<!-- 日期选择器 -->
<template>
  <div class="custom-date-picker">
    <el-date-picker
      :model-value="modelValue"
      type="datetimerange"
      format="YYYY-MM-DD HH:mm:ss"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :shortcuts="shortcuts"
      @update:model-value="(val) => emit('update:model-value', val)"
    />
  </div>
</template>

<script setup lang="ts">
// 定义组件属性
defineProps({
  modelValue: {
    type: Array as unknown as () => [Date, Date] | [],
    default: () => [],
  },
});

// 定义事件
const emit = defineEmits(["update:model-value"]);

// 快捷选项配置
const shortcuts = [
  {
    text: "近一天",
    value: () => {
      const end = new Date();
      const start = new Date();
      // 修正：起始时间为当前时间往前 24 小时
      start.setTime(start.getTime() - 3600 * 1000 * 24);
      return [start, end];
    },
  },
  {
    text: "近三天",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 3);
      return [start, end];
    },
  },
  {
    text: "近一周",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
      return [start, end];
    },
  },
  {
    text: "近一个月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
      return [start, end];
    },
  },
  {
    text: "近三个月",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
      return [start, end];
    },
  },
];
</script>

<style lang="scss" scoped>
.custom-date-picker {
  width: 100%;
}
</style>
