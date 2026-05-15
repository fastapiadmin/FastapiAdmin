import type { ComputedRef, Ref } from "vue";

/**
 * 表格多选状态管理
 *
 * @example
 * ```ts
 * const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
 *   useTableSelection<DictTable>();
 * ```
 */
export function useTableSelection<T extends object>() {
  const selectedRows = ref<T[]>([]) as Ref<T[]>;
  const selectedIds = computed(() =>
    selectedRows.value
      .map((r) => (r as Record<string, unknown>).id)
      .filter((id): id is number => id != null && !Number.isNaN(id))
  ) as ComputedRef<number[]>;
  const batchDeleting = ref(false);

  function onTableSelectionChange(rows: T[]) {
    selectedRows.value = rows;
  }

  function clearSelection() {
    selectedRows.value = [];
  }

  return {
    selectedRows,
    selectedIds,
    batchDeleting,
    onTableSelectionChange,
    clearSelection,
  };
}
