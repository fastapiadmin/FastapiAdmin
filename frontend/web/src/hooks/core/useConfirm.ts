/**
 * 确认弹窗 —— 封装 ElMessageBox.confirm 常用配置
 */

import { ElMessageBox } from "element-plus";

/** 删除确认 */
export async function confirmDelete(message = "确认删除该项数据?"): Promise<void> {
  await ElMessageBox.confirm(message, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
}

/** 批量删除确认 */
export async function confirmBatchDelete(count: number, names?: string[]): Promise<void> {
  const detail = names?.length
    ? `（${names.slice(0, 5).join("、")}${names.length > 5 ? `…等${count}条` : ""}）`
    : "";
  await ElMessageBox.confirm(`确定删除选中的 ${count} 条数据吗？${detail}`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
}

/** 状态切换确认 */
export async function confirmToggleStatus(value: "enable" | "disable"): Promise<void> {
  await ElMessageBox.confirm(`确认${value === "enable" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
}

/** 通用确认 */
export async function confirmAction(message: string, title = "警告"): Promise<void> {
  await ElMessageBox.confirm(message, title, {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
}
