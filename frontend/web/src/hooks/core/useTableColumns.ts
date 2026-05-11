/**
 * 表格列配置：显隐、拖拽排序、增删改；与 `useTable` 的 `columnsFactory` 配合。
 * 导出 `getColumnVisibility` / `getColumnChecks` 供表头等处复用同一套 visible/checked 规则。
 */

import { ref, computed, watch } from "vue";
import { $t } from "@/locales";
import type { ColumnOption } from "@/types/component";

/** selection / expand / index 等占位 prop，避免与业务列冲突 */
const SPECIAL_COLUMNS: Record<string, { prop: string; label: string }> = {
  selection: { prop: "__selection__", label: $t("table.column.selection") },
  expand: { prop: "__expand__", label: $t("table.column.expand") },
  index: { prop: "__index__", label: $t("table.column.index") },
};

export const getColumnKey = <T>(col: ColumnOption<T>) =>
  SPECIAL_COLUMNS[col.type as keyof typeof SPECIAL_COLUMNS]?.prop ?? (col.prop as string);

/** `visible` 优先；否则回退 `checked`，默认展示 */
export const getColumnVisibility = <T>(col: ColumnOption<T>): boolean => {
  if (col.visible !== undefined) {
    return col.visible;
  }
  return col.checked ?? true;
};

export const getColumnChecks = <T>(columns: ColumnOption<T>[]) =>
  columns.map((col) => {
    const special = col.type && SPECIAL_COLUMNS[col.type];
    const visibility = getColumnVisibility(col);

    if (special) {
      return { ...col, prop: special.prop, label: special.label, checked: true, visible: true };
    }
    return { ...col, checked: visibility, visible: visibility };
  });

/**
 * 动态列配置接口
 */
export interface DynamicColumnConfig<T = any> {
  /**
   * 新增列（支持单个或批量）
   * @param column 列配置或列配置数组
   * @param index 可选的插入位置，默认末尾（批量时为第一个列的位置）
   */
  addColumn: (column: ColumnOption<T> | ColumnOption<T>[], index?: number) => void;
  /**
   * 删除列（支持单个或批量）
   * @param prop 列的唯一标识或标识数组
   */
  removeColumn: (prop: string | string[]) => void;
  /**
   * 切换列显示状态（支持单个或批量）
   * @param prop 列的唯一标识或标识数组
   * @param visible 可选的显示状态，默认取反
   */
  toggleColumn: (prop: string | string[], visible?: boolean) => void;

  /**
   * 更新列（支持单个或批量）
   * @param prop 列的唯一标识或更新配置数组
   * @param updates 列配置更新（当 prop 为字符串时使用）
   */
  updateColumn: (
    prop: string | Array<{ prop: string; updates: Partial<ColumnOption<T>> }>,
    updates?: Partial<ColumnOption<T>>
  ) => void;
  /**
   * 批量更新列（兼容旧版本，推荐使用 updateColumn 的数组模式）
   * @param updates 列更新配置
   * @deprecated 推荐使用 updateColumn 的数组模式
   */
  batchUpdateColumns: (updates: Array<{ prop: string; updates: Partial<ColumnOption<T>> }>) => void;
  /**
   * 重新排序列
   * @param fromIndex 源索引
   * @param toIndex 目标索引
   */
  reorderColumns: (fromIndex: number, toIndex: number) => void;
  /**
   * 获取列配置
   * @param prop 列的唯一标识
   * @returns 列配置
   */
  getColumnConfig: (prop: string) => ColumnOption<T> | undefined;
  /**
   * 获取所有列配置
   * @returns 所有列配置
   */
  getAllColumns: () => ColumnOption<T>[];
  /**
   * 重置所有列
   */
  resetColumns: () => void;
}

export function useTableColumns<T = any>(
  columnsFactory: () => ColumnOption<T>[]
): {
  columns: any;
  columnChecks: any;
} & DynamicColumnConfig<T> {
  const dynamicColumns = ref<ColumnOption<T>[]>(columnsFactory());
  const columnChecks = ref<ColumnOption<T>[]>(getColumnChecks(dynamicColumns.value));

  // 当 dynamicColumns 变动时，重新生成 columnChecks 且保留已存在的显示状态
  watch(
    dynamicColumns,
    (newCols) => {
      const visibilityMap = new Map(
        columnChecks.value.map((c) => [getColumnKey(c), getColumnVisibility(c)])
      );
      const newChecks = getColumnChecks(newCols).map((c) => {
        const key = getColumnKey(c);
        const visibility = visibilityMap.has(key) ? visibilityMap.get(key) : getColumnVisibility(c);
        return {
          ...c,
          checked: visibility,
          visible: visibility,
        };
      });
      columnChecks.value = newChecks;
    },
    { deep: true }
  );

  // 当前显示列（基于 columnChecks 的 checked 或 visible）
  const columns = computed(() => {
    const colMap = new Map(dynamicColumns.value.map((c) => [getColumnKey(c), c]));
    return columnChecks.value
      .filter((c) => getColumnVisibility(c))
      .map((c) => colMap.get(getColumnKey(c)))
      .filter(Boolean) as ColumnOption<T>[];
  });

  // 支持 updater 返回新数组或直接在传入数组上 mutate
  const setDynamicColumns = (updater: (cols: ColumnOption<T>[]) => void | ColumnOption<T>[]) => {
    const copy = [...dynamicColumns.value];
    const result = updater(copy);
    dynamicColumns.value = Array.isArray(result) ? result : copy;
  };

  return {
    columns,
    columnChecks,

    /**
     * 新增列（支持单个或批量）
     */
    addColumn: (column: ColumnOption<T> | ColumnOption<T>[], index?: number) =>
      setDynamicColumns((cols) => {
        const next = [...cols];
        const columnsToAdd = Array.isArray(column) ? column : [column];
        const insertIndex =
          typeof index === "number" && index >= 0 && index <= next.length ? index : next.length;

        // 批量插入
        next.splice(insertIndex, 0, ...columnsToAdd);
        return next;
      }),

    /**
     * 删除列（支持单个或批量）
     */
    removeColumn: (prop: string | string[]) =>
      setDynamicColumns((cols) => {
        const propsToRemove = Array.isArray(prop) ? prop : [prop];
        return cols.filter((c) => !propsToRemove.includes(getColumnKey(c)));
      }),

    /**
     * 更新列（支持单个或批量）
     */
    updateColumn: (
      prop: string | Array<{ prop: string; updates: Partial<ColumnOption<T>> }>,
      updates?: Partial<ColumnOption<T>>
    ) => {
      // 批量模式：prop 是数组
      if (Array.isArray(prop)) {
        setDynamicColumns((cols) => {
          const map = new Map(prop.map((u) => [u.prop, u.updates]));
          return cols.map((c) => {
            const key = getColumnKey(c);
            const upd = map.get(key);
            return upd ? { ...c, ...upd } : c;
          });
        });
      }
      // 单个模式：prop 是字符串
      else if (updates) {
        setDynamicColumns((cols) =>
          cols.map((c) => (getColumnKey(c) === prop ? { ...c, ...updates } : c))
        );
      }
    },

    /**
     * 切换列显示状态（支持单个或批量）
     */
    toggleColumn: (prop: string | string[], visible?: boolean) => {
      const propsToToggle = Array.isArray(prop) ? prop : [prop];
      const next = [...columnChecks.value];

      propsToToggle.forEach((p) => {
        const i = next.findIndex((c) => getColumnKey(c) === p);
        if (i > -1) {
          const currentVisibility = getColumnVisibility(next[i]);
          const newVisibility = visible ?? !currentVisibility;
          // 同时更新 checked 和 visible 以保持兼容性
          next[i] = { ...next[i], checked: newVisibility, visible: newVisibility };
        }
      });

      columnChecks.value = next;
    },

    /**
     * 重置所有列
     */
    resetColumns: () => {
      dynamicColumns.value = columnsFactory();
    },

    /**
     * 批量更新列（兼容旧版本）
     * @deprecated 推荐使用 updateColumn 的数组模式
     */
    batchUpdateColumns: (updates) =>
      setDynamicColumns((cols) => {
        const map = new Map(updates.map((u) => [u.prop, u.updates]));
        return cols.map((c) => {
          const key = getColumnKey(c);
          const upd = map.get(key);
          return upd ? { ...c, ...upd } : c;
        });
      }),

    /**
     * 重新排序列
     */
    reorderColumns: (fromIndex: number, toIndex: number) =>
      setDynamicColumns((cols) => {
        if (
          fromIndex < 0 ||
          fromIndex >= cols.length ||
          toIndex < 0 ||
          toIndex >= cols.length ||
          fromIndex === toIndex
        ) {
          return cols;
        }
        const next = [...cols];
        const [moved] = next.splice(fromIndex, 1);
        next.splice(toIndex, 0, moved);
        return next;
      }),

    /**
     * 获取列配置
     */
    getColumnConfig: (prop: string) => dynamicColumns.value.find((c) => getColumnKey(c) === prop),

    /**
     * 获取所有列配置
     */
    getAllColumns: () => [...dynamicColumns.value],
  };
}
