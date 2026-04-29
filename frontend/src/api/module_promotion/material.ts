import request from "@/utils/request";

const API_PATH = "/promotion/material";

const MaterialAPI = {
  getDetail(id: number) {
    return request<ApiResponse<MaterialItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: MaterialQuery) {
    return request<ApiResponse<PageResult<MaterialItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: MaterialForm) {
    return request<ApiResponse<MaterialItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: MaterialForm) {
    return request<ApiResponse<MaterialItem>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  },

  delete(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete/${id}`,
      method: "delete",
    });
  },

  batchDelete(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch-delete`,
      method: "delete",
      data: ids,
    });
  },
};

export default MaterialAPI;

export interface MaterialQuery {
  name?: string;
  material_type?: string;
  storage_location?: string;
  status?: string;
}

export interface MaterialForm {
  name: string;
  material_type?: string;
  specification?: string;
  unit?: string;
  storage_location?: string;
  total_stock?: number;
  available_stock?: number;
  low_stock_threshold?: number;
  remark?: string;
}

export interface MaterialItem extends MaterialForm, BaseType {
  material_no?: string;
  material_type?: string;
  status?: string;
  low_stock_threshold?: number;
}
