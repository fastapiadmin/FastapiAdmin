import request from "@/utils/request";

const API_PATH = "/example/demo";

const DemoAPI = {
  getDemoList(query: DemoPageQuery) {
    return request<ApiResponse<PageResult<DemoTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  getDemoDetail(query: number) {
    return request<ApiResponse<DemoTable>>({
      url: `${API_PATH}/detail/${query}`,
      method: "get",
    });
  },

  createDemo(body: DemoForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  updateDemo(id: number, body: DemoForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  deleteDemo(body: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: body,
    });
  },

  batchDemo(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  exportDemo(body: DemoPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: body,
      responseType: "blob",
    });
  },

  downloadTemplateDemo() {
    return request<ApiResponse>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  importDemo(body: FormData) {
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

export default DemoAPI;

export interface DemoPageQuery extends PageQuery {
  name?: string;
  status?: string;
  created_time?: string[];
  updated_time?: string[];
  created_id?: number;
  updated_id?: number;
}

export interface DemoTable extends BaseType {
  name?: string;
  created_by?: creatorType;
  updated_by?: updatorType;
}

export interface DemoForm extends BaseFormType {
  name?: string;
}
