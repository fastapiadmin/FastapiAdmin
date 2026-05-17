<!-- 角色管理：Art + useTable；操作列最多 3 个外露 +「更多」 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="roleSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElCard
      shadow="hover"
      class="fa-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <FaTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_system:role:create']"
            :perm-export="['module_system:role:export']"
            :perm-delete="['module_system:role:delete']"
            :perm-patch="['module_system:role:patch']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @export="openExport"
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
      width="720px"
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
          :data="detailFormData"
          :items="roleDetailItems"
          max-height="75vh"
        >
          <template #data_scope="{ row }">
            <ElTag v-if="row?.data_scope === 1" type="primary">仅本人数据权限</ElTag>
            <ElTag v-else-if="row?.data_scope === 2" type="info">本部门数据权限</ElTag>
            <ElTag v-else-if="row?.data_scope === 3" type="warning">本部门及以下数据权限</ElTag>
            <ElTag v-else-if="row?.data_scope === 4" type="success">全部数据权限</ElTag>
            <ElTag v-else type="danger">自定义数据权限</ElTag>
          </template>
          <template #depts="{ row }">
            <template v-if="row?.depts && (row.depts as any[]).length > 0">
              <ElTag
                v-for="dept in row.depts as any[]"
                :key="dept.id"
                type="info"
                :style="'margin-right: 4px; margin-bottom: 4px'"
              >
                {{ dept.name }}
              </ElTag>
            </template>
            <span v-else :style="'color: var(--el-text-color-placeholder)'">-</span>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="roleFormRenderKey"
          scrollbar
          max-height="75vh"
          ref="dataFormRef"
          v-model="formData"
          :items="roleDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio value="0">启用</ElRadio>
              <ElRadio value="1">停用</ElRadio>
            </ElRadioGroup>
          </template>
        </FaForm>
      </template>
    </FaDialog>

    <FaPermissonDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :role-name="checkedRole.name"
      :role-id="checkedRole.id"
      @saved="refreshData"
    />

    <FaExportDialog
      v-model="exportVisible"
      :content-config="roleExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import type { ColumnOption } from "@/types/component";
import RoleAPI, {
  type RoleForm,
  type RoleTable,
  type TablePageQuery,
} from "@/api/module_system/role";
import { useAuth } from "@/hooks/core/useAuth";
import { useUserStore } from "@stores";
import type { IObject } from "@/components/modal/types";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElTag, ElMessage } from "element-plus";
import FaPermissonDrawer from "./components/FaPermissonDrawer.vue";

defineOptions({
  name: "Role",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type RoleSearchForm = {
  name?: string;
  status?: string;
  created_time?: string[];
};

function normalizeRoleQuery(params: Record<string, unknown>): TablePageQuery {
  const p = cleanEmptyArrayParams({ ...params });
  return p as unknown as TablePageQuery;
}

function buildRoleReplaceParams(p: RoleSearchForm): Record<string, unknown> {
  return {
    name: p.name,
    status: p.status,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

function dataScopeTag(row: RoleTable) {
  const ds = row.data_scope;
  if (ds === 1) return h(ElTag, { type: "primary" }, () => "仅本人数据权限");
  if (ds === 2) return h(ElTag, { type: "info" }, () => "本部门数据权限");
  if (ds === 3) return h(ElTag, { type: "warning" }, () => "本部门及以下数据权限");
  if (ds === 4) return h(ElTag, { type: "success" }, () => "全部数据权限");
  return h(ElTag, { type: "danger" }, () => "自定义数据权限");
}

function deptsCell(row: RoleTable) {
  const list = row.depts;
  if (!list?.length) {
    return h("span", { style: { color: "var(--el-text-color-placeholder)" } }, "-");
  }
  const tags = list
    .slice(0, 3)
    .map((dept) =>
      h(
        ElTag,
        { key: dept.id, type: "info", style: { marginRight: "4px", marginBottom: "4px" } },
        () => dept.name ?? ""
      )
    );
  if (list.length > 3) {
    tags.push(
      h(ElTag, { type: "info", style: { marginBottom: "4px" } }, () => `+${list.length - 3}`)
    );
  }
  return h("span", { class: "inline-flex flex-wrap items-center" }, tags);
}

function buildRoleRowActions(
  row: RoleTable,
  ctx: {
    onPerm: (id: number, name: string) => void;
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): TableOperationAction[] {
  const isSys = row.id === 1;
  const warnSys = () => ElMessage.warning("系统默认角色，不可操作");

  const all: TableOperationAction[] = [
    {
      key: "perm",
      label: "分配权限",
      artType: "view",
      icon: "ri:shield-keyhole-line",
      iconColor: "var(--el-color-primary)",
      perm: "module_system:role:permission",
      disabled: isSys,
      run: () => {
        if (isSys) {
          warnSys();
          return;
        }
        ctx.onPerm(row.id!, row.name);
      },
    },
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:role:detail",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:role:update",
      disabled: isSys,
      run: () => {
        if (isSys) {
          warnSys();
          return;
        }
        ctx.onEdit(row.id!);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:role:delete",
      disabled: isSys,
      run: () => {
        if (isSys) {
          warnSys();
          return;
        }
        ctx.onDelete(row.id!);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatRoleOperationCell(row: RoleTable, ctx: Parameters<typeof buildRoleRowActions>[1]) {
  return renderTableOperationCell(buildRoleRowActions(row, ctx), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 role-table-actions",
  });
}

const searchForm = ref<RoleSearchForm>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "true" },
  { label: "停用", value: "false" },
]);

const roleSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "角色名称",
    key: "name",
    type: "input",
    placeholder: "请输入角色名称",
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
  {
    label: "创建时间",
    key: "created_time",
    type: "datetimerange",
    span: 6,
    props: {
      type: "datetimerange",
      rangeSeparator: "至",
      startPlaceholder: "开始日期",
      endPlaceholder: "结束日期",
      format: "YYYY-MM-DD HH:mm:ss",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
      style: { width: "100%" },
    },
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);

// ─── 表格多选 ───
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<RoleTable>();

const drawerVisible = ref(false);
const checkedRole = ref({ id: 0, name: "" });

function handleOpenAssignPermDialog(roleId: number, roleName: string) {
  checkedRole.value = { id: roleId, name: roleName };
  drawerVisible.value = true;
}

async function deleteRoleRow(id: number) {
  try {
    await confirmDelete();
    await RoleAPI.deleteRole([id]);
    const userStore = useUserStore();
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<RoleTable>({} as RoleTable);

const roleDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "角色名称", prop: "name" },
    { label: "排序", prop: "order" },
    { label: "角色编码", prop: "code" },
    { label: "数据权限", prop: "data_scope", slot: "data_scope" },
    { label: "所属部门", prop: "depts", slot: "depts" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
    { label: "描述", prop: "description", span: 4 },
  ];

const formData = ref<RoleForm>({
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
});

const CODE_PATTERN = /^[A-Za-z][A-Za-z0-9_]{1,15}$/;

const rules = reactive({
  name: [{ required: true, message: "请输入角色名称", trigger: "blur" }],
  code: [
    { required: true, message: "请输入角色编码", trigger: "blur" },
    {
      pattern: CODE_PATTERN,
      message: "字母开头，2-16位字母/数字/下划线",
      trigger: "blur",
    },
  ],
  order: [{ required: true, message: "请输入角色排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const roleFormRenderKey = ref(0);

const initialFormData: RoleForm = {
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
};

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } = useCrudForm<RoleForm>({
  formData,
  initialFormData,
  dialogVisible,
  dataFormRef,
  formRenderKey: roleFormRenderKey,
  detailApi: RoleAPI.detailRole,
  createApi: RoleAPI.createRole,
  updateApi: RoleAPI.updateRole,
  titles: { create: "新增角色", update: "修改角色", detail: "角色详情" },
  detailFormData,
  onCreateSuccess: async () => {
    await refreshCreate();
  },
  onUpdateSuccess: async () => {
    await refreshUpdate();
  },
  onSubmitSuccess: async () => {
    const userStore = useUserStore();
    await userStore.getUserInfo();
  },
});

const opCtx = {
  onPerm: handleOpenAssignPermDialog,
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteRoleRow,
};

const roleDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "角色名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入角色名称" },
  },
  {
    label: "排序",
    key: "order",
    type: "number",
    span: 24,
    props: {
      controlsPosition: "right",
      min: 0,
      style: { width: "100px" },
    },
  },
  {
    label: "角色编码",
    key: "code",
    type: "input",
    span: 24,
    props: {
      placeholder: "字母开头，2-16位字母/数字/下划线",
      maxlength: 16,
      showWordLimit: true,
    },
  },
  {
    label: "状态",
    key: "status",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
]);

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
  searchParams,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: RoleAPI.listRole,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<RoleTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "角色名称", minWidth: 100, showOverflowTooltip: true },
      { prop: "code", label: "角色编码", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "data_scope",
        label: "数据权限",
        minWidth: 200,
        formatter: (row: RoleTable) => dataScopeTag(row),
      },
      {
        prop: "depts",
        label: "所属部门",
        minWidth: 200,
        formatter: (row: RoleTable) => deptsCell(row),
      },
      { prop: "order", label: "排序", width: 80, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: RoleTable) =>
          h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
            row.status === "0" ? "启用" : "停用"
          ),
      },
      { prop: "description", label: "描述", minWidth: 100, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: RoleTable) => formatRoleOperationCell(row, opCtx),
      },
    ],
  },
});

const roleCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<RoleTable>) => {
    const t = (c as { type?: string }).type;
    return {
      prop: c.prop,
      label: c.label,
      type: t === "selection" ? ("selection" as const) : ("default" as const),
      show: true,
    };
  })
);

const exportQueryParams = computed(() => {
  const sp = stripPaginationParams(searchParams as Record<string, unknown>);
  return normalizeRoleQuery(sp) as unknown as Record<string, unknown>;
});

const roleExportContentConfig = computed(() => ({
  permPrefix: "module_system:role",
  cols: roleCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const base = { ...(exportQueryParams.value as Record<string, unknown>) };
    const merged = normalizeRoleQuery({ ...base, ...params } as Record<string, unknown>);
    const res = await RoleAPI.exportRole(merged as TablePageQuery);
    return res.data as Blob;
  },
}));

const { exportVisible, openExport } = useImportExport();

async function handleSearchBarSearch(params: RoleSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildRoleReplaceParams(params));
  getData();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await RoleAPI.deleteRole(ids);
    const userStore = useUserStore();
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

async function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  try {
    await confirmToggleStatus(status);
    await RoleAPI.batchRole({ ids, status });
    await refreshData();
    const userStore = useUserStore();
    await userStore.getUserInfo();
  } catch {
    // 用户取消
  }
}
</script>
