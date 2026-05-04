import request from "@/utils/http";
import { NO_AUTH_FLAG } from "@/utils/http/config";

const API_PATH = "/system/param";

const ParamsAPI = {
  uploadFile(body: any) {
    return request<ApiResponse<UploadFilePath>>({
      url: `${API_PATH}/upload`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  /** 登录前拉取站点参数：不带 Token，避免过期 JWT 导致 401 无法展示底部备案等 */
  getInitConfig() {
    return request<ApiResponse<ConfigTable[]>>({
      url: `${API_PATH}/info`,
      method: "get",
      headers: {
        Authorization: NO_AUTH_FLAG,
      },
    });
  },

  listParams(query: ConfigPageQuery) {
    return request<ApiResponse<PageResult<ConfigTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailParams(query: number) {
    return request<ApiResponse<ConfigTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createParams(body: ConfigForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateParams(id: number, body: ConfigForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteParams(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  exportParams(body: ConfigPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default ParamsAPI;

export interface ConfigPageQuery extends PageQuery {
  config_name?: string;
  config_key?: string;
  config_type?: boolean;
  created_time?: string[];
  updated_time?: string[];
}

export interface ConfigTable extends BaseType {
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
}

export interface ConfigForm extends BaseFormType {
  config_name?: string;
  config_key?: string;
  config_value?: string;
  config_type?: boolean;
}
