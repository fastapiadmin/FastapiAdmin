import request from "@/utils/request";

const API_BASE = "/campus_return/volunteer";

export interface VolunteerHourItem {
  id: number;
  user_name: string;
  activity_name: string;
  activity_date: string;
  service_hours: number;
  second_class_credit: number;
  status: string;
}

export interface VolunteerHourForm {
  batch_id: number;
  user_id: number;
  user_name: string;
  student_number?: string;
  activity_name: string;
  activity_date: string;
  service_hours: number;
  service_type?: string;
  second_class_credit?: number;
  certificate_no?: string;
  certificate_url?: string;
  status?: string;
}

export const VolunteerAPI = {
  listHours: (params: { batch_id?: number; user_id?: number }) =>
    request.get<VolunteerHourItem[]>(`${API_BASE}/hours`, { params }),

  createHour: (data: VolunteerHourForm) =>
    request.post<{ id: number }>(`${API_BASE}/hours`, data),

  batchImport: (data: VolunteerHourForm[]) =>
    request.post<{ count: number }>(`${API_BASE}/hours/batch`, data),
};
