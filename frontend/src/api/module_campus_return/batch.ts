import request from "@/utils/request";

const API_BASE = "/campus_return";

export interface BatchItem {
  id?: number;
  batch_name: string;
  year: number;
  semester: string;
  description?: string;
  recruitment_start?: string;
  recruitment_end?: string;
  activity_start?: string;
  activity_end?: string;
  registration_deadline?: string;
  status: string;
  review_type: string;
  max_teams: number;
  min_team_members: number;
  max_team_members: number;
  require_training: boolean;
  require_exam: boolean;
  exam_pass_score: number;
  require_insurance: boolean;
  require_checkin: boolean;
  min_checkin_count: number;
  is_active: boolean;
  created_time?: string;
  updated_time?: string;
}

export interface BatchForm {
  batch_name: string;
  year: number;
  semester: string;
  description?: string;
  recruitment_start?: string;
  recruitment_end?: string;
  activity_start?: string;
  activity_end?: string;
  registration_deadline?: string;
  status?: string;
  review_type?: string;
  max_teams?: number;
  min_team_members?: number;
  max_team_members?: number;
  require_training?: boolean;
  require_exam?: boolean;
  exam_pass_score?: number;
  require_insurance?: boolean;
  require_checkin?: boolean;
  min_checkin_count?: number;
  is_active?: boolean;
}

export interface BatchQuery {
  page?: number;
  pageSize?: number;
  batch_name?: string;
  year?: number;
  semester?: string;
  status?: string;
}

export const BatchAPI = {
  list: (params: BatchQuery) =>
    request.get<{ list: BatchItem[]; total: number; page: number; page_size: number }>(
      `${API_BASE}/batch`,
      { params }
    ),

  getById: (id: number) =>
    request.get<BatchItem>(`${API_BASE}/batch/${id}`),

  create: (data: BatchForm) =>
    request.post<{ id: number }>(`${API_BASE}/batch`, data),

  update: (id: number, data: BatchForm) =>
    request.put<{ id: number }>(`${API_BASE}/batch/${id}`, data),

  delete: (id: number) =>
    request.delete<void>(`${API_BASE}/batch/${id}`),

  batchDelete: (ids: number[]) =>
    request.delete<void>(`${API_BASE}/batch/batch`, { data: { ids } }),
};
