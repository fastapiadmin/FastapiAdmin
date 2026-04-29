import request from "@/utils/request";

const API_PATH = "/ai/chat";

export const AiChatAPI = {
  getSessionList(query: {
    page_no: number;
    page_size: number;
    title?: string;
    created_at?: string[];
    updated_at?: string[];
  }) {
    return request<ApiResponse<PageResult<ChatSession[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  createSession(body: { title: string }) {
    return request<ApiResponse<ChatSession>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateSession(id: string, body: { title: string }) {
    return request<ApiResponse<ChatSession>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteSession(body: string[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  chat(body: { message: string; session_id?: string | null }) {
    return request<ApiResponse<AiChatResponse>>({
      url: `${API_PATH}/ai-chat`,
      method: "post",
      data: body,
    });
  },

  getSessionDetail(sessionId: string) {
    return request<ApiResponse<ChatSessionDetail>>({
      url: `${API_PATH}/detail/${sessionId}`,
      method: "get",
    });
  },
};

export default AiChatAPI;

export interface ChatSessionMessage {
  id: string;
  role: string;
  content: string;
  created_at: number | null;
}

export interface ChatSession {
  session_id: string;
  agent_id: string | null;
  team_id: string | null;
  team_name: string | null;
  workflow_id: string | null;
  user_id: string | null;
  session_data: Record<string, any> | null;
  agent_data: Record<string, any> | null;
  team_data: Record<string, any> | null;
  workflow_data: Record<string, any> | null;
  metadata: Record<string, any> | null;
  runs: Array<Record<string, any>> | null;
  summary: Record<string, any> | null;
  created_at: number | null;
  updated_at: number | null;

  id: string;
  title: string | null;
  created_time: string | null;
  updated_time: string | null;
  message_count: number;
  messages: ChatSessionMessage[];
}

export interface SessionGroup {
  id: string;
  title: string;
  sessions: ChatSession[];
}

export interface UserInfo {
  id: number;
  name: string;
  username: string;
  avatar: string;
  email: string;
}

export interface AiChatResponse {
  response: string;
  session_id: string;
  function_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }> | null;
}

export interface ChatSessionDetail {
  session_id: string;
  agent_id: string | null;
  team_id: string | null;
  team_name: string | null;
  workflow_id: string | null;
  user_id: string | null;
  session_data: Record<string, any> | null;
  agent_data: Record<string, any> | null;
  team_data: Record<string, any> | null;
  workflow_data: Record<string, any> | null;
  metadata: Record<string, any> | null;
  runs: Array<Record<string, any>> | null;
  summary: Record<string, any> | null;
  created_at: number | null;
  updated_at: number | null;

  id: string;
  title: string | null;
  created_time: string | null;
  updated_time: string | null;
  message_count: number;
  messages: ChatSessionMessage[];
}
