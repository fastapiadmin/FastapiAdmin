import request from '@/utils/http';

const API_PATH = '/task/workflow/definition';

const WorkflowDefinitionAPI = {
  /**
   * 获取工作流列表
   * @param query 查询参数
   * @returns 工作流列表
   */
  getWorkflowList(query: WorkflowPageQuery) {
    return request<PageResult<WorkflowTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取工作流详情
   * @param query 工作流ID
   * @returns 工作流详情
   */
  getWorkflowDetail(query: number) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建工作流
   * @param body 工作流信息
   * @returns 工作流详情
   */
  createWorkflow(body: WorkflowForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新工作流
   * @param id 工作流ID
   * @param body 工作流信息
   * @returns 工作流详情
   */
  updateWorkflow(id: number, body: WorkflowForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除工作流
   * @param body 工作流ID列表
   */
  deleteWorkflow(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 发布工作流
   * @param id 工作流ID
   * @param body 发布参数
   * @returns 工作流详情
   */
  publishWorkflow(id: number, body: WorkflowPublishForm) {
    return request<ApiResponse<WorkflowTable>>({
      url: `${API_PATH}/publish/${id}`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 执行工作流
   * @param body 执行参数
   * @returns 执行结果
   */
  executeWorkflow(body: WorkflowExecuteForm) {
    return request<ApiResponse<WorkflowExecuteResult>>({
      url: `${API_PATH}/execute`,
      method: 'post',
      data: body,
    });
  },
};

export default WorkflowDefinitionAPI;
export { WorkflowDefinitionAPI };

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
  deleted_by?: CommonType;
}

export interface WorkflowForm extends BaseFormType {
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  nodes?: any[];
  edges?: any[];
}

export interface WorkflowPublishForm {
  remark?: string;
}

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
  error?: string;
}
