import request from "@/utils/request";

const API_PATH = "/task/node";

const NodeAPI = {
  getNodeTypeOptions() {
    return request<ApiResponse<NodeType[]>>({
      url: `${API_PATH}/options`,
      method: "get",
    });
  },

  listNode(query: NodePageQuery) {
    return request<ApiResponse<PageResult<NodeTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailNode(query: number) {
    return request<ApiResponse<NodeTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createNode(body: NodeForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateNode(id: number, body: NodeForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteNode(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  clearNode() {
    return request<ApiResponse>({
      url: `${API_PATH}/clear`,
      method: "delete",
    });
  },

  executeNode(id: number, params: ExecuteNodeParams = { trigger: "now" }) {
    return request<ApiResponse<ExecuteNodeResult>>({
      url: `${API_PATH}/execute/${id}`,
      method: "post",
      data: params,
    });
  },
};

export default NodeAPI;

export interface NodePageQuery extends PageQuery {
  name?: string;
  code?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

export type TriggerType = "now" | "cron" | "interval" | "date";

export interface ExecuteNodeParams {
  trigger: TriggerType;
  trigger_args?: string;
  start_date?: string;
  end_date?: string;
}

export interface ExecuteNodeResult {
  job_id: number;
  status: string;
  trigger: TriggerType;
}

export interface NodeTable extends BaseType {
  name: string;
  code: string;
  jobstore?: string;
  executor?: string;
  trigger?: TriggerType;
  trigger_args?: string;
  func?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  start_date?: string;
  end_date?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

export interface NodeForm {
  id?: number;
  name: string;
  code?: string;
  jobstore?: string;
  executor?: string;
  func?: string;
  args?: string;
  kwargs?: string;
  coalesce?: boolean;
  max_instances?: number;
  start_date?: string;
  end_date?: string;
}

export interface NodeType {
  id: number;
  name: string;
  code: string;
  func?: string;
  args?: string;
  kwargs?: string;
}
