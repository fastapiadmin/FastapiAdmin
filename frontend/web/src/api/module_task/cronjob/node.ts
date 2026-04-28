import request from '@/utils/http';

const API_PATH = '/task/cronjob/node';

const NodeAPI = {
  /**
   * 获取节点类型选项
   * @returns 节点类型选项
   */
  getNodeTypeOptions() {
    return request<ApiResponse<NodeType[]>>({
      url: `${API_PATH}/options`,
      method: 'get',
    });
  },

  /**
   * 获取节点列表
   * @param query 查询参数
   * @returns 节点列表
   */
  listNode(query: NodePageQuery) {
    return request<PageResult<NodeTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取节点详情
   * @param id 节点ID
   * @returns 节点详情
   */
  detailNode(query: number) {
    return request<ApiResponse<NodeTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建节点
   * @param body 节点信息
   */
  createNode(body: NodeForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新节点
   * @param id 节点ID
   * @param body 节点信息
   */
  updateNode(id: number, body: NodeForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除节点
   * @param body 节点ID列表
   */
  deleteNode(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 清空所有节点
   */
  clearNode() {
    return request({
      url: `${API_PATH}/clear`,
      method: 'delete',
    });
  },

  /**
   * 执行节点
   * @param id 节点ID
   * @param params 执行参数
   * @returns 执行结果
   */
  executeNode(id: number, params: ExecuteNodeParams = { trigger: 'now' }) {
    return request<ApiResponse<ExecuteNodeResult>>({
      url: `${API_PATH}/execute/${id}`,
      method: 'post',
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

export type TriggerType = 'now' | 'cron' | 'interval' | 'date';

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
  deleted_by?: CommonType;
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
