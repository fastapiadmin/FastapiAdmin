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

  validate(id: number) {
    return request<ApiResponse<CheckinItem>>({
      url: `${API_PATH}/validate/${id}`,
      method: "post",
    });
  },

  gpsValidate(id: number) {
    return request<ApiResponse<CheckinItem>>({
      url: `${API_PATH}/gps-validate/${id}`,
      method: "post",
    });
  },
};

export default CheckinAPI;

export interface CheckinQuery {
  activity_id?: number;
  personnel_id?: number;
  checkin_type?: string;
}

export interface CheckinForm {
  activity_id?: number;
  personnel_id?: number;
  checkin_time?: string;
  checkin_type?: string;
  location?: string;
  longitude?: number;
  latitude?: number;
  target_longitude?: number;
  target_latitude?: number;
  allowed_radius?: number;
  photo_urls?: string;
  remarks?: string;
}

export interface CheckinItem extends CheckinForm, BaseType {
  checkin_type: string;
  gps_validated?: number;
  gps_distance?: number;
}
