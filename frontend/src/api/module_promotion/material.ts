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
  material_name?: string;
  material_type?: string;
  warehouse_location?: string;
  material_status?: string;
}

export interface MaterialForm {
  material_name: string;
  material_type?: string;
  specification?: string;
  unit?: string;
  warehouse_location?: string;
  total_stock?: number;
  available_stock?: number;
  material_status?: string;
  remark?: string;
}

export interface MaterialItem extends MaterialForm, BaseType {
  material_no: string;
  material_type: string;
  material_status: string;
}