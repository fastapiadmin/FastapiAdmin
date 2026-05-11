/**
 * 表格全局外观与交互：`FaTable` / `FaTableHeader` 通过 store 同步密度、斑马纹、边框、表头背景、全屏、行拖拽。
 *
 * ── 设计意图 ──
 * 将「表格显示偏好」提升到 Pinia store 层，而非每个页面各自维护。
 * 用户在一个页面调整密度/斑马纹后，其他页面也同步生效。
 *
 * 持久化：options.persist → localStorage "tableStore"，刷新后保留。
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
