import type { IObject, IComponentType, ISearchComponent } from "./types";
import { markRaw } from "vue";
import {
  ElCascader,
  ElCheckbox,
  ElCheckboxGroup,
  ElDatePicker,
  ElInput,
  ElInputNumber,
  ElInputTag,
  ElOption,
  ElRadio,
  ElRadioGroup,
  ElSelect,
  ElSwitch,
  ElText,
  ElTimePicker,
  ElTimeSelect,
  ElTreeSelect,
} from "element-plus";
import InputTag from "@/components/InputTag/index.vue";
import IconSelect from "@/components/IconSelect/index.vue";
import DatePicker from "@/components/DatePicker/index.vue";

export const getTooltipProps = (tips: string | IObject) => {
  return typeof tips === "string" ? { content: tips } : tips;
};

export const modalComponentMap = new Map<IComponentType, any>([
  ["input", markRaw(ElInput)],
  ["select", markRaw(ElSelect)],
  ["switch", markRaw(ElSwitch)],
  ["cascader", markRaw(ElCascader)],
  ["input-number", markRaw(ElInputNumber)],
  ["input-tag", markRaw(InputTag)],
  ["time-picker", markRaw(ElTimePicker)],
  ["time-select", markRaw(ElTimeSelect)],
  ["date-picker", markRaw(ElDatePicker)],
  ["tree-select", markRaw(ElTreeSelect)],
  ["custom-tag", markRaw(InputTag)],
  ["text", markRaw(ElText)],
  ["radio", markRaw(ElRadioGroup)],
  ["checkbox", markRaw(ElCheckboxGroup)],
  ["icon-select", markRaw(IconSelect)],
  ["custom", ""],
]);

export const searchComponentMap = new Map<ISearchComponent, any>([
  ["input", markRaw(ElInput)],
  ["select", markRaw(ElSelect)],
  ["cascader", markRaw(ElCascader)],
  ["input-number", markRaw(ElInputNumber)],
  ["date-picker", markRaw(DatePicker)],
  ["time-picker", markRaw(ElTimePicker)],
  ["time-select", markRaw(ElTimeSelect)],
  ["tree-select", markRaw(ElTreeSelect)],
  ["input-tag", markRaw(ElInputTag)],
  ["custom-tag", markRaw(InputTag)],
]);

export const childrenMap = new Map<IComponentType, any>([
  ["select", markRaw(ElOption)],
  ["radio", markRaw(ElRadio)],
  ["checkbox", markRaw(ElCheckbox)],
]);
