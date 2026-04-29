import request from "@/utils/request";

const API_BASE = "/campus_return/checkin";

export interface CheckInItem {
  id: number;
  checkin_type: string;
  checkin_time: string;
  location_name?: string;
  status: string;
}

export interface CheckInForm {
  batch_id: number;
  checkin_type?: string;
  checkin_time: string;
  latitude?: number;
  longitude?: number;
  location_name?: string;
  address?: string;
  photos?: string[];
  content?: string;
}

export interface SummaryItem {
  id: number;
  activity_name?: string;
  activity_date?: string;
  audience_count: number;
  status: string;
}

export interface SummaryForm {
  batch_id: number;
  activity_name?: string;
  activity_date?: string;
  audience_count?: number;
  content: string;
  photos?: string[];
  attachments?: string[];
}

export const CheckInAPI = {
  listCheckin: (params: { batch_id?: number; user_id?: number }) =>
    request.get<CheckInItem[]>(`${API_BASE}/list`, { params }),

  createCheckin: (data: CheckInForm) =>
    request.post<{ id: number }>(`${API_BASE}`, data),

  listSummary: (batchId?: number) =>
    request.get<SummaryItem[]>(`${API_BASE}/summary/list`, { params: { batch_id: batchId } }),

  createSummary: (data: SummaryForm) =>
    request.post<{ id: number }>(`${API_BASE}/summary`, data),
};
