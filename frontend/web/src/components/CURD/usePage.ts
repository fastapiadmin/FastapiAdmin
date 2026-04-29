import { ref, Ref } from "vue";
import type { IObject, PageContentInstance, PageModalInstance } from "./types";
import { useCrudList } from "./useCrudList";

/**
 * CURD页面组合式函数
 * @returns 包含各种引用和处理函数的对象
 */
function usePage() {
  const { searchRef, contentRef, handleQueryClick, handleResetClick } = useCrudList();
  const addModalRef = ref<PageModalInstance>();
  const editModalRef = ref<PageModalInstance>();
  const viewModalRef = ref<PageModalInstance>();

  /**
   * 处理新增点击事件
   * @param RefImpl 可选的模态框引用
   */
  function handleAddClick(RefImpl?: Ref<PageModalInstance>) {
    try {
      if (RefImpl) {
        RefImpl.value?.setModalVisible();
        RefImpl.value?.handleDisabled(false);
      } else {
        addModalRef.value?.setModalVisible();
        addModalRef.value?.handleDisabled(false);
      }
    } catch (error) {
      console.error("打开新增模态框失败:", error);
      ElMessage.error(
        "打开新增模态框失败: " + (error instanceof Error ? error.message : String(error))
      );
    }
  }

  /**
   * 处理编辑点击事件
   * @param row 行数据
   * @param callback 回调函数
   * @param RefImpl 可选的模态框引用
   */
  async function handleEditClick(
    row: IObject,
    callback?: (result?: IObject) => IObject | Promise<IObject>,
    RefImpl?: Ref<PageModalInstance>
  ) {
    try {
      if (RefImpl) {
        RefImpl.value?.setModalVisible();
        RefImpl.value?.handleDisabled(false);
        const from = await (callback?.(row) ?? Promise.resolve(row));
        RefImpl.value?.setFormData(from ? from : row);
      } else {
        editModalRef.value?.setModalVisible();
        editModalRef.value?.handleDisabled(false);
        const from = await (callback?.(row) ?? Promise.resolve(row));
        editModalRef.value?.setFormData(from ? from : row);
      }
    } catch (error) {
      console.error("打开编辑模态框失败:", error);
      ElMessage.error(
        "打开编辑模态框失败: " + (error instanceof Error ? error.message : String(error))
      );
    }
  }

  /**
   * 处理查看点击事件
   * @param row 行数据
   * @param callback 回调函数
   * @param RefImpl 可选的模态框引用
   */
  async function handleViewClick(
    row: IObject,
    callback?: (result?: IObject) => IObject | Promise<IObject>,
    RefImpl?: Ref<PageModalInstance>
  ) {
    try {
      if (RefImpl) {
        RefImpl.value?.setModalVisible();
        RefImpl.value?.handleDisabled(true);
        const from = await (callback?.(row) ?? Promise.resolve(row));
        RefImpl.value?.setFormData(from ? from : row);
      } else {
        viewModalRef.value?.setModalVisible();
        viewModalRef.value?.handleDisabled(true);
        const from = await (callback?.(row) ?? Promise.resolve(row));
        viewModalRef.value?.setFormData(from ? from : row);
      }
    } catch (error) {
      console.error("打开查看模态框失败:", error);
      ElMessage.error(
        "打开查看模态框失败: " + (error instanceof Error ? error.message : String(error))
      );
    }
  }

  /**
   * 处理表单提交点击事件
   */
  function handleSubmitClick() {
    try {
      //根据检索条件刷新列表数据
      const queryParams = searchRef.value?.getQueryParams() || {};
      contentRef.value?.fetchPageData(queryParams, true);
    } catch (error) {
      console.error("提交表单失败:", error);
      ElMessage.error("提交表单失败: " + (error instanceof Error ? error.message : String(error)));
    }
  }

  /**
   * 处理导出点击事件
   */
  function handleExportClick() {
    try {
      // 根据检索条件导出数据
      const queryParams = searchRef.value?.getQueryParams() || {};
      contentRef.value?.exportPageData(queryParams);
    } catch (error) {
      console.error("导出数据失败:", error);
      ElMessage.error("导出数据失败: " + (error instanceof Error ? error.message : String(error)));
    }
  }

  /**
   * 处理筛选改变事件
   * @param filterParams 筛选参数
   */
  function handleFilterChange(filterParams: IObject) {
    try {
      const queryParams = searchRef.value?.getQueryParams() || {};
      contentRef.value?.fetchPageData({ ...queryParams, ...filterParams }, true);
    } catch (error) {
      console.error("筛选数据失败:", error);
      ElMessage.error("筛选数据失败: " + (error instanceof Error ? error.message : String(error)));
    }
  }

  /**
   * 处理更多操作事件
   * @param name 操作名称
   * @param selectedRows 选中的行数据
   * @param callback 回调函数
   */
  async function handleMoreOperation(
    name: string,
    selectedRows: IObject[],
    callback?: (name: string, selectedRows: IObject[]) => Promise<void>
  ) {
    try {
      if (callback) {
        await callback(name, selectedRows);
      }
      // 默认刷新数据
      handleSubmitClick();
    } catch (error) {
      console.error("处理更多操作失败:", error);
      ElMessage.error(
        "处理更多操作失败: " + (error instanceof Error ? error.message : String(error))
      );
    }
  }

  return {
    searchRef,
    contentRef,
    addModalRef,
    editModalRef,
    viewModalRef,
    handleQueryClick,
    handleResetClick,
    handleAddClick,
    handleEditClick,
    handleViewClick,
    handleSubmitClick,
    handleExportClick,
    handleFilterChange,
    handleMoreOperation,
  };
}

export default usePage;
export { useCrudList } from "./useCrudList";
