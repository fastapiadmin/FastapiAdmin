import request from "@utils/http";

const API_PATH = "/example/demo01";

const Demo01API = {
  getDemo01List(query: Demo01PageQuery) {
    return request<ApiResponse<PageResult<Demo01Table>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getDemo01Detail(id: number) {
    return request<ApiResponse<Demo01Table>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  createDemo01(body: Demo01Form) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateDemo01(id: number, body: Demo01Form) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteDemo01(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchDemo01(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportDemo01(body: Demo01PageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadDemo01Template() {
    return request<ApiResponse>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importDemo01(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

export default Demo01API;

export interface Demo01PageQuery extends PageQuery {
  /** 与后端 Demo01QueryParam 一致 */
  name?: string;
  description?: string;
  /** 是否启用：0 启用 / 1 禁用（字符串） */
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

/**
 * 与后端 Demo01OutSchema 一致：
 * Demo01CreateSchema(name,status,description) + BaseSchema + UserBySchema
 */
export interface Demo01Table extends BaseType {
  name?: string;
  status?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
  deleted_by?: CommonType;
}

/** 与后端 Demo01CreateSchema / Demo01UpdateSchema 一致（不含 id，更新走 URL） */
export interface Demo01Form extends BaseFormType {
  name?: string;
  status?: string;
  description?: string;
}
