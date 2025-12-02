import request from "@/utils/request";
import { MenuTable, MenuForm } from "@/api/module_system/menu";

const API_PATH = "/system/user";

export const UserAPI = {
  getCurrentUserInfo() {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/current/info`,
      method: "get",
    });
  },

  uploadCurrentUserAvatar(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `${API_PATH}/current/avatar/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  updateCurrentUserInfo(body: InfoFormState) {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/current/info/update`,
      method: "put",
      data: body,
    });
  },

  changeCurrentUserPassword(body: PasswordFormState) {
    return request<ApiResponse>({
      url: `${API_PATH}/current/password/change`,
      method: "put",
      data: body,
    });
  },

  resetUserPassword(body: ResetPasswordForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/reset/password`,
      method: "put",
      data: body,
    });
  },

  registerUser(body: RegisterForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/register`,
      method: "post",
      data: body,
    });
  },

  forgetPassword(body: ForgetPasswordForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/forget/password`,
      method: "post",
      data: body,
    });
  },

  listUser(query: UserPageQuery) {
    return request<ApiResponse<PageResult<UserInfo[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailUser(query: number) {
    return request<ApiResponse<UserInfo>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createUser(body: UserForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateUser(id: number, body: UserForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteUser(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchUser(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportUser(body: UserPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadTemplateUser() {
    return request<ApiResponse>({
      url: `${API_PATH}/import/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importUser(body: any) {
    return request<ApiResponse>({
      url: `${API_PATH}/import/data`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
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
  dept_id?: deptTreeType["id"];
  dept_name?: deptTreeType["name"];
  roles?: roleSelectorType[];
  role_names?: roleSelectorType["name"][];
  role_ids?: roleSelectorType["id"][];
  positions?: positionSelectorType[];
  position_names?: positionSelectorType["name"][];
  position_ids?: positionSelectorType["id"][];
  is_superuser?: boolean;
  last_login?: string;
  created_by?: creatorType;
  updated_by?: updatorType;
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
