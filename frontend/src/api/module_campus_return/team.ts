import request from "@/utils/request";

const API_BASE = "/campus_return/team";

export interface TeamItem {
  id?: number;
  batch_id: number;
  team_name: string;
  team_code: string;
  captain_id: number;
  high_school_id?: number;
  high_school_name: string;
  status: string;
  max_members: number;
  description?: string;
  plan_date?: string;
  created_time?: string;
}

export interface TeamForm {
  batch_id: number;
  team_name: string;
  high_school_id?: number;
  high_school_name: string;
  max_members?: number;
  description?: string;
  plan_date?: string;
}

export interface TeamQuery {
  page?: number;
  pageSize?: number;
  batch_id?: number;
  status?: string;
  high_school_name?: string;
}

export const TeamAPI = {
  list: (params: TeamQuery) =>
    request.get<{ list: TeamItem[]; total: number; page: number; page_size: number }>(
      `${API_BASE}`,
      { params }
    ),

  getById: (id: number) =>
    request.get<TeamItem>(`${API_BASE}/${id}`),

  create: (data: TeamForm) =>
    request.post<{ id: number }>(`${API_BASE}`, data),

  joinByCode: (teamCode: string) =>
    request.post<{ id: number }>(`${API_BASE}/join`, null, { params: { team_code: teamCode } }),
};
