<!-- 租户管理：Art + useTable；操作列前 3 个为 FaButtonTable，其余收入「更多」下拉 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="tenantSearchItems"
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
            :perm-create="['module_system:tenant:create']"
            :perm-delete="['module_system:tenant:delete']"
            :delete-loading="batchDeleting"
            @add="handleOpenDialog('create')"
            @delete="handleBatchDelete"
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
      width="640px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="2"
          :data="detailFormData"
          :items="tenantDetailItems"
          max-height="75vh"
        />
      </template>
      <template v-else>
        <FaForm
          :key="tenantFormRenderKey"
          scrollbar
          max-height="75vh"
          ref="dataFormRef"
          v-model="formData"
          :items="tenantDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        />
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import type { ColumnOption } from "@/types/component";
import TenantAPI, {
  type TenantCreateForm,
  type TenantForm,
  type TenantTable,
  type TenantUpdateForm,
} from "@/api/module_system/tenant";
import { useAuth } from "@/hooks/core/useAuth";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import FaButtonTable from "@/components/forms/fa-button-table/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import {
  ElTag,
  ElMessage,
  ElTooltip,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
} from "element-plus";

defineOptions({
  name: "Tenant",
  inheritAttrs: false,
});

const MAX_INLINE_ROW_ACTIONS = 3;
const { hasAuth } = useAuth();

type TenantSearchForm = {
  name?: string;
  code?: string;
  status?: string;
  created_time?: string[];
};

function buildTenantReplaceParams(p: TenantSearchForm): Record<string, unknown> {
  return {
    name: p.name,
    code: p.code,
    status: p.status,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

type RowAction = {
  key: string;
  label: string;
  artType: "add" | "edit" | "delete" | "view" | "more";
  icon?: string;
  perm: string;
  disabled?: boolean;
  run: () => void;
};

function buildTenantRowActions(
  row: TenantTable,
  ctx: {
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): RowAction[] {
  const all: RowAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:tenant:query",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_system:tenant:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_system:tenant:delete",
      run: () => ctx.onDelete(row.id!),
    },
  ];
  return all.filter((a) => hasAuth(a.perm));
}

function formatTenantOperationCell(
  row: TenantTable,
  ctx: Parameters<typeof buildTenantRowActions>[1]
) {
  const actions = buildTenantRowActions(row, ctx);
  if (actions.length === 0) {
    return h("span", { class: "text-g-400" }, "—");
  }
  const inline = actions.slice(0, MAX_INLINE_ROW_ACTIONS);
  const overflow = actions.slice(MAX_INLINE_ROW_ACTIONS);

  const inlineNodes = inline.map((a) =>
    h(ElTooltip, { content: a.label, placement: "top" }, () =>
      h("span", { class: "inline-flex" }, [
        h(FaButtonTable, {
          type: a.artType,
          icon: a.icon,
          onClick: a.run,
        }),
      ])
    )
  );

  if (overflow.length === 0) {
    return h(
      "div",
      { class: "inline-flex flex-wrap items-center justify-end gap-1 tenant-table-actions" },
      inlineNodes
    );
  }

  const dropdown = h(
    ElDropdown,
    { trigger: "click" },
    {
      default: () =>
        h(ElTooltip, { content: "更多", placement: "top" }, () =>
          h("span", { class: "inline-flex align-middle" }, [
            h(FaButtonTable, {
              type: "more",
              onClick: () => {},
            }),
          ])
        ),
      dropdown: () =>
        h(
          ElDropdownMenu,
          null,
          overflow.map((a) =>
            h(
              ElDropdownItem,
              {
                key: a.key,
                disabled: a.disabled,
                onClick: () => a.run(),
              },
              () => a.label
            )
          )
        ),
    }
  );

  return h(
    "div",
    { class: "inline-flex flex-wrap items-center justify-end gap-1 tenant-table-actions" },
    [...inlineNodes, dropdown]
  );
}

const searchForm = ref<TenantSearchForm>({
  name: undefined,
  code: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "正常", value: "0" },
  { label: "禁用", value: "1" },
]);

const tenantSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "租户名称",
    key: "name",
    type: "input",
    placeholder: "请输入租户名称",
    clearable: true,
    span: 6,
  },
  {
    label: "租户编码",
    key: "code",
    type: "input",
    placeholder: "请输入租户编码",
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
const { selectedIds, batchDeleting, onTableSelectionChange } = useTableSelection<TenantTable>();

async function deleteTenantRow(id: number) {
  try {
    await confirmDelete();
    await TenantAPI.deleteTenant([id]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

const opCtx = {
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteTenantRow,
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
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: TenantAPI.listTenant,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<TenantTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "租户名称", minWidth: 140, showOverflowTooltip: true },
      { prop: "code", label: "租户编码", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: TenantTable) =>
          h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
            row.status === "0" ? "正常" : "禁用"
          ),
      },
      { prop: "start_time", label: "开始时间", width: 168, showOverflowTooltip: true },
      { prop: "end_time", label: "结束时间", width: 168, showOverflowTooltip: true },
      { prop: "description", label: "描述", minWidth: 150, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 200,
        fixed: "right",
        align: "right",
        formatter: (row: TenantTable) => formatTenantOperationCell(row, opCtx),
      },
    ],
  },
});

const detailFormData = ref<TenantTable>({ code: "", name: "", status: "0" });

const tenantDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "租户名称", prop: "name" },
    { label: "租户编码", prop: "code" },
    {
      label: "状态",
      prop: "status",
      span: 1,
      tag: {
        map: { "0": { type: "success", text: "正常" }, "1": { type: "danger", text: "禁用" } },
      },
    },
    { label: "开始时间", prop: "start_time", span: 1 },
    { label: "结束时间", prop: "end_time", span: 1 },
    { label: "描述", prop: "description" },
    { label: "创建时间", prop: "created_time" },
  ];

const formData = ref<TenantForm>({
  name: "",
  code: "",
  status: "0",
  description: "",
  start_time: undefined,
  end_time: undefined,
});

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const CODE_PATTERN = /^[A-Za-z0-9]+$/;

const validateTimeRange = (_rule: unknown, _value: unknown, callback: (e?: Error) => void) => {
  if (
    formData.value.start_time &&
    formData.value.end_time &&
    formData.value.start_time > formData.value.end_time
  ) {
    callback(new Error("结束时间不能早于开始时间"));
  } else {
    callback();
  }
};

const rules = reactive({
  name: [{ required: true, message: "请输入租户名称", trigger: "blur" }],
  code: [
    { required: true, message: "请输入租户编码", trigger: "blur" },
    {
      pattern: CODE_PATTERN,
      message: "编码仅允许字母与数字",
      trigger: "blur",
    },
  ],
  end_time: [{ validator: validateTimeRange, trigger: "change" }],
});

const initialFormData: TenantForm = {
  name: "",
  code: "",
  status: "0",
  description: "",
  start_time: undefined,
  end_time: undefined,
};

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const submitLoading = ref(false);
const tenantFormRenderKey = ref(0);

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await TenantAPI.detailTenant(id);
    if (type === "detail") {
      dialogVisible.title = "租户详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改租户";
      Object.assign(formData.value, response.data.data);
    }
  } else {
    dialogVisible.title = "新增租户";
    Object.assign(formData.value, initialFormData);
    formData.value.id = undefined;
  }
  tenantFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  dataFormRef.value?.resetFields();
  dataFormRef.value?.clearValidate();
  Object.assign(formData.value, initialFormData);
}

const tenantDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "租户名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入租户名称", maxlength: 100 },
  },
  {
    label: "租户编码",
    key: "code",
    type: "input",
    span: 24,
    props: {
      placeholder: "字母与数字，创建后不可改",
      maxlength: 100,
      disabled: dialogVisible.type === "update",
    },
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    span: 24,
    props: {
      placeholder: "请选择状态",
      style: { width: "100%" },
      options: [
        { label: "正常", value: "0" },
        { label: "禁用", value: "1" },
      ],
    },
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 3,
      maxlength: 255,
      placeholder: "请输入描述",
    },
  },
  {
    label: "开始时间",
    key: "start_time",
    type: "datetime",
    span: 24,
    props: {
      style: { width: "100%" },
      placeholder: "可选",
      type: "datetime",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
    },
  },
  {
    label: "结束时间",
    key: "end_time",
    type: "datetime",
    span: 24,
    props: {
      style: { width: "100%" },
      placeholder: "可选",
      type: "datetime",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
    },
  },
]);

async function handleSearchBarSearch(params: TenantSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildTenantReplaceParams(params));
  getData();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    code: undefined,
    status: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

async function handleSubmit() {
  const formRef = dataFormRef.value;
  if (!formRef) return;
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  const valid = await formRef.validate().catch(() => false);
  if (!valid) return;
  submitLoading.value = true;
  const id = formData.value.id as number | undefined;
  try {
    if (id) {
      const payload: TenantUpdateForm = {
        name: formData.value.name,
        start_time: formData.value.start_time,
        end_time: formData.value.end_time,
      };
      await TenantAPI.updateTenant(id, payload);
      await refreshUpdate();
    } else {
      const payload: TenantCreateForm = {
        name: formData.value.name as string,
        code: formData.value.code as string,
        start_time: formData.value.start_time,
        end_time: formData.value.end_time,
      };
      await TenantAPI.createTenant(payload);
      await refreshCreate();
    }
    dialogVisible.visible = false;
    dataFormRef.value?.resetFields();
    dataFormRef.value?.clearValidate();
    Object.assign(formData.value, initialFormData);
  } catch (error: unknown) {
    console.error(error);
  } finally {
    submitLoading.value = false;
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await TenantAPI.deleteTenant(ids);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}
</script>

<style scoped lang="scss">
::deep(.tenant-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
