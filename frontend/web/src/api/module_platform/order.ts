import { request } from "@utils";

// ─── 平台订单 ──────────────────────────────────────────
const ORDER_API = "/platform/order";
const PAYMENT_API = "/platform/payment";
const REFUND_API = "/platform/refund";
const TENANT_ORDER_API = "/tenant/order";

const OrderAPI = {
  // ─── 订单管理 ───
  listOrders(query?: OrderPageQuery) {
    return request<ApiResponse<{ items: OrderTable[]; total: number }>>({
      url: `${ORDER_API}/list`,
      method: "get",
      params: query,
    });
  },

  detailOrder(orderId: number) {
    return request<ApiResponse<OrderTable>>({
      url: `${ORDER_API}/detail/${orderId}`,
      method: "get",
    });
  },

  createOrder(body: OrderCreateForm) {
    return request<ApiResponse<{ id: number; order_no: string }>>({
      url: `${ORDER_API}/create`,
      method: "post",
      data: body,
    });
  },

  cancelOrder(orderId: number) {
    return request<ApiResponse<{ message: string }>>({
      url: `${ORDER_API}/cancel/${orderId}`,
      method: "post",
    });
  },

  // ─── 支付操作 ───
  payOrder(orderId: number, body?: { pay_method?: string }) {
    return request<
      ApiResponse<{ order_no: string; amount: number; qr_code_url?: string; pay_url?: string }>
    >({
      url: `${PAYMENT_API}/pay/${orderId}`,
      method: "post",
      data: body,
    });
  },

  queryPaymentStatus(orderId: number) {
    return request<ApiResponse<{ paid: boolean; order_no?: string; amount?: number }>>({
      url: `${PAYMENT_API}/status/${orderId}`,
      method: "get",
    });
  },

  mockPaymentCallback(orderId: number) {
    return request<ApiResponse>({
      url: `${PAYMENT_API}/mock/callback`,
      method: "post",
      data: { order_id: orderId },
    });
  },

  // ─── 支付记录 ───
  listPaymentRecords(query?: PageQuery) {
    return request<ApiResponse<{ items: PaymentRecordTable[]; total: number }>>({
      url: `${PAYMENT_API}/record/list`,
      method: "get",
      params: query,
    });
  },

  // ─── 退款管理 ───
  listRefunds(query?: RefundPageQuery) {
    return request<ApiResponse<{ items: RefundTable[]; total: number }>>({
      url: `${REFUND_API}/list`,
      method: "get",
      params: query,
    });
  },

  approveRefund(refundId: number) {
    return request<ApiResponse<{ message: string }>>({
      url: `${REFUND_API}/approve/${refundId}`,
      method: "put",
    });
  },

  rejectRefund(refundId: number, body: { reject_reason?: string }) {
    return request<ApiResponse<{ message: string }>>({
      url: `${REFUND_API}/reject/${refundId}`,
      method: "put",
      data: body,
    });
  },

  // ─── 租户端 ───
  tenantCreateOrder(body: {
    tenant_id: number;
    package_id?: number;
    plugin_id?: number;
    order_type: string;
    pay_method?: string;
  }) {
    return request<ApiResponse<{ id: number; order_no: string }>>({
      url: `${TENANT_ORDER_API}/create`,
      method: "post",
      data: body,
    });
  },

  tenantApplyRefund(orderId: number, body: { reason: string }) {
    return request<ApiResponse<{ id: number }>>({
      url: `${TENANT_ORDER_API}/refund/apply/${orderId}`,
      method: "post",
      data: body,
    });
  },
};

export default OrderAPI;

// ─── Order 类型 ──────────────────────────────────────────

export interface OrderPageQuery extends PageQuery, TenantByQueryParams {
  order_type?: string;
}

export interface OrderTable {
  id: number;
  order_no: string;
  tenant_id: number;
  package_id?: number;
  plugin_id?: number;
  order_type: string;
  amount: number;
  period_count: number;
  status: number;
  pay_method?: string;
  pay_time?: string;
  expire_time: string;
  created_time?: string;
}

export interface OrderCreateForm {
  tenant_id: number;
  package_id?: number;
  plugin_id?: number;
  order_type: "new" | "renew" | "upgrade" | "downgrade" | "plugin";
  pay_method?: string;
}

// ─── Payment 类型 ────────────────────────────────────────

export interface PaymentRecordTable {
  id: number;
  order_id: number;
  transaction_id?: string;
  pay_method: string;
  amount: number;
  status: number;
  pay_time?: string;
  created_time?: string;
}

// ─── Refund 类型 ─────────────────────────────────────────

export interface RefundPageQuery extends PageQuery, UserByQueryParams, TenantByQueryParams {
}

export interface RefundTable {
  id: number;
  order_id: number;
  refund_no: string;
  amount: number;
  reason: string;
  status: number;
  refund_transaction_id?: string;
  reviewer_id?: number;
  review_time?: string;
  reject_reason?: string;
  created_time?: string;
}
