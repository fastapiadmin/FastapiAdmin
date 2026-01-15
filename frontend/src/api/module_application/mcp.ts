import request from "@/utils/request";

const API_PATH = "/application/ai";

export const McpAPI = {
  /**
   * 查询应用列表
   * @param query 查询参数
   */
  chatMcp(query: AiChatQuery) {
    return request<ApiResponse>({
      url: `${API_PATH}/chat`,
      method: "post",
      params: query,
    });
  },
};

export default McpAPI;

/**
 * 应用表单
 */
export interface AiChatQuery {
  message: string;
}
