/**
 * 表格全局外观与交互：`FaTable` / `FaTableHeader` 通过 store 同步密度、斑马纹、边框、表头背景、全屏、行拖拽。
 * 持久化见 options.persist；跨页面保持用户偏好。
 */
import { defineStore } from "pinia";
import { ref } from "vue";
import { TableSizeEnum } from "@/enums/formEnum";

// 表格
export const useTableStore = defineStore(
  "tableStore",
  () => {
    // 表格大小
    const tableSize = ref(TableSizeEnum.DEFAULT);
    // 斑马纹
    const isZebra = ref(false);
    // 边框
    const isBorder = ref(false);
    // 表头背景
    const isHeaderBackground = ref(false);

    // 是否全屏
    const isFullScreen = ref(false);
    // 是否开启表格行拖拽排序（工具栏开关，与 ArtTable + VueDraggable 配合）
    const isRowDrag = ref(false);

    /**
     * 设置表格大小
     * @param size 表格大小枚举值
     */
    const setTableSize = (size: TableSizeEnum) => (tableSize.value = size);

    /**
     * 设置斑马纹显示状态
     * @param value 是否显示斑马纹
     */
    const setIsZebra = (value: boolean) => (isZebra.value = value);

    /**
     * 设置表格边框显示状态
     * @param value 是否显示边框
     */
    const setIsBorder = (value: boolean) => (isBorder.value = value);

    /**
     * 设置表头背景显示状态
     * @param value 是否显示表头背景
     */
    const setIsHeaderBackground = (value: boolean) => (isHeaderBackground.value = value);

    /**
     * 设置是否全屏
     * @param value 是否全屏
     */
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
