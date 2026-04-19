import request from "@/utils/request";

const API_PATH = "/promotion/trip";

const TripAPI = {
  getDetail(id: number) {
    return request<ApiResponse<TripItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: TripQuery) {
    return request<ApiResponse<PageResult<TripItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: TripForm) {
    return request<ApiResponse<TripItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: TripForm) {
    return request<ApiResponse<TripItem>>({
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

  updateLocation(id: number, data: { latitude: number; longitude: number; address?: string }) {
    return request<ApiResponse>({
      url: `${API_PATH}/location/${id}`,
      method: "put",
      data,
    });
  },
};

export default TripAPI;

export interface TripQuery {
  activity_id?: number;
  personnel_id?: number;
  trip_no?: string;
  departure_city?: string;
  destination_city?: string;
  trip_status?: string;
}

export interface TripForm {
  activity_id?: number;
  activity_name?: string;
  personnel_id?: number;
  personnel_name?: string;
  departure_city?: string;
  destination_city?: string;
  departure_time?: string;
  arrival_time?: string;
  transportation?: string;
  transportation_no?: string;
  hotel_name?: string;
  hotel_address?: string;
  check_in_date?: string;
  check_out_date?: string;
  trip_status?: string;
  remark?: string;
}

export interface TripItem extends TripForm, BaseType {
  trip_no: string;
  latitude?: number;
  longitude?: number;
  current_address?: string;
  trip_status: string;
}