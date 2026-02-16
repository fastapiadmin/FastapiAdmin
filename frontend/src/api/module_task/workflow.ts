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

  validateWorkflow(body: WorkflowValidateForm) {
    return request<ApiResponse<WorkflowValidateResult>>({
      url: `${API_PATH}/validate`,
      method: "post",
      data: body,
    });
  },

  getTemplates() {
    return request<ApiResponse<WorkflowTable[]>>({
      url: `${API_PATH}/templates`,
      method: "get",
    });
  },

  exportWorkflow(id: number) {
    return request<ApiResponse<WorkflowExportData>>({
      url: `${API_PATH}/export/${id}`,
      method: "get",
    });
  },

  importWorkflow(body: WorkflowImportData) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/import`,
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

  pauseWorkflow(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/pause/${id}`,
      method: "post",
    });
  },

  resumeWorkflow(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/resume/${id}`,
      method: "post",
    });
  },

  terminateWorkflow(id: number) {
    return request<ApiResponse>({
      url: `${API_PATH}/terminate/${id}`,
      method: "post",
    });
  },
};

const WorkflowRunAPI = {
  getWorkflowRunList(query: WorkflowRunPageQuery) {
    return request<ApiResponse<PageResult<WorkflowRunTable[]>>>({
      url: `${API_PATH}/run/list`,
      method: "get",
      params: query,
    });
  },

  getWorkflowRunDetail(id: number) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/detail/${id}`,
      method: "get",
    });
  },

  createWorkflowRun(body: WorkflowRunForm) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/create`,
      method: "post",
      data: body,
    });
  },

  updateWorkflowRun(id: number, body: WorkflowRunUpdateForm) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteWorkflowRun(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/run/delete`,
      method: "delete",
      data: { ids },
    });
  },

  clearWorkflowRun() {
    return request<ApiResponse>({
      url: `${API_PATH}/run/clear`,
      method: "delete",
    });
  },

  cancelWorkflowRun(id: number) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/cancel/${id}`,
      method: "post",
    });
  },

  retryWorkflowRun(id: number, retryCount: number = 1) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/retry/${id}`,
      method: "post",
      params: { retry_count: retryCount },
    });
  },

  pauseWorkflowRun(id: number) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/pause/${id}`,
      method: "post",
    });
  },

  resumeWorkflowRun(id: number) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/resume/${id}`,
      method: "post",
    });
  },

  terminateWorkflowRun(id: number) {
    return request<ApiResponse<WorkflowRunTable>>({
      url: `${API_PATH}/run/terminate/${id}`,
      method: "post",
    });
  },

  getWorkflowRunLogList(query: WorkflowRunLogPageQuery) {
    return request<ApiResponse<PageResult<WorkflowRunLogTable[]>>>({
      url: `${API_PATH}/run/log/list`,
      method: "get",
      params: query,
    });
  },
};

export default WorkflowAPI;
export { WorkflowAPI, WorkflowRunAPI };

export interface WorkflowPageQuery extends PageQuery {
  name?: string;
  code?: string;
  status?: string;
  category?: string;
  is_template?: boolean;
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
  version?: string;
  category?: string;
  tags?: string[];
  is_template?: boolean;
  template_id?: number;
  published_at?: string;
  published_by?: number;
  metadata?: Record<string, any>;
  canvas_state?: Record<string, any>;
  thumbnail?: string;
  statistics?: Record<string, any>;
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
  version?: string;
  category?: string;
  tags?: string[];
  is_template?: boolean;
  template_id?: number;
  metadata?: Record<string, any>;
}

export interface WorkflowPublishForm {
  version?: string;
}

export interface WorkflowValidateForm {
  nodes: any[];
  edges: any[];
}

export interface WorkflowValidateResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
  stats: Record<string, any>;
}

export interface WorkflowExportData {
  id: number;
  name: string;
  code: string;
  description?: string;
  nodes: Record<string, any>;
  edges: Record<string, any>;
  version: string;
  category?: string;
  metadata?: Record<string, any>;
  exportedAt: string;
}

export interface WorkflowImportData {
  name?: string;
  code?: string;
  description?: string;
  nodes: Record<string, any>;
  edges: Record<string, any>;
  version?: string;
  category?: string;
  metadata?: Record<string, any>;
}

export interface WorkflowExecuteForm {
  workflow_id: number;
  variables?: Record<string, any>;
  business_key?: string;
  job_id?: number;
}

export interface WorkflowExecuteResult {
  task_run_id: number;
  workflow_id: number;
  workflow_name: string;
  status: string;
  message: string;
}

export interface WorkflowRunPageQuery extends PageQuery {
  workflow_id?: number;
  workflow_name?: string;
  status?: string;
  business_key?: string;
  initiator?: number;
  job_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

export interface WorkflowRunTable extends BaseType {
  workflow_id: number;
  workflow_name: string;
  workflow_version: string;
  business_key?: string;
  initiator?: number;
  initiator_name?: string;
  variables?: Record<string, any>;
  status: string;
  error_message?: string;
  start_time?: string;
  end_time?: string;
  duration?: number;
  retry_count: number;
  max_retry: number;
  job_id?: number;
  metadata?: Record<string, any>;
  node_executions?: NodeExecution[];
}

export interface NodeExecution {
  node_id: string;
  node_name: string;
  node_type: string;
  status: string;
  start_time?: string;
  end_time?: string;
  duration?: number;
  error_message?: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
}

export interface WorkflowRunForm extends BaseFormType {
  workflow_id: number;
  workflow_name: string;
  workflow_version?: string;
  business_key?: string;
  initiator?: number;
  initiator_name?: string;
  variables?: Record<string, any>;
  job_id?: number;
}

export interface WorkflowRunUpdateForm extends BaseFormType {
  status?: string;
  error_message?: string;
  start_time?: string;
  end_time?: string;
  duration?: number;
  retry_count?: number;
  max_retry_count?: number;
  metadata?: Record<string, any>;
}

export interface WorkflowRunLogPageQuery extends PageQuery {
  task_run_id?: number;
  level?: string;
  node_id?: string;
  node_name?: string;
  created_time?: string[];
}

export interface WorkflowRunLogTable extends BaseType {
  task_run_id: number;
  level: string;
  node_id?: string;
  node_name?: string;
  message: string;
  data?: Record<string, any>;
}
