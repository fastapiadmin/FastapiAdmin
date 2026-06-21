<!-- 租户管理：Fa 布局 + useTable + renderTableOperationCell -->
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
            :create-loading="createLoading"
            @add="handleAdd"
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
      width="1000px"
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
          :label-width="'100px'"
          :data="detailFormData"
          :items="tenantDetailItems"
          max-height="75vh"
        >
          <template #logo_url="{ value }">
            <img v-if="value" :src="String(value)" class="detail-image" alt="网站 Logo" />
            <span v-else>-</span>
          </template>
          <template #favicon="{ value }">
            <img
              v-if="value"
              :src="String(value)"
              class="detail-image detail-favicon"
              alt="网站图标"
            />
            <span v-else>-</span>
          </template>
          <template #login_bg="{ value }">
            <img v-if="value" :src="String(value)" class="detail-image" alt="登录背景图" />
            <span v-else>-</span>
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <ElTabs v-model="activeTab" type="border-card" tabPosition="left">
          <ElTabPane label="基础信息" name="basic">
            <FaForm
              :key="tenantFormRenderKey"
              scrollbar
              max-height="65vh"
              ref="dataFormRef"
              v-model="formData"
              :items="basicFormItems"
              :rules="rules"
              label-suffix=":"
              :label-width="100"
              label-position="right"
              :span="12"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
              class="crud-dialog-art-form"
            />
          </ElTabPane>
          <ElTabPane label="网站信息" name="website">
            <FaForm
              v-model="formData"
              :items="websiteFormItems"
              :label-width="100"
              label-position="right"
              :span="12"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
            />
          </ElTabPane>
          <ElTabPane label="品牌标识" name="brand">
            <ElForm :model="formData" label-position="top">
              <ElRow :gutter="24">
                <ElCol :span="8">
                  <ElFormItem label="网站 Logo">
                    <FaUpload
                      v-model="formData.logo_url"
                      :data="{ type: 'tenant_logo' }"
                      name="file"
                      :max-file-size="5"
                      :show-tip="true"
                      :enable-preview="true"
                      :enable-crop="true"
                      v-bind="brandCropBind('tenant_logo')"
                    />
                  </ElFormItem>
                </ElCol>
                <ElCol :span="8">
                  <ElFormItem label="网站图标">
                    <FaUpload
                      v-model="formData.favicon"
                      :data="{ type: 'tenant_favicon' }"
                      name="file"
                      :max-file-size="5"
                      :show-tip="true"
                      :enable-preview="true"
                      :enable-crop="true"
                      v-bind="brandCropBind('tenant_favicon')"
                    />
                  </ElFormItem>
                </ElCol>
                <ElCol :span="8">
                  <ElFormItem label="登录背景图">
                    <FaUpload
                      v-model="formData.login_bg"
                      :data="{ type: 'tenant_login_bg' }"
                      name="file"
                      :max-file-size="10"
                      :show-tip="true"
                      :enable-preview="true"
                      :enable-crop="true"
                      v-bind="brandCropBind('tenant_login_bg')"
                    />
                  </ElFormItem>
                </ElCol>
              </ElRow>
            </ElForm>
          </ElTabPane>
          <ElTabPane label="安全隐私" name="security">
            <FaForm
              v-model="formData"
              :items="securityFormItems"
              :label-width="100"
              label-position="right"
              :span="12"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
            />
          </ElTabPane>
          <ElTabPane label="用户协议" name="agreement">
            <FaForm
              v-model="formData"
              :items="agreementFormItems"
              :label-width="100"
              label-position="right"
              :span="24"
              :gutter="16"
              :show-reset="false"
              :show-submit="false"
            />
          </ElTabPane>
        </ElTabs>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { useTable } from "@/hooks/core/useTable";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import TenantAPI, {
  type TenantCreateForm,
  type TenantForm,
  type TenantTable,
  type TenantUpdateForm,
} from "@/api/module_platform/tenant";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage, ElTabs, ElTabPane, ElForm, ElFormItem, ElRow, ElCol } from "element-plus";
import { h, ref } from "vue";

defineOptions({
  name: "Tenant",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type TenantSearchForm = {
  name?: string;
  code?: string;
  status?: number;
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

function buildTenantRowActions(
  row: TenantTable,
  ctx: {
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
    onToggleStatus: (id: number) => void;
  }
): TableOperationAction[] {
  const all: TableOperationAction[] = [
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
      icon: "ri:edit-2-line",
      perm: "module_system:tenant:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "toggle",
      label: row.status === 0 ? "禁用" : "启用",
      artType: "edit",
      icon: row.status === 0 ? "ri:forbid-2-line" : "ri:checkbox-circle-line",
      perm: "module_system:tenant:patch",
      run: () => ctx.onToggleStatus(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:tenant:delete",
      run: () => ctx.onDelete(row.id!),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
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
  { label: "正常", value: 0 },
  { label: "禁用", value: 1 },
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

const { selectedIds, batchDeleting, onTableSelectionChange } = useTableSelection<TenantTable>();

const createLoading = ref(false);

async function deleteTenantRow(id: number) {
  try {
    await confirmDelete();
    await TenantAPI.deleteTenant([id]);
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    ElMessage.info("删除取消");
  }
}

async function toggleTenantStatus(id: number) {
  try {
    await TenantAPI.toggleTenantStatus(id);
    // 直接更新当前行的 status，确保 UI 即时响应
    const row = (data.value as TenantTable[]).find((item) => item.id === id);
    if (row) {
      row.status = row.status === 0 ? 1 : 0;
    }
    await refreshData();
  } catch {
    ElMessage.error("状态切换失败");
  }
}

const opCtx = {
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteTenantRow,
  onToggleStatus: toggleTenantStatus,
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
    columnsFactory: resolveStatusColumns<TenantTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "租户名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "code", label: "租户编码", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 80,
        status: {
          0: { type: "success", text: "正常" },
          1: { type: "danger", text: "禁用" },
        },
      },
      { prop: "contact_name", label: "联系人", minWidth: 100, showOverflowTooltip: true },
      { prop: "contact_phone", label: "联系电话", width: 110, showOverflowTooltip: true },
      { prop: "start_time", label: "开始时间", width: 110, showOverflowTooltip: true },
      { prop: "end_time", label: "结束时间", width: 110, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 140, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 200,
        fixed: "right",
        align: "right",
        formatter: (row: TenantTable) =>
          renderTableOperationCell(buildTenantRowActions(row, opCtx)),
      },
    ]),
  },
});

const detailFormData = ref<TenantTable>({ code: "", name: "", status: 0 });

const tenantDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "租户名称", prop: "name" },
    { label: "租户编码", prop: "code" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { 0: { type: "success", text: "正常" }, 1: { type: "danger", text: "禁用" } },
      },
    },
    { label: "关联套餐ID", prop: "package_id" },
    { label: "排序", prop: "sort" },
    { label: "版本号", prop: "version" },
    { label: "联系人", prop: "contact_name" },
    { label: "联系电话", prop: "contact_phone" },
    { label: "联系邮箱", prop: "contact_email" },
    { label: "域名", prop: "domain" },
    { label: "地址", prop: "address" },
    { label: "Logo地址", prop: "logo_url", slot: "logo_url" },
    { label: "网站图标", prop: "favicon", slot: "favicon" },
    { label: "登录背景", prop: "login_bg", slot: "login_bg" },
    { label: "帮助文档", prop: "help_doc" },
    { label: "源码地址", prop: "git_code" },
    { label: "备案号", prop: "keep_record" },
    { label: "版权信息", prop: "copyright" },
    { label: "隐私政策", prop: "privacy" },
    { label: "服务条款", prop: "clause" },
    { label: "开始时间", prop: "start_time" },
    { label: "结束时间", prop: "end_time" },
    { label: "创建时间", prop: "created_time" },
    { label: "描述", prop: "description", span: 4 },
  ];

const formData = ref<TenantForm>({
  name: "",
  code: "",
  status: 0,
  description: "",
  package_id: undefined,
  start_time: undefined,
  end_time: undefined,
  contact_name: "",
  contact_phone: "",
  contact_email: "",
  address: "",
  domain: "",
  logo_url: "",
  sort: 0,
  version: "",
  favicon: "",
  login_bg: "",
  copyright: "",
  keep_record: "",
  help_doc: "",
  privacy: "",
  clause: "",
  git_code: "",
});

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
  status: 0,
  description: "",
  package_id: undefined,
  start_time: undefined,
  end_time: undefined,
  contact_name: "",
  contact_phone: "",
  contact_email: "",
  address: "",
  domain: "",
  logo_url: "",
  sort: 0,
  version: "",
  favicon: "",
  login_bg: "",
  copyright: "",
  keep_record: "",
  help_doc: "",
  privacy: "",
  clause: "",
  git_code: "",
};

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const submitLoading = ref(false);
const tenantFormRenderKey = ref(0);

function brandCropBind(key: string) {
  switch (key) {
    case "tenant_favicon":
      return {
        cropCutWidth: 64,
        cropCutHeight: 64,
        cropBoxWidth: 380,
        cropBoxHeight: 320,
        cropDialogTitle: "裁剪网站图标",
        cropInnerTitle: "调整图标",
        cropPreviewTitle: "预览",
      };
    case "tenant_logo":
      return {
        cropCutWidth: 320,
        cropCutHeight: 96,
        cropBoxWidth: 520,
        cropBoxHeight: 360,
        cropDialogTitle: "裁剪站点 Logo",
        cropInnerTitle: "调整 Logo",
        cropPreviewTitle: "预览",
      };
    case "tenant_login_bg":
      return {
        cropCutWidth: 960,
        cropCutHeight: 540,
        cropBoxWidth: 560,
        cropBoxHeight: 380,
        cropDialogTitle: "裁剪登录背景",
        cropInnerTitle: "调整背景图",
        cropPreviewTitle: "预览",
        cropFileType: "jpeg" as const,
      };
    default:
      return {};
  }
}

async function handleAdd() {
  createLoading.value = true;
  try {
    await handleOpenDialog("create");
  } finally {
    createLoading.value = false;
  }
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const detailRes = await TenantAPI.detailTenant(id);
    const detailData = detailRes.data?.data ?? detailRes.data;
    if (type === "detail") {
      dialogVisible.title = "租户详情";
      Object.assign(detailFormData.value, detailData);
    } else if (type === "update") {
      dialogVisible.title = "修改租户";
      formData.value = { ...initialFormData, ...detailData };
    }
  } else {
    dialogVisible.title = "新增租户";
    formData.value = { ...initialFormData };
    formData.value.id = undefined;
  }
  tenantFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  dataFormRef.value?.resetFields();
  dataFormRef.value?.clearValidate();
  formData.value = { ...initialFormData };
}

const activeTab = ref("basic");

const basicFormItems: FormItem[] = [
  {
    label: "租户名称",
    key: "name",
    type: "input",
    props: { placeholder: "请输入租户名称", maxlength: 100 },
  },
  {
    label: "租户编码",
    key: "code",
    type: "input",
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
    props: {
      placeholder: "请选择状态",
      style: { width: "100%" },
      options: [
        { label: "正常", value: 0 },
        { label: "禁用", value: 1 },
      ],
    },
  },
  {
    label: "关联套餐ID",
    key: "package_id",
    type: "number",
    props: { placeholder: "选填", min: 1, style: { width: "100%" } },
  },
  {
    label: "排序",
    key: "sort",
    type: "number",
    props: { placeholder: "请输入排序值", min: 0, style: { width: "100%" } },
  },
  {
    label: "联系人",
    key: "contact_name",
    type: "input",
    props: { placeholder: "请输入联系人姓名", maxlength: 64 },
  },
  {
    label: "联系电话",
    key: "contact_phone",
    type: "input",
    props: { placeholder: "请输入联系电话", maxlength: 20 },
  },
  {
    label: "联系邮箱",
    key: "contact_email",
    type: "input",
    props: { placeholder: "请输入联系邮箱", maxlength: 128 },
  },
  {
    label: "域名",
    key: "domain",
    type: "input",
    slots: {
      prepend: () => h("span", "https://"),
      append: () => h("span", ".com"),
    },
    props: { placeholder: "请输入域名", maxlength: 255 },
  },
  {
    label: "地址",
    key: "address",
    type: "input",
    props: { placeholder: "请输入地址", maxlength: 255 },
  },
  {
    label: "开始时间",
    key: "start_time",
    type: "datetime",
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
    props: {
      style: { width: "100%" },
      placeholder: "可选",
      type: "datetime",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
    },
  },
];

const websiteFormItems: FormItem[] = [
  {
    label: "版本号",
    key: "version",
    type: "input",
    props: { placeholder: "如 v1.0.0", maxlength: 20 },
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
];

const securityFormItems: FormItem[] = [
  {
    label: "帮助文档",
    key: "help_doc",
    type: "input",
    span: 24,
    props: { placeholder: "帮助文档链接", maxlength: 500 },
  },
  {
    label: "源码地址",
    key: "git_code",
    type: "input",
    span: 24,
    props: { placeholder: "Git 仓库地址", maxlength: 500 },
  },
  {
    label: "备案号",
    key: "keep_record",
    type: "input",
    span: 24,
    props: { placeholder: "ICP 备案号", maxlength: 100 },
  },
  {
    label: "版权信息",
    key: "copyright",
    type: "input",
    span: 24,
    props: { placeholder: "如 © 2024 Company", maxlength: 255 },
  },
  {
    label: "隐私政策",
    key: "privacy",
    type: "input",
    span: 24,
    props: { placeholder: "隐私政策链接", maxlength: 500 },
  },
];

const agreementFormItems: FormItem[] = [
  {
    label: "服务条款",
    key: "clause",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 5,
      maxlength: 500,
      placeholder: "服务条款链接",
    },
  },
];

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
  const valid = await (formRef as unknown as { validate: () => Promise<boolean> })
    .validate()
    .catch(() => false);
  if (!valid) return;
  submitLoading.value = true;
  const id = formData.value.id as number | undefined;
  try {
    if (id) {
      const payload: TenantUpdateForm = {
        name: formData.value.name,
        code: formData.value.code,
        status: formData.value.status,
        description: formData.value.description,
        package_id: formData.value.package_id,
        start_time: formData.value.start_time,
        end_time: formData.value.end_time,
        contact_name: formData.value.contact_name,
        contact_phone: formData.value.contact_phone,
        contact_email: formData.value.contact_email,
        address: formData.value.address,
        domain: formData.value.domain,
        logo_url: formData.value.logo_url,
        favicon: formData.value.favicon,
        login_bg: formData.value.login_bg,
        copyright: formData.value.copyright,
        keep_record: formData.value.keep_record,
        help_doc: formData.value.help_doc,
        privacy: formData.value.privacy,
        clause: formData.value.clause,
        git_code: formData.value.git_code,
        sort: formData.value.sort,
        version: formData.value.version,
      };
      await TenantAPI.updateTenant(id, payload);
      await refreshUpdate();
    } else {
      const payload: TenantCreateForm = {
        name: formData.value.name as string,
        code: formData.value.code as string,
        status: formData.value.status,
        description: formData.value.description,
        package_id: formData.value.package_id,
        start_time: formData.value.start_time,
        end_time: formData.value.end_time,
        contact_name: formData.value.contact_name,
        contact_phone: formData.value.contact_phone,
        contact_email: formData.value.contact_email,
        address: formData.value.address,
        domain: formData.value.domain,
        logo_url: formData.value.logo_url,
        favicon: formData.value.favicon,
        login_bg: formData.value.login_bg,
        copyright: formData.value.copyright,
        keep_record: formData.value.keep_record,
        help_doc: formData.value.help_doc,
        privacy: formData.value.privacy,
        clause: formData.value.clause,
        git_code: formData.value.git_code,
        sort: formData.value.sort,
        version: formData.value.version,
      };
      await TenantAPI.createTenant(payload);
      await refreshCreate();
    }
    dialogVisible.visible = false;
    dataFormRef.value?.resetFields();
    dataFormRef.value?.clearValidate();
    formData.value = { ...initialFormData };
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
.tenant-table-actions {
  :deep(.inline-flex) {
    vertical-align: middle;
  }
}

.detail-image {
  max-width: 120px;
  max-height: 80px;
  object-fit: contain;
  border: 1px solid var(--el-border-color-light);
  border-radius: 4px;
}

.detail-favicon {
  max-width: 48px;
  max-height: 48px;
}
</style>
