import { request } from "@utils";

const API_PATH = "/platform/package";

const PackageAPI = {
  listPackage(query?: PackagePageQuery) {
    return request<ApiResponse<PageResult<PackageTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailPackage(id: number) {
    return request<ApiResponse<PackageTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createPackage(body: PackageCreateForm) {
    return request<ApiResponse<PackageTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updatePackage(id: number, body: PackageUpdateForm) {
    return request<ApiResponse<PackageTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deletePackage(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchPackageStatus(body: { ids: number[]; status: number }) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },

  getPackageMenus(packageId: number) {
    return request<ApiResponse<number[]>>({
      url: `${API_PATH}/menus/${packageId}`,
      method: "get",
    });
  },

  setPackageMenus(packageId: number, menuIds: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/menus/${packageId}/set`,
      method: "post",
      data: { menu_ids: menuIds },
    });
  },

  getPackagePlugins(packageId: number) {
    return request<ApiResponse<number[]>>({
      url: `${API_PATH}/plugins/${packageId}`,
      method: "get",
    });
  },

  setPackagePlugins(packageId: number, pluginIds: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/plugins/${packageId}/set`,
      method: "post",
      data: { plugin_ids: pluginIds },
    });
  },
};

export default PackageAPI;

export interface PackagePageQuery extends PageQuery, UserByQueryParams, TenantByQueryParams {
  name?: string;
  code?: string;
}

export interface PackageTable extends BaseType {
  name: string;
  code: string;
  sort: number;
  price: number;
  period: string;
  trial_days: number;
  max_users: number;
  max_roles: number;
  max_depts: number;
  max_storage_mb: number;
  rate_limit: number;
  status?: number;
  description?: string;
}

export interface PackageForm extends BaseFormType {
  name?: string;
  code?: string;
  sort?: number;
  price?: number;
  period?: string;
  trial_days?: number;
  max_users?: number;
  max_roles?: number;
  max_depts?: number;
  max_storage_mb?: number;
  rate_limit?: number;
  status?: number;
  description?: string;
}

export interface PackageCreateForm {
  name: string;
  code: string;
  status?: number;
  sort?: number;
  description?: string;
  price?: number;
  period?: string;
  trial_days?: number;
  max_users?: number;
  max_roles?: number;
  max_depts?: number;
  max_storage_mb?: number;
  rate_limit?: number;
}

export interface PackageUpdateForm {
  name?: string;
  code?: string;
  status?: number;
  sort?: number;
  description?: string;
  price?: number;
  period?: string;
  trial_days?: number;
  max_users?: number;
  max_roles?: number;
  max_depts?: number;
  max_storage_mb?: number;
  rate_limit?: number;
}
