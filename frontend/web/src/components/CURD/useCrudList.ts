import { ElMessage } from 'element-plus';
import { ref } from 'vue';
import type { IObject, PageContentInstance, PageSearchInstance } from './types';

/**
 * 仅列表查询区 + 表格区时复用：searchRef / contentRef 与查询、重置拉数逻辑。
 * 合并 `PageSearch` 查询参数与 `PageContent.getFilterParams()`（表头筛选等），与 usePage 中同名逻辑一致。
 * 业务页可替换手写 `handleQueryClick` / `handleResetClick` + 双 ref，参见 `module_example/demo`。
 */
export function useCrudList() {
  const searchRef = ref<PageSearchInstance>();
  const contentRef = ref<PageContentInstance>();

  function handleQueryClick(queryParams: IObject) {
    try {
      const filterParams = contentRef.value?.getFilterParams() || {};
      contentRef.value?.fetchPageData({ ...queryParams, ...filterParams }, true);
    } catch (error) {
      console.error('查询数据失败:', error);
      ElMessage.error('查询数据失败: ' + (error instanceof Error ? error.message : String(error)));
    }
  }

  function handleResetClick(queryParams: IObject) {
    try {
      const filterParams = contentRef.value?.getFilterParams() || {};
      contentRef.value?.fetchPageData({ ...queryParams, ...filterParams }, true);
    } catch (error) {
      console.error('重置数据失败:', error);
      ElMessage.error('重置数据失败: ' + (error instanceof Error ? error.message : String(error)));
    }
  }

  /** 弹窗提交后等与「查询」同参刷新：合并搜索条件 + 表头筛选 */
  function refreshList() {
    try {
      const q = searchRef.value?.getQueryParams() ?? {};
      const f = contentRef.value?.getFilterParams() ?? {};
      contentRef.value?.fetchPageData({ ...q, ...f }, true);
    } catch (error) {
      console.error('刷新列表失败:', error);
      ElMessage.error('刷新列表失败: ' + (error instanceof Error ? error.message : String(error)));
    }
  }

  return {
    searchRef,
    contentRef,
    handleQueryClick,
    handleResetClick,
    refreshList,
  };
}
