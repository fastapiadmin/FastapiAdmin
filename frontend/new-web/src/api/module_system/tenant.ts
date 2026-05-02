import request from "@/utils/http";

const API_PATH = "/system/tenant";

const TenantAPI = {
  listTenant(query?: TenantPageQuery) {
    return request<ApiResponse<PageResult<TenantTable[]>>>({
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

  batchTenant(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },
};

export default TenantAPI;

export interface TenantPageQuery extends PageQuery {
  name?: string;
  code?: string;
  status?: string;
  created_time?: string[];
}

export interface TenantTable extends BaseType {
  name: string;
  code: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantForm {
  id?: number;
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantCreateForm {
  name: string;
  code: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantUpdateForm {
  name?: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface BatchType {
  ids: number[];
  status: string;
}
