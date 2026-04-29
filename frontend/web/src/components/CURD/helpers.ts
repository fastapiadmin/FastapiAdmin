import type { IObject, IComponentType, ISearchComponent } from "./types";
import { markRaw } from "vue";
import InputTag from "@/components/InputTag/index.vue";
import IconSelect from "@/components/IconSelect/index.vue";
import DatePicker from "@/components/DatePicker/index.vue";

/**
 * 获取提示属性
 * @param tips 提示内容
 * @returns 提示属性对象
 */
export const getTooltipProps = (tips: string | IObject) => {
  return typeof tips === "string" ? { content: tips } : tips;
};

/**
 * 模态框组件映射表
 */
export const modalComponentMap = new Map<IComponentType, any>([
  // @ts-ignore
  ["input", markRaw(ElInput)],
  // @ts-ignore
  ["select", markRaw(ElSelect)],
  // @ts-ignore
  ["switch", markRaw(ElSwitch)],
  // @ts-ignore
  ["cascader", markRaw(ElCascader)],
  // @ts-ignore
  ["input-number", markRaw(ElInputNumber)],
  // @ts-ignore
  ["input-tag", markRaw(InputTag)],
  // @ts-ignore
  ["time-picker", markRaw(ElTimePicker)],
  // @ts-ignore
  ["time-select", markRaw(ElTimeSelect)],
  // @ts-ignore
  ["date-picker", markRaw(ElDatePicker)],
  // @ts-ignore
  ["tree-select", markRaw(ElTreeSelect)],
  // @ts-ignore
  ["custom-tag", markRaw(InputTag)],
  // @ts-ignore
  ["text", markRaw(ElText)],
  // @ts-ignore
  ["radio", markRaw(ElRadioGroup)],
  // @ts-ignore
  ["checkbox", markRaw(ElCheckboxGroup)],
  // @ts-ignore
  ["icon-select", markRaw(IconSelect)],
  // @ts-ignore
  ["custom", ""],
]);

/**
 * 搜索组件映射表
 */
export const searchComponentMap = new Map<ISearchComponent, any>([
  // @ts-ignore
  ["input", markRaw(ElInput)],
  // @ts-ignore
  ["select", markRaw(ElSelect)],
  // @ts-ignore
  ["cascader", markRaw(ElCascader)],
  // @ts-ignore
  ["input-number", markRaw(ElInputNumber)],
  // @ts-ignore
  ["date-picker", markRaw(DatePicker)],
  // @ts-ignore
  ["time-picker", markRaw(ElTimePicker)],
  // @ts-ignore
  ["time-select", markRaw(ElTimeSelect)],
  // @ts-ignore
  ["tree-select", markRaw(ElTreeSelect)],
  // @ts-ignore
  ["input-tag", markRaw(ElInputTag)],
  // @ts-ignore
  ["custom-tag", markRaw(InputTag)],
]);

/**
 * 子组件映射表
 */
export const childrenMap = new Map<IComponentType, any>([
  // @ts-ignore
  ["select", markRaw(ElOption)],
  // @ts-ignore
  ["radio", markRaw(ElRadio)],
  // @ts-ignore
  ["checkbox", markRaw(ElCheckbox)],
]);
