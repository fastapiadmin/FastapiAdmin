import request from "@/utils/request";

const API_PATH = "/consultation/screening";

const ScreeningAPI = {
  getDetail(id: number) {
    return request<ApiResponse<ScreeningItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: ScreeningQuery) {
    return request<ApiResponse<PageResult<ScreeningItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: ScreeningForm) {
    return request<ApiResponse<ScreeningItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: ScreeningForm) {
    return request<ApiResponse<ScreeningItem>>({
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

  setDefault(id: number) {
    return request<ApiResponse<ScreeningItem>>({
      url: `${API_PATH}/set-default/${id}`,
      method: "put",
    });
  },

  getDefault() {
    return request<ApiResponse<ScreeningItem>>({
      url: `${API_PATH}/default`,
      method: "get",
    });
  },

  applyFilter(filterId: number) {
    return request<ApiResponse<any[]>>({
      url: `${API_PATH}/apply/${filterId}`,
      method: "post",
    });
  },
};

export default ScreeningAPI;

export interface ScreeningQuery {
  name?: string;
  is_default?: boolean;
}

export interface ScreeningForm {
  name: string;
  province?: string;
  city?: string;
  start_date_begin?: string;
  start_date_end?: string;
  organizer_type?: string;
  university_count_min?: number;
  university_count_max?: number;
  booth_fee_min?: number;
  booth_fee_max?: number;
  estimated_visitors_min?: number;
  estimated_visitors_max?: number;
  compliance_score_min?: number;
  compliance_score_max?: number;
  compliance_level?: string;
  source_type?: string;
  status?: string;
  order_by?: string;
  order_direction?: string;
  is_default?: boolean;
}

export interface ScreeningItem extends ScreeningForm, BaseType {
  id: number;
}
