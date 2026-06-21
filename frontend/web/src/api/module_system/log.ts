import { request } from "@utils";

// ==================== 操作日志 ====================

const OP_API = "/system/log/operation";

const OperationLogAPI = {
  list(query?: OperationLogPageQuery) {
    return request<ApiResponse<PageResult<OperationLogTable>>>({
      url: `${OP_API}/list`,
      method: "get",
      params: query,
    });
  },

  detail(id: number) {
    return request<ApiResponse<OperationLogTable>>({
      url: `${OP_API}/detail/${id}`,
      method: "get",
    });
  },

  delete(body: number[]) {
    return request<ApiResponse>({
      url: `${OP_API}/delete`,
      method: "delete",
      data: body,
    });
  },

  export(query?: OperationLogPageQuery) {
    return request<Blob>({
      url: `${OP_API}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },
};

export default OperationLogAPI;

export interface OperationLogPageQuery extends PageQuery {
  request_path?: string;
  creator_name?: string;
}

export interface OperationLogTable {
  id: number;
  tenant_id: number;
  request_path?: string;
  request_method?: string;
  request_payload?: Record<string, unknown> | string;
  response_code?: number;
  response_json?: Record<string, unknown> | string;
  process_time?: string;
  created_time?: string;
}

// ==================== 登录日志 ====================

const LOGIN_API = "/system/log/login";

export const LoginLogAPI = {
  list(query?: LoginLogPageQuery) {
    return request<ApiResponse<PageResult<LoginLogTable>>>({
      url: `${LOGIN_API}/list`,
      method: "get",
      params: query,
    });
  },

  detail(id: number) {
    return request<ApiResponse<LoginLogTable>>({
      url: `${LOGIN_API}/detail/${id}`,
      method: "get",
    });
  },

  delete(body: number[]) {
    return request<ApiResponse>({
      url: `${LOGIN_API}/delete`,
      method: "delete",
      data: body,
    });
  },
};

export interface LoginLogPageQuery extends PageQuery {
  username?: string;
}

export interface LoginLogTable {
  id: number;
  username: string;
  status: number;
  login_ip?: string;
  login_location?: string;
  request_os?: string;
  request_browser?: string;
  msg?: string;
  created_time?: string;
}
