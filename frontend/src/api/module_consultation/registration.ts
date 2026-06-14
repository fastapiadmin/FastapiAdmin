import request from "@/utils/request";

const API_PATH = "/consultation/registration";

const RegistrationAPI = {
  getDetail(id: number) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: RegistrationQuery) {
    return request<ApiResponse<PageResult<RegistrationItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: RegistrationForm) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: RegistrationForm) {
    return request<ApiResponse<RegistrationItem>>({
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

  approve(id: number, data: { booth_number?: string; booth_size?: string; comment?: string }) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/approve/${id}`,
      method: "post",
      data,
    });
  },

  reject(id: number, data: { comment: string }) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/reject/${id}`,
      method: "post",
      data,
    });
  },

  /** 一键报名 */
  oneClickRegister(id: number) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/one-click-register/${id}`,
      method: "post",
    });
  },

  /** 转发至招生组 */
  forwardToTeam(id: number, data: { team_leader_id?: number; assignee_ids?: number[] }) {
    return request<ApiResponse>({
      url: `${API_PATH}/forward-to-team/${id}`,
      method: "post",
      data,
    });
  },
};

export default RegistrationAPI;

export interface RegistrationQuery {
  consultation_id?: number;
  university_id?: number;
  university_name?: string;
  contact_person?: string;
  contact_phone?: string;
  registration_status?: string;
}

export interface RegistrationForm {
  consultation_id: number;
  university_id: number;
  university_name?: string;
  contact_person?: string;
  contact_phone?: string;
  contact_email?: string;
  booth_number?: string;
  booth_size?: string;
  registration_email?: string;
}

export interface RegistrationItem extends RegistrationForm, BaseType {
  consultation_name?: string;
  registration_status: string;
  registration_time?: string;
  approval_time?: string;
  approval_by?: number;
  approval_comment?: string;
  is_registered?: boolean;
  register_time?: string;
  created_id?: number;
}
