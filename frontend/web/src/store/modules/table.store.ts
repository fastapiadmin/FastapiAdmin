/**
 * 表格全局外观与交互：`ArtTable` / `ArtTableHeader` 通过 store 同步密度、斑马纹、边框、表头背景、全屏、行拖拽。
 * 持久化见 options.persist；跨页面保持用户偏好。
 */
import { defineStore } from "pinia";
import { ref } from "vue";
import { TableSizeEnum } from "@/enums/formEnum";

export const useTableStore = defineStore(
  "tableStore",
  () => {
    // --- 表格样式 ---
    const tableSize = ref(TableSizeEnum.DEFAULT);
    const isZebra = ref(false);
    const isBorder = ref(false);
    const isHeaderBackground = ref(false);

    // --- 交互 ---
    const isFullScreen = ref(false);
    /** 工具栏「行拖拽」；仅当表格数据为可变数组时有效 */
    const isRowDrag = ref(false);

    const setTableSize = (size: TableSizeEnum) => (tableSize.value = size);
    const setIsZebra = (value: boolean) => (isZebra.value = value);
    const setIsBorder = (value: boolean) => (isBorder.value = value);
    const setIsHeaderBackground = (value: boolean) => (isHeaderBackground.value = value);
    const setIsFullScreen = (value: boolean) => (isFullScreen.value = value);
    const setIsRowDrag = (value: boolean) => (isRowDrag.value = value);

    return {
      tableSize,
      isZebra,
      isBorder,
      isHeaderBackground,
      setTableSize,
      setIsZebra,
      setIsBorder,
      setIsHeaderBackground,
      isFullScreen,
      setIsFullScreen,
      isRowDrag,
      setIsRowDrag,
    };
  },
  {
    persist: {
      key: "table",
      storage: localStorage,
    },
  }
);
