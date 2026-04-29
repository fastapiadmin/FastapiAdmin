import request from "@/utils/request";

const API_BASE = "/campus_return/highschool";

export interface HighSchoolDockingItem {
  id: number;
  high_school_name: string;
  contact_name?: string;
  scheduled_date?: string;
  status: string;
  venue?: string;
}

export interface HighSchoolDockingForm {
  batch_id: number;
  high_school_id?: number;
  high_school_name: string;
  contact_name?: string;
  contact_phone?: string;
  contact_position?: string;
  scheduled_date?: string;
  scheduled_time?: string;
  venue?: string;
  expected_audience?: number;
  status?: string;
  remark?: string;
}

export const HighSchoolAPI = {
  listDocking: (batchId?: number) =>
    request.get<HighSchoolDockingItem[]>(`${API_BASE}/docking`, { params: { batch_id: batchId } }),

  createDocking: (data: HighSchoolDockingForm) =>
    request.post<{ id: number }>(`${API_BASE}/docking`, data),

  updateDocking: (id: number, data: Partial<HighSchoolDockingForm>) =>
    request.put<{ id: number }>(`${API_BASE}/docking/${id}`, data),
};
