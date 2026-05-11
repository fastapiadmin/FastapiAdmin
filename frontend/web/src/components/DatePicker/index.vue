<!-- 封装日期选择器，支持所有 ElDatePicker 类型，带快捷选项 -->
<template>
  <div class="custom-date-picker">
    <ElDatePicker
      :model-value="modelValue"
      :type="pickerType"
      :format="pickerFormat"
      :value-format="pickerFormat"
      :range-separator="rangeSeparator"
      :start-placeholder="startPlaceholder"
      :end-placeholder="endPlaceholder"
      :shortcuts="isRangeType ? shortcuts : undefined"
      v-bind="$attrs"
      @update:model-value="(val) => emit('update:model-value', val)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { ElDatePicker } from "element-plus";

type DatePickerType =
  | "year"
  | "month"
  | "date"
  | "dates"
  | "week"
  | "datetime"
  | "datetimerange"
  | "daterange"
  | "monthrange";

const props = withDefaults(
  defineProps<{
    modelValue?: any;
    type?: DatePickerType;
    format?: string;
    rangeSeparator?: string;
    startPlaceholder?: string;
    endPlaceholder?: string;
  }>(),
  {
    type: "datetimerange",
    rangeSeparator: "至",
    startPlaceholder: "开始日期",
    endPlaceholder: "结束日期",
  }
);

const emit = defineEmits(["update:model-value"]);

/** 是否为范围选择模式 */
const isRangeType = computed(() => {
  return ["datetimerange", "daterange", "monthrange"].includes(props.type);
});

/** 根据 type 推导默认格式 */
const pickerFormat = computed(() => {
  if (props.format) return props.format;
  switch (props.type) {
    case "datetime":
    case "datetimerange":
      return "YYYY-MM-DD HH:mm:ss";
    case "date":
    case "daterange":
      return "YYYY-MM-DD";
    case "month":
    case "monthrange":
      return "YYYY-MM";
    case "year":
      return "YYYY";
    case "week":
      return "YYYY-wo";
    default:
      return "YYYY-MM-DD";
  }
});

const pickerType = computed(() => props.type);

/** 快捷选项（仅范围选择器展示） */
const shortcuts = [
  {
    text: "近一天",
    value: () => {
      const end = new Date();
      const start = new Date();
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
