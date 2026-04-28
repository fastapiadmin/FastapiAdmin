import request from '@/utils/http';

const API_PATH = '/system/role';

const RoleAPI = {
  /**
   * 获取角色列表
   * @param query 查询参数
   * @returns 角色列表
   */
  listRole(query?: TablePageQuery) {
    return request<PageResult<RoleTable[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取角色详情
   * @param query 角色ID
   * @returns 角色详情
   */
  detailRole(query: number) {
    return request<ApiResponse<RoleTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建角色
   * @param body 角色信息
   */
  createRole(body: RoleForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新角色
   * @param id 角色ID
   * @param body 角色信息
   */
  updateRole(id: number, body: RoleForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除角色
   * @param body 角色ID列表
   */
  deleteRole(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置角色状态
   * @param body 批量操作参数
   */
  batchRole(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 批量设置角色权限
   * @param body 批量操作参数
   */
  setPermission(body: permissionDataType) {
    return request({
      url: `${API_PATH}/permission/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出角色列表
   * @param body 查询参数
   * @returns 导出的文件
   */
  exportRole(body: TablePageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },
};

export default RoleAPI;

export interface TablePageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
}

export interface RoleTable extends BaseType {
  id: number;
  name: string;
  order?: number;
  code: string;
  data_scope?: number;
  menus?: permissionMenuType[];
  depts?: permissionDeptType[];
}

export interface RoleForm extends BaseFormType {
  name?: string;
  order?: number;
  code: string;
}

export interface permissionDataType {
  data_scope: number;
  role_ids: RoleTable['id'][];
  menu_ids: permissionMenuType['id'][];
  dept_ids: permissionDeptType['id'][];
}

export interface permissionDeptType {
  id: number;
  name: string;
  parent_id: number;
  children: permissionDeptType[];
}

export interface permissionMenuType {
  id: number;
  name: string;
  type: number;
  permission: string;
  parent_id?: number;
  status: string;
  description?: string;
  children?: permissionMenuType[];
}
