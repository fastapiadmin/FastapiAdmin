<!-- 角色管理：Art + useTable；操作列最多 3 个外露 +「更多」 -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
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

    <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <ArtTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <ArtTableHeaderLeft
            :remove-ids="selectedIds"
            :perm-create="['module_system:role:create']"
            :perm-export="['module_system:role:export']"
            :perm-delete="['module_system:role:delete']"
            :perm-patch="['module_system:role:patch']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @export="openExportModal"
            @delete="handleBatchDelete"
            @more="handleMoreClick"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="artTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="paginationBind"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="720px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border>
            <ElDescriptionsItem label="角色名称" :span="2">
              {{ detailFormData.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="排序" :span="2">
              {{ detailFormData.order }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="角色编码" :span="2">
              {{ detailFormData.code }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="数据权限" :span="2">
              <ElTag v-if="detailFormData.data_scope === 1" type="primary">仅本人数据权限</ElTag>
              <ElTag v-else-if="detailFormData.data_scope === 2" type="info">本部门数据权限</ElTag>
              <ElTag v-else-if="detailFormData.data_scope === 3" type="warning">
                本部门及以下数据权限
              </ElTag>
              <ElTag v-else-if="detailFormData.data_scope === 4" type="success">全部数据权限</ElTag>
              <ElTag v-else type="danger">自定义数据权限</ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="所属部门" :span="2">
              <template v-if="detailFormData.depts && detailFormData.depts.length > 0">
                <ElTag
                  v-for="dept in detailFormData.depts"
                  :key="dept.id"
                  type="info"
                  style="margin-right: 4px; margin-bottom: 4px"
                >
                  {{ dept.name }}
                </ElTag>
              </template>
              <span v-else style="color: var(--el-text-color-placeholder)">-</span>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "启用" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建时间" :span="2">
              {{ detailFormData.created_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新时间" :span="2">
              {{ detailFormData.updated_time }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="4">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
          </ElDescriptions>
        </ElScrollbar>
      </template>
      <template v-else>
        <ElScrollbar max-height="75vh" :view-style="{ overflowX: 'hidden' }">
          <ElForm
            ref="dataFormRef"
            :model="formData"
            :rules="rules"
            label-suffix=":"
            label-width="auto"
            label-position="right"
          >
            <ElFormItem label="角色名称" prop="name">
              <ElInput v-model="formData.name" placeholder="请输入角色名称" />
            </ElFormItem>
            <ElFormItem label="排序" prop="order">
              <ElInputNumber
                v-model="formData.order"
                controls-position="right"
                :min="0"
                style="width: 100px"
              />
            </ElFormItem>
            <ElFormItem label="角色编码" prop="code">
              <ElInput
                v-model="formData.code"
                placeholder="字母开头，2-16位字母/数字/下划线"
                maxlength="16"
                show-word-limit
              />
            </ElFormItem>
            <ElFormItem label="状态" prop="status">
              <ElRadioGroup v-model="formData.status">
                <ElRadio value="0">启用</ElRadio>
                <ElRadio value="1">停用</ElRadio>
              </ElRadioGroup>
            </ElFormItem>
            <ElFormItem label="描述" prop="description">
              <ElInput
                v-model="formData.description"
                :rows="4"
                :maxlength="100"
                show-word-limit
                type="textarea"
                placeholder="请输入描述"
              />
            </ElFormItem>
          </ElForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton
            v-if="dialogVisible.type !== 'detail'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <PermissonDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :role-name="checkedRole.name"
      :role-id="checkedRole.id"
      @saved="refreshData"
    />

    <ArtExportDialog
      v-model="exportModalVisible"
      :content-config="roleExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive } from "vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import { renderTableOperationCell, type TableOperationAction } from "@/utils/table";
import type { IObject } from "@/components/Core/modal/types";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import type { ColumnOption } from "@/types/component";
import RoleAPI, {
  type RoleForm,
  type RoleTable,
  type TablePageQuery,
} from "@/api/module_system/role";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { useUserStore } from "@/store";
import PermissonDrawer from "./components/PermissonDrawer.vue";

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
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  if (typeof p.status === "string") {
    if (p.status === "true" || p.status === "false") {
      /* 与列表查询一致，保留字符串 */
    }
  }
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
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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
      style: { width: "340px" },
    },
  },
]);

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<RoleTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: RoleTable[]) {
  selectedRows.value = rows;
}

const drawerVisible = ref(false);
const checkedRole = ref({ id: 0, name: "" });

function handleOpenAssignPermDialog(roleId: number, roleName: string) {
  checkedRole.value = { id: roleId, name: roleName };
  drawerVisible.value = true;
}

function deleteRoleRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await RoleAPI.deleteRole([id]);
      const userStore = useUserStore();
      await userStore.getUserInfo();
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
}

const opCtx = {
  onPerm: handleOpenAssignPermDialog,
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteRoleRow,
};

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
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  const q = normalizeRoleQuery(sp);
  if (typeof q.status === "string") {
    const s = q.status;
    if (s === "true" || s === "false") {
      (q as unknown as Record<string, unknown>).status = s === "true";
    }
  }
  return q as unknown as Record<string, unknown>;
});

const roleExportContentConfig = computed(() => ({
  permPrefix: "module_system:role",
  cols: roleCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const base = { ...(exportQueryParams.value as Record<string, unknown>) };
    const merged = normalizeRoleQuery({
      ...base,
      ...params,
    } as Record<string, unknown>);
    if (typeof merged.status === "string") {
      const s = merged.status;
      if (s === "true" || s === "false") {
        (merged as unknown as Record<string, unknown>).status = s === "true";
      }
    }
    const res = await RoleAPI.exportRole(merged as TablePageQuery);
    return res.data as Blob;
  },
}));

const paginationBind = computed(() => {
  const p = pagination as unknown as {
    current?: number;
    size?: number;
    total?: number;
    page_no?: number;
    page_size?: number;
  };
  return {
    current: p.current ?? p.page_no ?? 1,
    size: p.size ?? p.page_size ?? 20,
    total: p.total ?? 0,
  };
});

const detailFormData = ref<RoleTable>({} as RoleTable);

const formData = reactive<RoleForm>({
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
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

const dataFormRef = ref();
const submitLoading = ref(false);

const initialFormData: RoleForm = {
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
};

const exportModalVisible = ref(false);

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

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await RoleAPI.detailRole(id);
    if (type === "detail") {
      dialogVisible.title = "角色详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改角色";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增角色";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.id;
    try {
      if (id) {
        await RoleAPI.updateRole(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await RoleAPI.createRole(formData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      const userStore = useUserStore();
      await userStore.getUserInfo();
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await RoleAPI.deleteRole(ids);
        const userStore = useUserStore();
        await userStore.getUserInfo();
        ElMessage.success("删除成功");
        artTableRef.value?.elTableRef?.clearSelection();
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await RoleAPI.batchRole({ ids, status });
      await refreshData();
      const userStore = useUserStore();
      await userStore.getUserInfo();
    })
    .catch(() => {});
}

function openExportModal() {
  exportModalVisible.value = true;
}
</script>

<style scoped lang="scss">
.art-full-height {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.art-table-card {
  flex: 1;
}

:deep(.role-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
