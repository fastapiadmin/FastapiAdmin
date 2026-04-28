import request from "@/utils/request";

const API_PATH = "/promotion/target-school";

const TargetSchoolAPI = {
  getDetail(id: number) {
    return request<ApiResponse<TargetSchoolItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: TargetSchoolQuery) {
    return request<ApiResponse<PageResult<TargetSchoolItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: TargetSchoolForm) {
    return request<ApiResponse<TargetSchoolItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: TargetSchoolForm) {
    return request<ApiResponse<TargetSchoolItem>>({
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

export default TargetSchoolAPI;

export interface TargetSchoolQuery {
  school_name?: string;
  school_code?: string;
  school_level?: string;
  province?: string;
  city?: string;
  follow_status?: string;
}

export interface TargetSchoolForm {
  school_name: string;
  school_code?: string;
  school_level?: string;
  province?: string;
  city?: string;
  district?: string;
  address?: string;
  contact_person?: string;
  contact_phone?: string;
  follow_status?: string;
  priority_level?: number;
  student_count?: number;
  remark?: string;
}

export interface TargetSchoolItem extends TargetSchoolForm, BaseType {
  school_no: string;
  school_level: string;
  follow_status: string;
}
