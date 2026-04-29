import request from "@/utils/request";

const API_BASE = "/campus_return/itinerary";

export interface ItineraryItem {
  id: number;
  trip_type: string;
  departure_city?: string;
  arrival_city?: string;
  departure_time?: string;
  status: string;
}

export interface ItineraryForm {
  batch_id: number;
  team_id?: number;
  user_id?: number;
  trip_type?: string;
  departure_city?: string;
  arrival_city?: string;
  departure_station?: string;
  arrival_station?: string;
  departure_time?: string;
  arrival_time?: string;
  train_no?: string;
  seat_no?: string;
  hotel_name?: string;
  hotel_address?: string;
  check_in_date?: string;
  check_out_date?: string;
  status?: string;
}

export const ItineraryAPI = {
  list: (params: { batch_id?: number; team_id?: number }) =>
    request.get<ItineraryItem[]>(`${API_BASE}/list`, { params }),

  create: (data: ItineraryForm) =>
    request.post<{ id: number }>(`${API_BASE}`, data),
};
