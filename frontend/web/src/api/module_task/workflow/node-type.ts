import { request } from "@utils";

/** 对应后端 `plugin.module_task.workflow.node_type` */
const API_PATH = "/task/workflow/node-type";

const WorkflowNodeTypeAPI = {
  getWorkflowNodeTypeOptions() {
    return request<ApiResponse<WorkflowNodeTypeOption[]>>({
      url: `${API_PATH}/options`,
      method: "get",
    });
  },

  getWorkflowNodeTypeList(query: WorkflowNodeTypePageQuery) {
    return request<ApiResponse<PageResult<WorkflowNodeTypeTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getWorkflowNodeTypeDetail(id: number) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createWorkflowNodeType(body: WorkflowNodeTypeForm) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateWorkflowNodeType(id: number, body: WorkflowNodeTypeForm) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteWorkflowNodeType(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },
};

export default WorkflowNodeTypeAPI;
export { WorkflowNodeTypeAPI };

/** 编排节点类型选项（对应后端 task_workflow_node_type） */
export interface WorkflowNodeTypeOption {
  id: number;
  code: string;
  name: string;
  category: string;
  args?: string;
  kwargs?: string;
}

export interface WorkflowNodeTypePageQuery extends PageQuery {
  name?: string;
  code?: string;
  category?: string;
  is_active?: boolean;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface WorkflowNodeTypeTable extends BaseType {
  name?: string;
  code?: string;
  category?: string;
  func?: string;
  args?: string;
  kwargs?: string;
  sort_order?: number;
  is_active?: boolean;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

export interface WorkflowNodeTypeForm {
  name: string;
  code: string;
  category?: string;
  func: string;
  args?: string;
  kwargs?: string;
  sort_order?: number;
  is_active?: boolean;
}
