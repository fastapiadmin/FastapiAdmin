import request from "@/utils/request";

const API_PATH = "/system/customer";

const CustomerAPI = {
  listCustomer(query: CustomerPageQuery) {
    return request<ApiResponse<PageResult<CustomerTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailCustomer(query: number) {
    return request<ApiResponse<CustomerTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createCustomer(body: CustomerForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateCustomer(id: number, body: CustomerForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteCustomer(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchCustomer(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportCustomer(body: CustomerPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadCustomer() {
    return request<ApiResponse>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importCustomer(body: FormData) {
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

export default CustomerAPI;

export interface CustomerPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
}

export interface CustomerTable extends BaseType { 
  name?: string;
  code?: string;
  created_by?: creatorType;
  updated_by?: updatorType;
  tenant?: CommonType;
}

export interface CustomerForm extends BaseFormType {
  name?: string;
  code?: string;
}
