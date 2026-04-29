import request from "@/utils/request";

const API_BASE = "/campus_return/registration";

export interface RegistrationItem {
  id?: number;
  batch_id: number;
  student_id: number;
  student_name: string;
  student_number?: string;
  phone?: string;
  email?: string;
  high_school_id?: number;
  high_school_name?: string;
  team_id?: number;
  motivation?: string;
  experience?: string;
  status: string;
  review_comment?: string;
  reviewed_by?: number;
  reviewed_time?: string;
  created_time?: string;
  updated_time?: string;
}

export interface RegistrationForm {
  batch_id: number;
  student_name: string;
  student_number?: string;
  phone?: string;
  email?: string;
  high_school_id?: number;
  high_school_name?: string;
  motivation?: string;
  experience?: string;
}

export interface RegistrationQuery {
  page?: number;
  pageSize?: number;
  batch_id?: number;
  status?: string;
  student_name?: string;
}

export const RegistrationAPI = {
  list: (params: RegistrationQuery) =>
    request.get<{ list: RegistrationItem[]; total: number; page: number; page_size: number }>(
      `${API_BASE}`,
      { params }
    ),

  getById: (id: number) =>
    request.get<RegistrationItem>(`${API_BASE}/${id}`),

  create: (data: RegistrationForm) =>
    request.post<{ id: number }>(`${API_BASE}`, data),

  update: (id: number, data: Partial<RegistrationForm>) =>
    request.put<{ id: number }>(`${API_BASE}/${id}`, data),

  delete: (id: number) =>
    request.delete<void>(`${API_BASE}/${id}`),

  submit: (id: number) =>
    request.post<RegistrationItem>(`${API_BASE}/${id}/submit`),

  approve: (id: number, comment?: string) =>
    request.post<RegistrationItem>(`${API_BASE}/${id}/approve`, null, { params: { comment } }),

  reject: (id: number, comment: string) =>
    request.post<RegistrationItem>(`${API_BASE}/${id}/reject`, null, { params: { comment } }),
};
