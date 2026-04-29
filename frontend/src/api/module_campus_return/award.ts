import request from "@/utils/request";

const API_BASE = "/campus_return/award";

export interface AwardCategoryItem {
  id: number;
  category_name: string;
  description?: string;
  quota: number;
}

export interface AwardNominationItem {
  id: number;
  user_name: string;
  nomination_reason: string;
  status: string;
  rank?: number;
}

export interface AwardNominationForm {
  batch_id: number;
  category_id: number;
  user_id: number;
  user_name: string;
  team_id?: number;
  nomination_reason: string;
  achievement_data?: Record<string, any>;
  photos?: string[];
}

export const AwardAPI = {
  listCategories: (batchId?: number) =>
    request.get<AwardCategoryItem[]>(`${API_BASE}/categories`, { params: { batch_id: batchId } }),

  listNominations: (params: { batch_id?: number; status?: string }) =>
    request.get<AwardNominationItem[]>(`${API_BASE}/nominations`, { params }),

  createNomination: (data: AwardNominationForm) =>
    request.post<{ id: number }>(`${API_BASE}/nominations`, data),

  reviewNomination: (id: number, data: { status: string; comment?: string; rank?: number }) =>
    request.put<{ id: number }>(`${API_BASE}/nominations/${id}/review`, null, { params: data }),
};
