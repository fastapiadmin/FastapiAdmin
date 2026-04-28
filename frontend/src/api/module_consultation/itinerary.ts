import request from "@/utils/request";

const API_PATH = "/consultation/itinerary";

const ItineraryAPI = {
  getDetail(id: number) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getList(params: ItineraryQuery) {
    return request<ApiResponse<PageResult<ItineraryItem[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params,
    });
  },

  create(data: ItineraryForm) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/create`,
      method: "post",
      data,
    });
  },

  update(id: number, data: ItineraryForm) {
    return request<ApiResponse<ItineraryItem>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data,
    });
  },

  delete(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete/${id}`,
      method: "delete",
    });
  },

  batchDelete(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/batch-delete`,
      method: "delete",
      data: ids,
    });
  },

  /** 获取看板视图 */
  getKanbanBoard(params?: KanbanBoardQuery) {
    return request<ApiResponse<KanbanBoardData>>({
      url: `${API_PATH}/kanban-board`,
      method: "get",
      params,
    });
  },

  /** 获取日历视图 */
  getCalendarBoard(params?: CalendarBoardQuery) {
    return request<ApiResponse<CalendarBoardData>>({
      url: `${API_PATH}/calendar-board`,
      method: "get",
      params,
    });
  },

  /** 移动任务到其他列 */
  moveTask(id: number, data: { board_column: string }) {
    return request<ApiResponse>({
      url: `${API_PATH}/move-task/${id}`,
      method: "post",
      data,
    });
  },
};

export default ItineraryAPI;

export interface KanbanBoardQuery {
  start_date_begin?: string;
  start_date_end?: string;
}

export interface KanbanBoardData {
  todo: ItineraryItem[];
  doing: ItineraryItem[];
  done: ItineraryItem[];
}

export interface CalendarBoardQuery {
  start_date_begin?: string;
  start_date_end?: string;
  month?: string;
}

export interface CalendarBoardData {
  [date: string]: ItineraryItem[];
}

export interface ItineraryQuery {
  consultation_id?: number;
  team_id?: number;
  itinerary_name?: string;
  itinerary_status?: string;
}

export interface ItineraryForm {
  consultation_id: number;
  team_id?: number;
  itinerary_name?: string;
  start_date: string;
  end_date?: string;
  departure_city?: string;
  destination_city?: string;
  transportation?: string;
  departure_time?: string;
  arrival_time?: string;
  transportation_no?: string;
  hotel_name?: string;
  hotel_address?: string;
  check_in_date?: string;
  check_out_date?: string;
  room_number?: string;
}

export interface ItineraryItem extends ItineraryForm, BaseType {
  itinerary_status: string;
  is_synced: boolean;
  board_column?: string;
  task_type?: string;
  auto_generated?: boolean;
}
