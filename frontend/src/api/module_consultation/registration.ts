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

  approve(id: number, data: { booth_number?: string; booth_size?: string; booth_fee?: number; comment?: string }) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/approve/${id}`,
      method: "post",
      data,
    });
  },

  reject(id: number, comment: string) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/reject/${id}`,
      method: "post",
      data: { comment },
    });
  },

  cancel(id: number, reason?: string) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/cancel/${id}`,
      method: "post",
      params: { reason },
    });
  },

  confirmPayment(id: number, payment_time: string, comment?: string) {
    return request<ApiResponse<RegistrationItem>>({
      url: `${API_PATH}/confirm-payment/${id}`,
      method: "post",
      data: { payment_time, comment },
    });
  },

  getStatisticsByStatus() {
    return request<ApiResponse<Record<string, number>>>({
      url: `${API_PATH}/statistics/status`,
      method: "get",
    });
  },

  getStatisticsByConsultation(consultationId: number) {
    return request<ApiResponse<Record<string, number>>>({
      url: `${API_PATH}/statistics/consultation/${consultationId}`,
      method: "get",
    });
  },
};

export default RegistrationAPI;

export interface RegistrationQuery extends PageQuery {
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
  booth_size?: string;
  remarks?: string;
}

export interface RegistrationItem extends RegistrationForm, BaseType {
  booth_number?: string;
  booth_fee?: number;
  is_paid: boolean;
  payment_time?: string;
  registration_status: string;
  registration_time?: string;
  approval_time?: string;
  approval_by?: number;
  approval_comment?: string;
  materials_submitted?: any[];
  materials_required?: any[];
}
