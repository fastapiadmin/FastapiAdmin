import request from "@/utils/request";

const API_PATH = "/application/ai";

const AiAPI = {
  listSession(query?: SessionPageQuery) {
    return request<ApiResponse<PageResult<SessionTable[]>>>({
      url: `${API_PATH}/session/list`,
      method: "get",
      params: query,
    });
  },

  detailSession(id: number) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/session/detail/${id}`,
      method: "get",
    });
  },

  createSession(body: SessionForm) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/session/create`,
      method: "post",
      data: body,
    });
  },

  updateSession(id: number, body: SessionForm) {
    return request<ApiResponse<SessionTable>>({
      url: `${API_PATH}/session/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteSession(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/session/delete`,
      method: "delete",
      data: body,
    });
  },

  listMessage(query?: MessagePageQuery) {
    return request<ApiResponse<PageResult<MessageTable[]>>>({
      url: `${API_PATH}/message/list`,
      method: "get",
      params: query,
    });
  },

  detailMessage(id: number) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/message/detail/${id}`,
      method: "get",
    });
  },

  getMessagesBySession(sessionId: number, query?: PageQuery) {
    return request<ApiResponse<PageResult<MessageTable[]>>>({
      url: `${API_PATH}/message/session/${sessionId}`,
      method: "get",
      params: query,
    });
  },

  createMessage(body: MessageForm) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/message/create`,
      method: "post",
      data: body,
    });
  },

  updateMessage(id: number, body: MessageForm) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/message/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteMessage(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/message/delete`,
      method: "delete",
      data: body,
    });
  },
};

export default AiAPI;

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

export interface MessagePageQuery extends PageQuery {
  session_id?: number;
  type?: string;
  content?: string;
  created_time?: string[];
}

export interface MessageTable extends BaseType {
  session_id: number;
  type: "user" | "assistant";
  content: string;
  timestamp: number;
  files?: Record<string, any>[];
}

export interface MessageForm extends BaseFormType {
  session_id?: number;
  type?: "user" | "assistant";
  content?: string;
  timestamp?: number;
  files?: Record<string, any>[];
}

export interface CommonType {
  id: number;
  name?: string;
  username?: string;
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

export interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: number;
  loading?: boolean;
  collapsed?: boolean;
  files?: UploadedFile[];
}

export interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  url?: string;
  file?: File;
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
  email?: string;
}
