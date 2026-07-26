import { request } from "@utils";

const API_PATH = "/system/role";

const RoleAPI = {
  listRole(query?: TablePageQuery) {
    return request<ApiResponse<PageResult<RoleTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailRole(query: number) {
    return request<ApiResponse<RoleTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createRole(body: RoleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateRole(id: number, body: RoleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteRole(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchRole(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },

  setPermission(body: permissionDataType) {
    return request<ApiResponse>({
      url: `${API_PATH}/permission`,
      method: "put",
      data: body,
    });
  },

  exportRole(query: TablePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  getRoleOptions() {
    return request<ApiResponse<OptionType[]>>({
      url: `${API_PATH}/options`,
      method: "get",
    });
  },
};

export default RoleAPI;

export interface TablePageQuery extends PageQuery, UserByQueryParams {
  name?: string;
  code?: string;
  status?: number;
}

export interface RoleTable extends BaseType {
  name: string;
  order?: number;
  code: string;
  data_scope?: number;
  menus?: permissionMenuType[];
  depts?: permissionDeptType[];
  status?: number;
  description?: string;
}

export interface RoleForm extends BaseFormType {
  name?: string;
  order?: number;
  code: string;
  data_scope?: number;
  status?: number;
  description?: string;
}

export interface permissionDataType {
  data_scope: number;
  role_ids: RoleTable["id"][];
  menu_ids: permissionMenuType["id"][];
  dept_ids: permissionDeptType["id"][];
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
  status: number;
  description?: string;
  children?: permissionMenuType[];
}
