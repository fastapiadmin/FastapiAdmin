import request from '@/utils/http';

const API_PATH = '/system/dept';

const DeptAPI = {
  /**
   * 获取部门树
   * @param query 查询参数
   * @returns 部门树
   */
  listDept(query?: DeptPageQuery) {
    return request<ApiResponse<DeptTable[]>>({
      url: `${API_PATH}/tree`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取部门详情
   * @param query 部门ID
   * @returns 部门详情
   */
  detailDept(query: number) {
    return request<ApiResponse<DeptTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建部门
   * @param body 部门信息
   */
  createDept(body: DeptForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新部门
   * @param id 部门ID
   * @param body 部门信息
   */
  updateDept(id: number, body: DeptForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除部门
   * @param body 部门ID列表
   */
  deleteDept(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置部门状态
   * @param body 批量设置部门状态请求体
   */
  batchDept(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },
};

export default DeptAPI;

export interface DeptPageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
}

export interface DeptTable extends BaseType {
  name?: string;
  order?: number;
  code: string;
  leader?: string;
  phone?: string;
  email?: string;
  parent_id?: number;
  parent_name?: string;
  children?: DeptTable[];
}

export interface DeptForm extends BaseFormType {
  name?: string;
  order?: number;
  code: string;
  leader?: string;
  phone?: string;
  email?: string;
  parent_id?: number;
}
