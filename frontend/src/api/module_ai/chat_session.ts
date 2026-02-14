import request from "@/utils/request";

const API_PATH = "/ai/chat_session";

const AiChatSessionAPI = {
  listSession(query?: SessionPageQuery) {
    return request<ApiResponse<PageResult<SessionTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailSession(id: number) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createSession(body: SessionForm) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateSession(id: number, body: SessionForm) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteSession(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },
};

export default AiChatSessionAPI;

export interface SessionPageQuery extends PageQuery {
  title?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface SessionTable extends BaseType {
  title: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

export interface SessionForm extends BaseFormType {
  title?: string;
}

export interface ChatSession {
  id: number;
  title: string;
  created_time: string;
  updated_time: string;
  message_count?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
}

export interface SessionGroup {
  title: string;
  sessions: ChatSession[];
}

export interface UserInfo {
  id: number;
  name: string;
  username: string;
  avatar?: string;
}
