import request from "@/utils/request";

const API_PATH = "/system/tenant";

const TenantAPI = {
  listTenant(query: TenantPageQuery) {
    return request<ApiResponse<PageResult<TenantTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailTenant(query: number) {
    return request<ApiResponse<TenantTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createTenant(body: TenantForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateTenant(id: number, body: TenantForm) {
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

  batchTenant(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportTenant(body: TenantPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadTenant() {
    return request<ApiResponse>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importTenant(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export default TenantAPI;

export interface TenantPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
}

export interface TenantTable extends BaseType {
  name?: string;
  code?: string;
  start_time?: string;
  end_time?: string;
  max_user_count?: number;
  enable_quota_limit?: boolean;
  current_user_count?: number;
}

export interface TenantForm extends BaseFormType {
  name?: string;
  code?: string;
  start_time?: string;
  end_time?: string;
  max_user_count?: number;
  enable_quota_limit?: boolean;
}
