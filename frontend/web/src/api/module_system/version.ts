import { request } from "@utils";

const API_PATH = "/system/versions";

const VersionAPI = {
  getVersionList(query: VersionPageQuery) {
    return request<ApiResponse<PageResult<VersionTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getPublishedVersions() {
    return request<ApiResponse<VersionTable[]>>({ url: `${API_PATH}/published`, method: "get" });
  },

  getVersionDetail(query: number) {
    return request<ApiResponse<VersionTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createVersion(body: VersionForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateVersion(id: number, body: VersionForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteVersion(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  setVersionStatus(id: number, body: { status: number }) {
    return request<ApiResponse<VersionTable>>({
      url: `${API_PATH}/${id}/status`,
      method: "put",
      data: body,
    });
  },
};

export default VersionAPI;

export interface VersionPageQuery extends PageQuery {
  status?: number;
}

export interface VersionTable extends BaseType {
  version?: string;
  title?: string;
  date?: string;
  content?: string;
  description?: string;
  sort?: number;
  status?: number;
  require_re_login?: boolean;
}

export interface VersionForm extends BaseFormType {
  version?: string;
  title?: string;
  date?: string;
  content?: string;
  description?: string;
  sort?: number;
  status?: number;
  require_re_login?: boolean;
}
