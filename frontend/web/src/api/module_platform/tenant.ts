import { request, NO_AUTH_FLAG } from "@utils";

const API_PATH = "/platform/tenant";

const TenantAPI = {
  listTenant(query?: TenantPageQuery) {
    return request<ApiResponse<PageResult<TenantTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailTenant(id: number) {
    return request<ApiResponse<TenantTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createTenant(body: TenantCreateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateTenant(id: number, body: TenantUpdateForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteTenant(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  /** 批量修改租户状态 */
  batchTenantStatus(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },

  /** 切换单个租户启用/禁用状态 */
  toggleTenantStatus(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/${id}`,
      method: "put",
    });
  },

  /** 租户续期 */
  renewTenant(id: number, body: { end_time: string }) {
    return request<ApiResponse<TenantTable>>({
      url: `${API_PATH}/renew/${id}`,
      method: "put",
      data: body,
    });
  },

  /** 套餐变更影响预览 */
  getPackageChangePreview(tenantId: number, newPackageId: number) {
    return request<ApiResponse<PackageChangePreview>>({
      url: `${API_PATH}/${tenantId}/package-change-preview`,
      method: "get",
      params: { new_package_id: newPackageId },
    });
  },

  getTenantUsers(tenantId: number) {
    return request<ApiResponse<TenantUser[]>>({
      url: `${API_PATH}/${tenantId}/users`,
      method: "get",
    });
  },

  addTenantUser(tenantId: number, body: TenantUserAddForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/${tenantId}/users`,
      method: "post",
      data: body,
    });
  },

  removeTenantUser(tenantId: number, userId: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/${tenantId}/users/${userId}`,
      method: "delete",
    });
  },

  /** 公开接口：无需登录即可获取租户配置（用于登录页等场景） */
  getTenantConfigInfo(tenantId: number) {
    return request<ApiResponse<TenantConfigItem[]>>({
      url: `${API_PATH}/${tenantId}/config/info`,
      method: "get",
      headers: {
        Authorization: NO_AUTH_FLAG,
      },
    });
  },

  /** 获取租户个性化配置 */
  getTenantConfig(tenantId: number) {
    return request<ApiResponse<TenantConfigItem[]>>({
      url: `${API_PATH}/${tenantId}/config`,
      method: "get",
    });
  },

  /** 批量更新租户个性化配置 */
  updateTenantConfig(tenantId: number, body: TenantConfigItem[]) {
    return request<ApiResponse<TenantConfigItem[]>>({
      url: `${API_PATH}/${tenantId}/config`,
      method: "put",
      data: body,
    });
  },
};

export default TenantAPI;

export interface TenantPageQuery extends PageQuery, UserByQueryParams, TenantByQueryParams {
  name?: string;
  code?: string;
}

export interface TenantTable extends BaseType {
  name: string;
  code: string;
  package_id?: number;
  start_time?: string;
  end_time?: string;
  contact_name?: string;
  contact_phone?: string;
  contact_email?: string;
  address?: string;
  domain?: string;
  logo_url?: string;
  sort?: number;
  version?: string;
  favicon?: string;
  login_bg?: string;
  copyright?: string;
  keep_record?: string;
  help_doc?: string;
  privacy?: string;
  clause?: string;
  git_code?: string;
  status?: number;
  description?: string;
}

export interface TenantForm extends BaseFormType {
  name?: string;
  code?: string;
  package_id?: number;
  start_time?: string;
  end_time?: string;
  contact_name?: string;
  contact_phone?: string;
  contact_email?: string;
  address?: string;
  domain?: string;
  logo_url?: string;
  sort?: number;
  version?: string;
  favicon?: string;
  login_bg?: string;
  copyright?: string;
  keep_record?: string;
  help_doc?: string;
  privacy?: string;
  clause?: string;
  git_code?: string;
  status?: number;
  description?: string;
}

export interface TenantCreateForm extends BaseFormType {
  name: string;
  code: string;
  package_id?: number;
  start_time?: string;
  end_time?: string;
  contact_name?: string;
  contact_phone?: string;
  contact_email?: string;
  address?: string;
  domain?: string;
  logo_url?: string;
  sort?: number;
  version?: string;
  favicon?: string;
  login_bg?: string;
  copyright?: string;
  keep_record?: string;
  help_doc?: string;
  privacy?: string;
  clause?: string;
  git_code?: string;
  status?: number;
  description?: string;
}

export interface TenantUpdateForm extends BaseFormType {
  name?: string;
  code?: string;
  package_id?: number;
  start_time?: string;
  end_time?: string;
  contact_name?: string;
  contact_phone?: string;
  contact_email?: string;
  address?: string;
  domain?: string;
  logo_url?: string;
  sort?: number;
  version?: string;
  favicon?: string;
  login_bg?: string;
  copyright?: string;
  keep_record?: string;
  help_doc?: string;
  privacy?: string;
  clause?: string;
  git_code?: string;
  status?: number;
  description?: string;
}

/** 套餐变更影响预览 */
export interface PackageChangePreview {
  new_package_id: number;
  new_package_name: string;
  affected_roles: Record<string, unknown>[];
  removed_menus: Record<string, unknown>[];
  added_menus: Record<string, unknown>[];
  quota_changes: Record<string, unknown>;
  total_affected_users: number;
}

export interface TenantUser {
  id: number;
  user_id: number;
  tenant_id: number;
  role: string;
  is_default: number;
  create_time?: string;
  username: string;
  name: string;
}

export interface TenantUserAddForm {
  user_id: number;
  role: string;
  is_default: number;
}

/** 租户配置项 */
export interface TenantConfigItem {
  config_key: string;
  config_value: string | null;
}
