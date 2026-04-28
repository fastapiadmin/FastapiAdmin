import request from '@/utils/http';

/** 对应后端 `plugin.module_task.workflow.node_type` */
const API_PATH = '/task/workflow/node-type';

const WorkflowNodeTypeAPI = {
  /**
   * 获取编排节点类型选项
   * @returns 编排节点类型选项
   */
  getWorkflowNodeTypeOptions() {
    return request<ApiResponse<WorkflowNodeTypeOption[]>>({
      url: `${API_PATH}/options`,
      method: 'get',
    });
  },

  /**
   * 获取编排节点类型列表
   * @param query 查询参数
   * @returns 编排节点类型列表
   */
  getWorkflowNodeTypeList(query: WorkflowNodeTypePageQuery) {
    return request<PageResult<WorkflowNodeTypeTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取编排节点类型详情
   * @param id 编排节点类型ID
   * @returns 编排节点类型详情
   */
  getWorkflowNodeTypeDetail(id: number) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: 'get',
    });
  },

  /**
   * 创建编排节点类型
   * @param body 编排节点类型信息
   * @returns 编排节点类型详情
   */
  createWorkflowNodeType(body: WorkflowNodeTypeForm) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新编排节点类型
   * @param id 编排节点类型ID
   * @param body 编排节点类型信息
   * @returns 编排节点类型详情
   */
  updateWorkflowNodeType(id: number, body: WorkflowNodeTypeForm) {
    return request<ApiResponse<WorkflowNodeTypeTable>>({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除编排节点类型
   * @param body 编排节点类型ID列表
   * @returns 删除结果
   * @returns 删除结果
   */
  deleteWorkflowNodeType(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
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
