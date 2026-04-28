import request from '@/utils/http';
import { MenuTable, MenuForm } from '@/api/module_system/menu';

const API_PATH = '/system/user';

export const UserAPI = {
  /**
   * 获取当前用户信息
   * @returns 当前用户信息
   */
  getCurrentUserInfo() {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/current/info`,
      method: 'get',
    });
  },

  /**
   * 上传当前用户头像
   * @param body 头像文件
   * @returns 上传后的文件路径
   */
  uploadCurrentUserAvatar(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `${API_PATH}/current/avatar/upload`,
      method: 'post',
      data: body,
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * 更新当前用户信息
   * @param body 用户信息
   * @returns 更新后的用户信息
   */
  updateCurrentUserInfo(body: InfoFormState) {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/current/info/update`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 更新当前用户密码
   * @param body 密码信息
   * @returns 更新后的用户信息
   */
  changeCurrentUserPassword(body: PasswordFormState) {
    return request({
      url: `${API_PATH}/current/password/change`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 重置用户密码
   * @param body 重置密码信息
   * @returns 重置密码后的用户信息
   */
  resetUserPassword(body: ResetPasswordForm) {
    return request({
      url: `${API_PATH}/reset/password`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 注册用户
   * @param body 注册信息
   * @returns 注册后的用户信息
   */
  registerUser(body: RegisterForm) {
    return request({
      url: `${API_PATH}/register`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 忘记密码
   * @param body 忘记密码信息
   * @returns 忘记密码后的用户信息
   */
  forgetPassword(body: ForgetPasswordForm) {
    return request({
      url: `${API_PATH}/forget/password`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 获取用户列表
   * @param query 查询参数
   * @returns 用户列表
   */
  listUser(query: UserPageQuery) {
    return request<PageResult<UserInfo[]>>({
      url: `${API_PATH}/list`,
      method: 'get',
      params: query,
    });
  },

  /**
   * 获取用户详情
   * @param id 用户ID
   * @returns 用户详情
   */
  detailUser(query: number) {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/detail/${query}`,
      method: 'get',
    });
  },

  /**
   * 创建用户
   * @param body 用户信息
   * @returns 创建后的用户信息
   */
  createUser(body: UserForm) {
    return request({
      url: `${API_PATH}/create`,
      method: 'post',
      data: body,
    });
  },

  /**
   * 更新用户
   * @param id 用户ID
   * @param body 用户信息
   * @returns 更新后的用户信息
   */
  updateUser(id: number, body: UserForm) {
    return request({
      url: `${API_PATH}/update/${id}`,
      method: 'put',
      data: body,
    });
  },

  /**
   * 删除用户
   * @param body 用户ID列表
   */
  deleteUser(body: number[]) {
    return request({
      url: `${API_PATH}/delete`,
      method: 'delete',
      data: body,
    });
  },

  /**
   * 批量设置用户状态
   * @param body 批量设置用户状态信息
   * @returns 批量设置用户状态后的用户列表
   */
  batchUser(body: BatchType) {
    return request({
      url: `${API_PATH}/available/setting`,
      method: 'patch',
      data: body,
    });
  },

  /**
   * 导出用户
   * @param body 查询参数
   * @returns 导出的用户文件
   */
  exportUser(body: UserPageQuery) {
    return request<ApiResponse<Blob>>({
      url: `${API_PATH}/export`,
      method: 'post',
      data: body,
      responseType: 'blob',
    });
  },

  /**
   * 下载用户导入模板
   * @returns 导入模板文件
   */
  downloadTemplateUser() {
    return request({
      url: `${API_PATH}/import/template`,
      method: 'post',
      responseType: 'blob',
    });
  },

  /**
   * 导入用户数据
   * @param body 导入数据文件
   * @returns 导入后的用户列表
   */
  importUser(body: any) {
    return request<ApiResponse<UserInfo[]>>({
      url: `${API_PATH}/import/data`,
      method: 'post',
      data: body,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default UserAPI;

export interface ForgetPasswordForm {
  username: string;
  new_password: string;
  mobile?: string;
  confirmPassword: string;
}

export interface RegisterForm {
  username: string;
  password: string;
  confirmPassword: string;
}

export interface UserPageQuery extends PageQuery {
  username?: string;
  name?: string;
  mobile?: string;
  email?: string;
  dept_id?: number;
  status?: string;
  created_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface searchSelectDataType {
  name?: string;
  status?: string;
}

export interface UserInfo extends BaseType {
  username?: string;
  name?: string;
  avatar?: string;
  email?: string;
  mobile?: string;
  gender?: string;
  password?: string;
  menus?: MenuTable[];
  dept?: deptTreeType;
  dept_id?: deptTreeType['id'];
  dept_name?: deptTreeType['name'];
  roles?: roleSelectorType[];
  role_names?: roleSelectorType['name'][];
  role_ids?: roleSelectorType['id'][];
  positions?: positionSelectorType[];
  position_names?: positionSelectorType['name'][];
  position_ids?: positionSelectorType['id'][];
  is_superuser?: boolean;
  last_login?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

export interface deptTreeType {
  id?: number;
  name?: string;
  parent_id?: number;
  children?: deptTreeType[];
}

export interface roleSelectorType {
  id?: number;
  name?: string;
  code?: string;
  status?: string;
  description?: string;
  menus?: MenuForm[];
}

export interface positionSelectorType {
  id?: number;
  name?: string;
  status?: string;
  description?: string;
}

export interface InfoFormState {
  id?: number;
  name?: string;
  gender?: number;
  mobile?: string;
  email?: string;
  username?: string;
  dept_name?: string;
  dept?: deptTreeType;
  positions?: positionSelectorType[];
  roles?: roleSelectorType[];
  avatar?: string;
  created_time?: string;
  updated_time?: string;
}

export interface PasswordFormState {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export interface ResetPasswordForm {
  id: number;
  password: string;
}

export interface UserForm extends BaseFormType {
  username?: string;
  name?: string;
  dept_id?: number;
  dept_name?: string;
  role_ids?: number[];
  role_names?: string[];
  position_ids?: number[];
  position_names?: string[];
  password?: string;
  gender?: number;
  email?: string;
  mobile?: string;
  is_superuser?: boolean;
}

export interface CurrentUserFormState {
  name?: string;
  gender?: number;
  mobile?: string;
  email?: string;
  avatar?: string;
}
