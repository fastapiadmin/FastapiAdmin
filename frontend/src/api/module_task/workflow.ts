import request from "@/utils/request";

const API_PATH = "/task/workflow";

const WorkflowAPI = {
  getWorkflowList(query: WorkflowPageQuery) {
    return request<ApiResponse<PageResult<WorkflowTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getWorkflowDetail(query: number) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createWorkflow(body: WorkflowForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateWorkflow(id: number, body: WorkflowForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteWorkflow(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  publishWorkflow(id: number, body: WorkflowPublishForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/publish/${id}`,
      method: "post",
      data: body,
    });
  },

  executeWorkflow(body: WorkflowExecuteForm) {
    return request<ApiResponse<WorkflowExecuteResult>>({
      url: `${API_PATH}/execute`,
      method: "post",
      data: body,
    });
  },
};

export default WorkflowAPI;
export { WorkflowAPI };

export interface WorkflowPageQuery extends PageQuery {
  name?: string;
  code?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface WorkflowTable extends BaseType {
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  nodes?: any[];
  edges?: any[];
  created_by?: CommonType;
  updated_by?: CommonType;
}

export interface WorkflowForm extends BaseFormType {
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  nodes?: any[];
  edges?: any[];
}

export interface WorkflowPublishForm {}

export interface WorkflowExecuteForm {
  workflow_id: number;
  variables?: Record<string, any>;
  business_key?: string;
  job_id?: number;
}

export interface WorkflowExecuteResult {
  workflow_id: number;
  workflow_name: string;
  status: string;
  start_time?: string;
  end_time?: string;
  variables?: Record<string, any>;
  node_results?: Record<string, any>;
}
