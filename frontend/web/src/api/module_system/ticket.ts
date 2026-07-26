import { request } from "@utils";

const API_PATH = "/system/ticket";

const TicketAPI = {
  listTicket(query?: TicketPageQuery) {
    return request<ApiResponse<PageResult<TicketTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },
  detailTicket(id: number) {
    return request<ApiResponse<TicketTable>>({ url: `${API_PATH}/detail/${id}`, method: "get" });
  },
  createTicket(body: TicketCreateForm) {
    return request<ApiResponse>({ url: `${API_PATH}/create`, method: "post", data: body });
  },
  updateTicket(id: number, body: TicketUpdateForm) {
    return request<ApiResponse>({ url: `${API_PATH}/update/${id}`, method: "put", data: body });
  },
  deleteTicket(body: number[]) {
    return request<ApiResponse>({ url: `${API_PATH}/delete`, method: "delete", data: body });
  },
  exportTicket(query?: TicketPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },
  batchTicket(body: { ids: number[]; status: number }) {
    return request<ApiResponse>({ url: `${API_PATH}/batch`, method: "put", data: body });
  },
};

export function getTicketComments(ticketId: number, params?: PageQuery) {
  return request<ApiResponse<PageResult<TicketCommentTable>>>({
    url: `${API_PATH}/${ticketId}/comments`,
    method: "get",
    params,
  });
}

export function createTicketComment(ticketId: number, data: TicketCommentCreateForm) {
  return request<ApiResponse<TicketCommentTable>>({
    url: `${API_PATH}/${ticketId}/comments`,
    method: "post",
    data,
  });
}

export default TicketAPI;

export interface TicketPageQuery extends PageQuery, UserByQueryParams {
  title?: string;
  ticket_type?: string;
  assigned_id?: number;
  status?: number;
}

export interface TicketTable extends BaseType {
  title: string;
  ticket_content?: string;
  summary?: string;
  ticket_type: string;
  images?: string;
  reply?: string;
  assigned_id?: number;
  assigned_by?: CommonType;
  status?: number;
  description?: string;
}

export interface TicketCreateForm {
  title: string;
  ticket_content?: string;
  summary?: string;
  ticket_type: string;
  images?: string;
  description?: string;
}

export interface TicketUpdateForm {
  title?: string;
  ticket_content?: string;
  summary?: string;
  ticket_type?: string;
  status?: number;
  reply?: string;
  assigned_id?: number;
  description?: string;
}

export interface TicketForm extends BaseFormType {
  title: string;
  ticket_content?: string;
  summary?: string;
  ticket_type: string;
  images?: string;
  reply?: string;
  assigned_id?: number;
  status?: number;
  description?: string;
}

// ─── 评论 ───
export interface TicketCommentTable extends BaseType {
  ticket_id: number;
  content: string;
  created_by_name?: string;
}

export interface TicketCommentPageQuery extends PageQuery {
  ticket_id: number;
}

export interface TicketCommentCreateForm {
  content: string;
}
