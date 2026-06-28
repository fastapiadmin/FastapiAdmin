<template>
  <div class="fa-full-height">
    <ElTabs v-model="activeTab" @tab-change="onTabChange">
      <!-- 平台端：全部发票 -->
      <ElTabPane v-if="isSuperAdmin" label="发票管理" name="platform">
        <FaSearchBar
          v-show="platformShowSearchBar"
          ref="platformSearchBarRef"
          v-model="platformSearchForm"
          :items="platformSearchItems"
          :rules="{}"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          include-audit
          @search="handlePlatformSearch"
          @reset="handlePlatformReset"
        />

        <ElCard
          class="fa-table-card"
          :style="{ 'margin-top': platformShowSearchBar ? '12px' : '0' }"
        >
          <FaTableHeader
            v-model:columns="platformColumnChecks"
            v-model:showSearchBar="platformShowSearchBar"
            :loading="platformLoading"
            @refresh="getPlatformData"
          />

          <FaTable
            ref="platformTableRef"
            :loading="platformLoading"
            :data="platformData"
            :columns="platformColumns"
            :pagination="platformPagination"
            @pagination:size-change="handlePlatformSizeChange"
            @pagination:current-change="handlePlatformCurrentChange"
          />
        </ElCard>
      </ElTabPane>

      <!-- 租户端：我的发票 -->
      <ElTabPane label="我的发票" name="my">
        <ElCard class="fa-table-card" :style="{ 'margin-top': '0' }">
          <FaTableHeader :loading="myLoading" @refresh="getMyData">
            <template #left>
              <FaTableHeaderLeft
                perm-create="tenant:admin"
                :create-loading="createLoading"
                @add="handleAdd"
              />
            </template>
          </FaTableHeader>

          <FaTable
            ref="myTableRef"
            :loading="myLoading"
            :data="myData"
            :columns="myColumns"
            :pagination="myPagination"
            @pagination:size-change="handleMySizeChange"
            @pagination:current-change="handleMyCurrentChange"
          />
        </ElCard>
      </ElTabPane>
    </ElTabs>

    <!-- 申请开票弹窗 -->
    <FaDialog v-model="applyDialogVisible" title="申请开票" width="520px">
      <FaForm
        ref="applyFormRef"
        v-model="applyFormData"
        :items="applyFormItems"
        :rules="applyRules"
        :show-footer="false"
      />
      <template #footer>
        <ElButton @click="applyDialogVisible = false">取消</ElButton>
        <ElButton type="primary" :loading="applySubmitting" @click="submitApply">提交申请</ElButton>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { ElMessageBox, ElButton, ElTabs, ElTabPane } from "element-plus";
import { useTable } from "@/hooks/core/useTable";
import { useAuth } from "@/hooks/core/useAuth";
import InvoiceAPI from "@/api/module_platform/invoice";
import type { InvoiceTable } from "@/api/module_platform/invoice";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";

defineOptions({ name: "Invoice" });

const { hasAuth } = useAuth();

const activeTab = ref("my");
const isSuperAdmin = ref(true);
const platformShowSearchBar = ref(true);

// ══════════════════ 平台端：全部发票 ════════════════════

function buildPlatformRowActions(row: InvoiceTable): TableOperationAction[] {
  const actions: TableOperationAction[] = [];
  if (row.status === 0) {
    actions.push({
      key: "issue",
      label: "开具",
      artType: "edit",
      perm: "module_platform:invoice:update",
      run: () => issueInvoice(row),
    });
  }
  if (row.status === 1) {
    actions.push({
      key: "void",
      label: "作废",
      artType: "delete",
      perm: "module_platform:invoice:update",
      run: () => voidInvoice(row),
    });
  }
  return actions.filter((a) => a.perm != null && hasAuth(String(a.perm)));
}

function formatPlatformOpCell(row: InvoiceTable) {
  const actions = buildPlatformRowActions(row);
  if (actions.length === 0) return "—";
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1",
  });
}

const platformSearchForm = ref<Record<string, unknown>>({ tenant_id: "", status: undefined });

const platformSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "租户ID",
    key: "tenant_id",
    type: "input",
    placeholder: "租户ID",
    span: 6,
    props: { clearable: true },
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    placeholder: "状态",
    span: 6,
    props: {
      clearable: true,
      options: [
        { label: "待开具", value: 0 },
        { label: "已开具", value: 1 },
        { label: "已作废", value: 2 },
      ],
    },
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
  {
    label: "更新时间",
    key: "updated_time",
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

const platformSearchBarRef = ref();

const {
  columns: platformColumns,
  columnChecks: platformColumnChecks,
  data: platformData,
  loading: platformLoading,
  pagination: platformPagination,
  getData: getPlatformData,
  replaceSearchParams: replacePlatformSearchParams,
  resetSearchParams: resetPlatformSearchParams,
  handleSizeChange: handlePlatformSizeChange,
  handleCurrentChange: handlePlatformCurrentChange,
} = useTable({
  core: {
    apiFn: InvoiceAPI.listInvoices,
    apiParams: {
      page_no: 1,
      page_size: 50,
    },
    columnsFactory: resolveStatusColumns<InvoiceTable>(() => [
      { prop: "tenant_id", label: "租户ID", width: 80 },
      { prop: "invoice_no", label: "发票号", width: 180, showOverflowTooltip: true },
      { prop: "title", label: "抬头", minWidth: 180, showOverflowTooltip: true },
      {
        prop: "invoice_type",
        label: "类型",
        width: 110,
        formatter: (row) => row.invoice_type || "—",
      },
      {
        prop: "amount",
        label: "金额",
        width: 120,
        formatter: (row) => `¥${((row.amount || 0) / 100).toFixed(2)}`,
      },
      {
        prop: "status",
        label: "状态",
        width: 100,
        status: {
          0: { type: "warning", text: "待开具" },
          1: { type: "success", text: "已开具" },
          2: { type: "danger", text: "开票失败" },
          3: { type: "info", text: "已作废" },
        },
      },
      { prop: "address_info", label: "地址电话", width: 180, showOverflowTooltip: true },
      { prop: "created_time", label: "申请时间", width: 160, showOverflowTooltip: true },
      {
        label: "操作",
        prop: "operation",
        width: 150,
        fixed: "right",
        align: "center",
        formatter: (row: InvoiceTable) => formatPlatformOpCell(row),
      },
    ]),
  },
});

function handlePlatformSearch() {
  const params: Record<string, unknown> = {};
  if (platformSearchForm.value.status !== undefined && platformSearchForm.value.status !== "") {
    params.status = platformSearchForm.value.status;
  }
  const tid = parseInt(String(platformSearchForm.value.tenant_id || ""));
  if (!isNaN(tid)) params.tenant_id = tid;
  replacePlatformSearchParams(params);
}

function handlePlatformReset() {
  platformSearchForm.value = { tenant_id: "", status: undefined };
  resetPlatformSearchParams();
}

async function issueInvoice(row: InvoiceTable) {
  try {
    await InvoiceAPI.issueInvoice(row.id, {});
    getPlatformData();
  } catch {
    /* ignore */
  }
}

async function voidInvoice(row: InvoiceTable) {
  try {
    const { value } = await ElMessageBox.prompt("请输入作废原因", "作废发票", { type: "warning" });
    await InvoiceAPI.voidInvoice(row.id, value);
    getPlatformData();
  } catch {
    /* cancelled */
  }
}

// ══════════════════ 租户端：我的发票 ════════════════════

const {
  columns: myColumns,
  data: myData,
  loading: myLoading,
  pagination: myPagination,
  getData: getMyData,
  handleSizeChange: handleMySizeChange,
  handleCurrentChange: handleMyCurrentChange,
} = useTable({
  core: {
    apiFn: InvoiceAPI.tenantListInvoices,
    apiParams: {
      page_no: 1,
      page_size: 50,
    },
    columnsFactory: resolveStatusColumns<InvoiceTable>(() => [
      { prop: "invoice_no", label: "发票号", width: 180, showOverflowTooltip: true },
      { prop: "title", label: "抬头", minWidth: 180, showOverflowTooltip: true },
      {
        prop: "invoice_type",
        label: "类型",
        width: 110,
        formatter: (row) => row.invoice_type || "—",
      },
      {
        prop: "amount",
        label: "金额",
        width: 120,
        formatter: (row) => `¥${((row.amount || 0) / 100).toFixed(2)}`,
      },
      {
        prop: "status",
        label: "状态",
        width: 100,
        status: {
          0: { type: "warning", text: "待开具" },
          1: { type: "success", text: "已开具" },
          2: { type: "danger", text: "开票失败" },
          3: { type: "info", text: "已作废" },
        },
      },
      {
        prop: "created_time",
        label: "申请时间",
        width: 160,
        showOverflowTooltip: true,
        formatter: (row) => row.created_time || "—",
      },
    ]),
  },
});

// ══════════════════ 申请开票弹窗 ════════════════════

const applyDialogVisible = ref(false);
const applySubmitting = ref(false);
const applyFormRef = ref();
let applyFormData = reactive({
  order_id: null as number | null,
  title: "",
  invoice_type: "vat_normal",
  tax_no: "",
  address_info: "",
  bank_info: "",
});

const applyFormItems: FormItem[] = [
  {
    label: "关联订单ID",
    key: "order_id",
    type: "inputNumber",
    span: 24,
    props: { min: 1, placeholder: "输入已支付订单ID" },
  },
  {
    label: "发票抬头",
    key: "title",
    type: "input",
    span: 24,
    props: { placeholder: "公司全称或个人姓名", maxlength: 100 },
  },
  {
    label: "发票类型",
    key: "invoice_type",
    type: "select",
    span: 24,
    props: {
      options: [
        { label: "普通发票", value: "vat_normal" },
        { label: "增值税专用发票", value: "vat_special" },
      ],
    },
  },
  {
    label: "税号",
    key: "tax_no",
    type: "input",
    span: 24,
    props: { placeholder: "统一社会信用代码（可选）", maxlength: 30 },
  },
  {
    label: "银行信息",
    key: "bank_info",
    type: "input",
    span: 24,
    props: { placeholder: "开户行及账号（可选）", maxlength: 100 },
  },
  {
    label: "地址电话",
    key: "address_info",
    type: "input",
    span: 24,
    props: { placeholder: "注册地址及电话（专票必填）", maxlength: 200 },
  },
];

const applyRules = {
  order_id: [{ required: true, message: "请输入订单ID", trigger: "blur" }],
  title: [{ required: true, message: "请输入发票抬头", trigger: "blur" }],
};

const createLoading = ref(false);

async function handleAdd() {
  createLoading.value = true;
  try {
    openApplyDialog();
  } finally {
    createLoading.value = false;
  }
}

function openApplyDialog() {
  Object.assign(applyFormData, {
    order_id: null,
    title: "",
    invoice_type: "vat_normal",
    tax_no: "",
    address_info: "",
    bank_info: "",
  });
  applyFormRef.value?.resetFields?.();
  applyDialogVisible.value = true;
}

async function submitApply() {
  const form: any = applyFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  applySubmitting.value = true;
  try {
    await InvoiceAPI.applyInvoice({
      order_id: applyFormData.order_id!,
      title: applyFormData.title,
      invoice_type: applyFormData.invoice_type,
      tax_no: applyFormData.tax_no || undefined,
      address_info: applyFormData.address_info || undefined,
      bank_info: applyFormData.bank_info || undefined,
    });
    applyDialogVisible.value = false;
    getMyData();
  } catch {
    /* ignore */
  } finally {
    applySubmitting.value = false;
  }
}

// ══════════════════ Tab 切换 ════════════════════

function onTabChange(tab: string | number) {
  if (tab === "platform") getPlatformData();
  else if (tab === "my") getMyData();
}

// ══════════════════ 初始化 ════════════════════

getMyData();
</script>

<style scoped lang="scss">
:deep(.el-tabs) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

:deep(.el-tabs__content) {
  flex: 1;
  min-height: 0;
  overflow: visible;
}

:deep(.el-tab-pane) {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
