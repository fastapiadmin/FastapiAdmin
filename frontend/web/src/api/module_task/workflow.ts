import { request } from "@utils";

const API_PATH = "/task/workflow";

export type WorkflowStepType = "approval" | "condition";

export interface WorkflowStep {
  type: WorkflowStepType;
  name: string;
  assignee_id?: number | null;
  field?: string | null;
  operator?: string | null;
  value?: string | number | null;
}

export interface WorkflowForm {
  name: string;
  description?: string;
  status: number;
  steps: WorkflowStep[];
}

export interface WorkflowItem extends WorkflowForm {
  id: number;
  created_time?: string;
  updated_time?: string;
}

export interface WorkflowInstance {
  id: number;
  workflow_id: number;
  workflow_name: string;
  status: "running" | "completed" | "rejected";
  current_index: number;
  steps: WorkflowStep[];
  context: Record<string, unknown>;
  error?: string | null;
  created_time?: string;
}

export interface WorkflowTask {
  id: number;
  instance_id: number;
  step_index: number;
  step_name: string;
  assignee_id?: number | null;
  status: "pending" | "approved" | "rejected";
  comment?: string | null;
  acted_at?: string | null;
  created_time?: string;
}

const WorkflowAPI = {
  getPage(params: Record<string, unknown>) {
    return request<ApiResponse<PageResult<WorkflowItem>>>({ url: `${API_PATH}/page`, method: "get", params });
  },
  getDetail(id: number) {
    return request<ApiResponse<WorkflowItem>>({ url: `${API_PATH}/detail/${id}`, method: "get" });
  },
  create(data: WorkflowForm) {
    return request<ApiResponse<WorkflowItem>>({ url: `${API_PATH}/create`, method: "post", data });
  },
  update(id: number, data: WorkflowForm) {
    return request<ApiResponse<WorkflowItem>>({ url: `${API_PATH}/update/${id}`, method: "put", data });
  },
  remove(ids: number[]) {
    return request<ApiResponse>({ url: `${API_PATH}/delete`, method: "delete", data: ids });
  },
  execute(id: number, context: Record<string, unknown>) {
    return request<ApiResponse<WorkflowInstance>>({
      url: `${API_PATH}/execute/${id}`,
      method: "post",
      data: { context },
    });
  },
  getInstances(params: Record<string, unknown>) {
    return request<ApiResponse<PageResult<WorkflowInstance>>>({
      url: `${API_PATH}/instances/page`,
      method: "get",
      params,
    });
  },
  getPendingTasks() {
    return request<ApiResponse<WorkflowTask[]>>({ url: `${API_PATH}/tasks/pending`, method: "get" });
  },
  act(taskId: number, approved: boolean, comment?: string) {
    return request<ApiResponse<WorkflowTask>>({
      url: `${API_PATH}/tasks/${taskId}/action`,
      method: "post",
      data: { approved, comment },
    });
  },
};

export default WorkflowAPI;
