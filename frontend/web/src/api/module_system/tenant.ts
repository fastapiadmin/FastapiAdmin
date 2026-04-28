import request from '@/utils/http';

const API_PATH = '/system/tenant';

const TenantAPI = {
  /**
   * 获取租户列表
   * @param query 查询参数
   * @returns 租户列表
   */
  listTenant(query?: TenantPageQuery) {
    return request<PageResult<TenantTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取租户详情
   * @param id 租户ID
   * @returns 租户详情
   */
  detailTenant(id: number) {
    return request<ApiResponse<TenantTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: 'get',
    });
  },

  /**
   * 创建租户
   * @param body 租户信息
   */
  createTenant(body: TenantCreateForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新租户
   * @param id 租户ID
   * @param body 租户信息
   */
  updateTenant(id: number, body: TenantUpdateForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除租户
   * @param body 租户ID列表
   */
  deleteTenant(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置租户状态
   * @param body 批量操作参数
   */
  batchTenant(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },
};

export default TenantAPI;

export interface TenantPageQuery extends PageQuery {
  name?: string;
  code?: string;
  status?: string;
  created_time?: string[];
}

export interface TenantTable extends BaseType {
  name: string;
  code: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantForm {
  id?: number;
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantCreateForm {
  name: string;
  code: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface TenantUpdateForm {
  name?: string;
  status?: string;
  description?: string;
  start_time?: string;
  end_time?: string;
}

export interface BatchType {
  ids: number[];
  status: string;
}
