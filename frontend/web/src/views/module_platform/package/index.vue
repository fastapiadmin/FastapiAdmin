<!-- 套餐管理：FA + useTable；含菜单权限管理 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="pkgSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      include-audit
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElCard class="fa-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <FaTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_package:package:create']"
            :perm-delete="['module_package:package:delete']"
            :perm-patch="['module_package:package:update']"
            :delete-loading="batchDeleting"
            :create-loading="createLoading"
            :more-loading="moreLoading"
            @add="handleAdd"
            @delete="handleBatchDelete"
            @more="handleMoreClick"
          />
        </template>
      </FaTableHeader>

      <FaTable
        ref="faTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="pagination"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="700px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :label-width="'110px'"
          :data="detailFormData"
          :items="pkgDetailItems"
          max-height="75vh"
        >
          <template #price="{ row }"> ¥{{ (Number(row?.price ?? 0) / 100).toFixed(2) }} </template>
          <template #period="{ row }">
            {{ row?.period === "month" ? "按月" : "按年" }}
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          scrollbar
          max-height="75vh"
          :key="pkgFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="pkgDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="120"
          label-position="right"
          :span="12"
          :gutter="20"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio :value="0">正常</ElRadio>
              <ElRadio :value="1">禁用</ElRadio>
            </ElRadioGroup>
          </template>
          <template #period>
            <ElRadioGroup v-model="formData.period">
              <ElRadio value="month">按月</ElRadio>
              <ElRadio value="year">按年</ElRadio>
            </ElRadioGroup>
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <!-- 套餐菜单权限 -->
    <FaDrawer
      v-model="menuDialogVisible"
      title="套餐菜单权限"
      size="400px"
      destroy-on-close
      @close="menuDialogVisible = false"
    >
      <FaMenuTreeTable
        ref="menuTreeTableRef"
        :menu-tree="menuTreeData"
        :checked-ids="menuCheckedIds"
        :loading="menuTreeLoading"
      />
      <template #footer>
        <ElButton @click="menuDialogVisible = false">取消</ElButton>
        <ElButton type="primary" :loading="menuSaveLoading" @click="handleSaveMenus">保存</ElButton>
      </template>
    </FaDrawer>
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import PackageAPI, { type PackageForm, type PackageTable } from "@/api/module_platform/package";
import MenuAPI from "@/api/module_platform/menu";
import { useAuth } from "@/hooks/core/useAuth";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaMenuTreeTable from "@/components/others/fa-menu-tree-table/index.vue";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";
import { ElMessage } from "element-plus";

defineOptions({
  name: "Package",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type PackageSearchForm = {
  name?: string;
  code?: string;
  status?: number;
};

function buildPkgReplaceParams(p: PackageSearchForm): Record<string, unknown> {
  return {
    name: p.name || undefined,
    code: p.code || undefined,
    status: p.status || undefined,
  };
}

function buildPkgRowActions(
  row: PackageTable,
  ctx: {
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
    onToggleStatus: (row: PackageTable) => void;
    onManageMenus: (id: number) => void;
  }
): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_package:package:query",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_package:package:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_package:package:delete",
      run: () => ctx.onDelete(row.id!),
    },
    {
      key: "toggle-status",
      label: row.status === 0 ? "禁用" : "启用",
      artType: "more",
      icon: "ri:toggle-line",
      perm: "module_package:package:update",
      run: () => ctx.onToggleStatus(row),
    },
    {
      key: "menus",
      label: "菜单权限",
      artType: "more",
      icon: "ri:menu-line",
      perm: "module_package:package:update",
      run: () => ctx.onManageMenus(row.id!),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatPkgOperationCell(row: PackageTable, ctx: Parameters<typeof buildPkgRowActions>[1]) {
  const actions = buildPkgRowActions(row, ctx);
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 pkg-table-actions",
  });
}

const searchForm = ref<PackageSearchForm>({
  name: undefined,
  code: undefined,
  status: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "正常", value: 0 },
  { label: "禁用", value: 1 },
]);

const pkgSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "套餐名称",
    key: "name",
    type: "input",
    placeholder: "请输入套餐名称",
    clearable: true,
    span: 6,
  },
  {
    label: "套餐编码",
    key: "code",
    type: "input",
    placeholder: "请输入套餐编码",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
      clearable: true,
    },
    span: 6,
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const { selectedIds, batchDeleting, onTableSelectionChange } = useTableSelection<PackageTable>();

const createLoading = ref(false);
const moreLoading = ref(false);

const opCtx = {
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deletePkgRow,
  onToggleStatus: (row: PackageTable) => togglePkgStatus(row),
  onManageMenus: (id: number) => openMenuDialog(id),
};

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: PackageAPI.listPackage,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: resolveStatusColumns<PackageTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "套餐名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "code", label: "套餐编码", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 80,
        status: {
          0: { type: "success", text: "正常" },
          1: { type: "danger", text: "禁用" },
        },
      },
      { prop: "sort", label: "排序", width: 60, align: "center" },
      {
        prop: "price",
        label: "价格",
        width: 100,
        align: "right",
        formatter: (row: PackageTable) => `¥${(Number(row.price ?? 0) / 100).toFixed(2)}`,
      },
      {
        prop: "period",
        label: "计费周期",
        width: 90,
        formatter: (row: PackageTable) => (row.period === "month" ? "按月" : "按年"),
      },
      { prop: "trial_days", label: "试用天数", width: 80, align: "center" },
      { prop: "max_users", label: "最大用户数", width: 90, align: "center" },
      { prop: "max_roles", label: "最大角色数", width: 90, align: "center" },
      { prop: "max_depts", label: "最大部门数", width: 90, align: "center" },
      { prop: "max_storage_mb", label: "存储(MB)", width: 90, align: "center" },
      { prop: "rate_limit", label: "速率限制", width: 80, align: "center" },
      {
        prop: "operation",
        label: "操作",
        width: 200,
        fixed: "right",
        align: "center",
        formatter: (row: PackageTable) => formatPkgOperationCell(row, opCtx),
      },
    ]),
  },
});

// 详情 & 表单
const formData = ref<PackageForm>({});
const detailFormData = ref<Partial<PackageTable>>({});
const pkgFormRenderKey = ref(0);

const pkgDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] = [
  { label: "套餐名称", prop: "name" },
  { label: "套餐编码", prop: "code" },
  {
    label: "状态",
    prop: "status",
    tag: { map: { 0: { type: "success", text: "正常" }, 1: { type: "danger", text: "禁用" } } },
  },
  { label: "排序", prop: "sort" },
  { label: "价格", prop: "price", slot: "price" },
  { label: "计费周期", prop: "period", slot: "period" },
  { label: "试用天数", prop: "trial_days" },
  { label: "最大用户数", prop: "max_users" },
  { label: "最大角色数", prop: "max_roles" },
  { label: "最大部门数", prop: "max_depts" },
  { label: "最大存储(MB)", prop: "max_storage_mb" },
  { label: "速率限制", prop: "rate_limit" },
  { label: "描述", prop: "description", span: 4 },
];

const pkgDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "套餐名称",
    key: "name",
    type: "input",
    props: {
      placeholder: "请输入套餐名称",
      maxlength: 100,
    },
    rules: [
      { required: true, message: "请输入套餐名称", trigger: "blur" },
      { max: 100, message: "最长 100 个字符", trigger: "blur" },
    ],
    span: 12,
  },
  {
    label: "套餐编码",
    key: "code",
    type: "input",
    props: {
      placeholder: "请输入套餐编码（仅字母数字）",
      maxlength: 100,
    },
    rules: [
      { required: true, message: "请输入套餐编码", trigger: "blur" },
      { pattern: /^[a-zA-Z0-9]+$/, message: "仅允许字母和数字", trigger: "blur" },
      { min: 2, message: "至少 2 个字符", trigger: "blur" },
    ],
    span: 12,
  },
  {
    label: "排序",
    key: "sort",
    type: "number",
    props: {
      placeholder: "排序",
      min: 0,
    },
    span: 12,
  },
  {
    label: "状态",
    key: "status",
    type: "slot",
    slot: "status",
    span: 12,
  },
  {
    label: "价格(分)",
    key: "price",
    type: "number",
    props: {
      placeholder: "价格（单位：分）",
      min: 0,
    },
    rules: [
      { required: true, message: "请输入价格", trigger: "blur" },
      { type: "number", min: 0, message: "价格不能为负数", trigger: "blur" },
    ],
    span: 12,
  },
  {
    label: "计费周期",
    key: "period",
    type: "slot",
    slot: "period",
    span: 12,
  },
  {
    label: "试用天数",
    key: "trial_days",
    type: "number",
    props: {
      placeholder: "免费试用天数",
      min: 0,
    },
    rules: [{ type: "number", min: 0, message: "不能为负数", trigger: "blur" }],
    span: 12,
  },
  {
    label: "最大用户数",
    key: "max_users",
    type: "number",
    props: {
      placeholder: "最大用户数",
      min: 0,
    },
    rules: [{ required: true, message: "请输入最大用户数", trigger: "blur" }],
    span: 12,
  },
  {
    label: "最大角色数",
    key: "max_roles",
    type: "number",
    props: {
      placeholder: "最大角色数",
      min: 0,
    },
    rules: [{ required: true, message: "请输入最大角色数", trigger: "blur" }],
    span: 12,
  },
  {
    label: "最大部门数",
    key: "max_depts",
    type: "number",
    props: {
      placeholder: "最大部门数",
      min: 0,
    },
    rules: [{ required: true, message: "请输入最大部门数", trigger: "blur" }],
    span: 12,
  },
  {
    label: "最大存储(MB)",
    key: "max_storage_mb",
    type: "number",
    props: {
      placeholder: "最大存储(MB)",
      min: 0,
    },
    rules: [{ required: true, message: "请输入最大存储", trigger: "blur" }],
    span: 12,
  },
  {
    label: "速率限制",
    key: "rate_limit",
    type: "number",
    props: {
      placeholder: "请求/10秒",
      min: 10,
    },
    rules: [
      { required: true, message: "请输入速率限制", trigger: "blur" },
      { type: "number", min: 10, message: "最低 10 请求/10秒", trigger: "blur" },
    ],
    span: 12,
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    props: {
      type: "textarea",
      placeholder: "套餐描述",
      maxlength: 255,
      rows: 2,
    },
    rules: [{ max: 255, message: "最长 255 个字符", trigger: "blur" }],
    span: 24,
  },
]);

const rules = reactive({
  name: [
    { required: true, message: "请输入套餐名称", trigger: "blur" },
    { max: 100, message: "最长 100 个字符", trigger: "blur" },
  ],
  code: [
    { required: true, message: "请输入套餐编码", trigger: "blur" },
    { pattern: /^[a-zA-Z0-9]+$/, message: "仅允许字母和数字", trigger: "blur" },
    { min: 2, message: "至少 2 个字符", trigger: "blur" },
  ],
  price: [
    { required: true, message: "请输入价格", trigger: "blur" },
    { type: "number", min: 0, message: "价格不能为负数", trigger: "blur" },
  ],
  trial_days: [{ type: "number", min: 0, message: "不能为负数", trigger: "blur" }],
  max_users: [{ required: true, message: "请输入最大用户数", trigger: "blur" }],
  max_roles: [{ required: true, message: "请输入最大角色数", trigger: "blur" }],
  max_depts: [{ required: true, message: "请输入最大部门数", trigger: "blur" }],
  max_storage_mb: [{ required: true, message: "请输入最大存储", trigger: "blur" }],
  rate_limit: [
    { required: true, message: "请输入速率限制", trigger: "blur" },
    { type: "number", min: 10, message: "最低 10 请求/10秒", trigger: "blur" },
  ],
  description: [{ max: 255, message: "最长 255 个字符", trigger: "blur" }],
});

const { dialogVisible } = useCrudDialog();
const dataFormRef = ref<any>(null);
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<PackageForm>({
    formData,
    initialFormData: {
      status: 0,
      period: "month",
      sort: 0,
      price: 0,
      trial_days: 0,
      max_users: 10,
      max_roles: 5,
      max_depts: 10,
      max_storage_mb: 1024,
      rate_limit: 60,
    },
    dialogVisible,
    dataFormRef,
    formRenderKey: pkgFormRenderKey,
    detailApi: PackageAPI.detailPackage as unknown as (
      id: number
    ) => Promise<{ data: { data?: PackageForm } }>,
    createApi: PackageAPI.createPackage as unknown as (form: PackageForm) => Promise<unknown>,
    updateApi: PackageAPI.updatePackage as unknown as (
      id: number,
      form: PackageForm
    ) => Promise<unknown>,
    detailFormData,
    titles: { create: "新增套餐", update: "修改套餐", detail: "套餐详情" },
    onCreateSuccess: refreshCreate,
    onUpdateSuccess: refreshCreate,
  });

async function handleAdd() {
  createLoading.value = true;
  try {
    await handleOpenDialog("create");
  } finally {
    createLoading.value = false;
  }
}

async function deletePkgRow(id: number) {
  try {
    await confirmDelete();
    await PackageAPI.deletePackage([id]);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

async function togglePkgStatus(row: PackageTable) {
  const newStatus = row.status === 0 ? 1 : 0;
  try {
    await confirmToggleStatus(newStatus);
    await PackageAPI.batchPackageStatus({ ids: [row.id!], status: Number(newStatus) });
    // 成功提示由 axios 拦截器统一处理
    await refreshData();
  } catch {
    // 用户取消 / 接口错误（已由拦截器提示）
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await PackageAPI.deletePackage(ids);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

function handleMoreClick() {
  // 预留
}

// 菜单权限管理
const menuDialogVisible = ref(false);
const menuTreeLoading = ref(false);
const menuSaveLoading = ref(false);
const menuTreeData = ref<any[]>([]);
const menuCheckedIds = ref<number[]>([]);
const menuTreeTableRef = ref<InstanceType<typeof FaMenuTreeTable>>();
const currentMenuPkgId = ref<number>(0);

async function openMenuDialog(packageId: number) {
  currentMenuPkgId.value = packageId;
  menuTreeData.value = [];
  menuCheckedIds.value = [];
  menuTreeLoading.value = true;
  menuDialogVisible.value = true;
  try {
    const menuRes = await MenuAPI.listMenu();
    menuTreeData.value = menuRes.data.data ?? [];
    const menuIdsRes = await PackageAPI.getPackageMenus(packageId);
    menuCheckedIds.value = menuIdsRes.data.data ?? [];
  } catch {
    menuTreeData.value = [];
  } finally {
    menuTreeLoading.value = false;
  }
}

async function handleSaveMenus() {
  const checkedIds = menuTreeTableRef.value?.getCheckedIds?.() ?? [];
  if (checkedIds.length === 0) {
    ElMessage.warning("请至少选择一个菜单或功能按钮");
    return;
  }
  menuSaveLoading.value = true;
  try {
    await PackageAPI.setPackageMenus(currentMenuPkgId.value, checkedIds);
    menuDialogVisible.value = false;
  } catch {
    // 错误由全局拦截处理
  } finally {
    menuSaveLoading.value = false;
  }
}

async function handleSearchBarSearch(params: PackageSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPkgReplaceParams(params));
  getData();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    code: undefined,
    status: undefined,
  };
  void resetSearchParams();
}
</script>
