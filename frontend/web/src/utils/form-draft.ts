/**
 * 创建表单草稿缓存的底层工具（localStorage 读写）。
 *
 * 用于「新建/新增/添加」表单：用户填了一半误关窗口，再次打开时恢复已填写内容。
 * 仅缓存创建态表单，编辑态表单由详情接口回填、不缓存。
 *
 * 本文件只提供底层读写；自动绑定对话框生命周期的组合式函数见
 * ``hooks/core/useFormDraft.ts`` 的 ``useFormDraft``。
 *
 * 存储键统一加 ``market-form-draft:`` 前缀，与业务数据隔离。
 */

const PREFIX = "market-form-draft:";

/** 读取创建表单草稿，无草稿或解析失败返回 null */
export function loadFormDraft<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(`${PREFIX}${key}`);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

/** 保存创建表单草稿（剔除 id，避免把编辑态带入新建） */
export function saveFormDraft(key: string, data: Record<string, unknown>): void {
  try {
    const { id: _id, ...rest } = data;
    void _id;
    localStorage.setItem(`${PREFIX}${key}`, JSON.stringify(rest));
  } catch {
    // 存储不可用/超限时静默忽略，不影响主流程
  }
}

/** 清除创建表单草稿（提交成功后调用） */
export function clearFormDraft(key: string): void {
  try {
    localStorage.removeItem(`${PREFIX}${key}`);
  } catch {
    // 忽略
  }
}
