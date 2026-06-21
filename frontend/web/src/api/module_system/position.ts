import { request } from "@utils";

const API_PATH = "/system/position";

const PositionAPI = {
  listPosition(query?: PositionPageQuery) {
    return request<ApiResponse<PageResult<PositionTable>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  detailPosition(query: number) {
    return request<ApiResponse<PositionTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createPosition(body: PositionForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updatePosition(id: number, body: PositionForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deletePosition(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchPosition(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/status/batch`,
      method: "patch",
      data: body,
    });
  },

  exportPosition(body: PositionPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },
};

export default PositionAPI;

export interface PositionPageQuery extends PageQuery, UserByQueryParams {
  name?: string;
}

export interface PositionTable extends BaseType {
  name?: string;
  code?: string;
  order?: number;
  status?: number;
  description?: string;
}

export interface PositionForm extends BaseFormType {
  name?: string;
  code?: string;
  order?: number;
  status?: number;
  description?: string;
}
