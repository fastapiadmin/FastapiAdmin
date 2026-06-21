import { request } from "@utils";

const API_PATH = "/platform/tenant";

const SelfServiceAPI = {
  /** 可选购的套餐列表 */
  getAvailablePackages() {
    return request<ApiResponse<{ packages: AvailablePackage[] }>>({
      url: `${API_PATH}/package/available`,
      method: "get",
    });
  },

  /** 套餐变更预览 */
  previewPackageChange(packageId: number) {
    return request<ApiResponse<PackageChangePreview>>({
      url: `${API_PATH}/package/preview`,
      method: "get",
      params: { target_package_id: packageId },
    });
  },

  /** 创建自助订单 */
  createOrder(body: SelfServiceOrderForm) {
    return request<ApiResponse<{ order_id: number; amount: number }>>({
      url: `${API_PATH}/order/create`,
      method: "post",
      data: body,
    });
  },

  /** 我的订单列表 */
  listMyOrders(query?: PageQuery) {
    return request<ApiResponse<PageResult<SelfServiceOrderItem>>>({
      url: `${API_PATH}/order/list`,
      method: "get",
      params: query,
    });
  },

  /** 订单详情 */
  detailMyOrder(orderId: number) {
    return request<ApiResponse<SelfServiceOrderItem>>({
      url: `${API_PATH}/order/detail/${orderId}`,
      method: "get",
    });
  },

  /** 租户工作台概览 */
  getWorkspace() {
    return request<ApiResponse<WorkspaceData>>({
      url: `${API_PATH}/workspace`,
      method: "get",
    });
  },

  /** 购买付费插件 */
  purchasePlugin(body: { plugin_id: number; pay_method?: string }) {
    return request<ApiResponse<{ id: number; order_no: string }>>({
      url: `${API_PATH}/plugin/purchase`,
      method: "post",
      data: body,
    });
  },
};

export default SelfServiceAPI;

export interface AvailablePackage {
  id: number;
  name: string;
  price: number;
  period: string;
  trial_days: number;
  max_users: number;
  max_roles: number;
  max_depts: number;
  max_storage_mb: number;
  description: string | null;
  is_current: boolean;
  available_actions: string[];
}

export interface PackageChangePreview {
  current_package: string;
  target_package: string;
  action: string;
  amount: number;
  period: string;
  gained_menus: { id: number; name: string; path: string }[];
  lost_menus: { id: number; name: string; path: string }[];
  affected_roles: string[];
  affected_users: number;
}

export interface SelfServiceOrderForm {
  package_id: number;
  order_type: "buy" | "renew" | "upgrade" | "downgrade";
  pay_method?: string;
}

export interface SelfServiceOrderItem {
  id: number;
  order_no: string;
  package_name: string;
  order_type: string;
  amount: number;
  status: number;
  pay_method?: string;
  pay_time?: string;
  created_at: string;
}

export interface WorkspaceData {
  tenant: {
    id: number;
    name: string;
    code: string;
    status: string;
    status_label: string;
    start_time: string | null;
    end_time: string | null;
    days_remaining: number;
  };
  package: {
    id: number;
    name: string;
    price: number;
    period: string;
  } | null;
  quota: {
    max_users: number;
    max_roles: number;
    max_depts: number;
    current_users: number;
    current_roles: number;
    current_depts: number;
    usage_percent: {
      users: number;
      roles: number;
      depts: number;
    };
  };
  recent_orders: {
    id: number;
    order_no: string;
    amount: number;
    order_type: string;
    status: number;
    created_at: string | null;
  }[];
}
