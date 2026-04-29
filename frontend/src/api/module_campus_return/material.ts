import request from "@/utils/request";

const API_BASE = "/campus_return/material";

export interface MaterialItem {
  id: number;
  material_name: string;
  material_type: string;
  total_quantity: number;
  available_quantity: number;
  unit: string;
}

export interface MaterialApplicationForm {
  material_id: number;
  quantity: number;
}

export const MaterialAPI = {
  list: (batchId?: number) =>
    request.get<MaterialItem[]>(`${API_BASE}/list`, { params: { batch_id: batchId } }),

  apply: (data: MaterialApplicationForm) =>
    request.post<{ id: number }>(`${API_BASE}/apply`, null, { params: data }),
};
