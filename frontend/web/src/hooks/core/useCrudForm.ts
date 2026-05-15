import type { Ref } from "vue";
import type { CrudDialogState, DialogType } from "./useCrudDialog";

/**
 * CRUD 表单管理
 *
 * 将对话框 + 表单 + 提交逻辑统一管理，减少每个 CRUD 页面 ~60 行重复代码
 *
 * @example
 * ```ts
 * const crud = useCrudForm<DeptForm>({
 *   formData: ref({ id: undefined, name: "", status: "0" }),
 *   initialFormData: { id: undefined, name: "", status: "0" },
 *   dialogVisible,        // 来自 useCrudDialog()
 *   dataFormRef,          // FaForm 的 ref
 *   formRenderKey,        // 用于 :key 重新渲染
 *   detailApi: DeptAPI.detailDept,
 *   createApi: DeptAPI.createDept,
 *   updateApi: DeptAPI.updateDept,
 *   onCreateSuccess: async () => { await refreshCreate(); },
 *   onUpdateSuccess: async () => { await refreshUpdate(); },
 * });
 *
 * // 模板中
 * crud.handleOpenDialog("create");
 * crud.handleOpenDialog("update", row.id);
 * crud.handleSubmit();
 * crud.handleCloseDialog();
 * ```
 */
export function useCrudForm<T extends object>(options: {
  /** 响应式表单数据 */
  formData: Ref<T>;
  /** 初始表单值（用于重置） */
  initialFormData: T;
  /** 对话框状态（来自 useCrudDialog） */
  dialogVisible: CrudDialogState;
  /** FaForm 实例 ref */
  dataFormRef: Ref<InstanceType<
    (typeof import("./../../components/forms/fa-form/index.vue"))["default"]
  > | null>;
  /** 表单渲染 key（用于 :key 重新渲染） */
  formRenderKey: Ref<number>;
  /** 详情 API（传入 id，返回 response） */
  detailApi?: (id: number) => Promise<{ data: { data?: T } }>;
  /** 新增 API */
  createApi?: (form: T) => Promise<unknown>;
  /** 修改 API（接收 id + form） */
  updateApi?: (id: number, form: T) => Promise<unknown>;
  /** 各类型打开时的标题映射 */
  titles?: Partial<Record<DialogType, string>>;
  /** 详情数据（用于 FaDescriptions 展示） */
  detailFormData?: Ref<Partial<T>>;
  /** 新增成功回调 */
  onCreateSuccess?: () => Promise<void> | void;
  /** 修改成功回调 */
  onUpdateSuccess?: () => Promise<void> | void;
  /** 提交成功后额外操作（如刷新字典、配置等） */
  onSubmitSuccess?: (formData: T) => Promise<void> | void;
}) {
  const {
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey,
    detailApi,
    createApi,
    updateApi,
    titles,
    detailFormData,
    onCreateSuccess,
    onUpdateSuccess,
    onSubmitSuccess,
  } = options;

  const submitLoading = ref(false);

  /** 重置表单 */
  async function resetForm() {
    dataFormRef.value?.resetFields();
    dataFormRef.value?.clearValidate();
    Object.assign(formData.value, initialFormData);
  }

  /** 关闭对话框并重置表单 */
  async function handleCloseDialog() {
    dialogVisible.visible = false;
    await resetForm();
  }

  /** 打开对话框 */
  async function handleOpenDialog(type: DialogType, id?: number, extra?: Record<string, unknown>) {
    dialogVisible.type = type;
    const titleMap = titles ?? {};
    const defaultTitles: Record<DialogType, string> = {
      create: "新增",
      update: "修改",
      detail: "详情",
    };

    if (id && detailApi) {
      const response = await detailApi(id);
      const data = response.data.data;
      if (type === "detail") {
        dialogVisible.title = titleMap.detail ?? defaultTitles.detail;
        if (detailFormData) {
          Object.assign(detailFormData.value, data ?? {});
        }
      } else if (type === "update") {
        dialogVisible.title = titleMap.update ?? defaultTitles.update;
        Object.assign(formData.value, data);
      }
    } else {
      dialogVisible.title = titleMap.create ?? defaultTitles.create;
      Object.assign(formData.value, initialFormData);
      (formData.value as Record<string, unknown>).id = undefined;
      if (extra) {
        Object.assign(formData.value, extra);
      }
    }
    formRenderKey.value += 1;
    dialogVisible.visible = true;
  }

  /** 提交表单 */
  async function handleSubmit() {
    const form = dataFormRef.value;
    if (!form) return;
    const valid = await (form.validate as () => Promise<boolean>)().catch(() => false);
    if (!valid) return;

    submitLoading.value = true;
    const id = (formData.value as Record<string, unknown>).id as number | undefined;
    try {
      if (id && updateApi) {
        await updateApi(id, { id, ...formData.value });
        await onUpdateSuccess?.();
      } else if (createApi) {
        await createApi(formData.value);
        await onCreateSuccess?.();
      }
      dialogVisible.visible = false;
      await resetForm();
      await onSubmitSuccess?.(formData.value);
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  }

  return {
    submitLoading,
    resetForm,
    handleCloseDialog,
    handleOpenDialog,
    handleSubmit,
  };
}
