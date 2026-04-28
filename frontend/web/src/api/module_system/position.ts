import request from '@/utils/http';

const API_PATH = '/system/position';

const PositionAPI = {
  /**
   * 获取岗位列表
   * @param query 查询参数
   * @returns 岗位列表
   */
  listPosition(query?: PositionPageQuery) {
    return request<PageResult<PositionTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取岗位详情
   * @param query 岗位ID
   * @returns 岗位详情
   */
  detailPosition(query: number) {
    return request<ApiResponse<PositionTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建岗位
   * @param body 岗位信息
   */
  createPosition(body: PositionForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新岗位
   * @param id 岗位ID
   * @param body 岗位信息
   */
  updatePosition(id: number, body: PositionForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除岗位
   * @param body 岗位ID列表
   */
  deletePosition(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置岗位状态
   * @param body 批量操作参数
   */
  batchPosition(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出岗位
   * @param body 查询参数
   * @returns 导出的岗位文件
   */
  exportPosition(body: PositionPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },
};

export default PositionAPI;

export interface PositionPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

export interface PositionTable extends BaseType {
  name?: string;
  order?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

export interface PositionForm extends BaseFormType {
  name?: string;
  order?: number;
}
