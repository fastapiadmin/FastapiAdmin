import request from "@/utils/request";

const API_BASE = "/campus_return/insurance";

export interface InsurancePolicyItem {
  id: number;
  user_name: string;
  id_card: string;
  policy_no?: string;
  status: string;
  insurance_company?: string;
}

export interface InsurancePolicyForm {
  batch_id: number;
  user_id: number;
  user_name: string;
  id_card: string;
  policy_no?: string;
  insurance_company?: string;
  start_date?: string;
  end_date?: string;
  status?: string;
  premium?: number;
  coverage?: number;
}

export const InsuranceAPI = {
  listPolicies: (batchId?: number) =>
    request.get<InsurancePolicyItem[]>(`${API_BASE}/policies`, { params: { batch_id: batchId } }),

  importPolicy: (data: InsurancePolicyForm) =>
    request.post<{ id: number }>(`${API_BASE}/import`, data),
};
