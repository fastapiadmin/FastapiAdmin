import request from "@/utils/request";

const API_PATH = "/ai/chat_message";

const AiChatMessageAPI = {
  listMessage(query?: MessagePageQuery) {
    return request<ApiResponse<PageResult<MessageTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailMessage(id: number) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getMessagesBySession(sessionId: number, query?: PageQuery) {
    return request<ApiResponse<PageResult<MessageTable[]>>>({
      url: `${API_PATH}/session/${sessionId}`,
      method: "get",
      params: query,
    });
  },

  createMessage(body: MessageForm) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateMessage(id: number, body: MessageForm) {
    return request<ApiResponse<MessageTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteMessage(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },
};

export default AiChatMessageAPI;

export interface MessagePageQuery extends PageQuery {
  session_id?: number;
  type?: string;
  content?: string;
  created_time?: string[];
  updated_time?: string[];
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
