import request from "@/utils/request";

const API_PATH = "/promotion/activity-apply";

const ActivityApplyAPI = {
  getDetail(id: number) {
    return request<ApiResponse<ActivityApplyItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: ActivityApplyQuery) {
    return request<ApiResponse<PageResult<ActivityApplyItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: ActivityApplyForm) {
    return request<ApiResponse<ActivityApplyItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: ActivityApplyForm) {
    return request<ApiResponse<ActivityApplyItem>>({
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

  approve(id: number, data: { approved: boolean; comment?: string }) {
    return request<ApiResponse>({
      url: `${API_PATH}/approve/${id}`,
      method: "put",
      data,
    });
  },
};

export default ActivityApplyAPI;

export interface ActivityApplyQuery {
  activity_name?: string;
  activity_no?: string;
  apply_status?: string;
}

export interface ActivityApplyForm {
  activity_name: string;
  activity_type?: string;
  activity_no?: string;
  target_school_id?: number;
  target_school_name?: string;
  planned_date?: string;
  end_date?: string;
  expected_headcount?: number;
  expected_budget?: number;
  contact_person?: string;
  contact_phone?: string;
  description?: string;
  apply_status?: string;
}

export interface ActivityApplyItem extends ActivityApplyForm, BaseType {
  activity_no: string;
  apply_status: string;
}