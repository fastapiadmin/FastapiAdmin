import request from "@/utils/request";

const API_PATH = "/system/role";

const RoleAPI = {
  listRole(query?: TablePageQuery) {
    return request<ApiResponse<PageResult<RoleTable[]>>>({
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
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  setPermission(body: permissionDataType) {
    return request<ApiResponse>({
      url: `${API_PATH}/permission/setting`,
      method: "patch",
      data: body,
    });
  },

  exportRole(body: TablePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default RoleAPI;

export interface TablePageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

export interface RoleTable extends BaseType {
  id: number;
  name: string;
  order?: number;
  code?: string;
  data_scope?: number;
  menus?: permissionMenuType[];
  depts?: permissionDeptType[];
  created_by?: creatorType;
  updated_by?: updatorType;
}

export interface RoleForm extends BaseFormType {
  name?: string;
  order?: number;
  code?: string;
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
  status: string;
  description?: string;
  children?: permissionMenuType[];
}
