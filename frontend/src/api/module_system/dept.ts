import request from "@/utils/request";

const API_PATH = "/system/dept";

const DeptAPI = {
  listDept(query?: DeptPageQuery) {
    return request<ApiResponse<DeptTable[]>>({
      url: `${API_PATH}/tree`,
      method: "get",
      params: query,
    });
  },

  detailDept(query: number) {
    return request<ApiResponse<DeptTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createDept(body: DeptForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateDept(id: number, body: DeptForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteDept(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchDept(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
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
  code?: string;
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
  code?: string;
  leader?: string;
  phone?: string;
  email?: string;
  parent_id?: number;
}
