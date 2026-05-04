/**
 * CrudArtTableDemo（Art 栈）演示：ArtSearchBar + ArtTableHeader + ArtTable + useTable。
 */
import { h, ref, computed } from "vue";
import type { TableError } from "@/utils/table/tableUtils";
import { ElMessage, ElMessageBox } from "element-plus";
import { useTable } from "@/hooks/core/useTable";
import { fetchGetUserList } from "@/api/system-manage";
import { ACCOUNT_TABLE_DATA } from "@/mock/temp/formData";
import { getColumnKey } from "@/hooks/core/useTableColumns";

export interface DemoUserRow {
  id?: number;
  nickName?: string;
  userName: string;
  userGender?: string;
  userPhone?: string;
  userEmail?: string;
  avatar?: string;
  status?: string;
  department?: string;
  score?: number;
}

export function useCrudArtTableDemo() {
  const selectedRows = ref<DemoUserRow[]>([]);
  const tableRef = ref();
  const searchBarRef = ref();
  const phoneSearch = ref("");

  const tableConfig = ref({
    height: "100%",
    fixedHeight: false,
  });

  const computedTableHeight = computed(() => (tableConfig.value.fixedHeight ? "500px" : ""));

  const searchFormState = ref({
    name: "",
    phone: "",
    status: "1",
    department: "",
    daterange: ["2025-01-01", "2025-02-10"] as [string, string],
  });

  const rules = {
    name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
    phone: [
      { required: true, message: "请输入手机号", trigger: "blur" },
      { pattern: /^1[3456789]\d{9}$/, message: "请输入正确的手机号", trigger: "blur" },
    ],
  };

  const searchItems = computed(() => [
    {
      key: "name",
      label: "用户名",
      type: "input",
      props: { placeholder: "请输入用户名" },
    },
    {
      key: "phone",
      label: "手机号",
      type: "input",
      props: { placeholder: "请输入手机号", maxlength: "11" },
    },
    {
      key: "status",
      label: "状态",
      type: "select",
      options: [
        { label: "全部", value: "" },
        { label: "在线", value: "1" },
        { label: "离线", value: "2" },
        { label: "异常", value: "3" },
        { label: "注销", value: "4" },
      ],
    },
    {
      key: "department",
      label: "部门",
      type: "select",
      options: [
        { label: "全部", value: "" },
        { label: "技术部", value: "技术部" },
        { label: "产品部", value: "产品部" },
        { label: "运营部", value: "运营部" },
        { label: "市场部", value: "市场部" },
        { label: "设计部", value: "设计部" },
      ],
    },
    {
      key: "daterange",
      label: "日期范围",
      type: "daterange",
      props: {
        type: "daterange",
        startPlaceholder: "开始日期",
        endPlaceholder: "结束日期",
        valueFormat: "YYYY-MM-DD",
      },
    },
  ]);

  const USER_STATUS_CONFIG = {
    "1": { type: "success" as const, text: "在线" },
    "2": { type: "info" as const, text: "离线" },
    "3": { type: "warning" as const, text: "异常" },
    "4": { type: "danger" as const, text: "注销" },
  } as const;

  const getUserStatusConfig = (status: string) =>
    USER_STATUS_CONFIG[status as keyof typeof USER_STATUS_CONFIG] ?? {
      type: "info" as const,
      text: "未知",
    };

  const exportColumns = computed(() => ({
    userName: { title: "用户名", width: 15 },
    userEmail: { title: "邮箱", width: 20 },
    userPhone: { title: "手机号", width: 15 },
    userGender: { title: "性别", width: 10 },
    department: { title: "部门", width: 15 },
    status: {
      title: "状态",
      width: 10,
      formatter: (value: string) => getUserStatusConfig(value).text,
    },
  }));

  const buildSearchParams = (params: typeof searchFormState.value) => {
    const { daterange, ...filtersParams } = params;
    const [startTime, endTime] = Array.isArray(daterange) ? daterange : [null, null];
    return { ...filtersParams, startTime, endTime };
  };

  const {
    data,
    loading,
    pagination,
    handleSizeChange,
    handleCurrentChange,
    replaceSearchParams,
    resetSearchParams,
    getData,
    getDataDebounced,
    clearData,
    refreshData,
    refreshCreate,
    refreshUpdate,
    refreshRemove,
    columns,
    columnChecks,
    addColumn,
    removeColumn,
    updateColumn,
    toggleColumn,
    resetColumns,
    reorderColumns,
    getColumnConfig,
    getAllColumns,
  } = useTable({
    core: {
      apiFn: (params) => fetchGetUserList(params),
      apiParams: {
        current: 1,
        size: 20,
        ...searchFormState.value,
      },
      excludeParams: ["daterange"],
      immediate: true,
      columnsFactory: () => [
        { type: "selection", width: 50 },
        { type: "globalIndex", width: 60, label: "序号" },
        {
          prop: "avatar",
          label: "用户信息",
          minWidth: 200,
          useSlot: true,
          useHeaderSlot: true,
          sortable: false,
        },
        {
          prop: "userGender",
          label: "性别",
          sortable: true,
          formatter: (row: unknown) => String((row as DemoUserRow).userGender ?? "未知"),
        },
        {
          prop: "userPhone",
          label: "手机号",
          useHeaderSlot: true,
          sortable: true,
        },
        { prop: "department", label: "部门", sortable: true },
        { prop: "score", label: "评分", useSlot: true, sortable: true },
        { prop: "status", label: "状态", useSlot: true, sortable: true },
        {
          prop: "operation",
          label: "操作",
          width: 190,
          useSlot: true,
          fixed: "right",
        },
      ],
    },
    transform: {
      dataTransformer: (records) => {
        if (!Array.isArray(records)) return [];
        return records.map((item: unknown, index: number) => {
          const row = item as DemoUserRow;
          return {
            ...row,
            avatar: ACCOUNT_TABLE_DATA[index % ACCOUNT_TABLE_DATA.length].avatar,
            department: ["技术部", "产品部", "运营部", "市场部", "设计部"][
              Math.floor(Math.random() * 5)
            ],
            score: Math.floor(Math.random() * 5) + 1,
            status: ["1", "2", "3", "4"][Math.floor(Math.random() * 4)],
          };
        }) as typeof records;
      },
    },
    performance: {
      enableCache: true,
      cacheTime: 5 * 60 * 1000,
      debounceTime: 300,
      maxCacheSize: 100,
    },
    hooks: {
      onError: (error: TableError) => {
        ElMessage.error(error.message);
      },
    },
    debug: {
      enableLog: false,
      logLevel: "info",
    },
  });

  const artPagination = computed(() => {
    const p = pagination as unknown as Record<string, unknown>;
    return {
      current: Number(p.current ?? p.page_no ?? 1),
      size: Number(p.size ?? p.page_size ?? 10),
      total: Number(p.total ?? 0),
    };
  });

  interface SortInfo {
    prop: string;
    order: "ascending" | "descending" | null;
  }

  const handleSelectionChange = (selection: DemoUserRow[]) => {
    selectedRows.value = selection;
  };

  const handleRowClick = (row: DemoUserRow) => {
    console.log("行点击:", row.userName);
  };

  const handleHeaderClick = (column: { label: string; property: string }) => {
    console.log("表头点击:", column.label);
  };

  const handleSortChange = (sortInfo: SortInfo) => {
    console.log("排序:", sortInfo.prop, sortInfo.order);
  };

  const handleSearch = async () => {
    await searchBarRef.value?.validate?.();
    replaceSearchParams(buildSearchParams(searchFormState.value));
    getData();
  };

  const handleReset = () => {
    resetSearchParams();
  };

  const handlePhoneSearch = (value: string) => {
    searchFormState.value.phone = value;
    replaceSearchParams(buildSearchParams(searchFormState.value));
    getDataDebounced();
  };

  const handleRefresh = () => {
    refreshData();
  };

  const handleAdd = () => {
    ElMessage.success("新增用户成功");
    refreshCreate();
  };

  const handleEdit = (row: DemoUserRow) => {
    ElMessage.success(`编辑用户 ${row.userName} 成功`);
    setTimeout(() => refreshUpdate(), 1000);
  };

  const handleDelete = async (row: DemoUserRow) => {
    try {
      await ElMessageBox.confirm(`确定要删除用户 ${row.userName} 吗？`, "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      });
      ElMessage.success("删除成功");
      setTimeout(() => refreshRemove(), 1000);
    } catch {
      ElMessage.info("已取消删除");
    }
  };

  const handleView = (row: DemoUserRow) => {
    ElMessage.info(`查看用户 ${row.userName}`);
  };

  const handleBatchDelete = async () => {
    try {
      await ElMessageBox.confirm(
        `确定要删除选中的 ${selectedRows.value.length} 个用户吗？`,
        "警告",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      );
      ElMessage.success(`批量删除 ${selectedRows.value.length} 个用户成功`);
      selectedRows.value = [];
      setTimeout(() => refreshRemove(), 1000);
    } catch {
      ElMessage.info("已取消删除");
    }
  };

  const handleExportSuccess = (_filename: string, count: number) => {
    ElMessage.success(`导出 ${count} 条数据成功`);
  };

  const handleImportSuccess = (rows: Record<string, unknown>[]) => {
    ElMessage.success(`导入 ${rows.length} 条数据成功`);
    refreshCreate();
  };

  const handleImportError = (error: Error) => {
    ElMessage.error(`导入失败：${error.message}`);
  };

  const handleClearData = () => {
    clearData();
    ElMessage.info("数据已清空");
  };

  const handleColumnCommand = (command: string): void => {
    switch (command) {
      case "addColumn": {
        addColumn?.({
          prop: "remark",
          label: "备注",
          width: 150,
          formatter: () => h("span", { style: "color: #999" }, "暂无备注"),
        });
        ElMessage.success('已新增"备注"列');
        break;
      }
      case "batchAddColumns": {
        addColumn?.(
          [
            {
              prop: "remark",
              label: "备注",
              width: 150,
              formatter: () => h("span", { style: "color: #999" }, "暂无备注"),
            },
            {
              prop: "tags",
              label: "标签",
              width: 120,
              formatter: () => h("span", { style: "color: #67c23a" }, "新用户"),
            },
          ],
          5
        );
        ElMessage.success('已批量新增"备注"和"标签"列');
        break;
      }
      case "toggleColumn": {
        if (getColumnConfig?.("userPhone")) {
          toggleColumn?.("userPhone");
          ElMessage.success("已切换手机号列显示状态");
        }
        break;
      }
      case "batchToggleColumns": {
        toggleColumn?.(["userGender", "userPhone"]);
        ElMessage.success("已批量切换性别和手机号列显示状态");
        break;
      }
      case "removeColumn": {
        removeColumn?.("status");
        ElMessage.success("已删除状态列");
        break;
      }
      case "batchRemoveColumns": {
        removeColumn?.(["status", "score"]);
        ElMessage.success("已批量删除状态和评分列");
        break;
      }
      case "updateColumn": {
        updateColumn?.("userPhone", { label: "联系电话", width: 140 });
        ElMessage.success('手机号列已更新为"联系电话"');
        break;
      }
      case "batchUpdateColumns": {
        updateColumn?.([
          { prop: "userGender", updates: { width: 200, label: "性别-已更新", sortable: false } },
          { prop: "userPhone", updates: { width: 200, label: "手机号-已更新", sortable: false } },
        ]);
        ElMessage.success("已批量更新性别和手机号列");
        break;
      }
      case "reorderColumns": {
        const allCols = getAllColumns?.();
        if (allCols) {
          const genderIndex = allCols.findIndex((col) => getColumnKey(col) === "userGender");
          const phoneIndex = allCols.findIndex((col) => getColumnKey(col) === "userPhone");
          if (genderIndex !== -1 && phoneIndex !== -1) {
            reorderColumns?.(genderIndex, phoneIndex);
            ElMessage.success("已交换性别和手机号列位置");
          }
        }
        break;
      }
      case "resetColumns": {
        resetColumns?.();
        ElMessage.success("已重置所有列配置");
        break;
      }
      default:
        console.warn("未知的列配置命令:", command);
    }
  };

  return {
    searchBarRef,
    searchFormState,
    searchItems,
    rules,
    phoneSearch,
    selectedRows,
    tableRef,
    columnChecks,
    loading,
    data,
    artPagination,
    columns,
    computedTableHeight,
    exportColumns,
    getUserStatusConfig,
    handleSearch,
    handleReset,
    handlePhoneSearch,
    handleRefresh,
    handleSelectionChange,
    handleRowClick,
    handleHeaderClick,
    handleSortChange,
    handleSizeChange,
    handleCurrentChange,
    handleAdd,
    handleEdit,
    handleDelete,
    handleView,
    handleBatchDelete,
    handleExportSuccess,
    handleImportSuccess,
    handleImportError,
    handleClearData,
    handleColumnCommand,
  };
}
