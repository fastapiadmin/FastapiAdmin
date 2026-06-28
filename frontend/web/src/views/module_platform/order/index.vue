<template>
  <div class="fa-full-height">
    <ElTabs v-model="activeTab" @tab-change="onTabChange">
      <!-- 订单列表 -->
      <ElTabPane label="订单列表" name="orders">
        <FaSearchBar
          v-show="orderShowSearchBar"
          ref="orderSearchBarRef"
          v-model="orderSearchForm"
          :items="orderSearchItems"
          :rules="{}"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          include-audit
          @search="handleOrderSearch"
          @reset="handleOrderReset"
        />

        <ElCard class="fa-table-card" :style="{ 'margin-top': orderShowSearchBar ? '12px' : '0' }">
          <FaTableHeader
            v-model:columns="orderColumnChecks"
            v-model:showSearchBar="orderShowSearchBar"
            :loading="orderLoading"
            @refresh="getOrderData"
          />

          <FaTable
            ref="orderTableRef"
            :loading="orderLoading"
            :data="orderData"
            :columns="orderColumns"
            :pagination="orderPagination"
            @pagination:size-change="handleOrderSizeChange"
            @pagination:current-change="handleOrderCurrentChange"
          />
        </ElCard>
      </ElTabPane>

      <!-- 支付记录 -->
      <ElTabPane label="支付记录" name="payments">
        <ElCard class="fa-table-card" :style="{ 'margin-top': '0' }">
          <FaTableHeader :loading="paymentLoading" @refresh="getPaymentData" />

          <FaTable
            ref="paymentTableRef"
            :loading="paymentLoading"
            :data="paymentData"
            :columns="paymentColumns"
            :pagination="paymentPagination"
            @pagination:size-change="handlePaymentSizeChange"
            @pagination:current-change="handlePaymentCurrentChange"
          />
        </ElCard>
      </ElTabPane>

      <!-- 退款审核 -->
      <ElTabPane label="退款审核" name="refunds">
        <FaSearchBar
          v-show="refundShowSearchBar"
          ref="refundSearchBarRef"
          v-model="refundSearchForm"
          :items="refundSearchItems"
          :rules="{}"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          :button-left-limit="0"
          @search="handleRefundSearch"
          @reset="handleRefundReset"
        />

        <ElCard class="fa-table-card" :style="{ 'margin-top': refundShowSearchBar ? '12px' : '0' }">
          <FaTableHeader
            v-model:columns="refundColumnChecks"
            v-model:showSearchBar="refundShowSearchBar"
            :loading="refundLoading"
            @refresh="getRefundData"
          />

          <FaTable
            ref="refundTableRef"
            :loading="refundLoading"
            :data="refundData"
            :columns="refundColumns"
            :pagination="refundPagination"
            @pagination:size-change="handleRefundSizeChange"
            @pagination:current-change="handleRefundCurrentChange"
          />
        </ElCard>
      </ElTabPane>
    </ElTabs>

    <!-- 订单详情弹窗 -->
    <FaDialog v-model="detailVisible" title="订单详情" width="560px" :show-footer="false">
      <FaDescriptions
        v-if="orderDetail"
        :column="2"
        border
        :items="detailItems"
        :data="orderDetail"
      />
    </FaDialog>

    <!-- 驳回退款弹窗 -->
    <FaDialog v-model="rejectVisible" title="驳回退款" width="420px">
      <FaForm
        ref="rejectFormRef"
        v-model="rejectFormData"
        :items="rejectFormItems"
        :rules="rejectRules"
        :show-footer="false"
      />
      <template #footer>
        <ElButton @click="rejectVisible = false">取消</ElButton>
        <ElButton type="danger" :loading="rejectSubmitting" @click="submitReject">驳回</ElButton>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { ElMessageBox, ElButton, ElTabs, ElTabPane } from "element-plus";
import { useTable } from "@/hooks/core/useTable";
import { useAuth } from "@/hooks/core/useAuth";
import OrderAPI from "@/api/module_platform/order";
import type { OrderTable, PaymentRecordTable, RefundTable } from "@/api/module_platform/order";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";

defineOptions({ name: "Order" });

const { hasAuth } = useAuth();

// ══════════════════ Tab ════════════════════
const activeTab = ref("orders");
const orderShowSearchBar = ref(true);
const refundShowSearchBar = ref(true);

// ══════════════════ 标签函数 ════════════════════
function orderTypeLabel(t: string): string {
  const m: Record<string, string> = {
    new: "新购",
    renew: "续费",
    upgrade: "升级",
    downgrade: "降级",
  };
  return m[t] || t;
}

function payMethodLabel(m: string): string {
  const mp: Record<string, string> = { alipay: "支付宝", wxpay: "微信支付" };
  return mp[m] || m;
}

// ══════════════════ 订单列表 ════════════════════

function buildOrderRowActions(row: OrderTable): TableOperationAction[] {
  const actions: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_platform:order:query",
      run: () => showOrderDetail(row),
    },
  ];
  if (row.status === 0) {
    actions.push({
      key: "cancel",
      label: "取消",
      artType: "delete",
      perm: "module_platform:order:create",
      run: () => cancelOrder(row.id),
    });
  }
  return actions.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatOrderOpCell(row: OrderTable) {
  return renderTableOperationCell(buildOrderRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1",
  });
}

const orderSearchForm = ref<Record<string, unknown>>({ status: undefined, order_type: undefined });

const orderSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "订单状态",
    key: "status",
    type: "select",
    placeholder: "订单状态",
    span: 6,
    props: {
      clearable: true,
      options: [
        { label: "待支付", value: 0 },
        { label: "已支付", value: 1 },
        { label: "已取消", value: 2 },
        { label: "已退款", value: 3 },
        { label: "已过期", value: 4 },
      ],
    },
  },
  {
    label: "订单类型",
    key: "order_type",
    type: "select",
    placeholder: "订单类型",
    span: 6,
    props: {
      clearable: true,
      options: [
        { label: "新购", value: "new" },
        { label: "续费", value: "renew" },
        { label: "升级", value: "upgrade" },
        { label: "降级", value: "downgrade" },
      ],
    },
  },
]);

const {
  columns: orderColumns,
  columnChecks: orderColumnChecks,
  data: orderData,
  loading: orderLoading,
  pagination: orderPagination,
  getData: getOrderData,
  replaceSearchParams: replaceOrderSearchParams,
  resetSearchParams: resetOrderSearchParams,
  handleSizeChange: handleOrderSizeChange,
  handleCurrentChange: handleOrderCurrentChange,
} = useTable({
  core: {
    apiFn: OrderAPI.listOrders,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: resolveStatusColumns<OrderTable>(() => [
      { prop: "order_no", label: "订单号", minWidth: 180, showOverflowTooltip: true },
      { prop: "tenant_id", label: "租户ID", width: 80 },
      { prop: "package_id", label: "套餐ID", width: 80 },
      {
        prop: "order_type",
        label: "类型",
        width: 90,
        status: {
          new: { type: "info", text: "新购" },
          renew: { type: "info", text: "续费" },
          upgrade: { type: "info", text: "升级" },
          downgrade: { type: "info", text: "降级" },
        },
      },
      {
        prop: "amount",
        label: "金额",
        width: 120,
        formatter: (row: OrderTable) => `¥${(row.amount / 100).toFixed(2)}`,
      },
      {
        prop: "status",
        label: "状态",
        width: 90,
        status: {
          0: { type: "warning", text: "待支付" },
          1: { type: "success", text: "已支付" },
          2: { type: "info", text: "已取消" },
          3: { type: "danger", text: "已退款" },
          4: { type: "danger", text: "已过期" },
        },
      },
      {
        prop: "pay_method",
        label: "支付方式",
        width: 90,
        formatter: (row: OrderTable) => (row.pay_method ? payMethodLabel(row.pay_method) : "—"),
      },
      {
        prop: "pay_time",
        label: "支付时间",
        width: 160,
        showOverflowTooltip: true,
        formatter: (row: OrderTable) => row.pay_time || "—",
      },
      { prop: "expire_time", label: "过期时间", width: 160, showOverflowTooltip: true },
      {
        label: "操作",
        prop: "operation",
        width: 140,
        fixed: "right",
        align: "center",
        formatter: (row: OrderTable) => formatOrderOpCell(row),
      },
    ]),
  },
});

function handleOrderSearch() {
  const params: Record<string, unknown> = {};
  if (orderSearchForm.value.status !== undefined && orderSearchForm.value.status !== "") {
    params.status = orderSearchForm.value.status;
  }
  if (orderSearchForm.value.order_type) params.order_type = orderSearchForm.value.order_type;
  replaceOrderSearchParams(params);
}

function handleOrderReset() {
  orderSearchForm.value = { status: undefined, order_type: undefined };
  resetOrderSearchParams();
}

const detailVisible = ref(false);
const orderDetail = ref<OrderTable | null>(null);

async function showOrderDetail(row: OrderTable) {
  try {
    const res = await OrderAPI.detailOrder(row.id);
    const data = res.data.data as OrderTable;
    if (data) {
      data.amount = data.amount / 100;
      data.order_type = orderTypeLabel(data.order_type);
      data.pay_method = data.pay_method ? payMethodLabel(data.pay_method) : "";
    }
    orderDetail.value = data;
    detailVisible.value = true;
  } catch {
    /* ignore */
  }
}

async function cancelOrder(orderId: number) {
  try {
    await ElMessageBox.confirm("确定取消该订单吗？", "确认取消", { type: "warning" });
    await OrderAPI.cancelOrder(orderId);
    getOrderData();
  } catch {
    /* cancelled */
  }
}

const detailItems = computed<
  import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[]
>(() => {
  if (!orderDetail.value) return [];
  return [
    { label: "订单ID", prop: "id" },
    { label: "订单号", prop: "order_no" },
    { label: "租户ID", prop: "tenant_id" },
    { label: "套餐ID", prop: "package_id" },
    { label: "订单类型", prop: "order_type" },
    { label: "金额", prop: "amount" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: {
          "0": { type: "warning", text: "待支付" },
          "1": { type: "success", text: "已支付" },
          "2": { type: "info", text: "已取消" },
          "3": { type: "warning", text: "已退款" },
          "4": { type: "danger", text: "已过期" },
        },
      },
    },
    { label: "支付方式", prop: "pay_method" },
    { label: "支付时间", prop: "pay_time" },
    { label: "过期时间", prop: "expire_time" },
    { label: "创建时间", prop: "created_time" },
  ];
});

// ══════════════════ 支付记录 ════════════════════

const {
  columns: paymentColumns,
  data: paymentData,
  loading: paymentLoading,
  pagination: paymentPagination,
  getData: getPaymentData,
  handleSizeChange: handlePaymentSizeChange,
  handleCurrentChange: handlePaymentCurrentChange,
} = useTable({
  core: {
    apiFn: OrderAPI.listPaymentRecords,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: resolveStatusColumns<PaymentRecordTable>(() => [
      { prop: "order_id", label: "订单ID", width: 80 },
      {
        prop: "transaction_id",
        label: "交易流水号",
        minWidth: 220,
        showOverflowTooltip: true,
        formatter: (row: PaymentRecordTable) => row.transaction_id || "—",
      },
      {
        prop: "pay_method",
        label: "支付方式",
        width: 100,
        formatter: (row: PaymentRecordTable) => payMethodLabel(row.pay_method),
      },
      {
        prop: "amount",
        label: "金额",
        width: 120,
        formatter: (row: PaymentRecordTable) => `¥${(row.amount / 100).toFixed(2)}`,
      },
      {
        prop: "status",
        label: "状态",
        width: 90,
        status: {
          1: { type: "success", text: "成功" },
          0: { type: "danger", text: "失败" },
        },
      },
      { prop: "pay_time", label: "支付时间", width: 160, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 160, showOverflowTooltip: true },
    ]),
  },
});

// ══════════════════ 退款审核 ════════════════════

function buildRefundRowActions(row: RefundTable): TableOperationAction[] {
  if (row.status !== 0) return [];
  const actions: TableOperationAction[] = [
    {
      key: "approve",
      label: "批准",
      artType: "edit",
      perm: "module_platform:order:update",
      run: () => approveRefund(row.id),
    },
    {
      key: "reject",
      label: "驳回",
      artType: "delete",
      perm: "module_platform:order:update",
      run: () => showRejectDialog(row.id),
    },
  ];
  return actions.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatRefundOpCell(row: RefundTable) {
  const actions = buildRefundRowActions(row);
  if (actions.length === 0) return "—";
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1",
  });
}

const refundSearchForm = ref<Record<string, unknown>>({ status: undefined });

const refundSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "退款状态",
    key: "status",
    type: "select",
    placeholder: "退款状态",
    span: 6,
    props: {
      clearable: true,
      options: [
        { label: "待审核", value: 0 },
        { label: "已批准", value: 1 },
        { label: "已驳回", value: 2 },
        { label: "已完成", value: 3 },
      ],
    },
  },
]);

const {
  columns: refundColumns,
  columnChecks: refundColumnChecks,
  data: refundData,
  loading: refundLoading,
  pagination: refundPagination,
  getData: getRefundData,
  replaceSearchParams: replaceRefundSearchParams,
  resetSearchParams: resetRefundSearchParams,
  handleSizeChange: handleRefundSizeChange,
  handleCurrentChange: handleRefundCurrentChange,
} = useTable({
  core: {
    apiFn: OrderAPI.listRefunds,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: resolveStatusColumns<RefundTable>(() => [
      { prop: "refund_no", label: "退款单号", minWidth: 180, showOverflowTooltip: true },
      { prop: "order_id", label: "订单ID", width: 80 },
      {
        prop: "amount",
        label: "退款金额",
        width: 120,
        formatter: (row: RefundTable) => `¥${(row.amount / 100).toFixed(2)}`,
      },
      { prop: "reason", label: "退款原因", minWidth: 160, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 100,
        status: {
          0: { type: "warning", text: "待审核" },
          1: { type: "success", text: "已批准" },
          2: { type: "danger", text: "已驳回" },
          3: { type: "info", text: "已完成" },
        },
      },
      {
        prop: "reject_reason",
        label: "驳回原因",
        minWidth: 140,
        showOverflowTooltip: true,
        formatter: (row: RefundTable) =>
          row.reject_reason ? h("span", { style: "color: #f56c6c" }, row.reject_reason) : "—",
      },
      { prop: "review_time", label: "审核时间", width: 160, showOverflowTooltip: true },
      { prop: "created_time", label: "申请时间", width: 160, showOverflowTooltip: true },
      {
        label: "操作",
        prop: "operation",
        width: 160,
        fixed: "right",
        align: "center",
        formatter: (row: RefundTable) => formatRefundOpCell(row),
      },
    ]),
  },
});

function handleRefundSearch() {
  const params: Record<string, unknown> = {};
  if (refundSearchForm.value.status !== undefined && refundSearchForm.value.status !== "") {
    params.status = refundSearchForm.value.status;
  }
  replaceRefundSearchParams(params);
}

function handleRefundReset() {
  refundSearchForm.value = { status: undefined };
  resetRefundSearchParams();
}

async function approveRefund(refundId: number) {
  try {
    await ElMessageBox.confirm("确定批准该退款申请吗？款项将原路退回。", "确认批准", {
      type: "warning",
    });
    await OrderAPI.approveRefund(refundId);
    getRefundData();
  } catch {
    /* cancelled */
  }
}

// ══════════════════ 驳回弹窗 ════════════════════
const rejectVisible = ref(false);
const rejectSubmitting = ref(false);
const rejectFormRef = ref();
let rejectFormData = reactive({ reject_reason: "" });
const currentRefundId = ref<number | null>(null);

const rejectFormItems: FormItem[] = [
  {
    label: "驳回原因",
    key: "reject_reason",
    type: "textarea",
    span: 24,
    props: { rows: 3, maxlength: 500, placeholder: "请输入驳回原因" },
  },
];

const rejectRules = {
  reject_reason: [{ required: true, message: "请输入驳回原因", trigger: "blur" }],
};

function showRejectDialog(refundId: number) {
  currentRefundId.value = refundId;
  rejectFormData.reject_reason = "";
  rejectVisible.value = true;
}

async function submitReject() {
  const form: any = rejectFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  rejectSubmitting.value = true;
  try {
    await OrderAPI.rejectRefund(currentRefundId.value!, {
      reject_reason: rejectFormData.reject_reason,
    });
    rejectVisible.value = false;
    getRefundData();
  } catch {
    /* ignore */
  } finally {
    rejectSubmitting.value = false;
  }
}

// ══════════════════ Tab 切换 ════════════════════

function onTabChange(tab: string | number) {
  if (tab === "orders") getOrderData();
  else if (tab === "payments") getPaymentData();
  else if (tab === "refunds") getRefundData();
}

// ══════════════════ 初始化 ════════════════════

getOrderData();
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
