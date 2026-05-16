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
export async function confirmBatchDelete(count: number): Promise<void> {
  await ElMessageBox.confirm(`确定删除选中的 ${count} 条数据吗？`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  });
}

/** 状态切换确认 */
export async function confirmToggleStatus(status: string): Promise<void> {
  await ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
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
