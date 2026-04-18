import request from "@/utils/request";

const API_PATH = "/consultation/itinerary";

const ItineraryAPI = {
  getDetail(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: ItineraryQuery) {
    return request<ApiResponse<PageResult<ItineraryItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: ItineraryForm) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: ItineraryForm) {
    return request<ApiResponse<ItineraryItem>>({
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

  confirm(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/confirm/${id}`,
      method: "post",
    });
  },

  execute(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/execute/${id}`,
      method: "post",
    });
  },

  archive(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/archive/${id}`,
      method: "post",
    });
  },

  syncCalendar(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/sync-calendar/${id}`,
      method: "post",
    });
  },

  addConsultation(id: number, consultationId: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/add-consultation/${id}`,
      method: "post",
      params: { consultation_id: consultationId },
    });
  },

  removeConsultation(id: number, consultationId: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/remove-consultation/${id}`,
      method: "post",
      params: { consultation_id: consultationId },
    });
  },

  optimizeRoute(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/optimize-route/${id}`,
      method: "post",
    });
  },
};

export default ItineraryAPI;

export interface ItineraryQuery extends PageQuery {
  name?: string;
  university_id?: number;
  team_id?: number;
  status?: string;
}

export interface ItineraryForm {
  name: string;
  description?: string;
  university_id?: number;
  team_id?: number;
  start_date: string;
  end_date: string;
  consultation_ids?: number[];
  transportation_plan?: any[];
  accommodation_plan?: any[];
  total_distance?: number;
  estimated_duration?: number;
  estimated_cost?: number;
}

export interface ItineraryItem extends ItineraryForm, BaseType {
  consultation_details?: any[];
  status: string;
  is_synced: boolean;
}
