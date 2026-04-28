import request from "@/utils/request";

const API_PATH = "/promotion/checkin";

const CheckinAPI = {
  getDetail(id: number) {
    return request<ApiResponse<CheckinItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: CheckinQuery) {
    return request<ApiResponse<PageResult<CheckinItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: CheckinForm) {
    return request<ApiResponse<CheckinItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: CheckinForm) {
    return request<ApiResponse<CheckinItem>>({
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

export default CheckinAPI;

export interface CheckinQuery {
  activity_id?: number;
  personnel_id?: number;
  checkin_type?: string;
  checkin_status?: string;
}

export interface CheckinForm {
  activity_id?: number;
  activity_name?: string;
  personnel_id?: number;
  personnel_name?: string;
  checkin_time?: string;
  checkin_type?: string;
  location_name?: string;
  latitude?: number;
  longitude?: number;
  checkin_photo?: string;
  description?: string;
  checkin_status?: string;
}

export interface CheckinItem extends CheckinForm, BaseType {
  checkin_no: string;
  checkin_type: string;
  checkin_status: string;
}
