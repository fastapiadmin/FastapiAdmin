import request from "@/utils/request";

const API_PATH = "/task/node";

const NodeAPI = {
  getNodeTypes(query: NodeTypePageQuery) {
    return request<ApiResponse<PageResult<NodeType[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getNodeTypeDetail(id: number) {
    return request<ApiResponse<NodeType>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  getNodeTypeOptions() {
    return request<ApiResponse<NodeType[]>>({
      url: `${API_PATH}/options`,
      method: "get",
    });
  },

  createNodeType(body: NodeTypeForm) {
    return request<ApiResponse<NodeType>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateNodeType(id: number, body: NodeTypeForm) {
    return request<ApiResponse<NodeType>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteNodeType(ids: number[]) {
    return request<ApiResponse<null>>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: { ids },
    });
  },
};

export default NodeAPI;

export interface NodeType extends BaseType {
  code: string;
  name: string;
  category: string;
  description?: string;
  config_schema?: Record<string, any>;
  input_schema?: Record<string, any>;
  output_schema?: Record<string, any>;
  handler?: string;
  is_system?: boolean;
  is_active?: boolean;
  sort_order?: number;
  metadata?: Record<string, any>;
}

export interface NodeTypeForm extends BaseFormType {
  code: string;
  name: string;
  category?: string;
  description?: string;
  config_schema?: Record<string, any>;
  input_schema?: Record<string, any>;
  output_schema?: Record<string, any>;
  handler?: string;
  is_system?: boolean;
  is_active?: boolean;
  sort_order?: number;
  metadata?: Record<string, any>;
}

export interface NodeTypePageQuery extends PageQuery {
  code?: string;
  name?: string;
}
