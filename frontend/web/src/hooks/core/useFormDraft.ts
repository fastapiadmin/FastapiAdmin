import { watch, type Ref } from "vue";
import { clearFormDraft, loadFormDraft, saveFormDraft } from "@/utils/form-draft";

/**
 * 创建表单草稿组合式函数：自动绑定对话框生命周期，实现「误关恢复」。
 *
 * 与 ``useCrudForm`` 的 ``cacheKey`` 定位一致，但面向「自管对话框」的手写表单：
 * - ``openCreate``：打开新建表单（可选预设 preset），自动重置 + 恢复草稿；
 * - 内部 ``watch`` 监听对话框关闭，自动保存草稿（仅新建态、且非提交成功）；
 * - ``done``：提交成功后调用，清除草稿并标记跳过本次关闭保存。
 *
 * 编辑态（``mode`` 为 update）不参与草稿读写；不传 ``mode`` 视为恒为新建态。
 */
export interface UseFormDraftOptions<T extends object> {
  /** 草稿缓存键 */
  key: string;
  /** 对话框可见性（v-model） */
  dialogVisible: Ref<boolean>;
  /** 表单数据 */
  form: Ref<T>;
  /** 新建态初始值工厂 */
  blank: () => T;
  /** 对话框模式；不传则视为恒为新建态（无编辑态的表单） */
  mode?: Ref<"create" | "update">;
}

export function useFormDraft<T extends object>(options: UseFormDraftOptions<T>) {
  const { key, dialogVisible, form, blank, mode } = options;
  // 提交成功后标记跳过本次「关闭时保存草稿」，防止提交后残留草稿
  let submitted = false;

  // 关闭对话框时自动保存草稿（仅新建态，且非提交成功）
  watch(dialogVisible, (visible) => {
    if (visible) return;
    if ((!mode || mode.value === "create") && !submitted) {
      saveFormDraft(key, form.value as Record<string, unknown>);
    }
    submitted = false;
  });

  /** 打开新建表单：重置为初始值 → 恢复草稿 → 应用预设（预设优先级最高） */
  function openCreate(preset?: Partial<T>): void {
    form.value = blank();
    const draft = loadFormDraft<Record<string, unknown>>(key);
    if (draft) Object.assign(form.value, draft);
    if (preset) Object.assign(form.value, preset);
    submitted = false;
    dialogVisible.value = true;
  }

  /** 提交成功后调用：清除草稿并标记跳过本次关闭保存 */
  function done(): void {
    submitted = true;
    clearFormDraft(key);
  }

  return { openCreate, done };
}
