import { ref } from "vue";

/**
 * 导入/导出弹窗状态管理
 * 减少各页面重复的 importModalVisible / exportModalVisible 及 open 函数
 */
export function useImportExport() {
  const importVisible = ref(false);
  const exportVisible = ref(false);

  return {
    importVisible,
    exportVisible,
    openImport: () => {
      importVisible.value = true;
    },
    openExport: () => {
      exportVisible.value = true;
    },
  };
}
