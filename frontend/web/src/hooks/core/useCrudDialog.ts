export type DialogType = "create" | "update" | "detail";

export interface CrudDialogState {
  title: string;
  visible: boolean;
  type: DialogType;
}

/**
 * CRUD 对话框状态管理
 *
 * @example
 * ```ts
 * const { dialogVisible, openDialog, closeDialog } = useCrudDialog();
 * openDialog("create");           // 新增
 * openDialog("update", "修改XX"); // 编辑
 * openDialog("detail", "XX详情"); // 详情
 * closeDialog();                  // 关闭
 * ```
 */
export function useCrudDialog() {
  const dialogVisible = reactive<CrudDialogState>({
    title: "",
    visible: false,
    type: "create",
  });

  function openDialog(type: DialogType, title?: string) {
    dialogVisible.type = type;
    if (type === "create") {
      dialogVisible.title = title ?? "新增";
    } else if (type === "update") {
      dialogVisible.title = title ?? "修改";
    } else {
      dialogVisible.title = title ?? "详情";
    }
    dialogVisible.visible = true;
  }

  function closeDialog() {
    dialogVisible.visible = false;
  }

  return {
    dialogVisible,
    openDialog,
    closeDialog,
  };
}
